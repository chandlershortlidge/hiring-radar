"""Seed a throwaway database with plausible jobs and extractions, for looking at the dashboard.

Does: write ~40 synthetic jobs across both cities with skill mentions drawn from the real
taxonomy, a few reposts, closed jobs and proposed skills. No model calls.
Does NOT: touch data/hiring-radar.db unless you point HIRING_RADAR_DB at it (don't).

    HIRING_RADAR_DB=/tmp/demo.db uv run python scripts/seed_demo.py && HIRING_RADAR_DB=/tmp/demo.db uv run python -m app serve
"""

import os
import random
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from app import db  # noqa: E402
from app.extract import Extraction, Mention, Proposed, Seniority  # noqa: E402
from app.ingest import ingest_one  # noqa: E402
from app.pipeline import store_extraction  # noqa: E402
from app.sources import Posting  # noqa: E402
from app.taxonomy import Taxonomy  # noqa: E402

COMPANIES = ["Kestrel Labs", "Halyard Security", "Oberbaum Analytics", "Tessellate", "Fernweh Mobility", "Quillmark",
             "Sundial Health", "Brightline Freight", "Mosaic Ledger", "Aurelia Bio", "Nordlicht", "Parallax Audio",
             "Cinder Robotics", "Weissensee AI", "Harbor & Vane", "Lumen Legal", "Tidewater", "Spreewald Systems"]
TITLES = [("Senior AI Engineer, LLM Platform", "senior"), ("Applied ML Engineer", "mid"), ("AI Engineer (RAG & Search)", "mid"),
          ("Machine Learning Engineer, Agents", None), ("Data Scientist, GenAI", "mid"), ("Founding AI Engineer", "senior"),
          ("LLM Engineer", None), ("MLOps Engineer", "mid"), ("AI Engineer, Document Intelligence", "junior"),
          ("Applied Scientist, Foundation Models", "senior"), ("Junior AI Engineer", "junior"), ("Staff ML Engineer", "senior")]
WEIGHTS = {"python": 0.9, "llms": 0.75, "rag": 0.5, "aws": 0.4, "docker": 0.4, "pytorch": 0.35, "kubernetes": 0.3,
           "sql": 0.3, "langchain": 0.25, "gcp": 0.2, "vector-databases": 0.2, "fastapi": 0.18, "prompt-engineering": 0.18,
           "ci-cd": 0.15, "typescript": 0.15, "react": 0.1, "langgraph": 0.12, "llm-evaluation": 0.12, "mlops": 0.2}


def main():
    path = Path(os.environ.get("HIRING_RADAR_DB", "/tmp/hiring-radar-demo.db"))
    if path.name == "hiring-radar.db":
        sys.exit("refusing to seed the real database; set HIRING_RADAR_DB to a scratch path")
    if path.exists():
        path.unlink()
    conn = db.connect(path)
    db.migrate(conn)
    tax = Taxonomy.load()
    ids = [i for i in WEIGHTS if i in tax.skills]
    missing = [i for i in WEIGHTS if i not in tax.skills]
    if missing:
        print("skipping ids not in taxonomy:", missing)
    rng = random.Random(7)
    now = datetime(2026, 10, 17, 12, tzinfo=timezone.utc)
    n = 0
    for k in range(42):
        company = COMPANIES[k % len(COMPANIES)]
        title, sen = TITLES[(k * 5) % len(TITLES)]
        city = "Berlin" if k % 3 else "San Francisco"
        src = rng.choice(["arbeitnow", "startup_jobs", "greenhouse", "greenhouse", "screenshot", "paste"]) if city == "Berlin" else rng.choice(["greenhouse", "lever", "ashby", "url"])
        age = rng.choice([0, 0, 1, 1, 2, 3, 5, 8, 14, 25, 40, 70])
        first = (now - timedelta(days=age)).strftime("%Y-%m-%dT%H:%M:%SZ")
        skills = [s for s in ids if rng.random() < WEIGHTS[s] * (1.2 if city == "San Francisco" and s in ("pytorch", "typescript") else 1)]
        text = f"{company} is hiring a {title} in {city}. Requirements: " + ", ".join(tax.skills[s].display for s in skills) + ". " + f"Posting {k}."
        p = Posting(src, f"{src}-{k}" if src in ("arbeitnow", "startup_jobs", "greenhouse", "lever", "ashby") else "",
                    f"https://example.com/jobs/{k}", company, title, city, text)
        out = ingest_one(conn, p, first, require_city=False, trust_title=True, found_via="linkedin" if src in ("url", "paste", "screenshot") else None)
        if not out.startswith("new:"):
            continue
        job_id = int(out[4:])
        n += 1
        # feed jobs seen recently stay open; older ones were last seen when they were first seen
        last = now - timedelta(days=min(age, rng.choice([0, 0, 1, 2]))) if age < 10 else now - timedelta(days=age)
        conn.execute("UPDATE job SET last_seen=?, repost_count=? WHERE id=?",
                     (last.strftime("%Y-%m-%dT%H:%M:%SZ"), rng.choice([0, 0, 0, 0, 1, 2, 3]), job_id))
        mentions = [Mention(s, "required" if rng.random() < 0.75 else "nice_to_have", tax.skills[s].display) for s in skills]
        proposed = [Proposed(l, "required", f"experience with {l} is a plus") for l in rng.sample(["Model Context Protocol (MCP)", "DSPy", "Unsloth", "Modal"], k=1)] if rng.random() < 0.2 else []
        store_extraction(conn, job_id, Extraction(seniority=Seniority(sen, "stated", title) if sen else Seniority(None, None, None),
                                                   mentions=mentions, proposed=proposed, extractor_version="demo", taxonomy_version=tax.version))
    conn.commit()
    print(f"seeded {n} jobs into {path}")


if __name__ == "__main__":
    main()
