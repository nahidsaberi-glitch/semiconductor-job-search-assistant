from __future__ import annotations

import re
import requests


def _clean_html(text: str) -> str:
    text = re.sub(r"<[^>]+>", " ", text or "")
    return re.sub(r"\s+", " ", text).strip()


def search_greenhouse(company: str, config: dict, query: str, location: str = "", limit: int = 20) -> list[dict]:
    board_token = config["board_token"]
    url = f"https://api.greenhouse.io/v1/boards/{board_token}/jobs"
    r = requests.get(url, params={"content": "true"}, timeout=30)
    r.raise_for_status()
    jobs = r.json().get("jobs", [])
    q = f"{query} {location}".lower().strip()
    words = [w for w in re.split(r"\W+", q) if len(w) > 2]

    normalized = []
    for job in jobs:
        title = job.get("title", "")
        offices = job.get("offices") or []
        loc = ", ".join(o.get("name", "") for o in offices if o.get("name")) or job.get("location", {}).get("name", "")
        content = _clean_html(job.get("content", ""))
        haystack = f"{title} {loc} {content}".lower()
        if words and not any(w in haystack for w in words):
            continue
        normalized.append({
            "source": "Native Career Connector — Greenhouse",
            "source_query": q,
            "title": title,
            "company": company,
            "location": loc,
            "description": content[:4000],
            "apply_link": job.get("absolute_url", ""),
            "created": job.get("updated_at", ""),
            "salary_min": "",
            "salary_max": "",
        })
        if len(normalized) >= limit:
            break
    return normalized
