## 2026-11-17 — The site's look: plum-led colours, and the "data first" layout (HIR-285)

**What Chandler chose, from pictures.** Colours on 14 Nov ("the colors are great"): a
plum-led palette on a warm off-white, with peach, coral and butter as accents. Layout on
17 Nov: direction A, "data first", plus one piece of direction B.

- **Home.** A headline built from live numbers, the "[job family] in [city]" pickers
  under it, the real top-skills chart beside it, and every market below as one ranked
  table (city, open jobs, top three skills) instead of a grid of cards.
- **City page.** Chart on the left, jobs on the right, so clicking a bar filters a list
  that is already in view; they stack on a phone. Filters are a row of pills above the
  chart.
- **From B.** Once a profile exists, the city page opens with "You have N of the 15
  skills [city] asks for most" and the biggest gaps as chips. With no profile the line is
  not shown.
- **Connect Claude.** A small plum strip (under the hero at home, on top of the jobs list
  on a city page) and a coral-outlined pill in the header. He rejected a full-width band
  as "very distracting".
- **Not chosen.** B's CV-upload home page and C's job-board page.

**Why.** The first visitor is a stranger without a CV. What they want at once is their
city and their job, so the market data has to work with no input.

**The rules.** Written down in `docs/style.md`: colours, buttons, type, spacing, cards
and charts. Every later frontend change follows that file without asking; changing the
look itself stays Chandler's call.

**What stays as it was.** The "[job family] in [city]" sentence, the searchable city
picker and compare as a mode (5 Nov wireframes). Only the market grid changed shape, into
the ranked table.

**Still open** (his, not settled by this): a colour for a third compared city; how compare
shows skills not in the profile; the final wording of the headline and of the
Connect-Claude line.
