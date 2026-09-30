# Google Ads reporting MCP: components and decisions

## Purpose

| Question | Answer |
| --- | --- |
| **Whom?** | advertising analyst comparing explicitly selected Google Ads customer accounts. |
| **What?** | The FastMCP server lazily creates AccountManager, which resolves a named profile and caches a GoogleAdsClient. |
| **Where?** | gads/server.py, tests/test_server.py. |
| **Why it exists?** | Google Ads reporting MCP needs this document to locate the component that owns the requested behavior. |
| **Why this approach?** | The FastMCP server lazily creates AccountManager, which resolves a named profile and caches a GoogleAdsClient. |
| **Why it matters?** | Reporting is read-only with respect to advertising campaigns. |

## Components, flow and rationale

The FastMCP server lazily creates AccountManager, which resolves a named profile and caches a GoogleAdsClient. Each reporting handler builds GAQL, calls with_retry(run_query, ...), and maps protobuf rows into dictionaries. run_query strips hyphens from customer IDs and materializes search_stream results. AccountManager owns JSON configuration and client lifecycle; query.py owns execution; retry.py handles selected transient failures. This separation is visible in source and supports mocked boundary testing. No recorded architecture decision comparing alternative frameworks was found; maintain this small existing design rather than invent that history.

## State boundary

No application database. Configuration JSON contains a default profile name and accounts map; OAuth profiles reference token files, service profiles reference credential files and optional impersonation. set_default_account rewrites the configuration file, so it is a persistent local mutation. Clients cache per profile in process. Reporting rows are ephemeral outputs; do not persist customer data or raw provider errors in public evidence. Query annotations call rows dictionaries, but the implementation returns protobuf rows until server mapping.

## Evolution and current mismatch

The current main candidate is 39471e2 (2026-09-16 CI gate merge). July history records hermetic tests and documentation; ce7ebaf (2026-07-19) removed an empty auth scaffold and adjusted dead-code analysis. These are implementation milestones, not a running-service handoff.

1. list_customers accepts customer_id and claims MCC child discovery, but never uses customer_id; it lists accessible customers for the login. 2. compare_periods accepts breakdown="account" but always queries/maps campaigns. 3. Missing-token text suggests an auth subcommand that is absent from the inspected CLI entrypoint. 4. Source tests do not establish report semantics, paging completeness or fresh provider compatibility. Proposed next work is a bounded contract reconciliation with fake clients; no owner-ranked product backlog or current account task was found.

## Supporting sources

- [gads/server.py](../../gads/server.py)
- [tests/test_server.py](../../tests/test_server.py)

## Continue

Return to [INDEX.md](../../INDEX.md) and finish all routes relevant to the latest task before acting. After verification, update affected owning facts, REPORT and HANDOFFS.
