import json
from pathlib import Path

import pytest

from app.taxonomy import Taxonomy, TaxonomyError

ROOT = Path(__file__).resolve().parent.parent


def tax(skills):
    return Taxonomy({"version": 1, "skills": skills})


def s(id, display, aliases=(), parents=()):
    return {"id": id, "display": display, "aliases": list(aliases), "parents": list(parents)}


def test_resolve_by_display_and_alias_case_insensitively():
    t = tax([s("llms", "LLMs", ["large language models"])])
    assert t.resolve("LLMs") == "llms"
    assert t.resolve("  large Language Models ") == "llms"
    assert t.resolve("Large language model") is None  # no fuzzy guessing


def test_react_and_react_agent_pattern_stay_distinct():
    t = tax([s("react", "React"), s("react-agent-pattern", "ReAct")])
    assert t.resolve("React") == "react"
    assert t.resolve("ReAct") == "react-agent-pattern"


def test_alias_claimed_by_two_skills_is_rejected():
    with pytest.raises(TaxonomyError):
        tax([s("a", "A", ["shared"]), s("b", "B", ["shared"])])


def test_unknown_parent_and_cycles_are_rejected():
    with pytest.raises(TaxonomyError):
        tax([s("a", "A", parents=["missing"])])
    with pytest.raises(TaxonomyError):
        tax([s("a", "A", parents=["b"]), s("b", "B", parents=["a"])])


def test_ancestors_are_transitive():
    t = tax([s("vertex-ai", "Vertex AI", parents=["gcp"]), s("gcp", "GCP", parents=["cloud"]), s("cloud", "Cloud")])
    assert t.ancestors("vertex-ai") == {"gcp", "cloud"}
    assert t.ancestors("cloud") == set()


def test_committed_taxonomy_loads_and_covers_every_golden_label():
    t = Taxonomy.load()
    for p in sorted((ROOT / "evals/goldens").glob("golden_*.json")):
        g = json.loads(p.read_text())
        for e in g["expected"]:
            assert e["skill_id"] in t.skills, f"{p.name}: {e['skill_id']} not in taxonomy"


def test_every_golden_has_a_valid_seniority_label():
    # None ("no usable signal", LABELING.md) is a label; a level needs a basis, a stated
    # level needs a signal, and a signal must be quoted from the posting.
    for p in sorted((ROOT / "evals/goldens").glob("golden_*.json")):
        g = json.loads(p.read_text())
        if g.get("draft"):
            continue
        assert "seniority" in g, p.name
        if g["seniority"] is None:
            assert g.get("seniority_basis") is None, p.name
            continue
        assert g["seniority"] in ("junior", "mid", "senior"), p.name
        assert g["seniority_basis"] in ("stated", "inferred"), p.name
        sig = g.get("seniority_signal")
        assert sig or g["seniority_basis"] == "inferred", f"{p.name}: stated without a signal"
        if sig:
            norm = lambda x: " ".join(x.split()).lower()
            assert norm(sig) in norm(g["job_description"]), f"{p.name}: signal not in text"


# --- HIR-72: taxonomy v5, the HIR-70 label gaps ---------------------------------------

def test_ambiguous_bare_labels_still_resolve_to_nothing():
    # DECISIONS 2026-10-20 and 2026-11-01: "Triton" is ambiguous between NVIDIA's inference
    # server and OpenAI's kernel language — two unrelated products sharing a word — so the
    # bare label must stay unresolvable rather than pick a side. HIR-128 left it that way:
    # it is at 1 job, and a higher count would not make the word less ambiguous.
    t = Taxonomy.load()
    assert t.resolve("Triton") is None
    assert t.resolve("triton") is None
    assert t.resolve("NVIDIA Triton") == "triton-inference-server"
    assert t.resolve("Ray Serve") == "ray-serve"


def test_bare_ray_resolves_now_that_ray_itself_is_an_entry():
    # Until v8 bare "Ray" resolved to nothing, but for a different reason than "Triton":
    # the only ambiguity was between Ray and its own component Ray Serve, and `ray` had no
    # entry to point at. HIR-72's triage recorded `ray` [distributed-systems] as an entry to
    # land once it reached 3 jobs; HIR-128 landed it, so the framework is the plain reading
    # of the bare word and the longer name still wins where a posting uses it.
    t = Taxonomy.load()
    assert t.resolve("Ray") == "ray"
    assert t.resolve("ray") == "ray"
    assert t.resolve("Ray Serve") == "ray-serve"


def test_german_phrases_fold_onto_their_english_entry():
    # The HIR-70 run reported German and English spellings of one skill as two unmapped
    # labels. Aliases are the fix: they cost no new row on the chart.
    t = Taxonomy.load()
    assert t.resolve("Container-Orchestrierung") == "containerization"
    assert t.resolve("Retrieval-Pipelines") == "rag"
    assert t.resolve("Tool-Engineering") == "tool-calling"
    assert t.resolve("produktiver Betrieb von KI-Modellen") == "mlops"
    assert t.resolve("Training von KI Modellen") == "model-development"


def test_v5_entries_absorb_their_spelling_variants():
    t = Taxonomy.load()
    for label, expected in [
        ("Spring", "spring-boot"), ("SpringBoot", "spring-boot"), ("Spring/SpringBoot", "spring-boot"),
        ("distillation", "knowledge-distillation"), ("Model Distillation", "knowledge-distillation"),
        ("model quantization", "quantization"), ("quantization-aware training", "quantization"),
        ("CUDA", "cuda"), ("KServe", "kserve"), ("Speculative Decoding", "speculative-decoding"),
        ("NVIDIA Dynamo", "nvidia-dynamo"),
    ]:
        assert t.resolve(label) == expected, label


# --- HIR-97: taxonomy v6, the spellings the first real CV run missed -------------------

def test_v6_cv_spellings_resolve():
    # Every phrase here is one the HIR-14 matcher met in a real CV and could not map
    # (DECISIONS 2026-11-01). The singular "LLM" is the load-bearing one: `llms` is the
    # most-asked-for skill, and the taxonomy had only the plural and "LLM APIs".
    t = Taxonomy.load()
    for label, expected in [
        ("LLM", "llms"), ("llm", "llms"),
        ("ChromaDB", "vector-databases"), ("Chroma", "vector-databases"),
        ("Postgres", "postgresql"),
        ("tool-call", "tool-calling"), ("tool calls", "tool-calling"),
        ("spaCy", "nlp"), ("Named Entity Recognition", "nlp"),
        ("OpenCV", "computer-vision"),
    ]:
        assert t.resolve(label) == expected, label


def test_ner_stays_unresolvable():
    # Three characters and ambiguous in a CV, so it is deliberately not an alias of `nlp`:
    # the unambiguous spelling carries the same meaning. DECISIONS 2026-11-01.
    assert Taxonomy.load().resolve("NER") is None


def test_v6_cv_spellings_clear_the_browser_matchers_minimum():
    # web/src/cvSkills.js refuses any phrase under MIN_PHRASE = 3 characters, so an alias
    # shorter than that would resolve server-side and still never tick a chip. "llm" is
    # exactly 3 and passes; this test fails if a future alias sneaks under the bar.
    t = Taxonomy.load()
    for label in ("llm", "chroma", "chromadb", "postgres", "tool-call", "tool calls",
                  "spacy", "named entity recognition", "opencv"):
        assert len(label) >= 3, label
        assert t.resolve(label) is not None, label


# --- HIR-101: taxonomy v7, the German and short-form spellings the Golden pass found ---

def test_v7_german_spellings_resolve():
    # Every phrase here is one a Golden posting uses and the taxonomy spelled only in
    # English before v7 (DECISIONS 2026-11-01, HIR-101). Aliases, so no new chart row.
    t = Taxonomy.load()
    for label, expected in [
        ("Vektordatenbanken", "vector-databases"), ("Vector DB", "vector-databases"),
        ("Container", "containerization"), ("Containerisierung", "containerization"),
        ("Softwareentwicklung", "software-engineering"),
        ("Architekturdesign", "software-architecture"),
        ("Machine-Learning-Konzepte", "machine-learning"),
        ("verteilte Systeme", "distributed-systems"),
        ("Datenpipelines", "data-pipelines"),
        ("Datenmodelle", "data-modeling"),
        ("Evaluierung", "evaluation"),
        ("Versionierung", "model-versioning"),
        ("Versionskontrolle", "git"),
        ("Feinabstimmung", "fine-tuning"),
        ("automatisierte Tests", "testing"), ("Testautomatisierung", "testing"),
        ("Netzwerke", "networking"),
        ("statistische Methoden", "statistics"),
        ("Orchestrierungs-Frameworks", "llm-orchestration"),
    ]:
        assert t.resolve(label) == expected, label


def test_v7_short_forms_resolve():
    # The bare product names a stack list uses. "Spark" alone is unambiguous in this
    # corpus — no company called Spark appears in it (DECISIONS 2026-11-01).
    t = Taxonomy.load()
    for label, expected in [
        ("Spark", "apache-spark"),
        ("HuggingFace", "hugging-face"),
        ("NodeJS", "node-js"),
        ("Bedrock", "aws-bedrock"),
        ("S3", "aws-s3"),
    ]:
        assert t.resolve(label) == expected, label


def test_deployment_stays_unresolvable():
    # Bare "deployment" reads as a whole word in 23 of the 46 Goldens, five of them in
    # postings that never ask for AI deployment ("deployment and monitoring of data
    # pipelines"). It is a broader thing than `ai-deployment`, not another spelling of it,
    # so it is deliberately not an alias. DECISIONS 2026-11-01, HIR-101.
    t = Taxonomy.load()
    assert t.resolve("Deployment") is None
    assert t.resolve("deployment") is None
    assert t.resolve("model deployment") == "ai-deployment"


def test_the_postgress_typo_stays_out():
    # A misspelling in one Golden's stack list, not another name for the thing. Aliases
    # are spellings a writer might reasonably use; a typo is not. DECISIONS 2026-11-01.
    assert Taxonomy.load().resolve("postgress") is None


def test_the_short_language_names_are_display_names_and_gain_no_aliases():
    # "C#", "R" and "Go" are each an entry's own display name, so a posting naming one
    # resolves. HIR-101 adds no alias for them: under cvSkills.js's MIN_PHRASE = 3 the
    # browser never matches them in a CV, which is the point — bare "R" and "Go" in prose
    # are an initial or "go-live" far more often than a skill claim. "Go" stays reachable
    # in a CV through "golang".
    t = Taxonomy.load()
    assert t.resolve("C#") == "csharp"
    assert t.resolve("R") == "r-lang"
    assert t.resolve("Go") == "go"
    for sid in ("csharp", "r-lang", "go"):
        assert all(len(a) >= 3 for a in t.skills[sid].aliases), sid


def test_v7_aliases_clear_the_browser_matchers_minimum_except_s3():
    # cvSkills.js refuses any phrase under MIN_PHRASE = 3 characters. Every v7 alias
    # clears it except "s3", which is kept on purpose: two characters, so it resolves a
    # job posting's stack list and is silently ignored in a CV, where "S3" is as likely a
    # model number. DECISIONS 2026-11-01 records the exception.
    t = Taxonomy.load()
    v7 = ["vektordatenbanken", "vector db", "container", "containerisierung",
          "softwareentwicklung", "architekturdesign", "machine-learning-konzepte",
          "verteilte systeme", "datenpipelines", "datenmodelle", "evaluierung",
          "versionierung", "versionskontrolle", "feinabstimmung", "automatisierte tests",
          "testautomatisierung", "netzwerke", "statistische methoden",
          "orchestrierungs-frameworks", "spark", "huggingface", "nodejs", "bedrock", "s3"]
    for label in v7:
        assert t.resolve(label) is not None, label
        if label == "s3":
            assert len(label) == 2, "the one documented exception"
        else:
            assert len(label) >= 3, label


# --- HIR-128: taxonomy v8, the seven that cleared 3 jobs in the SF queue ---------------

def test_v8_entries_resolve_with_their_spellings():
    # DECISIONS 2026-11-03. Each of these cleared the 2026-10-20 bar of 3 jobs counting
    # only jobs at the current extractor stamp; the aliases are spellings the SF postings
    # used. `temporal` is the durable-execution engine, capitalised in all three postings.
    t = Taxonomy.load()
    for label, expected in [
        ("Ansible", "ansible"), ("NCCL", "nccl"), ("nccl", "nccl"),
        ("Bash", "bash"), ("bash scripting", "bash"),
        ("Redis", "redis"), ("Temporal", "temporal"), ("temporal.io", "temporal"),
        ("SageMaker", "sagemaker"), ("aws sagemaker", "sagemaker"),
        ("amazon sagemaker", "sagemaker"),
    ]:
        assert t.resolve(label) == expected, label


def test_v8_leaves_out_the_labels_it_deliberately_left_out():
    # Bare "Triton" is out for good: two unrelated products share the word (see above).
    # FSDP and Datadog were out only of *that* change (HIR-131, DECISIONS 2026-11-03).
    # FSDP landed in v11 with the HIR-219 batch; Datadog is still at 2 postings.
    t = Taxonomy.load()
    assert t.resolve("Triton") is None
    assert t.resolve("Datadog") is None


def test_v11_adds_the_queue_batch_after_the_german_launch():
    # The 27 suggestions at 3+ distinct postings on 11 Nov. DECISIONS 2026-11-11 (HIR-219).
    t = Taxonomy.load()
    for label, expected in [
        ("Angular", "angular"), ("Ruby on Rails", "ruby-on-rails"), ("Ruby", "ruby"),
        ("Azure AI Foundry", "azure-ai-foundry"), ("Azure AI Studio", "azure-ai-foundry"),
        ("Jenkins", "jenkins"), ("SLURM", "slurm"), ("Azure Key Vault", "azure-key-vault"),
        ("Microsoft Entra ID", "microsoft-entra-id"), ("Entra ID", "microsoft-entra-id"),
        ("Azure AD", "microsoft-entra-id"), ("MongoDB", "mongodb"), (".NET", "dotnet"),
        ("Microsoft Fabric", "microsoft-fabric"), ("Nest.js", "nestjs"), ("NestJS", "nestjs"),
        ("Azure DevOps", "azure-devops"), ("Playwright", "playwright"), ("PowerBI", "power-bi"),
        ("FSDP", "fsdp"), ("PydanticAI", "pydanticai"), ("OpenShift", "openshift"),
        ("Azure AI Search", "azure-ai-search"), ("Transformers", "transformers"),
        ("Megatron", "megatron-lm"), ("Megatron-LM", "megatron-lm"), ("Hadoop", "hadoop"),
        ("Semantic Kernel", "semantic-kernel"), ("OAuth 2.0", "oauth"), ("OAuth/OIDC", "oauth"),
        ("Bazel", "bazel"), ("Secrets Management", "secrets-management"),
        ("ArgoCD", "argocd"), ("Argo CD", "argocd"),
    ]:
        assert t.resolve(label) == expected, label
    # Entra ID is its own entry under Active Directory, not a spelling of it.
    assert "active-directory" in t.ancestors("microsoft-entra-id")
    assert t.resolve("Active Directory") == "active-directory"
    assert "ruby" in t.ancestors("ruby-on-rails")


def test_v11_leaves_out_what_is_below_the_bar_or_not_a_skill():
    # At 2 distinct postings once a posting stored twice is counted once; Scrum is a working
    # method (HIR-72); bare Argo may be Argo Workflows. DECISIONS 2026-11-11 (HIR-219).
    t = Taxonomy.load()
    for label in ["AWS Glue", "Power Platform", "Neo4j", "Scrum", "Argo", "sentence-transformers"]:
        assert t.resolve(label) is None, label


def test_ray_serve_hangs_under_ray_without_losing_distributed_systems():
    # HIR-72's triage recorded `ray-serve` [ray]; it shipped with `distributed-systems`
    # instead only because `ray` had not landed yet. v8 restores the recorded shape, and
    # `distributed-systems` survives as an ancestor through `ray`, so a parent walk is
    # unchanged. DECISIONS 2026-11-03.
    t = Taxonomy.load()
    assert t.skills["ray-serve"].parents == ("model-serving", "ray")
    assert "distributed-systems" in t.ancestors("ray-serve")
    assert "ray" in t.ancestors("ray-serve")
    assert t.skills["ray"].parents == ("distributed-systems",)


def test_v8_parents_follow_the_existing_precedents():
    # `ansible` under infrastructure-as-code follows `terraform`; `sagemaker` under `aws`
    # follows `vertex-ai` under `gcp`; `bash` takes no parent, as every other language
    # entry does. `nccl` takes `distributed-training` because `gpu-computing`, the id
    # HIR-72 proposed above it, never landed. DECISIONS 2026-11-03.
    t = Taxonomy.load()
    assert t.skills["ansible"].parents == ("infrastructure-as-code",)
    assert t.skills["terraform"].parents == ("infrastructure-as-code",)
    assert t.skills["sagemaker"].parents == ("aws",)
    assert t.skills["nccl"].parents == ("distributed-training",)
    assert t.skills["bash"].parents == ()
    assert t.skills["redis"].parents == ()
    assert "gpu-computing" not in t.skills


# --- HIR-177: taxonomy v9, the "test" word boundary ---

def test_v9_testing_is_displayed_as_software_testing_but_keeps_its_id():
    # The chart reads "Software Testing"; the id stays `testing` because 72 stored postings
    # and the Golden set point at it, and an id is never renamed once rows reference it
    # (taxonomy/README.md). DECISIONS 2026-11-05, HIR-177.
    t = Taxonomy.load()
    assert t.version >= 9
    assert t.skills["testing"].display == "Software Testing"


def test_v9_the_bare_word_testing_still_resolves():
    # It used to resolve as the display name. Renaming the display without adding the alias
    # would silently break two paths: extract.py's `new:` branch, where an unresolvable
    # label becomes a *proposed* skill instead of a mention, and web/src/cvSkills.js, which
    # matches a CV against display names and aliases. DECISIONS 2026-11-05, HIR-177.
    t = Taxonomy.load()
    for label in ("testing", "Testing", "Software Testing", "software testing"):
        assert t.resolve(label) == "testing", label


def test_v9_the_test_sharing_phrases_land_on_their_own_skills():
    # Four skills share the word "test". The boundary is written down in
    # taxonomy/README.md, "Skill boundaries". DECISIONS 2026-11-05, HIR-177.
    t = Taxonomy.load()
    for label, expected in [
        ("A/B test", "a-b-testing"), ("A/B testing", "a-b-testing"),
        ("split test", "a-b-testing"), ("split testing", "a-b-testing"),
        ("statistical testing", "statistics"), ("hypothesis testing", "statistics"),
        ("significance testing", "statistics"),
        ("model evaluation", "evaluation"), ("llm evaluation", "evaluation"),
        ("evaluation frameworks", "evaluation"), ("Evaluierung", "evaluation"),
        ("automated testing", "testing"), ("integration testing", "testing"),
        ("test automation", "testing"), ("automatisierte Tests", "testing"),
        ("Testautomatisierung", "testing"),
    ]:
        assert t.resolve(label) == expected, label


def test_v9_the_boundary_is_written_down_where_a_labeller_reaches_it():
    # The skill list has no per-entry description field, so the boundary lives in
    # taxonomy/README.md — which evals/LABELING.md already names as the source of truth for
    # what counts as a skill. This test fails if the section is deleted, which is how the
    # skill would drift back. DECISIONS 2026-11-05, HIR-177.
    readme = (Path(__file__).resolve().parent.parent / "taxonomy" / "README.md").read_text()
    assert "## Skill boundaries" in readme
    section = readme.split("## Skill boundaries", 1)[1].split("\n## ", 1)[0]
    for sid in ("a-b-testing", "statistics", "evaluation"):
        assert sid in section, sid
    labeling = (Path(__file__).resolve().parent.parent / "evals" / "LABELING.md").read_text()
    assert "taxonomy/README.md" in labeling


# --- HIR-181: taxonomy v10, the AI-assisted-coding skill in the market's own words ---

def test_v10_ai_coding_tools_is_the_display_name_and_the_id_is_unchanged():
    # The chart reads "AI Coding Tools" — one posting uses exactly that phrase and four
    # more say "AI coding tools". The id stays `ai-developer-tooling` because 70 stored
    # postings and six Goldens point at it, and an id is never renamed once rows reference
    # it (taxonomy/README.md). DECISIONS 2026-11-05, HIR-181.
    t = Taxonomy.load()
    assert t.version >= 10
    assert t.skills["ai-developer-tooling"].display == "AI Coding Tools"


def test_v10_the_old_display_name_still_resolves():
    # "AI developer tooling" used to resolve as the display name, and two stored postings
    # plus golden_009 quote it. Renaming without keeping the alias would send that phrase
    # down extract.py's `new:` path as a *proposed* skill instead of a mention, and would
    # stop web/src/cvSkills.js matching it in a CV. DECISIONS 2026-11-05, HIR-181.
    t = Taxonomy.load()
    for label in ("AI developer tooling", "ai developer tooling", "AI development tools"):
        assert t.resolve(label) == "ai-developer-tooling", label


def test_v10_the_market_spellings_resolve():
    # Every one of these was read off a stored `skill_mention.raw_text` for this skill, in
    # the 61 distinct quotes behind its 70 jobs — not guessed. DECISIONS 2026-11-05.
    t = Taxonomy.load()
    for label in (
        "AI Coding Tools", "AI coding tools", "AI coding assistants", "AI coding agents",
        "coding agents", "coding agent", "Agentic Coding", "agentic coding tools",
        "AI-assisted coding", "coding copilots", "AI-assisted development tools",
        "AI-assisted developer tooling", "AI-powered development tools",
        "AI-powered developer tools", "AI dev tools", "GenAI coding tools",
        # the German postings
        "KI-Coding-Agenten", "AI-Coding-Copiloten", "KI-gestützte Tools",
        "KI-Entwicklungstools", "Coding-Agenten",
    ):
        assert t.resolve(label) == "ai-developer-tooling", label


def test_v10_leaves_out_the_phrases_that_belong_to_the_neighbours():
    # "agentic development" and "agent-driven development" appear in real quotes but sit one
    # word from `agents` (building agents) and `tool-calling` (a model calling tools), which
    # the ticket names as the confusion to avoid. Bare "AI tools" / "KI-Tools" is too broad:
    # a posting asking for them need not mean coding. DECISIONS 2026-11-05, HIR-181.
    t = Taxonomy.load()
    for label in ("agentic development", "agent-driven development", "AI tools", "KI-Tools"):
        assert t.resolve(label) is None, label
    assert t.resolve("agents") == "agents"
    assert t.resolve("tool calling") == "tool-calling"


def test_v10_cursor_and_copilot_still_hang_off_it():
    # The two children are the specific tools under the renamed parent; the rename must not
    # move them. DECISIONS 2026-11-05, HIR-181.
    t = Taxonomy.load()
    assert t.skills["cursor"].parents == ("ai-developer-tooling",)
    assert t.skills["github-copilot"].parents == ("ai-developer-tooling",)
    for sid in ("cursor", "github-copilot"):
        assert "ai-developer-tooling" in t.ancestors(sid), sid


def test_v10_aliases_clear_the_browser_matchers_minimum():
    # cvSkills.js refuses any phrase under MIN_PHRASE = 3 characters, so an alias shorter
    # than that would resolve a job posting and be silently ignored in a CV.
    t = Taxonomy.load()
    for a in t.skills["ai-developer-tooling"].aliases:
        assert len(a) >= 3, a
        assert a == a.strip().lower(), a


# --- a skill id is never removed once rows reference it (HIR-209) ----------------------
#
# taxonomy/README.md: an id is "stable; never rename once rows reference it". Nothing
# checked it. A removed or renamed id takes that skill off the chart for every job that
# mentions it — skill_mention rows keep pointing at an id the taxonomy no longer knows, and
# nothing raises. tests/fixtures/skill_ids.json is the list of ids that have ever been
# committed; `uv run python scripts/record_skill_ids.py` appends new ones and never removes
# one, so an id that disappears cannot be made to pass by re-running it.

KNOWN_IDS = ROOT / "tests" / "fixtures" / "skill_ids.json"


def test_no_skill_id_has_disappeared_from_the_taxonomy():
    known = set(json.loads(KNOWN_IDS.read_text()))
    current = set(Taxonomy.load().skills)
    gone = sorted(known - current)
    assert not gone, (
        "skill id(s) removed or renamed: " + ", ".join(gone)
        + ". Every job that mentions one loses that skill from the chart, with no error"
          " anywhere, and the stored rows still point at it. Keep the id and change the"
          " display name, or add the old spelling as an alias of the new entry.")


def test_every_current_skill_id_is_recorded():
    """So a removal cannot be hidden by deleting the id from the list in the same commit."""
    known = set(json.loads(KNOWN_IDS.read_text()))
    missing = sorted(set(Taxonomy.load().skills) - known)
    assert not missing, (
        "new skill id(s) not recorded: " + ", ".join(missing)
        + ". Run `uv run python scripts/record_skill_ids.py` and commit"
          " tests/fixtures/skill_ids.json with them.")


def test_the_recorded_list_is_sorted_and_has_no_duplicates():
    """It is appended to by a script and read in diffs, so its order is part of it."""
    ids = json.loads(KNOWN_IDS.read_text())
    assert ids == sorted(set(ids))
