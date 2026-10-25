# Google Ads reporting MCP: evidence and unresolved claims

## Purpose

| Question | Answer |
| --- | --- |
| **Whom?** | advertising analyst comparing explicitly selected Google Ads customer accounts. |
| **What?** | list_customers accepts customer_id and claims MCC child discovery, but never uses customer_id; it lists accessible customers for the login. |
| **Where?** | README.md, pyproject.toml, gads/server.py. |
| **Why it exists?** | Google Ads reporting MCP needs this document to show what is observed, what remains unknown and what decision follows. |
| **Why this approach?** | list_customers accepts customer_id and claims MCC child discovery, but never uses customer_id; it lists accessible customers for the login. |
| **Why it matters?** | These limits keep the next task honest and bounded. |

## Reconstruction finding

Source reconstruction: 2026-09-26; candidate `39471e2ed644bca3ea1e2b3a8b57bf09f731c4fd` on `main`; source version `0.1.0`. This is a dated source observation, not a live-service or installed-version claim.

The earlier workflow-adoption completion has been superseded by the user’s request for substantive product reconstruction. The enduring product outcome is: Make Google Ads account, campaign, keyword, search-term and ad reporting available through one local multi-account MCP server, without switching servers for each account.

## Established from sources

The FastMCP server lazily creates AccountManager, which resolves a named profile and caches a GoogleAdsClient. Each reporting handler builds GAQL, calls with_retry(run_query, ...), and maps protobuf rows into dictionaries. run_query strips hyphens from customer IDs and materializes search_stream results. AccountManager owns JSON configuration and client lifecycle; query.py owns execution; retry.py handles selected transient failures. This separation is visible in source and supports mocked boundary testing. No recorded architecture decision comparing alternative frameworks was found; maintain this small existing design rather than invent that history.

The current main candidate is 39471e2 (2026-09-16 CI gate merge). July history records hermetic tests and documentation; ce7ebaf (2026-07-19) removed an empty auth scaffold and adjusted dead-code analysis. These are implementation milestones, not a running-service handoff.

## Unresolved product claims

Open work and blockers are owned by [HANDOFFS.md](HANDOFFS.md); read that section before planning changes here.

## Evidence limits and value

This reconstruction makes the next task’s interfaces, boundaries and prior intent recoverable. It does not establish new customer value, provider success or a deployed fix. No current product build, account request, browser launch, private corpus read, publish or release was performed. Structural document validation and source-grounded scenario read-through are recorded separately from product acceptance. [TESTING](TESTING.md) identifies the additional proof a future implementation needs.

## Supporting sources

- [README.md](../../README.md)
- [pyproject.toml](../../pyproject.toml)
- [gads/server.py](../../gads/server.py)

## Continue

Return to [INDEX.md](../../INDEX.md) and finish all routes relevant to the latest task before acting. After verification, update affected owning facts, REPORT and HANDOFFS.


## 2026-10-24: concise project guidance

Project startup now routes to task-relevant documents. Product boundaries remain in
AGENTS; detailed conventions, verification and security contracts stay in their owning
documents. The current runtime catalog selects skills when needed. This documentation
change preserves runtime code, provider access and existing product acceptance limits.
The owner authorized reviewed PR delivery; checks and independent review precede merge.

Validation: 25 existing document-checker fixtures passed. Tracked link/navigation
and review-snapshot checks are rerun after final metadata updates. Product live-acceptance
limits remain unchanged in the review snapshot; no provider call or deployment was made.

Independent read-only GLM-5.3/high review confirmed the removed project conventions
remain in CODE_STYLE and product acceptance blockers are retained. Its one wording
finding was fixed: the link now describes task workflow guidance, not a retired selector.
