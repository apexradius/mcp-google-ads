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
        ):
            with self.assertRaises(AccountError) as ctx:
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


if __name__ == "__main__":
    unittest.main()
