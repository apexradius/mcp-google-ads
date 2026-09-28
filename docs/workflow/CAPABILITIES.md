# Google Ads reporting MCP: available capability boundaries

## Purpose

| Question | Answer |
| --- | --- |
| **Whom?** | advertising analyst comparing explicitly selected Google Ads customer accounts. |
| **What?** | Ten tools: list_accounts(); set_default_account(account); list_customers(account?, customer_id?); get_account_summary(customer_id,start_date,end_date,account?); list_campaigns(customer_id,status?,account?); get_campaign_performance(customer_id,start_date,end_date,campaign_id?,account?); compare_periods(customer_id,period1_start,period1_end,period2_start,period2_end,breakdown="campaign",account?); get_keyword_performance(...,row_limit=50); search_terms_report(...,row_limit=50); get_ad_performance(...,row_limit=25). |
| **Where?** | README.md, pyproject.toml, gads/server.py. |
| **Why it exists?** | Google Ads reporting MCP needs this document to distinguish available implementation from authorized operation. |
| **Why this approach?** | Reporting is read-only with respect to advertising campaigns. |
| **Why it matters?** | Reporting is read-only with respect to advertising campaigns. |

## Implemented surface

Ten tools: list_accounts(); set_default_account(account); list_customers(account?, customer_id?); get_account_summary(customer_id,start_date,end_date,account?); list_campaigns(customer_id,status?,account?); get_campaign_performance(customer_id,start_date,end_date,campaign_id?,account?); compare_periods(customer_id,period1_start,period1_end,period2_start,period2_end,breakdown="campaign",account?); get_keyword_performance(...,row_limit=50); search_terms_report(...,row_limit=50); get_ad_performance(...,row_limit=25). Keyword/search-term limits clamp to 1..1000; ad limits to 1..500; campaign reports cap at 100; comparisons query 50 campaigns per period. list_campaigns uses LAST_30_DAYS and enabled/paused by default. Cost and average CPC divide micros by 1,000,000; CTR is percentage in mapped reports. Errors return {error: message}, including functions annotated as lists. Retry permits five attempts on RESOURCE_EXHAUSTED, INTERNAL and UNAVAILABLE, with 1/2/4/8-second waits. Entry transport defaults stdio; MCP_TRANSPORT=sse uses MCP_HOST default 127.0.0.1 and MCP_PORT default 3001.

## Capability does not imply authorization

Reporting is read-only with respect to advertising campaigns. A configured account is the credential profile; customer_id is the advertising customer being queried. Do not confuse them. Currency micro-units become major units; a report is bounded and is not a complete data export.

The code interpolates date/status/campaign filters into GAQL without comprehensive domain validation. Treat those inputs as untrusted and add validation if the tool contract is changed. Reports can disclose account data despite being read-only. The server has no per-call human-approval mechanism. A configuration path or profile listing is not permission to query every account.

Route the current task through [the conductor selector](../../prompt.md#select-the-conductor). No native runtime, MCP connection, paid model, hook or third-party account is activated by this inventory. Verify availability in the actual invocation instead of inferring it from installed source.

## Supporting sources

- [README.md](../../README.md)
- [pyproject.toml](../../pyproject.toml)
- [gads/server.py](../../gads/server.py)

## Continue

Return to [INDEX.md](../../INDEX.md) and finish all routes relevant to the latest task before acting. After verification, update affected owning facts, REPORT and HANDOFFS.
