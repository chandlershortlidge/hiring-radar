// CV text → taxonomy skill ids, to pre-select the profile's chips. Runs in the browser and
// nowhere else: the CV never reaches the server or a provider (DECISIONS 2026-11-01, HIR-14).
//
// Does: find every taxonomy skill whose display name or one of its aliases appears in the
// CV text as a whole word, and report which phrase matched so the UI can show its work.
//
// Does NOT: call a model, rank, score, infer a seniority or anything else about the person,
// read files (that's cvText.js), or decide what a skill is — the taxonomy does that. The
// result is a suggestion the person edits before saving; it is never saved on its own.
//
// Invariants:
//   - Matching is literal. A paraphrase the taxonomy has no alias for is missed, by design:
//     a miss costs one click, a false positive quietly corrupts every job match afterwards.
//   - A phrase matches only at word boundaries, so "Go" does not match "going" and "RAG"
//     does not match "ragged". A boundary is required on each side where the phrase's own
//     edge character is a letter or digit — so "C++" still matches in "C++11".
//   - Case-insensitive, except the phrases in CASE_SENSITIVE: "ReAct" (the agent pattern)
//     and "React" (the framework) differ only by case, exactly as app/taxonomy.py has it.
//   - Phrases shorter than MIN_PHRASE characters are never matched. "R", "C#" and "Go" as
//     bare tokens are far more often prose, an initial or "go-live" than a skill claim.
//     "Go" is still reachable through its "golang" alias; R and C# stay hand-ticked.
//   - Whitespace is collapsed before matching, the same way app/extract.py's _norm does it,
//     so a PDF that wraps "Machine Learning" across two lines still matches. Without this a
//     wrapped multi-word skill is missed, and PDFs wrap constantly.
//   - Pure and deterministic: same text in, same ids out, sorted by id.

export const MIN_PHRASE = 3;
export const CASE_SENSITIVE = new Set(["ReAct", "React"]);

const ALNUM = /[\p{L}\p{N}]/u;

function alnum(ch) {
  return ch !== undefined && ALNUM.test(ch);
}

// One space between words, no leading or trailing space. Mirrors app/extract.py's _norm.
export function collapse(s) {
  return (s || "").replace(/\s+/g, " ").trim();
}

// A phrase occurs in `text` as a whole word. `text` and `phrase` must already agree on case.
export function occursAsWord(text, phrase) {
  if (!phrase) return false;
  const needLeft = alnum(phrase[0]);
  const needRight = alnum(phrase[phrase.length - 1]);
  let from = 0;
  for (;;) {
    const at = text.indexOf(phrase, from);
    if (at === -1) return false;
    const leftOk = !needLeft || !alnum(text[at - 1]);
    const rightOk = !needRight || !alnum(text[at + phrase.length]);
    if (leftOk && rightOk) return true;
    from = at + 1;
  }
}

// The phrases that stand for a skill: its display name first, then its aliases.
export function phrasesFor(skill) {
  const all = [skill.display, ...(skill.aliases || [])];
  return all
    .filter((p) => typeof p === "string")
    .map(collapse)
    .filter((p) => p.length >= MIN_PHRASE);
}

/**
 * Match a CV's text against the taxonomy.
 *
 * `skills` is the taxonomy as the browser already holds it: [{ id, display, aliases }].
 * Returns { ids, found }, where `found` carries the phrase that matched each skill so the
 * drawer can tell the person why a chip is ticked. Sorted by id.
 */
export function matchCvSkills(cvText, skills) {
  const text = collapse(typeof cvText === "string" ? cvText : "");
  const lower = text.toLowerCase();
  const found = [];

  for (const skill of skills || []) {
    if (!skill || !skill.id) continue;
    for (const phrase of phrasesFor(skill)) {
      const exact = CASE_SENSITIVE.has(phrase);
      const hit = exact
        ? occursAsWord(text, phrase)
        : occursAsWord(lower, phrase.toLowerCase());
      if (hit) {
        found.push({ id: skill.id, display: skill.display, phrase });
        break; // one reason is enough; the display name is tried first
      }
    }
  }

  found.sort((a, b) => (a.id < b.id ? -1 : a.id > b.id ? 1 : 0));
  return { ids: found.map((f) => f.id), found };
}
