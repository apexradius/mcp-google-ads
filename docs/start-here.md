# Start Here

This server exposes Google Ads reporting and account tools through MCP. It is designed for
multi-account work where a single AI session needs to switch between named Google Ads accounts.

## First Run

```bash
uvx mcp-google-ads-multi
```

Then configure an MCP client with `GOOGLE_ADS_DEVELOPER_TOKEN` and
`GOOGLE_ADS_ACCOUNTS_CONFIG`.

## Account Setup

1. Create or confirm a Google Ads developer token.
2. Create OAuth desktop app credentials in Google Cloud.
3. Copy `accounts.example.json` to your config directory.
4. Add one named account per customer or login context.
5. Restart the MCP client and call `list_accounts`.

## Development Loop

```bash
uv sync
uv run ruff check .
uv run python -m gads.server
```

Use `gads/server.py` for tool registration, `gads/accounts.py` for account loading, and
`gads/query.py` for Google Ads query construction.
