import requests
from utils.secrets import get_secret

def search_adzuna(query: str, location: str, country: str = "us", results_per_page: int = 20):
    app_id = get_secret("ADZUNA_APP_ID")
    app_key = get_secret("ADZUNA_APP_KEY")
    if not app_id or not app_key:
        return []

    url = f"https://api.adzuna.com/v1/api/jobs/{country}/search/1"
    params = {
        "app_id": app_id,
        "app_key": app_key,
        "results_per_page": results_per_page,
        "what": query,
        "where": location,
        "content-type": "application/json",
    }
    response = requests.get(url, params=params, timeout=20)
    response.raise_for_status()
    return response.json().get("results", [])

def normalize_adzuna_job(job: dict, source_query: str) -> dict:
    company = job.get("company", {}).get("display_name", "")
    location_parts = job.get("location", {}).get("area", [])
    location = ", ".join(location_parts[-3:]) if location_parts else ""
    return {
        "source": "Adzuna",
        "source_query": source_query,
        "title": job.get("title", ""),
        "company": company,
        "location": location,
        "description": job.get("description", ""),
        "apply_link": job.get("redirect_url", ""),
        "created": job.get("created", ""),
        "salary_min": job.get("salary_min", ""),
        "salary_max": job.get("salary_max", ""),
    }
