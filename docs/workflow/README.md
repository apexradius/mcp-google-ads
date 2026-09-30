# Google Ads reporting MCP: orientation

## Purpose

| Question | Answer |
| --- | --- |
| **Whom?** | advertising analyst comparing explicitly selected Google Ads customer accounts. |
| **What?** | Make Google Ads account, campaign, keyword, search-term and ad reporting available through one local multi-account MCP server, without switching servers for each account. |
| **Where?** | README.md, pyproject.toml, gads/server.py. |
| **Why it exists?** | Google Ads reporting MCP needs this document to recover the purpose and correct owning implementation before acting. |
| **Why this approach?** | The FastMCP server lazily creates AccountManager, which resolves a named profile and caches a GoogleAdsClient. |
| **Why it matters?** | Reporting is read-only with respect to advertising campaigns. |

## Product and scope

Make Google Ads account, campaign, keyword, search-term and ad reporting available through one local multi-account MCP server, without switching servers for each account.

Reporting is read-only with respect to advertising campaigns. A configured account is the credential profile; customer_id is the advertising customer being queried. Do not confuse them. Currency micro-units become major units; a report is bounded and is not a complete data export.

## Find the owning behavior

The FastMCP server lazily creates AccountManager, which resolves a named profile and caches a GoogleAdsClient. Each reporting handler builds GAQL, calls with_retry(run_query, ...), and maps protobuf rows into dictionaries. run_query strips hyphens from customer IDs and materializes search_stream results. AccountManager owns JSON configuration and client lifecycle; query.py owns execution; retry.py handles selected transient failures. This separation is visible in source and supports mocked boundary testing. No recorded architecture decision comparing alternative frameworks was found; maintain this small existing design rather than invent that history.

Use [API](API.md) for the exact interface, [DATABASE](DATABASE.md) for state, [TESTING](TESTING.md) for proof and [HANDOFFS](HANDOFFS.md) for current uncertainty. [The root README](../../README.md) remains the original manual; known stale statements are preserved and explained here, not silently adopted.

## Current baseline

The current main candidate is 39471e2 (2026-09-16 CI gate merge). July history records hermetic tests and documentation; ce7ebaf (2026-07-19) removed an empty auth scaffold and adjusted dead-code analysis. These are implementation milestones, not a running-service handoff.

## Supporting sources

- [README.md](../../README.md)
- [pyproject.toml](../../pyproject.toml)
- [gads/server.py](../../gads/server.py)

## Continue

Return to [INDEX.md](../../INDEX.md) and finish all routes relevant to the latest task before acting. After verification, update affected owning facts, REPORT and HANDOFFS.
