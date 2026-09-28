# Google Ads reporting MCP: state and persistence

## Purpose

| Question | Answer |
| --- | --- |
| **Whom?** | advertising analyst comparing explicitly selected Google Ads customer accounts. |
| **What?** | No application database. |
| **Where?** | gads/accounts.py. |
| **Why it exists?** | Google Ads reporting MCP needs this document to identify what persists, what is transient and what requires recovery. |
| **Why this approach?** | No application database. |
| **Why it matters?** | Reporting is read-only with respect to advertising campaigns. |

## Actual state model

No application database. Configuration JSON contains a default profile name and accounts map; OAuth profiles reference token files, service profiles reference credential files and optional impersonation. set_default_account rewrites the configuration file, so it is a persistent local mutation. Clients cache per profile in process. Reporting rows are ephemeral outputs; do not persist customer data or raw provider errors in public evidence. Query annotations call rows dictionaries, but the implementation returns protobuf rows until server mapping.

## State transition and recovery

The package entrypoint is gads.server:main. Inspect the chosen Python environment and profile reference before starting. No server was started during this reconstruction. Retry exhaustion should surface the error rather than repeat the whole report indefinitely. A release needs the repository CI path and package-version decision; the September CI-gate commit is history, not proof of a current installation.

## Private-input boundary

GOOGLE_ADS_DEVELOPER_TOKEN is an environment input. GOOGLE_ADS_ACCOUNTS_CONFIG selects a private accounts JSON; the default location is ~/.config/mcp-google-ads/accounts.json. OAuth files hold client_id, client_secret and refresh_token; service-account files are loaded by path. Document names and storage responsibility only. Neither credential values nor customer identifiers are required to maintain the reporting code.

## Supporting sources

- [gads/accounts.py](../../gads/accounts.py)

## Continue

Return to [INDEX.md](../../INDEX.md) and finish all routes relevant to the latest task before acting. After verification, update affected owning facts, REPORT and HANDOFFS.
