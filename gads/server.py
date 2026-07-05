import os
from typing import Optional

from fastmcp import FastMCP

from gads.accounts import AccountManager, AccountError
from gads.query import run_query
from gads.retry import with_retry

mcp = FastMCP("mcp-google-ads")

_manager: Optional[AccountManager] = None


def _get_manager() -> AccountManager:
    global _manager
    if _manager is None:
        _manager = AccountManager()
    return _manager


def _err(e: Exception) -> dict:
    if isinstance(e, (AccountError, RuntimeError)):
        return {"error": str(e)}
    return {"error": f"{type(e).__name__}: {str(e)}"}


# ---------------------------------------------------------------------------
# Account management
# ---------------------------------------------------------------------------

@mcp.tool()
def list_accounts() -> list[dict]:
    """List all configured Google Ads accounts and which is the current default."""
    try:
        return _get_manager().list_accounts()
    except Exception as e:
        return _err(e)


@mcp.tool()
def set_default_account(account: str) -> dict:
    """Set the default account used when no account is specified in other tools."""
    try:
        _get_manager().set_default(account)
        return {"success": True, "default": account}
    except Exception as e:
        return _err(e)


# ---------------------------------------------------------------------------
# Account & customer discovery
# ---------------------------------------------------------------------------

@mcp.tool()
def list_customers(
    account: Optional[str] = None,
    customer_id: Optional[str] = None,
) -> list[dict]:
    """
    List all accessible Google Ads customer accounts.

    If customer_id is provided, lists child accounts under that MCC.
    Otherwise lists all accessible accounts for this login.
    """
    try:
        client = _get_manager().get_client(account)
        service = client.get_service("CustomerService")
        accessible = service.list_accessible_customers()
        customers = []
        for resource_name in accessible.resource_names:
            cid = resource_name.split("/")[-1]
            try:
                gaql = """
                    SELECT customer.id, customer.descriptive_name, customer.currency_code,
                           customer.time_zone, customer.manager, customer.status
                    FROM customer
                    LIMIT 1
                """
                rows = with_retry(run_query, client, cid, gaql)
                if rows:
                    r = rows[0].customer
                    customers.append({
                        "id": str(r.id),
                        "name": r.descriptive_name,
                        "currency": r.currency_code,
                        "timezone": r.time_zone,
                        "is_manager": r.manager,
                        "status": r.status.name,
                    })
            except Exception:
                customers.append({"id": cid, "name": "(access restricted)"})
        return customers
    except Exception as e:
        return _err(e)


@mcp.tool()
def get_account_summary(
    customer_id: str,
    start_date: str,
    end_date: str,
    account: Optional[str] = None,
) -> dict:
    """
    Get top-level spend and conversion totals for an account.

    Args:
        customer_id: Google Ads customer ID (e.g. '123-456-7890' or '1234567890')
        start_date: YYYY-MM-DD
        end_date: YYYY-MM-DD
        account: Named account from config (uses default if omitted)
    """
    try:
        client = _get_manager().get_client(account)
        gaql = f"""
            SELECT
                metrics.clicks,
                metrics.impressions,
                metrics.ctr,
                metrics.average_cpc,
                metrics.cost_micros,
                metrics.conversions,
                metrics.conversions_value,
                metrics.search_impression_share
            FROM customer
            WHERE segments.date BETWEEN '{start_date}' AND '{end_date}'
        """
        rows = with_retry(run_query, client, customer_id, gaql)
        if not rows:
            return {"customer_id": customer_id, "period": f"{start_date} to {end_date}", "clicks": 0}
        m = rows[0].metrics
        return {
            "customer_id": customer_id,
            "period": f"{start_date} to {end_date}",
            "clicks": m.clicks,
            "impressions": m.impressions,
            "ctr": round(m.ctr * 100, 2),
            "avg_cpc": round(m.average_cpc / 1_000_000, 2),
            "cost": round(m.cost_micros / 1_000_000, 2),
            "conversions": round(m.conversions, 1),
            "conversion_value": round(m.conversions_value, 2),
            "search_impression_share": round(m.search_impression_share * 100, 1) if m.search_impression_share else None,
        }
    except Exception as e:
        return _err(e)


# ---------------------------------------------------------------------------
# Campaign tools
# ---------------------------------------------------------------------------

@mcp.tool()
def list_campaigns(
    customer_id: str,
    status: Optional[str] = None,
    account: Optional[str] = None,
) -> list[dict]:
    """
    List campaigns for an account.

    Args:
        customer_id: Google Ads customer ID
        status: Filter by status — ENABLED, PAUSED, REMOVED (default: ENABLED and PAUSED)
        account: Named account from config
    """
    try:
        client = _get_manager().get_client(account)
        where = f"AND campaign.status = '{status}'" if status else "AND campaign.status IN ('ENABLED', 'PAUSED')"
        gaql = f"""
            SELECT
                campaign.id,
                campaign.name,
                campaign.status,
                campaign.advertising_channel_type,
                campaign_budget.amount_micros,
                metrics.clicks,
                metrics.impressions,
                metrics.cost_micros,
                metrics.conversions
            FROM campaign
            WHERE segments.date DURING LAST_30_DAYS
            {where}
            ORDER BY metrics.cost_micros DESC
            LIMIT 100
        """
        rows = with_retry(run_query, client, customer_id, gaql)
        return [
            {
                "id": str(r.campaign.id),
                "name": r.campaign.name,
                "status": r.campaign.status.name,
                "type": r.campaign.advertising_channel_type.name,
                "budget_daily": round(r.campaign_budget.amount_micros / 1_000_000, 2),
                "clicks_30d": r.metrics.clicks,
                "impressions_30d": r.metrics.impressions,
                "cost_30d": round(r.metrics.cost_micros / 1_000_000, 2),
                "conversions_30d": round(r.metrics.conversions, 1),
            }
            for r in rows
        ]
    except Exception as e:
        return _err(e)


@mcp.tool()
def get_campaign_performance(
    customer_id: str,
    start_date: str,
    end_date: str,
    campaign_id: Optional[str] = None,
    account: Optional[str] = None,
) -> list[dict]:
    """
    Get campaign performance metrics for a date range.

    Args:
        customer_id: Google Ads customer ID
        start_date: YYYY-MM-DD
        end_date: YYYY-MM-DD
        campaign_id: Filter to a specific campaign ID (optional)
        account: Named account from config
    """
    try:
        client = _get_manager().get_client(account)
        campaign_filter = f"AND campaign.id = {campaign_id}" if campaign_id else ""
        gaql = f"""
            SELECT
                campaign.id,
                campaign.name,
                campaign.status,
                campaign.advertising_channel_type,
                metrics.clicks,
                metrics.impressions,
                metrics.ctr,
                metrics.average_cpc,
                metrics.cost_micros,
                metrics.conversions,
                metrics.conversions_value,
                metrics.cost_per_conversion,
                metrics.search_impression_share,
                metrics.search_top_impression_share
            FROM campaign
            WHERE segments.date BETWEEN '{start_date}' AND '{end_date}'
            AND campaign.status != 'REMOVED'
            {campaign_filter}
            ORDER BY metrics.cost_micros DESC
            LIMIT 100
        """
        rows = with_retry(run_query, client, customer_id, gaql)
        return [
            {
                "id": str(r.campaign.id),
                "name": r.campaign.name,
                "status": r.campaign.status.name,
                "type": r.campaign.advertising_channel_type.name,
                "clicks": r.metrics.clicks,
                "impressions": r.metrics.impressions,
                "ctr": round(r.metrics.ctr * 100, 2),
                "avg_cpc": round(r.metrics.average_cpc / 1_000_000, 2),
                "cost": round(r.metrics.cost_micros / 1_000_000, 2),
                "conversions": round(r.metrics.conversions, 1),
                "conversion_value": round(r.metrics.conversions_value, 2),
                "cost_per_conversion": round(r.metrics.cost_per_conversion / 1_000_000, 2) if r.metrics.cost_per_conversion else None,
                "search_impression_share": round(r.metrics.search_impression_share * 100, 1) if r.metrics.search_impression_share else None,
                "search_top_is": round(r.metrics.search_top_impression_share * 100, 1) if r.metrics.search_top_impression_share else None,
            }
            for r in rows
        ]
    except Exception as e:
        return _err(e)


@mcp.tool()
def compare_periods(
    customer_id: str,
    period1_start: str,
    period1_end: str,
    period2_start: str,
    period2_end: str,
    breakdown: str = "campaign",
    account: Optional[str] = None,
) -> dict:
    """
    Compare performance between two date ranges.

    Args:
        customer_id: Google Ads customer ID
        period1_start / period1_end: First period (YYYY-MM-DD)
        period2_start / period2_end: Second period to compare against
        breakdown: 'campaign' or 'account' level comparison
        account: Named account from config
    """
    try:
        client = _get_manager().get_client(account)

        def fetch(start, end):
            gaql = f"""
                SELECT
                    campaign.id, campaign.name,
                    metrics.clicks, metrics.impressions, metrics.cost_micros, metrics.conversions
                FROM campaign
                WHERE segments.date BETWEEN '{start}' AND '{end}'
                AND campaign.status != 'REMOVED'
                ORDER BY metrics.cost_micros DESC
                LIMIT 50
            """
            return with_retry(run_query, client, customer_id, gaql)

        p1_rows = fetch(period1_start, period1_end)
        p2_rows = fetch(period2_start, period2_end)

        def to_dict(rows):
            return {
                str(r.campaign.id): {
                    "name": r.campaign.name,
                    "clicks": r.metrics.clicks,
                    "impressions": r.metrics.impressions,
                    "cost": round(r.metrics.cost_micros / 1_000_000, 2),
                    "conversions": round(r.metrics.conversions, 1),
                }
                for r in rows
            }

        p1 = to_dict(p1_rows)
        p2 = to_dict(p2_rows)

        comparison = []
        for cid in set(p1) | set(p2):
            r1 = p1.get(cid, {})
            r2 = p2.get(cid, {})
            comparison.append({
                "campaign_id": cid,
                "name": r1.get("name") or r2.get("name", ""),
                "period1": {k: r1.get(k, 0) for k in ["clicks", "impressions", "cost", "conversions"]},
                "period2": {k: r2.get(k, 0) for k in ["clicks", "impressions", "cost", "conversions"]},
                "delta_clicks": r2.get("clicks", 0) - r1.get("clicks", 0),
                "delta_cost": round(r2.get("cost", 0) - r1.get("cost", 0), 2),
                "delta_conversions": round(r2.get("conversions", 0) - r1.get("conversions", 0), 1),
            })

        comparison.sort(key=lambda x: abs(x["delta_cost"]), reverse=True)
        return {
            "period1": f"{period1_start} to {period1_end}",
            "period2": f"{period2_start} to {period2_end}",
            "campaigns": comparison,
        }
    except Exception as e:
        return _err(e)


# ---------------------------------------------------------------------------
# Keyword tools
# ---------------------------------------------------------------------------

@mcp.tool()
def get_keyword_performance(
    customer_id: str,
    start_date: str,
    end_date: str,
    campaign_id: Optional[str] = None,
    row_limit: int = 50,
    account: Optional[str] = None,
) -> list[dict]:
    """
    Get keyword-level performance including quality scores.

    Args:
        customer_id: Google Ads customer ID
        start_date / end_date: YYYY-MM-DD
        campaign_id: Filter to a specific campaign (optional)
        row_limit: Number of keywords to return (default 50, max 1000)
        account: Named account from config
    """
    try:
        client = _get_manager().get_client(account)
        campaign_filter = f"AND campaign.id = {campaign_id}" if campaign_id else ""
        limit = min(max(1, row_limit), 1000)
        gaql = f"""
            SELECT
                ad_group_criterion.keyword.text,
                ad_group_criterion.keyword.match_type,
                ad_group_criterion.quality_info.quality_score,
                ad_group_criterion.quality_info.creative_quality_score,
                ad_group_criterion.quality_info.post_click_quality_score,
                ad_group_criterion.quality_info.search_predicted_ctr,
                ad_group_criterion.status,
                campaign.name,
                ad_group.name,
                metrics.clicks,
                metrics.impressions,
                metrics.ctr,
                metrics.average_cpc,
                metrics.cost_micros,
                metrics.conversions
            FROM keyword_view
            WHERE segments.date BETWEEN '{start_date}' AND '{end_date}'
            AND ad_group_criterion.status != 'REMOVED'
            {campaign_filter}
            ORDER BY metrics.cost_micros DESC
            LIMIT {limit}
        """
        rows = with_retry(run_query, client, customer_id, gaql)
        return [
            {
                "keyword": r.ad_group_criterion.keyword.text,
                "match_type": r.ad_group_criterion.keyword.match_type.name,
                "quality_score": r.ad_group_criterion.quality_info.quality_score or None,
                "ad_relevance": r.ad_group_criterion.quality_info.creative_quality_score.name if r.ad_group_criterion.quality_info.creative_quality_score else None,
                "landing_page": r.ad_group_criterion.quality_info.post_click_quality_score.name if r.ad_group_criterion.quality_info.post_click_quality_score else None,
                "expected_ctr": r.ad_group_criterion.quality_info.search_predicted_ctr.name if r.ad_group_criterion.quality_info.search_predicted_ctr else None,
                "status": r.ad_group_criterion.status.name,
                "campaign": r.campaign.name,
                "ad_group": r.ad_group.name,
                "clicks": r.metrics.clicks,
                "impressions": r.metrics.impressions,
                "ctr": round(r.metrics.ctr * 100, 2),
                "avg_cpc": round(r.metrics.average_cpc / 1_000_000, 2),
                "cost": round(r.metrics.cost_micros / 1_000_000, 2),
                "conversions": round(r.metrics.conversions, 1),
            }
            for r in rows
        ]
    except Exception as e:
        return _err(e)


@mcp.tool()
def search_terms_report(
    customer_id: str,
    start_date: str,
    end_date: str,
    campaign_id: Optional[str] = None,
    row_limit: int = 50,
    account: Optional[str] = None,
) -> list[dict]:
    """
    Get actual search terms that triggered your ads.

    Args:
        customer_id: Google Ads customer ID
        start_date / end_date: YYYY-MM-DD
        campaign_id: Filter to specific campaign (optional)
        row_limit: Rows to return (default 50, max 1000)
        account: Named account from config
    """
    try:
        client = _get_manager().get_client(account)
        campaign_filter = f"AND campaign.id = {campaign_id}" if campaign_id else ""
        limit = min(max(1, row_limit), 1000)
        gaql = f"""
            SELECT
                search_term_view.search_term,
                search_term_view.status,
                campaign.name,
                ad_group.name,
                metrics.clicks,
                metrics.impressions,
                metrics.ctr,
                metrics.average_cpc,
                metrics.cost_micros,
                metrics.conversions
            FROM search_term_view
            WHERE segments.date BETWEEN '{start_date}' AND '{end_date}'
            {campaign_filter}
            ORDER BY metrics.clicks DESC
            LIMIT {limit}
        """
        rows = with_retry(run_query, client, customer_id, gaql)
        return [
            {
                "search_term": r.search_term_view.search_term,
                "status": r.search_term_view.status.name,
                "campaign": r.campaign.name,
                "ad_group": r.ad_group.name,
                "clicks": r.metrics.clicks,
                "impressions": r.metrics.impressions,
                "ctr": round(r.metrics.ctr * 100, 2),
                "avg_cpc": round(r.metrics.average_cpc / 1_000_000, 2),
                "cost": round(r.metrics.cost_micros / 1_000_000, 2),
                "conversions": round(r.metrics.conversions, 1),
            }
            for r in rows
        ]
    except Exception as e:
        return _err(e)


# ---------------------------------------------------------------------------
# Ad performance
# ---------------------------------------------------------------------------

@mcp.tool()
def get_ad_performance(
    customer_id: str,
    start_date: str,
    end_date: str,
    campaign_id: Optional[str] = None,
    row_limit: int = 25,
    account: Optional[str] = None,
) -> list[dict]:
    """
    Get ad-level performance (headlines, descriptions, CTR, conversions).

    Args:
        customer_id: Google Ads customer ID
        start_date / end_date: YYYY-MM-DD
        campaign_id: Filter to specific campaign (optional)
        row_limit: Ads to return (default 25)
        account: Named account from config
    """
    try:
        client = _get_manager().get_client(account)
        campaign_filter = f"AND campaign.id = {campaign_id}" if campaign_id else ""
        limit = min(max(1, row_limit), 500)
        gaql = f"""
            SELECT
                ad_group_ad.ad.id,
                ad_group_ad.ad.type,
                ad_group_ad.ad.final_urls,
                ad_group_ad.ad.responsive_search_ad.headlines,
                ad_group_ad.status,
                campaign.name,
                ad_group.name,
                metrics.clicks,
                metrics.impressions,
                metrics.ctr,
                metrics.average_cpc,
                metrics.cost_micros,
                metrics.conversions
            FROM ad_group_ad
            WHERE segments.date BETWEEN '{start_date}' AND '{end_date}'
            AND ad_group_ad.status != 'REMOVED'
            {campaign_filter}
            ORDER BY metrics.clicks DESC
            LIMIT {limit}
        """
        rows = with_retry(run_query, client, customer_id, gaql)
        result = []
        for r in rows:
            ad = r.ad_group_ad.ad
            headlines = []
            if ad.responsive_search_ad and ad.responsive_search_ad.headlines:
                headlines = [h.text for h in ad.responsive_search_ad.headlines[:3]]
            result.append({
                "ad_id": str(ad.id),
                "type": ad.type_.name if ad.type_ else None,
                "headlines": headlines,
                "final_url": ad.final_urls[0] if ad.final_urls else None,
                "status": r.ad_group_ad.status.name,
                "campaign": r.campaign.name,
                "ad_group": r.ad_group.name,
                "clicks": r.metrics.clicks,
                "impressions": r.metrics.impressions,
                "ctr": round(r.metrics.ctr * 100, 2),
                "avg_cpc": round(r.metrics.average_cpc / 1_000_000, 2),
                "cost": round(r.metrics.cost_micros / 1_000_000, 2),
                "conversions": round(r.metrics.conversions, 1),
            })
        return result
    except Exception as e:
        return _err(e)


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

def main():
    transport = os.environ.get("MCP_TRANSPORT", "stdio")
    if transport == "sse":
        host = os.environ.get("MCP_HOST", "127.0.0.1")
        port = int(os.environ.get("MCP_PORT", "3001"))
        mcp.run(transport="sse", host=host, port=port)
    else:
        mcp.run(transport="stdio")


if __name__ == "__main__":
    main()
