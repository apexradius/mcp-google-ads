# Google Ads reporting MCP: requirements and value

## Purpose

| Question | Answer |
| --- | --- |
| **Whom?** | advertising analyst comparing explicitly selected Google Ads customer accounts. |
| **What?** | Account profiles must resolve explicitly or through the configured default, unknown profiles must fail, and missing configuration must return a clean error. |
| **Where?** | README.md. |
| **Why it exists?** | Google Ads reporting MCP needs this document to keep implementation choices tied to the promised outcome. |
| **Why this approach?** | Account profiles must resolve explicitly or through the configured default, unknown profiles must fail, and missing configuration must return a clean error. |
| **Why it matters?** | Reporting is read-only with respect to advertising campaigns. |

## Vision and user value

Make Google Ads account, campaign, keyword, search-term and ad reporting available through one local multi-account MCP server, without switching servers for each account.

## Requirements and acceptance meaning

Account profiles must resolve explicitly or through the configured default, unknown profiles must fail, and missing configuration must return a clean error. Ten registered tools expose discovery and reporting, not campaign creation, budget edits, billing or conversion uploads. Required report context is customer, credential profile, date range, metric units and row limit. Preserve honest missing data rather than infer zero spend from every empty result.

## Non-negotiable boundaries

Reporting is read-only with respect to advertising campaigns. A configured account is the credential profile; customer_id is the advertising customer being queried. Do not confuse them. Currency micro-units become major units; a report is bounded and is not a complete data export.

## Why this implementation

The FastMCP server lazily creates AccountManager, which resolves a named profile and caches a GoogleAdsClient. Each reporting handler builds GAQL, calls with_retry(run_query, ...), and maps protobuf rows into dictionaries. run_query strips hyphens from customer IDs and materializes search_stream results. AccountManager owns JSON configuration and client lifecycle; query.py owns execution; retry.py handles selected transient failures. This separation is visible in source and supports mocked boundary testing. No recorded architecture decision comparing alternative frameworks was found; maintain this small existing design rather than invent that history.

## Current requirement debt

1. list_customers accepts customer_id and claims MCC child discovery, but never uses customer_id; it lists accessible customers for the login. 2. compare_periods accepts breakdown="account" but always queries/maps campaigns. 3. Missing-token text suggests an auth subcommand that is absent from the inspected CLI entrypoint. 4. Source tests do not establish report semantics, paging completeness or fresh provider compatibility. Proposed next work is a bounded contract reconciliation with fake clients; no owner-ranked product backlog or current account task was found.

Classify a future statement as original requirement, later amendment, observed implementation, inferred rationale or proposed change. Preserve the distinction: source behavior does not silently repeal an original promise, and a plausible rationale is not a recorded decision.

## Supporting sources

- [README.md](../../README.md)

## Continue

Return to [INDEX.md](../../INDEX.md) and finish all routes relevant to the latest task before acting. After verification, update affected owning facts, REPORT and HANDOFFS.
