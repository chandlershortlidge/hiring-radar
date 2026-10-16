"""Decide whether a new posting is one we already have.

Does: normalize company names and titles into comparison keys, measure text similarity
between job descriptions, and pick the best existing match for a new posting.

Does NOT: read or write the database (callers pass candidate rows in), or know about
sources — "same source id" short-circuiting happens in ingest before this runs.

Invariants: pure and deterministic; similarity is symmetric and in [0, 1]; a match requires
the same normalized company AND similarity >= THRESHOLD, so two different roles at one
company never merge on company alone.
"""

import re
from dataclasses import dataclass

THRESHOLD = 0.7        # shingle Jaccard at or above this = same posting
SHINGLE = 3            # words per shingle
_GENDER_TAG = re.compile(r"\(\s*[mfwdx]\s*(/\s*[mfwdx]\s*){1,2}\)|\(all genders\)|\ball genders\b", re.I)
_SUFFIX = re.compile(r"\b(gmbh|ag|se|inc\.?|ltd\.?|llc|co\.?|kg|ug|b\.?v\.?|s\.?a\.?)\b\.?", re.I)
_NONWORD = re.compile(r"[^a-z0-9]+")


def company_key(company: str | None) -> str:
    s = (company or "").lower()
    s = _SUFFIX.sub(" ", s)
    return _NONWORD.sub(" ", s).strip()


def title_key(title: str) -> str:
    s = _GENDER_TAG.sub(" ", title.lower())
    return _NONWORD.sub(" ", s).strip()


def _words(text: str) -> list[str]:
    return _NONWORD.sub(" ", text.lower()).split()


def shingles(text: str, n: int = SHINGLE) -> set[str]:
    w = _words(text)
    if len(w) < n:
        return {" ".join(w)} if w else set()
    return {" ".join(w[i:i + n]) for i in range(len(w) - n + 1)}


def similarity(a: str, b: str) -> float:
    sa, sb = shingles(a), shingles(b)
    if not sa or not sb:
        return 0.0
    return len(sa & sb) / len(sa | sb)


@dataclass(frozen=True)
class Candidate:
    job_id: int
    company: str | None
    title: str
    description_text: str


@dataclass(frozen=True)
class Match:
    job_id: int
    similarity: float


def find_match(company: str | None, description_text: str, candidates: list[Candidate],
               threshold: float = THRESHOLD) -> Match | None:
    ck = company_key(company)
    if not ck:
        return None
    best: Match | None = None
    for c in candidates:
        if company_key(c.company) != ck:
            continue
        s = similarity(description_text, c.description_text)
        if s >= threshold and (best is None or s > best.similarity):
            best = Match(c.job_id, s)
    return best
