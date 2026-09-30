# Google Ads reporting MCP: operation and recovery

## Purpose

| Question | Answer |
| --- | --- |
| **Whom?** | advertising analyst comparing explicitly selected Google Ads customer accounts. |
| **What?** | The package entrypoint is gads.server:main. |
| **Where?** | README.md. |
| **Why it exists?** | Google Ads reporting MCP needs this document to recover safely from the actual failure modes rather than repeat old operations. |
| **Why this approach?** | The package entrypoint is gads.server:main. |
| **Why it matters?** | Reporting is read-only with respect to advertising campaigns. |

## Runtime and recovery

The package entrypoint is gads.server:main. Inspect the chosen Python environment and profile reference before starting. No server was started during this reconstruction. Retry exhaustion should surface the error rather than repeat the whole report indefinitely. A release needs the repository CI path and package-version decision; the September CI-gate commit is history, not proof of a current installation.

## Prioritized uncertainty

1. list_customers accepts customer_id and claims MCC child discovery, but never uses customer_id; it lists accessible customers for the login. 2. compare_periods accepts breakdown="account" but always queries/maps campaigns. 3. Missing-token text suggests an auth subcommand that is absent from the inspected CLI entrypoint. 4. Source tests do not establish report semantics, paging completeness or fresh provider compatibility. Proposed next work is a bounded contract reconciliation with fake clients; no owner-ranked product backlog or current account task was found.

## Closeout

Verify the requested result at the correct layer, reconcile the owning manual/interface and update [HANDOFFS](HANDOFFS.md). Record a [knowledge event](REFERENCES.md) for material source/decision/freshness changes. Do not run package publishing, provider writes, private index sync or browser automation just to refresh a document.

## Supporting sources

- [README.md](../../README.md)

## Continue

Return to [INDEX.md](../../INDEX.md) and finish all routes relevant to the latest task before acting. After verification, update affected owning facts, REPORT and HANDOFFS.
