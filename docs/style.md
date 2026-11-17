# How the site looks: the style rules (HIR-285)

Chandler chose this look from pictures: the colours on 14 Nov 2026, the layout on 17 Nov
2026 (direction A, "data first", plus the fit line from direction B). Every frontend
change follows these rules without asking. A change that needs to break one is a visual
direction call, and those are Chandler's (AGENTS.md "What Chandler is asked", item 3).

The values live once, as CSS variables at the top of `web/src/styles.css`. Use the
variable, never a hex code, in new CSS.

## Colour

| Name | Variable | Hex | Used for |
|---|---|---|---|
| Background | `--ground` | `#F9F7F5` | Page background, the hover and open state of a row |
| White | `--paper` | `#FFFFFF` | Cards, the header, the hero band, inputs |
| Light stone | `--stone` | `#EEE8E1` | Bar tracks, chart grid lines, row dividers, neutral chips and badges |
| Warm grey | `--warm-grey` | `#D0C3B7` | Card and input borders, dashed "add" controls |
| Ink | `--ink` | `#1F1A1C` | Text |
| Secondary text | `--ink-2` | `#6B5F63` | Labels and muted text (4.5:1 on white and on the background) |
| Plum | `--plum` | `#603C5F` | Leads the site: skill bars, the first city in compare, active filter pills, links, the logo, the Connect-Claude strip |
| Plum tint | `--plum-tint` | `#CFC4CF` | Skills not yet in the profile: their bars, their chips, the gap chips |
| Peach | `--peach` | `#FAB995` | The second city in compare; the fill of the main buttons |
| Coral | `--coral` | `#F38155` | Outlines only: main buttons, the job-family button, the Connect-Claude pill, warning chips on a job; the dot in the logo |
| Butter | `--butter` | `#FCDEA6` | Highlights: best-fit badges (90% and up), open-job counts, the proposed-skills count, the underline behind a headline number |
| Brand gradient | `--brand-gradient` | `#FCDEA6` → `#F89781` → `#6B4769` | One 4px rule under the header. Nowhere else, never behind data |

Rules that follow from the palette:

- **Text on colour.** White text only on plum. Peach, coral, butter, plum tint and stone
  always carry ink text (white on coral is 2.6:1, on peach 1.7:1).
- **Coral is never a fill.** Chandler rejected solid coral buttons.
- **One series is plum.** A second series is peach. There is no chosen colour for a third
  compared city; it is drawn in warm grey until Chandler picks one.
- **Missing is a colour, not a pattern.** A skill the visitor does not have is plum tint,
  solid. No hatching, no hollow outlines (both tried and rejected).
- **Peach bars are below the 3:1 guideline for chart marks** (about 1.6:1 on white).
  Chandler accepted the look; every peach bar therefore has its percentage printed
  beside it.
- **No new colours.** No shadows tinted with colour, no gradients other than the header
  rule, no darker "edge" on a bar.

Tried and rejected, so not to be proposed again: solid coral buttons; a darker coral edge
on bars; mustard `#F1AC34` for badges; coral bars for the second city; hollow bars for
missing skills; a full-width Connect-Claude band ("very distracting").

## Buttons and controls

| Control | Fill | Outline | Text | Class |
|---|---|---|---|---|
| Main button ("+ Add a job", the city picker, a drawer's submit) | Peach | Coral | Ink | `.btn.primary`, `.btn.outline`, `.qb-btn` on the city picker |
| Job-family picker | White | Coral, 2px | Ink | `select.qb-sel` |
| Secondary button ("Show 15 more", "Load 20 more") | White | Plum | Plum | `.btn` |
| Filter pill, off | White | Warm grey | Ink | `.fpill` |
| Filter pill, on | Plum | Plum | White | `.fpill[aria-pressed="true"]`, `.fpill.on` |
| "Add" control ("+ Compare with…", "More filters", "+ Add skill") | White | Warm grey, dashed | Secondary text | `.qb-btn.add`, `.fpill.more`, `.chip-add` |
| Header pill (profile, proposed skills) | White | Warm grey | Ink | `.pill` |
| Connect-Claude pill | White | Coral, 2px | Ink | `.pill.connect` |

- Anything a finger presses on its own is 44px high: header pills, buttons, filter pills,
  pickers. Small controls inside a dense row (the star, the flag, a chip's remove button)
  may be smaller.
- Pills are fully rounded (radius = half the height). Buttons and inputs have a 6px
  radius, pickers 8px.
- Keyboard focus is a 2px plum outline, 2px away from the control.

## Type

Two families, both already loaded: **IBM Plex Sans** for everything a person reads,
**IBM Plex Mono** for numbers, counts, the logo and small uppercase labels.

| Role | Size / line height | Weight | Notes |
|---|---|---|---|
| Home headline | 46px / 1.12 (30px on a phone) | 700 | letter-spacing -0.02em; headline numbers get a butter underline |
| Fit line ("You have 12 of the 15…") | 26px / 1.2 (20px on a phone) | 700 | letter-spacing -0.015em |
| Card title (the chart's heading, a job's title on its page) | 21px (17px on a phone) | 600 | letter-spacing -0.01em |
| Section heading ("All 7 markets") | 18px | 600 | |
| Small card heading (jobs list, related skills) | 15–16px | 600 | |
| Body | 14px / 1.4 | 400 | |
| Secondary line, help text | 12.5–13px | 400 | secondary text colour |
| Numbers beside bars, badges | 12px mono | 500–600 | |
| Label above a block ("BERLIN · 271 OPEN JOBS") | 11.5–12px mono, uppercase | 400 | letter-spacing 0.06em, secondary text colour; class `.eyebrow` |

Nothing smaller than 10.5px. No third font family.

## Spacing and layout

- The page is one centred column, at most 1200px wide, with 24px at the sides (16px on a
  phone). The phone breakpoint is 720px.
- Spacing steps: 4, 8, 12, 16, 20, 24px. Cards sit 16px apart. A card's padding is
  20–24px (16px on a phone).
- **Home:** a white band holding the headline and the pickers on the left and the
  top-skills chart on the right; under it the Connect-Claude strip; under that every
  market as one ranked table. The band's two halves stack on a narrow screen.
- **City page:** the fit line (only once a profile has skills) in a white band; then the
  chart on the left and the jobs on the right, side by side from 1024px up, stacked below
  that. Smaller panels (what's rising, related skills) go under the chart, in the left
  column.
- **Compare** keeps one column: the chart needs the full width for its two or three
  city columns.

## Cards, tables and rows

- A card is white, with a 1px warm-grey border and an 8px radius. No shadow. (Pop-overs
  and drawers, which float above the page, keep a soft neutral shadow.)
- A list inside a card (jobs, markets) is rows divided by a 1px light-stone line. A row
  that is a link or a button turns the background colour on hover.
- A job row is two lines: the title in 14px/600, then company · city · when in secondary
  text. The fit badge sits on the right.
- Badges and neutral chips: mono 12px, 4px radius, light-stone fill. Best fit (90% and
  up) is butter. A warning on a job (flagged, a hard requirement the profile fails) is a
  white chip with a coral outline.

## Charts

- Bars are plain CSS, 22px high, with a 3px radius on the right end only, on a track of
  light-stone grid lines at every quarter of the scale.
- The value sits to the right of the bar in mono: the count in ink, the percentage in
  secondary text.
- With a profile: plum for a skill in it, plum tint for one not yet in it, and a legend
  under the chart that says so.
- Small bars inside a table row (the markets table) are 6px high, fully rounded, plum on
  a light-stone track.

## The Connect-Claude (MCP) pieces

- A small plum strip with butter "MCP" label and white text: under the hero on the home
  page, on top of the jobs list on a city page. Never a full-width band.
- A coral-outlined "Connect Claude" pill in the header on every page.
- Their wording is a placeholder until the Claude connection is built and the launch
  wording is settled; until then both say that it is not available yet and neither is a
  working button.

## What these rules do not settle

- A colour for a third compared city.
- How compare shows skills that are not in the profile.
- The final wording of the home headline and the Connect-Claude line (launch wording).
