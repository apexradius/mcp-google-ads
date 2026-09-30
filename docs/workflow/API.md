# Google Ads reporting MCP: executable interfaces

## Purpose

| Question | Answer |
| --- | --- |
| **Whom?** | advertising analyst comparing explicitly selected Google Ads customer accounts. |
| **What?** | Ten tools: list_accounts(); set_default_account(account); list_customers(account?, customer_id?); get_account_summary(customer_id,start_date,end_date,account?); list_campaigns(customer_id,status?,account?); get_campaign_performance(customer_id,start_date,end_date,campaign_id?,account?); compare_periods(customer_id,period1_start,period1_end,period2_start,period2_end,breakdown="campaign",account?); get_keyword_performance(...,row_limit=50); search_terms_report(...,row_limit=50); get_ad_performance(...,row_limit=25). |
| **Where?** | gads/server.py, tests/test_server.py. |
| **Why it exists?** | Google Ads reporting MCP needs this document to prevent unsupported parameters or misleading success results from guiding an action. |
| **Why this approach?** | Ten tools: list_accounts(); set_default_account(account); list_customers(account?, customer_id?); get_account_summary(customer_id,start_date,end_date,account?); list_campaigns(customer_id,status?,account?); get_campaign_performance(customer_id,start_date,end_date,campaign_id?,account?); compare_periods(customer_id,period1_start,period1_end,period2_start,period2_end,breakdown="campaign",account?); get_keyword_performance(...,row_limit=50); search_terms_report(...,row_limit=50); get_ad_performance(...,row_limit=25). |
| **Why it matters?** | Reporting is read-only with respect to advertising campaigns. |

## Exact current interface

Ten tools: list_accounts(); set_default_account(account); list_customers(account?, customer_id?); get_account_summary(customer_id,start_date,end_date,account?); list_campaigns(customer_id,status?,account?); get_campaign_performance(customer_id,start_date,end_date,campaign_id?,account?); compare_periods(customer_id,period1_start,period1_end,period2_start,period2_end,breakdown="campaign",account?); get_keyword_performance(...,row_limit=50); search_terms_report(...,row_limit=50); get_ad_performance(...,row_limit=25). Keyword/search-term limits clamp to 1..1000; ad limits to 1..500; campaign reports cap at 100; comparisons query 50 campaigns per period. list_campaigns uses LAST_30_DAYS and enabled/paused by default. Cost and average CPC divide micros by 1,000,000; CTR is percentage in mapped reports. Errors return {error: message}, including functions annotated as lists. Retry permits five attempts on RESOURCE_EXHAUSTED, INTERNAL and UNAVAILABLE, with 1/2/4/8-second waits. Entry transport defaults stdio; MCP_TRANSPORT=sse uses MCP_HOST default 127.0.0.1 and MCP_PORT default 3001.

## Complete registered signatures

These signatures are transcribed from the current Python handler definitions. Optional defaults are source behavior; effect labels distinguish configuration/authentication changes from reporting.

| Handler signature | Effect |
| --- | --- |
| `list_accounts()` | provider read or local discovery |
| `set_default_account(account: str)` | persistent configuration write |
| `list_customers(account: Optional[str]=None, customer_id: Optional[str]=None)` | provider read or local discovery |
| `get_account_summary(customer_id: str, start_date: str, end_date: str, account: Optional[str]=None)` | provider read or local discovery |
| `list_campaigns(customer_id: str, status: Optional[str]=None, account: Optional[str]=None)` | provider read or local discovery |
| `get_campaign_performance(customer_id: str, start_date: str, end_date: str, campaign_id: Optional[str]=None, account: Optional[str]=None)` | provider read or local discovery |
| `compare_periods(customer_id: str, period1_start: str, period1_end: str, period2_start: str, period2_end: str, breakdown: str='campaign', account: Optional[str]=None)` | provider read or local discovery |
| `get_keyword_performance(customer_id: str, start_date: str, end_date: str, campaign_id: Optional[str]=None, row_limit: int=50, account: Optional[str]=None)` | provider read or local discovery |
| `search_terms_report(customer_id: str, start_date: str, end_date: str, campaign_id: Optional[str]=None, row_limit: int=50, account: Optional[str]=None)` | provider read or local discovery |
| `get_ad_performance(customer_id: str, start_date: str, end_date: str, campaign_id: Optional[str]=None, row_limit: int=25, account: Optional[str]=None)` | provider read or local discovery |

## Authorization and error limits

The code interpolates date/status/campaign filters into GAQL without comprehensive domain validation. Treat those inputs as untrusted and add validation if the tool contract is changed. Reports can disclose account data despite being read-only. The server has no per-call human-approval mechanism. A configuration path or profile listing is not permission to query every account.

## Contract gaps

1. list_customers accepts customer_id and claims MCC child discovery, but never uses customer_id; it lists accessible customers for the login. 2. compare_periods accepts breakdown="account" but always queries/maps campaigns. 3. Missing-token text suggests an auth subcommand that is absent from the inspected CLI entrypoint. 4. Source tests do not establish report semantics, paging completeness or fresh provider compatibility. Proposed next work is a bounded contract reconciliation with fake clients; no owner-ranked product backlog or current account task was found.

## Supporting sources

- [gads/server.py](../../gads/server.py)
- [tests/test_server.py](../../tests/test_server.py)

## Continue

Return to [INDEX.md](../../INDEX.md) and finish all routes relevant to the latest task before acting. After verification, update affected owning facts, REPORT and HANDOFFS.
