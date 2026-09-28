# Google Ads reporting MCP: product continuity

## Purpose

| Question | Answer |
| --- | --- |
| **Whom?** | advertising analyst comparing explicitly selected Google Ads customer accounts. |
| **What?** | list_customers accepts customer_id and claims MCC child discovery, but never uses customer_id; it lists accessible customers for the login. |
| **Where?** | README.md. |
| **Why it exists?** | Google Ads reporting MCP needs this document to separate finished historical work from an actual task that can resume. |
| **Why this approach?** | The current main candidate is 39471e2 (2026-09-16 CI gate merge). |
| **Why it matters?** | The next agent must not repeat a dated delivery or convert a suggested fix into an approved operation. |

## Durable product state

Make Google Ads account, campaign, keyword, search-term and ad reporting available through one local multi-account MCP server, without switching servers for each account.

The current main candidate is 39471e2 (2026-09-16 CI gate merge). July history records hermetic tests and documentation; ce7ebaf (2026-07-19) removed an empty auth scaffold and adjusted dead-code analysis. These are implementation milestones, not a running-service handoff.

## Open work and blockers

1. list_customers accepts customer_id and claims MCC child discovery, but never uses customer_id; it lists accessible customers for the login. 2. compare_periods accepts breakdown="account" but always queries/maps campaigns. 3. Missing-token text suggests an auth subcommand that is absent from the inspected CLI entrypoint. 4. Source tests do not establish report semantics, paging completeness or fresh provider compatibility. Proposed next work is a bounded contract reconciliation with fake clients; no owner-ranked product backlog or current account task was found.

The latest user request selects the actual task. These proposed maintenance priorities are not an approved feature roadmap, provider action or automatic queue. If the user only says “read and begin,” reconcile these findings against the current candidate and report the smallest useful next action; do not resume completed documentation adoption or replay an old submission.

## Next handoff contract

Record the concrete requested outcome, exact repository/candidate, selected conductor, touched source and task state, completed behavior with evidence level, unresolved blocker, next safe action, approvals and effects already performed. Include operation identity/duplicate-prevention state for any external effect. Preserve requirement/decision changes and pending knowledge events. A source/test inventory is not a release acceptance receipt.

## Supporting sources

- [README.md](../../README.md)

## Continue

Return to [INDEX.md](../../INDEX.md) and finish all routes relevant to the latest task before acting. After verification, update affected owning facts, REPORT and HANDOFFS.
