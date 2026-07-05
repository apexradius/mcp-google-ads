# Start Here — mcp-google-ads

## What this repo ships

- One Python package: `mcp-google-ads-multi`
- One MCP server entry point: `gads.server:main`
- One account-manager layer that lets one MCP server address many Google Ads accounts

## First run

1. Install the package:

```bash
python -m pip install mcp-google-ads-multi
```

2. Create the accounts config:

```bash
mkdir -p ~/.config/mcp-google-ads
cp accounts.example.json ~/.config/mcp-google-ads/accounts.json
```

3. Export the required token and config path:

```bash
export GOOGLE_ADS_DEVELOPER_TOKEN="your-developer-token"
export GOOGLE_ADS_ACCOUNTS_CONFIG="$HOME/.config/mcp-google-ads/accounts.json"
```

## Required environment

| Variable | Required | Notes |
|---|---|---|
| `GOOGLE_ADS_DEVELOPER_TOKEN` | yes | Required by the Google Ads API |
| `GOOGLE_ADS_ACCOUNTS_CONFIG` | yes | Path to the multi-account config file |
| `MCP_TRANSPORT` | optional | `stdio` by default, `sse` for remote hosting |
| `MCP_HOST` / `MCP_PORT` | optional | SSE bind address when remote transport is enabled |

## Validation commands

```bash
python -m compileall gads
python -m build
```

## Common failures

| Symptom | Likely cause | Fix |
|---|---|---|
| Account not found | Config alias mismatch | Check the `default` key and account names in `accounts.json` |
| OAuth prompt never completes | Local OAuth credentials missing | Recreate the desktop OAuth client in Google Cloud |
| API auth error | Developer token missing or wrong | Re-export `GOOGLE_ADS_DEVELOPER_TOKEN` |
