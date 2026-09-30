# Google Ads reporting MCP: implementation conventions

## Purpose

| Question | Answer |
| --- | --- |
| **Whom?** | advertising analyst comparing explicitly selected Google Ads customer accounts. |
| **What?** | Python 3.11+, FastMCP decorators and snake_case functions; Ruff line length 100, target py311. |
| **Where?** | pyproject.toml. |
| **Why it exists?** | Google Ads reporting MCP needs this document to preserve the implementation’s existing conventions at the change boundary. |
| **Why this approach?** | Python 3.11+, FastMCP decorators and snake_case functions; Ruff line length 100, target py311. |
| **Why it matters?** | Small compatible changes remain easier to review and recover. |

## Existing conventions

Python 3.11+, FastMCP decorators and snake_case functions; Ruff line length 100, target py311. Preserve lazy manager construction so importing the module does not require credentials. Reuse the shared query and retry modules. Keep numerical conversions at the response mapping boundary and test schema and error shape when a tool changes.

## Change boundary

The FastMCP server lazily creates AccountManager, which resolves a named profile and caches a GoogleAdsClient. Each reporting handler builds GAQL, calls with_retry(run_query, ...), and maps protobuf rows into dictionaries. run_query strips hyphens from customer IDs and materializes search_stream results. AccountManager owns JSON configuration and client lifecycle; query.py owns execution; retry.py handles selected transient failures. This separation is visible in source and supports mocked boundary testing. No recorded architecture decision comparing alternative frameworks was found; maintain this small existing design rather than invent that history.

Prefer the smallest change in the component that already owns the behavior. Preserve generated artifacts and original requirements. Test a changed contract at its actual boundary; do not add scaffolding, services or broad refactors only to satisfy a documentation layout.

## Supporting sources

- [pyproject.toml](../../pyproject.toml)

## Continue

Return to [INDEX.md](../../INDEX.md) and finish all routes relevant to the latest task before acting. After verification, update affected owning facts, REPORT and HANDOFFS.
