"""Rules duplicate detection must keep for every input, not just the ones we thought of.

Each test states one rule and Hypothesis generates the postings (HIR-333). The postings
are a mix of two kinds on purpose: free text, which finds the odd characters, and words
drawn from a small vocabulary, which is the only way two generated postings ever overlap
enough to reach the similarity and containment paths.

What "blank" means here: a posting with no title words and no text words, as dedup itself
sees words (letters a-z and digits). A posting with a title and no text is NOT blank to
dedup: an exact title match at the same company is a duplicate with no text at all, by
design (HIR-108), and `test_no_text_matches_only_on_the_exact_title` pins exactly that.
"""

from hypothesis import assume, example, given, strategies as st

from app import dedup

VOCAB = ("ai engineer senior python rag llm berlin team build agents data pipeline cloud "
         "aws docker kubernetes remote hybrid years experience we you our gmbh m w d und").split()
SPACES = (" ", "  ", "\n", "\t", "\r\n", " \n ")

free_text = st.text(max_size=60)
vocab_text = st.lists(st.sampled_from(VOCAB), max_size=90).map(" ".join)
text = st.one_of(free_text, vocab_text)
titles = st.one_of(st.text(max_size=30), st.lists(st.sampled_from(VOCAB), max_size=5).map(" ".join))
blank = st.text(alphabet=" \t\n-–·!?()/äöü", max_size=12)
posting = st.tuples(titles, text)


def is_blank(s: str) -> bool:
    return not dedup._words(s)


@st.composite
def respaced(draw, s: str) -> str:
    """`s` with every run of whitespace swapped for another, and padding at both ends."""
    gap = st.sampled_from(SPACES)
    parts = s.split()
    out = draw(st.sampled_from(("",) + SPACES))
    for i, part in enumerate(parts):
        out += part + (draw(gap) if i < len(parts) - 1 else "")
    return out + draw(st.sampled_from(("",) + SPACES))


RECASE = (str.upper, str.lower, str.swapcase, str.title, str.capitalize)


@given(posting, posting)
def test_the_answer_does_not_depend_on_order(a, b):
    (ta, xa), (tb, xb) = a, b
    assert dedup.similarity(xa, xb) == dedup.similarity(xb, xa)
    assert dedup.containment(xa, xb) == dedup.containment(xb, xa)
    assert dedup.is_same_posting(ta, xa, tb, xb) == dedup.is_same_posting(tb, xb, ta, xa)


@given(posting, st.sampled_from(("Acme GmbH", "logen.ai", "Über AG")))
def test_a_posting_is_a_duplicate_of_itself(p, company):
    title, body = p
    assume(not (is_blank(title) and is_blank(body)))
    assert dedup.is_same_posting(title, body, title, body)
    match = dedup.find_match(company, title, body, [dedup.Candidate(7, company, title, body)])
    assert match is not None and match.job_id == 7


@given(st.data(), posting)
def test_extra_whitespace_does_not_stop_a_posting_matching_itself(data, p):
    title, body = p
    assume(not (is_blank(title) and is_blank(body)))
    title2, body2 = data.draw(respaced(title)), data.draw(respaced(body))
    assert dedup.title_key(title2) == dedup.title_key(title)
    assert dedup.is_same_posting(title, body, title2, body2)


@given(posting, st.sampled_from(RECASE), st.sampled_from(RECASE))
@example(("", "0ß"), str.upper, str.upper)   # what the first sweep found: ß is SS in capitals
def test_letter_case_does_not_stop_a_posting_matching_itself(p, recase_title, recase_body):
    title, body = p
    assume(not (is_blank(title) and is_blank(body)))
    assert dedup.is_same_posting(title, body, recase_title(title), recase_body(body))


@given(text, text)
def test_similarity_is_between_0_and_1(a, b):
    assert 0.0 <= dedup.similarity(a, b) <= 1.0
    assert 0.0 <= dedup.containment(a, b) <= 1.0
    match = dedup.find_match("Acme", "AI Engineer", a, [dedup.Candidate(1, "Acme", "AI Engineer", b)])
    assert match is not None and 0.0 <= match.similarity <= 1.0


@given(blank, blank, posting)
def test_a_blank_posting_is_never_a_duplicate(blank_title, blank_body, other):
    title, body = other
    assert not dedup.is_same_posting(blank_title, blank_body, title, body)
    assert not dedup.is_same_posting(title, body, blank_title, blank_body)
    assert not dedup.is_same_posting(blank_title, blank_body, blank_title, blank_body)
    assert dedup.find_match("Acme", blank_title, blank_body, [dedup.Candidate(1, "Acme", title, body)]) is None
    assert dedup.find_match("Acme", title, body, [dedup.Candidate(1, "Acme", blank_title, blank_body)]) is None


@given(titles, blank, posting)
def test_no_text_matches_only_on_the_exact_title(title, blank_body, other):
    """A posting with a title and no text is a duplicate of another only when the two titles
    normalize to the same thing: the one path that needs no text (HIR-108)."""
    other_title, other_body = other
    same_title = bool(dedup.title_key(title)) and dedup.title_key(title) == dedup.title_key(other_title)
    assert dedup.is_same_posting(title, blank_body, other_title, other_body) == same_title


@given(blank, posting, posting)
def test_a_posting_with_no_company_never_matches(blank_company, new, stored):
    cands = [dedup.Candidate(1, blank_company, *stored), dedup.Candidate(2, "Acme", *stored)]
    assert dedup.find_match(blank_company, *new, cands) is None
