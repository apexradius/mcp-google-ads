# Google Ads reporting MCP: operator experience

## Purpose

| Question | Answer |
| --- | --- |
| **Whom?** | advertising analyst comparing explicitly selected Google Ads customer accounts. |
| **What?** | The user experience is the MCP tool schema and report result, not a web page. |
| **Where?** | gads/server.py, tests/test_server.py. |
| **Why it exists?** | Google Ads reporting MCP needs this document to make the human-facing contract explicit even when the interface is a CLI or MCP tool. |
| **Why this approach?** | The user experience is the MCP tool schema and report result, not a web page. |
| **Why it matters?** | Reporting is read-only with respect to advertising campaigns. |

## Operator experience

The user experience is the MCP tool schema and report result, not a web page. Present dates, customer, currency context and units before interpreting change. compare_periods returns campaigns with period1, period2, delta_clicks, delta_cost and delta_conversions sorted by absolute cost change. It does not compute statistical significance or attribute causation. Keep unavailable impression-share values distinct from numeric zero.

## State and error presentation

Choose the authorized credential profile and customer -> discover accessible customers -> select dates -> fetch a bounded report -> inspect errors and missing rows -> compare only compatible periods/units -> return a source-backed finding. Do not change the global default just to make one query; pass account explicitly. A request to pause a campaign leaves this implementation scope and requires a separately selected write-capable tool and approval.

## Review standard

Review the actual interface changed: schema/error/citation output for tools, and visible rendered pages where this product creates a document or browser experience. Do not invent screen designs, visual tokens or customer flows that the product does not contain. User-facing success must name what succeeded and what remains unverified.

## Supporting sources

- [gads/server.py](../../gads/server.py)
- [tests/test_server.py](../../tests/test_server.py)

## Continue

Return to [INDEX.md](../../INDEX.md) and finish all routes relevant to the latest task before acting. After verification, update affected owning facts, REPORT and HANDOFFS.
