from __future__ import annotations

import re
import requests


def _strip_html(text: str) -> str:
    text = re.sub(r"<[^>]+>", " ", text or "")
    return re.sub(r"\s+", " ", text).strip()


def search_sitime(company: str, config: dict, query: str, location: str = "", limit: int = 20) -> list[dict]:
    """SiTime currently exposes job listings on its own site page.

    This connector scrapes the public listings page without using Google/SerpAPI.
    If SiTime changes the page, this function safely returns no results instead of crashing.
    """
    url = config.get("url", "https://www.sitime.com/job-listings")
    r = requests.get(url, headers={"User-Agent": "Mozilla/5.0"}, timeout=30)
    r.raise_for_status()
    html = r.text

    # First try JSON-ish embedded records.
    candidates = []
    for match in re.finditer(r'href="([^"]*job[^"]*)"[^>]*>([^<]{4,120})<', html, flags=re.I):
        link, title = match.groups()
        title = _strip_html(title)
        if not title or title.lower() in {"job listings", "current openings"}:
            continue
        if link.startswith("/"):
            link = "https://www.sitime.com" + link
        candidates.append((title, link))

    # Fallback: pick title/location rows visible in the page text.
    if not candidates:
        text = _strip_html(html)
        for title in re.findall(r'((?:Sr\.|Senior|Principal|Staff|Engineer|Technician|Manager|Director|Analyst)[^|\n]{5,100})', text):
            candidates.append((_strip_html(title), url))

    q = f"{query} {location}".lower().strip()
    words = [w for w in re.split(r"\W+", q) if len(w) > 2]
    jobs = []
    seen = set()
    for title, link in candidates:
        key = (title, link)
        if key in seen:
            continue
        seen.add(key)
        haystack = title.lower()
        if words and not any(w in haystack for w in words):
            continue
        jobs.append({
            "source": "Native Career Connector — SiTime Site",
            "source_query": q,
            "title": title,
            "company": company,
            "location": "",
            "description": "SiTime public job listing. Open the apply link for the full description.",
            "apply_link": link,
            "created": "",
            "salary_min": "",
            "salary_max": "",
        })
        if len(jobs) >= limit:
            break
    return jobs
