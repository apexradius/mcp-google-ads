"""Hermetic tests for the Google Ads MCP server.

No network calls and no real Google Ads credentials are used. These cover the
tool contract the server advertises, the customer-id normaliser, and the
missing-credential path (which must return a clean error, not crash).
"""

import asyncio
import unittest
from unittest import mock

from gads import server
from gads.accounts import AccountError, AccountManager
from gads.query import clean_id

EXPECTED_TOOLS = {
    "list_accounts",
    "set_default_account",
    "list_customers",
    "get_account_summary",
    "list_campaigns",
    "get_campaign_performance",
    "compare_periods",
    "get_keyword_performance",
    "search_terms_report",
    "get_ad_performance",
}


class ToolRegistrationTests(unittest.TestCase):
    def test_server_exposes_expected_tools_with_schemas(self):
        tools = asyncio.run(server.mcp.list_tools())
        names = {t.name for t in tools}
        self.assertEqual(names, EXPECTED_TOOLS)
        for t in tools:
            self.assertIsInstance(t.parameters, dict, f"{t.name} has no schema")
            self.assertIn("properties", t.parameters, f"{t.name} schema missing properties")


class ConfigValidationTests(unittest.TestCase):
    def test_missing_config_raises_account_error(self):
        with mock.patch.dict(
            "os.environ",
            {"GOOGLE_ADS_ACCOUNTS_CONFIG": "/nonexistent/path/accounts.json"},
            clear=True,
        ), self.assertRaises(AccountError) as ctx:
            AccountManager()
        self.assertIn("not found", str(ctx.exception))

    def test_tool_returns_clean_error_when_unconfigured(self):
        server._manager = None
        try:
            with mock.patch.dict(
                "os.environ",
                {"GOOGLE_ADS_ACCOUNTS_CONFIG": "/nonexistent/path/accounts.json"},
                clear=True,
            ):
                result = server.list_accounts()
        finally:
            server._manager = None
        self.assertIsInstance(result, dict)
        self.assertIn("error", result)


class CleanIdTests(unittest.TestCase):
    def test_strips_dashes(self):
        self.assertEqual(clean_id("123-456-7890"), "1234567890")

    def test_leaves_plain_id_untouched(self):
        self.assertEqual(clean_id("1234567890"), "1234567890")



class ComparePeriodsTests(unittest.TestCase):
    def compare(self, breakdown):
        return server.compare_periods('123-456-7890', '2026-01-01', '2026-01-31',
                                      '2026-02-01', '2026-02-28', breakdown=breakdown,
                                      account='fixture-profile')

    def test_account_comparison_queries_customer_totals(self):
        from types import SimpleNamespace as NS

        queries = []
        def query(client, customer, gaql):
            queries.append(gaql)
            self.assertEqual(customer, '123-456-7890')
            self.assertIn('FROM customer', gaql)
            self.assertNotIn('campaign.', gaql)
            self.assertNotIn('LIMIT 50', gaql)
            return [NS(customer=NS(id=1234567890, descriptive_name='Fixture account'),
                       metrics=NS(clicks=100 * len(queries), impressions=1000,
                                  cost_micros=123450000, conversions=2.5))]

        with mock.patch.object(server, '_get_manager') as manager, mock.patch.object(server, 'run_query', side_effect=query):
            result = self.compare('account')
        self.assertNotIn('error', result)
        manager.return_value.get_client.assert_called_once_with('fixture-profile')
        self.assertEqual(len(queries), 2)
        self.assertEqual(result['accounts'][0]['customer_id'], '1234567890')
        self.assertEqual(result['accounts'][0]['period1']['cost'], 123.45)
        self.assertEqual(result['accounts'][0]['period2']['clicks'], 200)

    def test_campaign_comparison_keeps_existing_shape(self):
        from types import SimpleNamespace as NS

        row = NS(campaign=NS(id=7, name='Fixture campaign'),
                 metrics=NS(clicks=2, impressions=20, cost_micros=1500000, conversions=1))
        with mock.patch.object(server, '_get_manager'), mock.patch.object(server, 'run_query', return_value=[row]) as query:
            result = self.compare('campaign')
        self.assertEqual(result['campaigns'][0]['campaign_id'], '7')
        self.assertEqual(result['campaigns'][0]['period1']['cost'], 1.5)
        self.assertIn('FROM campaign', query.call_args.args[2])
        self.assertIn('LIMIT 50', query.call_args.args[2])

    def test_invalid_breakdown_denied_before_provider_access(self):
        with mock.patch.object(server, '_get_manager') as manager:
            self.assertIn('error', self.compare('unsupported'))
        manager.assert_not_called()

    def test_empty_account_results_remain_empty(self):
        with mock.patch.object(server, '_get_manager'), mock.patch.object(server, 'run_query', return_value=[]):
            self.assertEqual(self.compare('account')['accounts'], [])


if __name__ == "__main__":
    unittest.main()
