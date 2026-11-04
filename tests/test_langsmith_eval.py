"""Mocked. Nothing here reaches LangSmith — tests/conftest.py unsets the key, and the
fake client below records calls instead of making them."""

import sys
from types import SimpleNamespace
from uuid import uuid4

import pytest

from app import evaluation as ev
from app import langsmith_eval as ls
from app.extract import Extraction, Mention, Proposed


def golden(gid="g1", split="dev", **extra):
    return {"id": gid, "split": split, "source_sha256": "abc",
            "job_description": "We want Python and SQL",
            "expected": [{"skill_id": "python", "requirement": "required", "raw_text": "Python"}],
            **extra}


class FakeClient:
    """Records what would have been sent."""

    def __init__(self, datasets=None, examples=None):
        self._datasets = datasets if datasets is not None else {}
        self._examples = examples or []
        self.created = []
        self.updated = []
        self.feedback = []
        self.projects = []
        self.closed = []

    def read_dataset(self, dataset_name=None):
        if dataset_name not in self._datasets:
            raise LookupError(f"no dataset {dataset_name}")
        return self._datasets[dataset_name]

    def create_dataset(self, name, description=None):
        ds = SimpleNamespace(id=uuid4(), name=name)
        self._datasets[name] = ds
        return ds

    def list_examples(self, dataset_id=None):
        return list(self._examples)

    def create_examples(self, dataset_id=None, examples=None):
        for e in examples:
            self._examples.append(SimpleNamespace(id=uuid4(), metadata=e["metadata"],
                                                  inputs=e["inputs"], outputs=e["outputs"]))
        self.created.extend(examples)

    def update_examples(self, dataset_id=None, updates=None):
        self.updated.extend(updates)

    def create_project(self, name, **kw):
        p = SimpleNamespace(id=uuid4(), name=name, **kw)
        self.projects.append(p)
        return p

    def update_project(self, project_id, **kw):
        self.closed.append((project_id, kw))

    def create_feedback(self, run_id=None, key=None, score=None, **kw):
        self.feedback.append((key, score))


META = {"run_id": "20261104T120000Z_dev_x2-abc", "split": "dev", "n_goldens": 1, "repeats": 3,
        "model": "m", "extractor_version": "x2-abc", "taxonomy_version": 7}


# --- off by default ---------------------------------------------------------------

def test_disabled_without_a_key():
    assert ls.enabled() is False           # conftest unset it
    assert ls.start([golden()], META) is None


def test_wrap_client_is_a_no_op_when_disabled():
    client = object()
    assert ls.wrap_client(client) is client


def test_enabled_only_reads_the_api_key(monkeypatch):
    monkeypatch.setenv("LANGSMITH_API_KEY", "x")
    assert ls.enabled() is True


# --- the held-out guard -----------------------------------------------------------

def test_a_heldout_golden_is_refused_before_anything_is_sent():
    client = FakeClient()
    with pytest.raises(ValueError, match="only the dev split"):
        ls.sync_dataset(client, [golden(), golden("g2", split="heldout")])
    assert client.created == [] and client._datasets == {}


# --- the dataset ------------------------------------------------------------------

def test_example_carries_the_labels_the_eval_scores():
    inputs, outputs, metadata = ls.example_payload(
        golden(title="Data Engineer", german="required", production=None))
    assert inputs == {"job_description": "We want Python and SQL", "title": "Data Engineer"}
    assert outputs["expected"][0]["skill_id"] == "python"
    assert outputs["german"] == "required"
    assert outputs["production"] is None      # the key is present, so the label is "not mentioned"
    assert "seniority" not in outputs         # unlabeled stays absent, not null
    assert metadata == {"golden_id": "g1", "split": "dev", "source_sha256": "abc"}


def test_a_new_dataset_gets_one_example_per_golden():
    client = FakeClient()
    dataset_id, examples = ls.sync_dataset(client, [golden(), golden("g2")])
    assert len(client.created) == 2
    assert sorted(examples) == ["g1", "g2"]
    assert dataset_id is not None


def test_a_golden_already_there_is_updated_not_duplicated():
    existing_id = uuid4()
    ds = SimpleNamespace(id=uuid4(), name=ls.DATASET_NAME)
    client = FakeClient(datasets={ls.DATASET_NAME: ds},
                        examples=[SimpleNamespace(id=existing_id, metadata={"golden_id": "g1"})])
    _, examples = ls.sync_dataset(client, [golden(), golden("g2")])
    assert [u["id"] for u in client.updated] == [existing_id]   # g1 in place
    assert len(client.created) == 1                             # g2 is new
    assert examples["g1"] == existing_id


def test_a_dataset_failure_does_not_stop_the_eval(capsys):
    class Broken(FakeClient):
        def create_dataset(self, name, description=None):
            raise RuntimeError("502 bad gateway")

    dataset_id, examples = ls.sync_dataset(Broken(), [golden()])
    assert (dataset_id, examples) == (None, {})
    assert "continuing without it" in capsys.readouterr().err


# --- the experiment ---------------------------------------------------------------

def test_the_experiment_is_named_after_the_extractor_version(monkeypatch):
    monkeypatch.setenv("LANGSMITH_API_KEY", "x")
    client = FakeClient()
    # start() does `from langsmith import Client`, so the fake goes in as the module.
    monkeypatch.setitem(sys.modules, "langsmith", SimpleNamespace(Client=lambda: client))

    exp = ls.start([golden()], META)
    assert exp.name == "x2-abc-20261104T120000Z"       # version, then the run's timestamp
    [project] = client.projects
    assert project.num_repetitions == 3
    assert project.metadata["taxonomy_version"] == 7


def test_finish_puts_the_whole_run_scores_on_the_experiment():
    client = FakeClient()
    project = SimpleNamespace(id=uuid4(), name="x2-abc-t")
    exp = ls.Experiment(client, project, {})
    exp.finish(META, {"f1": {"mean": 0.8}}, [{"precision": 0.9, "n_errors": 0}])
    [(pid, kw)] = client.closed
    assert pid == project.id
    assert kw["metadata"]["summary_scores"] == {"f1": 0.8}
    assert kw["metadata"]["per_repeat"] == [
        {"precision": 0.9, "recall": None, "f1": None, "rank_spearman": None,
         "top10_overlap": None, "grounding_accuracy": None, "n_errors": 0}]
    assert kw["end_time"] is not None


# --- the span ---------------------------------------------------------------------

class FakeRunTree:
    def __init__(self):
        self.id = uuid4()
        self.trace_id = self.id
        self.outputs = None
        self.children = []

    def add_outputs(self, outputs):
        self.outputs = outputs

    def create_child(self, name, run_type=None, inputs=None):
        child = SimpleNamespace(name=name, run_type=run_type, inputs=inputs, outputs=None,
                                end=lambda outputs=None: setattr(child, "outputs", outputs),
                                post=lambda: self.children.append(child))
        return child


def test_the_mapping_step_is_a_child_span_showing_kept_and_rejected():
    rt = FakeRunTree()
    span = ls.Span(FakeClient(), rt)
    span.mapping(Extraction(
        mentions=[Mention("python", "required", "Python")],
        proposed=[Proposed("Polars", "required", "Polars")],
        rejected=[{"item": {}, "reason": "unknown skill_id"}],
        taxonomy_version=7))
    [child] = rt.children
    assert (child.name, child.run_type) == ("taxonomy_mapping", "parser")
    assert child.inputs == {"taxonomy_version": 7}
    assert child.outputs["kept"] == [{"skill_id": "python", "requirement": "required",
                                      "raw_text": "Python"}]
    assert child.outputs["proposed"][0]["label"] == "Polars"
    assert child.outputs["rejected"][0]["reason"] == "unknown skill_id"


def test_per_golden_scores_are_attached_as_feedback():
    client = FakeClient()
    span = ls.Span(client, FakeRunTree())
    score = ev.score_golden(
        "g1",
        [{"skill_id": "python", "requirement": "required"},
         {"skill_id": "sql", "requirement": "required"}],
        [{"skill_id": "python", "requirement": "required"},
         {"skill_id": "dbt", "requirement": "required"}],
        grounding=(1, 2), german=("required", "required"))
    span.record(score)
    span.flush()
    got = dict(client.feedback)
    assert got["skill_precision"] == pytest.approx(0.5)
    assert got["skill_recall"] == pytest.approx(0.5)
    assert got["grounding"] == pytest.approx(0.5)
    assert got["extras"] == 1.0 and got["missed"] == 1.0
    assert got["german"] == 1.0
    assert "seniority" not in got      # this Golden carries no seniority label


def test_an_unlabeled_attribute_gets_no_score():
    client = FakeClient()
    span = ls.Span(client, FakeRunTree())
    span.record(ev.score_golden("g1", [{"skill_id": "python", "requirement": "required"}], []))
    span.flush()
    keys = dict(client.feedback)
    assert "german" not in keys and "degree" not in keys and "production" not in keys
    assert keys["skill_recall"] == 0.0


def test_a_failed_golden_puts_its_error_on_the_trace():
    rt = FakeRunTree()
    span = ls.Span(FakeClient(), rt)
    span.result({"error": "ExtractionError: no tool call"})
    assert rt.outputs == {"error": "ExtractionError: no tool call"}


# --- the hook into run_once -------------------------------------------------------

def test_run_once_drives_the_span_for_every_golden():
    seen = []

    class Recorder:
        def __init__(self, gid):
            self.gid = gid

        def __enter__(self):
            return self

        def __exit__(self, *a):
            return False

        def mapping(self, extraction):
            seen.append(("mapping", self.gid, len(extraction.mentions)))

        def result(self, prediction):
            seen.append(("result", self.gid, "error" in prediction))

        def record(self, score):
            seen.append(("record", self.gid, len(score.tp)))

    def extract_fn(text):
        return Extraction(mentions=[Mention("python", "required", "Python")])

    ev.run_once([golden(), golden("g2")], extract_fn, trace=lambda g: Recorder(g["id"]))
    assert seen == [("mapping", "g1", 1), ("result", "g1", False), ("record", "g1", 1),
                    ("mapping", "g2", 1), ("result", "g2", False), ("record", "g2", 1)]


def test_a_failing_extraction_is_still_scored_and_reported():
    seen = []

    class Recorder:
        def __enter__(self):
            return self

        def __exit__(self, *a):
            return False

        def mapping(self, extraction):
            seen.append("mapping")       # must not happen: there is nothing to map

        def result(self, prediction):
            seen.append(("result", prediction["error"]))

        def record(self, score):
            seen.append(("record", score.fn))

    def boom(text):
        raise RuntimeError("401 invalid x-api-key")

    out = ev.run_once([golden()], boom, trace=lambda g: Recorder())
    assert out.summary["n_errors"] == 1
    assert seen == [("result", "RuntimeError: 401 invalid x-api-key"), ("record", ["python"])]


def test_run_once_without_a_trace_hook_is_unchanged():
    def extract_fn(text):
        return Extraction(mentions=[Mention("python", "required", "Python")])

    out = ev.run_once([golden()], extract_fn)
    assert out.summary["recall"] == 1.0
