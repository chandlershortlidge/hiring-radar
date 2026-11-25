## 2026-11-25 — Forward Deployed Engineer is its own career track, decided by the title's FDE words first (HIR-408)

Chandler, 21 Nov, re-confirmed 25 Nov: Forward Deployed Engineer is its own career choice
in the job-type menu, live in every city.

**Why.** A forward deployed engineer builds and ships AI systems inside a customer's
environment. The skills asked for are AI-engineering skills plus customer-facing work, so
the existing skill list reads these postings well. But until now most of them were not
collected at all: the title filter wanted an AI word in the title, and "Forward Deployed
Engineer" usually has none. The ones that did get in landed under AI Engineer (about 60 of
the stored jobs on 25 Nov), where they could not be told apart.

**Which titles are Forward Deployed Engineer.** From the title alone, like every other
track. The title is lowercased, the characters `- / ( ) , .` become spaces (the same set
the `mle` test uses), and the title counts when it contains:

| the title says | example |
| -- | -- |
| "forward deployed" or "forward deployment" as words, **and** "engineer" anywhere | "Forward Deployed AI Engineer", "Software Engineer, Forward Deployed AI Solutions", "Forward Deployment Engineer", "Senior Manager, AI Forward Deployed Engineering" |
| "FDE" as a word | "Senior Software Engineer - AI, FDE", "Forward Deployed AI Architect – FDE" |
| "deployed engineer" | "Deployed Engineer" |

**The FDE words decide first.** A title that names an FDE role and another track goes to
Forward Deployed Engineer: "Forward Deployed Machine Learning Engineer" is FDE, not ML
Engineer; "AI Engineer / Forward Deployed Engineer" is FDE, not AI Engineer. This is the
one track whose words outrank the built-in AI/ML rule. It departs on purpose from the
rule of 21 Nov (HIR-395) that a track added later takes only titles the five original
tracks do not hold: Chandler's ticket asks for exactly this, and without it the ~60 FDE
jobs already stored would stay under AI Engineer. Any track added after this one still
follows the 21 Nov rule unless its own line says otherwise.

**A title with the FDE words passes the title filter without an AI word.** Sales titles
stay out as before ("Forward Deployed Sales Engineer", "pre-sales": the rule of 16 Nov,
HIR-246).

**The boundary.** Solutions engineer, solutions architect, customer engineer and
implementation engineer are **not** Forward Deployed Engineer and are not collected for
it. They are the adjacent roles, often sales-leaning; none of their titles contains the
FDE words, so the rule above leaves them out without a list of its own. One with an AI
word in the title ("AI Solutions Engineer") stays where the built-in rule puts it, as
before.

**Known limits.**

- "Forward Deployed Data Scientist" or "Forward Deployed Strategist" name no engineer, so
  they are not FDE: a data scientist stays a data scientist, and a strategist with no AI
  word is not collected.
- "Deployed engineer" is in the rule because the ticket names it. A non-AI "Field Deployed
  Engineer" would be collected under it. None is stored today; if they appear, the phrase
  goes.
- "FDE" next to a character outside the list above ("[FDE]", "FDE:") is not read as the
  word. Every stored FDE title is matched by its other words anyway.

**The model does not decide the track.** The ticket asked for the extractor's
`job_family` to gain the value. The extractor has no such field: the track is a title
rule (5 Nov, "Job family is a title rule (v1)", HIR-186), so the model's prompt and
version are unchanged, no job is re-read, and the eval gate does not apply.

**Stored jobs.** A migration re-labels every stored job with the full rule, so stored jobs
and new ones agree. The only jobs it can move are titles with the FDE words; a test holds
it to that.

**To undo:** set the track to incubating in `app/scope.py` to hide it at once; to remove
it, revert the change and add a migration that runs the 24 Nov rule (027) over every job
again. Titles are untouched, so every job goes back where it was. FDE postings collected
meanwhile with no AI word in the title would then sit under AI Engineer: delete them or
leave the track incubating.
