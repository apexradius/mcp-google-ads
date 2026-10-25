# Google Ads reporting MCP - begin here

## Purpose

| Question | Answer |
| --- | --- |
| **Whom?** | advertising analyst comparing explicitly selected Google Ads customer accounts. |
| **What?** | Make Google Ads account, campaign, keyword, search-term and ad reporting available through one local multi-account MCP server, without switching servers for each account. |
| **Where?** | README.md, pyproject.toml, gads/server.py. |
| **Why it exists?** | Google Ads reporting MCP needs this document to start the next task with the product’s actual purpose. |
| **Why this approach?** | Reporting is read-only with respect to advertising campaigns. |
| **Why it matters?** | Reporting is read-only with respect to advertising campaigns. |

## Product goal

Make Google Ads account, campaign, keyword, search-term and ad reporting available through one local multi-account MCP server, without switching servers for each account.

## Invariants

Reporting is read-only with respect to advertising campaigns. A configured account is the credential profile; customer_id is the advertising customer being queried. Do not confuse them. Currency micro-units become major units; a report is bounded and is not a complete data export.

## Recover the current task

Source reconstruction: 2026-09-26; candidate `39471e2ed644bca3ea1e2b3a8b57bf09f731c4fd` on `main`; source version `0.1.0`. This is a dated source observation, not a live-service or installed-version claim.

The current main candidate is 39471e2 (2026-09-16 CI gate merge). July history records hermetic tests and documentation; ce7ebaf (2026-07-19) removed an empty auth scaffold and adjusted dead-code analysis. These are implementation milestones, not a running-service handoff.

Use the latest user request as the task selector. This dossier is standing product context, not an instruction to repeat a completed documentation rollout. Recover applicable repository instructions, exact branch/candidate and dirty state, then bind the requested outcome and acceptance. If the only instruction is “read and begin,” finish this chain and perform a bounded read-only reconciliation of the current handoff and source; report the smallest next action, without inventing a product task or replaying historical external actions.

## Read chain

**Next: [INDEX.md](INDEX.md).** Read only task-relevant contracts before acting. Resolve relevant source contradictions before implementation; existing source documents remain canonical. Read deeper source when the selected task touches it.

## Task workflow

Select relevant skills from the active runtime's current catalog and instructions when the task requires them. This document does not activate a crew, pipeline, provider, or release.

## First unresolved work

Open work and blockers are owned by [docs/workflow/HANDOFFS.md](docs/workflow/HANDOFFS.md); read that section before planning new work.

Before implementation, state the requested outcome, smallest useful change, evidence required and stop condition. Verify the actual result, update canonical sources and HANDOFFS, and leave knowledge events honest about freshness.
