# Google Ads reporting MCP: task journeys

## Purpose

| Question | Answer |
| --- | --- |
| **Whom?** | advertising analyst comparing explicitly selected Google Ads customer accounts. |
| **What?** | Choose the authorized credential profile and customer -> discover accessible customers -> select dates -> fetch a bounded report -> inspect errors and missing rows -> compare only compatible periods/units -> return a source-backed finding. |
| **Where?** | README.md, gads/server.py, tests/test_server.py. |
| **Why it exists?** | Google Ads reporting MCP needs this document to show the order of observations and actions required for a real task. |
| **Why this approach?** | Choose the authorized credential profile and customer -> discover accessible customers -> select dates -> fetch a bounded report -> inspect errors and missing rows -> compare only compatible periods/units -> return a source-backed finding. |
| **Why it matters?** | Reporting is read-only with respect to advertising campaigns. |

## Concrete interaction flow

Choose the authorized credential profile and customer -> discover accessible customers -> select dates -> fetch a bounded report -> inspect errors and missing rows -> compare only compatible periods/units -> return a source-backed finding. Do not change the global default just to make one query; pass account explicitly. A request to pause a campaign leaves this implementation scope and requires a separately selected write-capable tool and approval.

## Entry, result and failure states

The user experience is the MCP tool schema and report result, not a web page. Present dates, customer, currency context and units before interpreting change. compare_periods returns campaigns with period1, period2, delta_clicks, delta_cost and delta_conversions sorted by absolute cost change. It does not compute statistical significance or attribute causation. Keep unavailable impression-share values distinct from numeric zero.

The code interpolates date/status/campaign filters into GAQL without comprehensive domain validation. Treat those inputs as untrusted and add validation if the tool contract is changed. Reports can disclose account data despite being read-only. The server has no per-call human-approval mechanism. A configuration path or profile listing is not permission to query every account.

This is a sequence specification for the current interface. It does not introduce an unimplemented graphical application. Use the source tool/CLI contract for exact input fields.

## Supporting sources

- [README.md](../../README.md)
- [gads/server.py](../../gads/server.py)
- [tests/test_server.py](../../tests/test_server.py)

## Continue

Return to [INDEX.md](../../INDEX.md) and finish all routes relevant to the latest task before acting. After verification, update affected owning facts, REPORT and HANDOFFS.
