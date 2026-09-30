# Google Ads reporting MCP: configuration and private inputs

## Purpose

| Question | Answer |
| --- | --- |
| **Whom?** | advertising analyst comparing explicitly selected Google Ads customer accounts. |
| **What?** | GOOGLE_ADS_DEVELOPER_TOKEN is an environment input. |
| **Where?** | gads/server.py, gads/accounts.py, tests/test_server.py. |
| **Why it exists?** | Google Ads reporting MCP needs this document to resolve configuration responsibility without exposing values. |
| **Why this approach?** | GOOGLE_ADS_DEVELOPER_TOKEN is an environment input. |
| **Why it matters?** | Private input access is not necessary to understand the product contract. |

## Metadata-only configuration map

GOOGLE_ADS_DEVELOPER_TOKEN is an environment input. GOOGLE_ADS_ACCOUNTS_CONFIG selects a private accounts JSON; the default location is ~/.config/mcp-google-ads/accounts.json. OAuth files hold client_id, client_secret and refresh_token; service-account files are loaded by path. Document names and storage responsibility only. Neither credential values nor customer identifiers are required to maintain the reporting code.

## Access discipline

This document carries configuration names, purpose and responsibility only. Never paste values, tokens, private prompts, unrestricted provider output or account exports. For a real credential failure, identify the approved storage/rotation path without printing its contents; verify the authorized replacement in the actual runtime and retain a redacted receipt. Secret presence, file readability and connector access are not approval to perform the task.

## Supporting sources

- [gads/server.py](../../gads/server.py)
- [gads/accounts.py](../../gads/accounts.py)
- [tests/test_server.py](../../tests/test_server.py)

## Continue

Return to [INDEX.md](../../INDEX.md) and finish all routes relevant to the latest task before acting. After verification, update affected owning facts, REPORT and HANDOFFS.
