# Home screen wireframes (HIR-188)

Drawn 5 Nov 2026. Grey wireframes, not visual design: spacing and hierarchy are the spec, colours are not.

The look chosen since (colours 14 Nov, layout 17 Nov, HIR-285) is in [`../style.md`](../style.md). Where the two differ, `style.md` wins: the market grid in `01-home.png` is now a ranked table, and a city's chart and jobs sit side by side.

| file | screen |
|---|---|
| 01-home.png | First visit, no city chosen: query bar + market grid |
| 02-dashboard.png | Returning visitor: query bar replaces the city tabs |
| 03-city-picker.png | City picker open: search, grouped list, counts |
| 04-compare.png | Compare mode: up to three cities as columns |
| 05-phone.png | Phone width |

`[n]` marks numbers the real page takes from `/api/stats` and `/api/skills`. "New this week" is shown on the cards but has no data yet and is out of scope for HIR-188.
