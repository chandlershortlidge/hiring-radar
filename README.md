# hiring-radar

What skills is the AI-engineering job market asking for — and how does that differ by city?

hiring-radar collects job descriptions from job-board feeds, pasted links, and
screenshots, maps each one to a versioned skill taxonomy with an LLM, and shows which
skills appear most often. Extraction quality is measured against a labeled set with a
held-out split.

**Status:** early. Schema, taxonomy, and labeled Goldens are in place; extraction, intake,
and the dashboard are next. See [DECISIONS.md](DECISIONS.md) for the design and why.

This is a rebuild of [job-skills-dashboard](https://github.com/chandlershortlidge/job-skills-dashboard),
a one-day hackathon project.

```bash
uv sync
uv run pytest
```

MIT licensed.
