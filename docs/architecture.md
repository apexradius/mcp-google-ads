# Architecture — mcp-google-ads

## Component map

| Component | File | Role |
|---|---|---|
| MCP server | [`../gads/server.py`](../gads/server.py) | Declares the tool surface and normalizes responses |
| Account manager | [`../gads/accounts.py`](../gads/accounts.py) | Resolves named accounts and builds clients |
| Query helpers | [`../gads/query.py`](../gads/query.py) | Cleans IDs and executes GAQL |
| Retry wrapper | [`../gads/retry.py`](../gads/retry.py) | Retries transient Google Ads API failures |
| Package metadata | [`../pyproject.toml`](../pyproject.toml) | Version, dependency set, script entry point |

## Runtime lifecycle

1. The MCP client launches `mcp-google-ads-multi`.
2. `FastMCP` registers the account, summary, campaign, keyword, and ad-reporting tools.
3. The selected tool resolves the named or default account through `AccountManager`.
4. GAQL queries run through reusable query helpers and the retry wrapper.
5. Results return as plain dictionaries and lists for the MCP client.
