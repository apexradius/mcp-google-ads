# Architecture

`mcp-google-ads` is a Python MCP server around the Google Ads API. Its main job is to route a
natural-language AI request into a named Google Ads account, build a GAQL query, and return a
structured MCP result.

## Components

```mermaid
flowchart TD
    Main[gads/server.py] --> Tools[MCP tool handlers]
    Tools --> Accounts[gads/accounts.py]
    Tools --> Query[gads/query.py]
    Tools --> Retry[gads/retry.py]

    Accounts --> Config[accounts.example.json shape]
    Accounts --> OAuth[gads/auth]
    Query --> GAQL[GAQL builder]
    Retry --> Backoff[API retry policy]
    OAuth --> API[Google Ads API]
    GAQL --> API
    Backoff --> API
```

## Request Sequence

```mermaid
sequenceDiagram
    actor User
    participant Client as MCP client
    participant Server as gads/server.py
    participant Accounts as gads/accounts.py
    participant Google as Google Ads API

    User->>Client: Ask for campaign metrics
    Client->>Server: Call Ads tool
    Server->>Accounts: Resolve default or named account
    Accounts-->>Server: Credentials and customer context
    Server->>Google: Run GAQL request
    Google-->>Server: Metrics rows
    Server-->>Client: Structured MCP result
    Client-->>User: Answer with account data
```

## Data Boundaries

| Data | Source | Storage |
|---|---|---|
| Developer token | Environment variable | Never committed. |
| Account map | `accounts.json` based on `accounts.example.json` | Local config path. |
| OAuth token files | Paths declared per account | Local machine or mounted config. |
| Google Ads metrics | Google Ads API | Returned through MCP; not persisted by this repo. |

## Extension Points

| Change | File |
|---|---|
| Add a new MCP tool | `gads/server.py` |
| Add account-loading behavior | `gads/accounts.py` |
| Change Ads query construction | `gads/query.py` |
| Tune transient error handling | `gads/retry.py` |
