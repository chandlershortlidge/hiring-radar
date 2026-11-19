## 2026-11-19 — Skill list v12: nine entries from the three German labelling batches, reviewed as one pass (HIR-350)

**Why this came up.** The Hamburg, Frankfurt and Munich labelling batches (8 Nov, 42
postings) produced **299 phrases the two labelling models could not place** on the skill
list. Two Hamburg postings came out with no skills at all. The cause is dates, not a broken
lookup: those batches were labelled against v10, and v11 (HIR-219, 11 Nov) added 27 entries
three days later. Seventeen of the 299 resolve today without any change — Jenkins,
OpenShift, Azure DevOps, Angular, ArgoCD, Entra ID, MongoDB, Playwright and the rest.

**The bar, same as HIR-128 and HIR-219: three distinct postings.** Counted over the three
batches, with each posting counted once however many models named the phrase. Spelling
variants of one thing are merged; different products are not. Eight concepts cleared the
bar; 251 phrases sit at one or two postings and stay parked, listed on HIR-350.

**Nine entries land, v12, 253 skills.** Chandler's yes, 19 Nov, item by item.

- Azure data services, from the two postings that produced no skills at all:
  `azure-data-factory` [azure, data-pipelines], `azure-functions` [azure, serverless],
  `azure-sql-database` [azure, sql], `azure-data-lake-storage` [azure].
- `data-engineering` — six postings, the most asked-for of the lot. A practice, not a
  product, which the skill rules allow.
- `power-automate` 3 [workflow-automation] — the same kind of tool as n8n and Zapier, which
  are already entries. **"Power Platform" is not a spelling of it** and stays pending as
  HIR-219 left it: a posting naming the suite is not asking for Power Automate.
- `access-control` 3 — one entry for IAM, RBAC, ACL, identity management and least
  privilege, which the list had nothing for.
- `data-warehousing` 3 — "DWH", "data warehouse". **Star Schema and Data Vault become
  spellings of `data-modeling`** rather than entries of their own.
- `context-engineering` 3 — "context window management", "context window". The closest
  call: it sits beside prompt engineering and chain-of-thought, both already entries.

**Spellings added to entries we already had.** "Microsoft Foundry" → `azure-ai-foundry`
(the same product). "Pinecone" and "Qdrant" → `vector-databases`, as Chroma already is.
The Azure network phrases — VNets, private endpoints, service endpoints, network policies —
→ `networking`. "Security by design", "security reviews", "security standards" and
"Sicherheitskonzepte" → `cybersecurity`.

**Left out although they cleared the bar**, by the rule that a skill is a language,
framework, tool, platform, technique or technical practice:

- **Agile methods / agile ways of working** (3 postings) — a way of working. Consistent with
  Scrum staying out in HIR-219 and HIR-72.
- **JSON** (3 postings) — a data format. The list has no YAML, XML or CSV either.

**What it does not do.** Jobs already stored were read at v11 or earlier, so they do not
carry the new skills until they are read again; the re-read is a follow-up. The three German
batches must be labelled again by both models against v12 before their items are ruled on —
their cached replies say "unplaceable" for phrases the list now has.
