from __future__ import annotations

import requests
from typing import Any


def _text(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, str):
        return value
    if isinstance(value, dict):
        return " ".join(_text(v) for v in value.values())
    if isinstance(value, list):
        return " ".join(_text(v) for v in value)
    return str(value)


def _location_from_posting(posting: dict) -> str:
    locations = []
    for key in ("locationsText", "location", "locations"):
        value = posting.get(key)
        if isinstance(value, str) and value:
            locations.append(value)
        elif isinstance(value, list):
            for item in value:
                if isinstance(item, str):
                    locations.append(item)
                elif isinstance(item, dict):
                    locations.append(item.get("descriptor") or item.get("displayName") or item.get("name") or "")
        elif isinstance(value, dict):
            locations.append(value.get("descriptor") or value.get("displayName") or value.get("name") or "")
    return ", ".join(dict.fromkeys([x for x in locations if x]))


def _normalize(company: str, config: dict, posting: dict, query: str) -> dict:
    title = posting.get("title") or posting.get("jobTitle") or posting.get("externalPath") or ""
    external_path = posting.get("externalPath") or posting.get("bulletFields", [{}])[0].get("externalPath", "") if posting.get("bulletFields") else posting.get("externalPath", "")
    if external_path and external_path.startswith("/"):
        apply_link = config["base_url"].rstrip("/") + external_path
    else:
        apply_link = config["site_url"].rstrip("/")
    description = _text(posting.get("bulletFields"))
    location = _location_from_posting(posting)
    return {
        "source": "Native Career Connector — Workday",
        "source_query": query,
        "title": title,
        "company": company,
        "location": location,
        "description": description,
        "apply_link": apply_link,
        "created": posting.get("postedOn") or posting.get("startDate") or "",
        "salary_min": "",
        "salary_max": "",
    }


def search_workday(company: str, config: dict, query: str, location: str = "", limit: int = 20) -> list[dict]:
    """Search public Workday CXS job feeds.

    Expected config keys:
    base_url: e.g. https://intel.wd1.myworkdayjobs.com
    tenant: e.g. intel
    site: e.g. External
    site_url: e.g. https://intel.wd1.myworkdayjobs.com/External
    """
    base_url = config["base_url"].rstrip("/")
    tenant = config["tenant"].strip("/")
    site = config["site"].strip("/")
    endpoint = f"{base_url}/wday/cxs/{tenant}/{site}/jobs"

    search_text = " ".join(part for part in [query, location] if part).strip()
    payload = {
        "appliedFacets": {},
        "limit": limit,
        "offset": 0,
        "searchText": search_text,
    }
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "User-Agent": "Mozilla/5.0",
    }

    r = requests.post(endpoint, json=payload, headers=headers, timeout=30)
    r.raise_for_status()
    data = r.json()
    postings = data.get("jobPostings") or data.get("jobs") or data.get("postings") or []
    return [_normalize(company, config, posting, search_text) for posting in postings]
