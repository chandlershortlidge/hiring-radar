"""Decide whether a new posting is one we already have.

Does: normalize company names and titles into comparison keys, measure text similarity
between job descriptions, and pick the best existing match for a new posting.

Does NOT: read or write the database (callers pass candidate rows in), or know about
sources — "same source id" short-circuiting happens in ingest before this runs.

Invariants: pure and deterministic; similarity is symmetric and in [0, 1]; a match requires
the same normalized company AND a text test, so two different roles at one company never
merge on company alone. There are two text tests, either of which is enough: Jaccard
>= THRESHOLD, or — for the aggregator-snippet case, where one source stores a short extract
of a posting another stores in full — the shorter text almost entirely contained in the
longer one, with the title corroborating. See `is_same_posting`.
"""

import re
from dataclasses import dataclass

THRESHOLD = 0.7        # shingle Jaccard at or above this = same posting
SHINGLE = 3            # words per shingle

# The second path: a short text wholly inside a long one. Jaccard cannot see this, because
# the union it divides by grows with the longer text — Cloover's snippet sat at 0.68 against
# the full posting it is a literal prefix of. Containment is 1.0 there. All three guards
# below are needed together; the numbers come from the 246 stored jobs (HIR-113):
CONTAINED = 0.9        # of the shorter text's shingles must appear in the longer one...
MIN_CONTAINED = 60     # ...which must itself be at least this many shingles (~60 words),
                       #    since less text than that cannot establish identity; and
TITLE_CONTAINED = 1.0  # every word of the shorter title must appear in the longer one.
                       #    Without this last guard two different pplwise roles sharing a
                       #    recruiter's boilerplate reach containment 0.93 and would merge.
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


def containment(a: str, b: str) -> float:
    """How much of the shorter text appears in the longer one: |A∩B| / min(|A|,|B|).

    Symmetric, in [0, 1], and 1.0 when either text's shingles are a subset of the other's.
    """
    sa, sb = shingles(a), shingles(b)
    if not sa or not sb:
        return 0.0
    return len(sa & sb) / min(len(sa), len(sb))


def _title_containment(a: str, b: str) -> float:
    wa, wb = set(title_key(a).split()), set(title_key(b).split())
    if not wa or not wb:
        return 0.0
    return len(wa & wb) / min(len(wa), len(wb))


def is_same_posting(title_a: str, text_a: str, title_b: str, text_b: str,
                    threshold: float = THRESHOLD) -> bool:
    """Do these two postings (already known to be at the same company) say the same thing?

    True on either path: plain shingle Jaccard at or above `threshold`, or the containment
    path — the shorter text almost wholly inside the longer, long enough to mean something,
    and with the shorter title's words all present in the longer title. The title is only
    ever a *supporting* signal here; it can never carry a match on its own.
    """
    if similarity(text_a, text_b) >= threshold:
        return True
    sa, sb = shingles(text_a), shingles(text_b)
    if min(len(sa), len(sb)) < MIN_CONTAINED:
        return False
    return (containment(text_a, text_b) >= CONTAINED
            and _title_containment(title_a, title_b) >= TITLE_CONTAINED)


@dataclass(frozen=True)
class Candidate:
    job_id: int
    company: str | None
    title: str
    description_text: str


@dataclass(frozen=True)
class Match:
    job_id: int
    similarity: float   # the plain Jaccard, reported as measured — so a match found on the
                        # containment path carries a value below THRESHOLD. Informational.


def find_match(company: str | None, title: str, description_text: str,
               candidates: list[Candidate], threshold: float = THRESHOLD) -> Match | None:
    """The best existing job this posting is a copy of, or None.

    Requires the same normalized company, then `is_same_posting`. Among several matches the
    highest Jaccard wins, so an exact repost is preferred to a contained snippet.
    """
    ck = company_key(company)
    if not ck:
        return None
    best: Match | None = None
    for c in candidates:
        if company_key(c.company) != ck:
            continue
        if not is_same_posting(title, description_text, c.title, c.description_text, threshold):
            continue
        s = similarity(description_text, c.description_text)
        if best is None or s > best.similarity:
            best = Match(c.job_id, s)
    return best
