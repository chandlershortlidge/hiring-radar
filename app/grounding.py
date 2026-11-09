"""Does every snippet the model quoted as evidence really appear in the posting?

Does: one pure count, (grounded, total), over the quotes of a single extraction.

Does NOT: read files, call a model, store anything, or decide what to do about a failure.
The eval turns the count into a score (app/evaluation.py); the live pipeline puts it on
the job's trace (app/langsmith_live.py). Neither changes what is stored because of it.

Invariants: pure and deterministic; the comparison is whitespace- and case-insensitive,
the same one app/extract.py makes when it drops a quote it cannot find. It lives here,
below both callers, so the eval and the live poll can never measure grounding differently
(HIR-160).
"""

import re

_WS = re.compile(r"\s+")

# The reason app/extract.py records when it drops a skill whose quote is not in the
# posting. Those rejects are grounding failures the extractor already caught, and they
# count against the total here, so catching one does not improve the score.
UNGROUNDED_REASON = "raw_text not found in job text"


def _quote(item) -> str:
    """raw_text off a Mention/Proposed dataclass or the dict form of one."""
    if isinstance(item, dict):
        return str(item.get("raw_text") or "")
    return str(getattr(item, "raw_text", "") or "")


def grounding(jd_text: str, mentions, proposed, rejected) -> tuple[int, int]:
    """(grounded, total) over every skill quote the model returned for one posting.

    An invented quote is a different failure from a wrong skill: it says the model made
    its evidence up. The extractor already drops a skill whose quote it cannot find, so
    those arrive here in `rejected` and count against the total. The quotes it kept are
    re-checked all the same, so a regression in that check shows as a falling score
    instead of passing silently.

    Whitespace- and case-insensitive, the same comparison the extractor makes.
    """
    jd = _WS.sub(" ", jd_text).strip().lower()
    kept = [_quote(x) for x in list(mentions) + list(proposed)]
    grounded = sum(1 for q in kept if q and _WS.sub(" ", q).strip().lower() in jd)
    ungrounded = sum(1 for r in rejected if isinstance(r, dict) and r.get("reason") == UNGROUNDED_REASON)
    return grounded, len(kept) + ungrounded
