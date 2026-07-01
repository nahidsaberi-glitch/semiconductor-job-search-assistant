from __future__ import annotations

from config import NATIVE_CAREER_CONNECTORS
from career_connectors.workday import search_workday
from career_connectors.greenhouse import search_greenhouse
from career_connectors.lever import search_lever
from career_connectors.sitime import search_sitime

CONNECTOR_FUNCTIONS = {
    "workday": search_workday,
    "greenhouse": search_greenhouse,
    "lever": search_lever,
    "sitime_site": search_sitime,
}


def companies_with_native_connectors() -> list[str]:
    return sorted(NATIVE_CAREER_CONNECTORS.keys())


def search_native_company(company: str, query: str, location: str = "", limit: int = 20) -> list[dict]:
    config = NATIVE_CAREER_CONNECTORS.get(company)
    if not config:
        return []
    connector_type = config.get("type")
    fn = CONNECTOR_FUNCTIONS.get(connector_type)
    if not fn:
        return []
    return fn(company=company, config=config, query=query, location=location, limit=limit)
