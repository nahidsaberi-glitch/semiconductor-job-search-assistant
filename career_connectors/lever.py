from __future__ import annotations

import re
import requests


def search_lever(company: str, config: dict, query: str, location: str = "", limit: int = 20) -> list[dict]:
    account = config["account"]
    url = f"https://api.lever.co/v0/postings/{account}"
    r = requests.get(url, params={"mode": "json"}, timeout=30)
    r.raise_for_status()
    postings = r.json()
    q = f"{query} {location}".lower().strip()
    words = [w for w in re.split(r"\W+", q) if len(w) > 2]

    jobs = []
    for p in postings:
        title = p.get("text", "")
        loc = p.get("categories", {}).get("location", "")
        desc = " ".join([p.get("descriptionPlain", ""), p.get("additionalPlain", "")]).strip()
        haystack = f"{title} {loc} {desc}".lower()
        if words and not any(w in haystack for w in words):
            continue
        jobs.append({
            "source": "Native Career Connector — Lever",
            "source_query": q,
            "title": title,
            "company": company,
            "location": loc,
            "description": desc[:4000],
            "apply_link": p.get("hostedUrl", ""),
            "created": "",
            "salary_min": "",
            "salary_max": "",
        })
        if len(jobs) >= limit:
            break
    return jobs
