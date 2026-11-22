## 2026-11-21 — A slash between two skills of the same kind ("Terraform/CloudFormation") offers either one (HIR-390)

**The rule.** In the labelling guide's "any one of" markers (`alternative_group`), a slash
between two skills of the same kind offers either one: "Terraform/CloudFormation",
"PyTorch/TensorFlow". Both skills are labelled as usual and share one group.

**Not a pair.** A slash that does not join two skills of the same kind: "CI/CD" (one skill),
"Power BI/DAX" (a tool and its formula language), "Git & GitHub" (no slash; a tool and a
service built on it). Those are labelled as before and not grouped.

**Why.** Chandler, 20 Nov, spot-checking the 19 Nov city batches on a Slalom posting
("AWS Agentic AI Engineer – Amazon Quick Suite", batch 20261119T141542Z, golden_108),
which lists under Preferred "Terraform/CloudFormation, Git, CI/CD, testing and Jira":
"“Terraform/CloudFormation” is an either/or pair, so the two should share a group." The
guide's markers did not name a slash, so the two grouping models left the pair ungrouped,
and CloudFormation was not on the skill list. It was added in the same change (skill list
v13).

**Scope.** The rule is in the guide that the labelling models and the grouping models read.
The extractor's own grouping instruction does not name the slash yet; until it does, the
skill-group score can count a slash pair the extractor leaves ungrouped as a miss.

**How to undo.** Remove the slash bullet from the guide's `alternative_group` section, and
the groups this change added to answer keys and batch review files (listed in the HIR-390
pull request).
