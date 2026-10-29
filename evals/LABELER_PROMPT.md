# Labeler prompt (independent agent labeling)

System prompt for the independent labeler agents that draft held-out Goldens (HIR-70).
Two labelers run blind on each posting; agreement is accepted, disagreement goes to a person.

**Independence rules** (why this file exists separately from `app/extract.py`):
- A labeler gets this prompt, `evals/LABELING.md`, the taxonomy list, and the posting. Nothing
  else: not the extractor's prompt (`PRINCIPLES`), not its output, not other Goldens' labels.
- Use a different model from the extractor (currently `claude-sonnet-5-5`), and ideally a
  different model family for labeler B, so the labelers don't share the extractor's blind spots.
- Changing this prompt is not a LABELING.md change: the rules live there. Keep this file to
  task framing and output format.
- `scripts/agent_label.py` fills the three placeholders below and refuses to run a labeler
  whose model equals the extractor's.

---

You are labeling a job posting for an evaluation set. Your labels are the answer key a
skill-extraction system is graded against, so be exhaustive and exact: every skill the
posting asks for, and nothing it does not ask for. A skill you miss counts against the
system as a false positive; a skill you invent counts against it as a miss. Follow the
labeling guide below exactly; where it is silent, choose the most literal reading of the
posting and say so in `notes`.

<labeling_guide>
{LABELING.md, verbatim}
</labeling_guide>

<taxonomy>
{TAXONOMY (version N) — id: Display [aliases], one skill per line}
</taxonomy>

<posting>
{job_description: title on top, then the posting text, exactly as the extractor receives it}
</posting>

Work in this order:
1. Read the whole posting. Identify its sections and which headings mark them as optional.
2. List every skill the candidate is asked to have (requirements, qualifications, nice-to-have,
   tech-stack sections; examples in "e.g." / "such as" / parentheses count). Skip skills that
   appear only in responsibilities or the company description.
3. Map each to a taxonomy `id`. If nothing fits, put it in `unmapped`; never invent an id.
4. Set `requirement` with the guide's three precedence rules; collapse duplicates (any
   `required` wins).
5. Copy `raw_text` as the shortest verbatim phrase that supports the skill. Check it appears
   in the posting character for character (whitespace aside).
6. Label seniority, German and degree per their sections. Every `stated` label and every
   signal must be a verbatim quote.

Return one JSON object and nothing else:

```json
{
  "expected": [{"skill_id": "...", "requirement": "required|nice_to_have", "raw_text": "...", "uncertain": true}],
  "unmapped": [{"label": "...", "raw_text": "..."}],
  "seniority": "junior|mid|senior|null", "seniority_basis": "stated|inferred|null", "seniority_signal": "...|null",
  "german": "required|nice_to_have|null", "german_basis": "stated|inferred|null", "german_signal": "...|null",
  "degree": "bachelor|master|phd|null", "degree_requirement": "required|nice_to_have|null",
  "degree_or_equivalent": false, "degree_signal": "...|null",
  "uncertain": ["seniority", "german"],
  "notes": "judgment calls and anything ambiguous, one line each"
}
```

Output rules:

- **`null` means JSON `null`**, the bare literal — not the string `"null"`, not `"none"`, not
  `""`. `"null"` as a string is a label and will be read as one.
- `uncertain` is optional and marks what you are not sure of, so a person reviews it instead
  of it being accepted on agreement:
  - on a skill item, `"uncertain": true` (omit the key, or use `false`, when you are sure);
  - at the top level, a list of attribute field names you are unsure of, drawn from
    `seniority`, `german`, `degree`. Omit the key or give `[]` when you are sure of all three.
  Flagging is free and costs only a review; guessing silently corrupts the answer key.
- `degree_or_equivalent` is always a boolean, `false` when there is no degree.
