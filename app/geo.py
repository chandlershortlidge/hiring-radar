"""Map a source's free-text location to one of the cities we track.

Does: recognize the tracked cities (and their common spellings) inside a location string,
and say which of them are active.

A city can be tracked without being active. `city_of` recognizes every tracked city (manual
adds keep their real city). Only ACTIVE_CITIES pass the ingest and discover-boards filters
(`active_city`). Making a tracked city active is a deliberate one-line change: San
Francisco waits until Berlin extraction passes the held-out eval (DECISIONS 2026-10-19).

Does NOT: geocode, handle cities we don't track (returns None), or decide remote policy —
"Remote (Germany)" maps to None, and that's deliberate for a by-city comparison.

Invariant: pure; matching is case-insensitive on whole words.
"""

import re

CITIES: dict[str, tuple[str, ...]] = {
    "Berlin": ("berlin",),
    "San Francisco": ("san francisco", "sf bay area", "bay area", "south san francisco"),
}

ACTIVE_CITIES: tuple[str, ...] = ("Berlin",)

_PATTERNS = {city: re.compile(r"\b(" + "|".join(re.escape(a) for a in aliases) + r")\b", re.I)
             for city, aliases in CITIES.items()}


def city_of(location_raw: str | None) -> str | None:
    if not location_raw:
        return None
    for city, pat in _PATTERNS.items():
        if pat.search(location_raw):
            return city
    return None


def active_city(location_raw: str | None) -> str | None:
    """The city if it is tracked AND active, else None. This is the filter ingest uses."""
    city = city_of(location_raw)
    return city if city in ACTIVE_CITIES else None
