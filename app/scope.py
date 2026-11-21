"""The one list of what is collected, and whether the public may see it yet (HIR-395).

Does: give every collected place (a city, or EU-remote) and every career track one of two
states. `live` is collected and shown. `incubating` is collected in exactly the same way
(fetched, deduplicated, screened, read, looked after; reading can be put off, below) and shown nowhere public: not on the
dashboard, not in its counts, pickers or "what's rising", not through the public API and
not through any MCP tool. An incubating place or track gathers history, so that on the day
it is switched to live it already has weeks behind it.

Switching one to live is changing its state on its line below, and nothing is collected
again: the jobs keep the day they were first seen. Two checks then name what else that
line needs, and fail until it is there: the dashboard's own list of places and tracks
(tests/test_frontend_lists.py), and for a city the launch check (scripts/launch_check.py).

Adding a track is two things. Its line in TRACKS, with the title pattern that says which
job titles belong to it; and a migration that adds its name to the values the database
accepts in `job.family` (tests/test_allowed_answers.py fails, naming the column, until
both agree). Adding a city is its line in PLACE_STATE plus what app/geo.py already asks of
any collected city (its spellings, its start date, its region).

Reading can wait (HIR-396). A place or track can also be set to `read: later`: its
postings are still fetched, deduplicated, screened, dated and stored, but the model does
not read them until someone runs `python -m app read-pending` for it, once its skill list
exists. Only an incubating place or track may read later (tests/test_scope.py): a live one
would show jobs with no skills. A track says so on its own line (`read=READ_LATER`); a
place by an entry in PLACE_READ, which lists only the places that read later. Which jobs
that holds back is app/pipeline.py's `held_clause`.

Does NOT: decide which places or tracks are collected or incubated (Chandler names them),
recognise a place in a location string (app/geo.py), or judge a title (app/ingest.py reads
the patterns below). It imports nothing from this project, so every module may read it.

Invariants: every state is LIVE or INCUBATING; the readers below look the state up at call
time, so a changed state takes effect everywhere at once; PLACE_STATE's order is the order
places are listed in, and TRACKS' order is the order of the dashboard's buttons.
"""

from dataclasses import dataclass

LIVE, INCUBATING = "live", "incubating"
STATES = (LIVE, INCUBATING)

# Whether the model reads a place's or track's postings as they arrive, or only when
# `python -m app read-pending` is run for it (HIR-396).
READ_NOW, READ_LATER = "now", "later"
READS = (READ_NOW, READ_LATER)

# Every collected place. The names are app/geo.py's (a key of geo.CITIES, or geo.REMOTE_EU);
# tests/test_scope.py fails on a name geo does not know.
PLACE_STATE: dict[str, str] = {
    "Berlin": LIVE,
    "Remote (EU)": LIVE,
    "San Francisco": LIVE,
    "New York": LIVE,
    "Hamburg": LIVE,
    "Frankfurt": LIVE,
    "Munich": LIVE,
    "Austin": LIVE,
    "Boston": LIVE,
    "London": LIVE,
    "Amsterdam": LIVE,
    "Seattle": LIVE,
    "Los Angeles": LIVE,
    "Chicago": LIVE,
    "San Jose": LIVE,
}

# The places whose postings are stored unread (HIR-396). A place not listed reads now.
PLACE_READ: dict[str, str] = {}


@dataclass(frozen=True)
class Track:
    """One career track. `title_pattern` is a regular expression (matched anywhere in the
    title, case-insensitive) naming the titles that belong to the track. None means the
    track is one of the five the built-in AI/ML title rule sorts (app/ingest.py: an AI/ML
    domain word plus a technical role word, then `family_of`).

    A track with a pattern only ever takes titles the built-in rule does not: a title the
    five tracks already hold stays where it is, so adding a track, in either state, never
    changes what the existing tracks collect or show.

    `read` is READ_LATER while the track's postings are stored without being read by the
    model (HIR-396)."""

    state: str
    title_pattern: str | None = None
    read: str = READ_NOW


TRACKS: dict[str, Track] = {
    "ai-engineer": Track(LIVE),
    "ml-engineer": Track(LIVE),
    "data-scientist": Track(LIVE),
    "ml-platform": Track(LIVE),
    "research": Track(LIVE),
}


def places(state: str | None = None) -> tuple[str, ...]:
    """The collected places, in order; with a state, only the places in that state."""
    return tuple(p for p, s in PLACE_STATE.items() if state is None or s == state)


def tracks(state: str | None = None) -> tuple[str, ...]:
    """The collected tracks, in order; with a state, only the tracks in that state."""
    return tuple(t for t, track in TRACKS.items() if state is None or track.state == state)


def live_places() -> tuple[str, ...]:
    return places(LIVE)


def incubating_places() -> tuple[str, ...]:
    return places(INCUBATING)


def live_tracks() -> tuple[str, ...]:
    return tracks(LIVE)


def incubating_tracks() -> tuple[str, ...]:
    return tracks(INCUBATING)


def read_later_places() -> tuple[str, ...]:
    """The places whose postings are stored unread until `read-pending` is run (HIR-396)."""
    return tuple(p for p in PLACE_STATE if PLACE_READ.get(p, READ_NOW) == READ_LATER)


def read_later_tracks() -> tuple[str, ...]:
    """The tracks whose postings are stored unread until `read-pending` is run (HIR-396)."""
    return tuple(t for t, track in TRACKS.items() if track.read == READ_LATER)
