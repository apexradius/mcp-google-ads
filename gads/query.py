"""GAQL query helpers."""
from typing import Any

from google.ads.googleads.client import GoogleAdsClient


def run_query(client: GoogleAdsClient, customer_id: str, gaql: str) -> list[dict]:
    """Execute a GAQL query and return rows as plain dicts."""
    service = client.get_service("GoogleAdsService")
    stream = service.search_stream(customer_id=customer_id.replace("-", ""), query=gaql)
    rows = []
    for batch in stream:
        for row in batch.results:
            rows.append(row)
    return rows


def clean_id(customer_id: str) -> str:
    return customer_id.replace("-", "")
