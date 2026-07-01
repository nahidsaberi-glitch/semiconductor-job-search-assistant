from config import CAREER_PATH_ROLE_QUERIES, CAREER_SITE_URLS
from urllib.parse import quote_plus

def build_queries(selected_paths: list[str], selected_companies: list[str], include_company_queries: bool = True):
    role_queries = []
    for path in selected_paths:
        role_queries.extend(CAREER_PATH_ROLE_QUERIES.get(path, []))
    role_queries = list(dict.fromkeys(role_queries))
    queries = list(role_queries)
    if include_company_queries:
        for company in selected_companies:
            for role in role_queries:
                queries.append(f"{company} {role}")
    return list(dict.fromkeys(queries))

def make_search_links(query: str, location: str, selected_companies: list[str]) -> dict:
    q = quote_plus(query)
    loc = quote_plus(location)
    links = {
        "LinkedIn": f"https://www.linkedin.com/jobs/search/?keywords={q}&location={loc}",
        "Indeed": f"https://www.indeed.com/jobs?q={q}&l={loc}",
        "Google Jobs": f"https://www.google.com/search?q={q}+jobs+{loc}",
    }
    for company in selected_companies:
        site_url = CAREER_SITE_URLS.get(company, "")
        if site_url:
            links[f"{company} Careers"] = site_url
    return links

def make_google_site_search_links(query: str, selected_companies: list[str]) -> dict:
    links = {}
    for company in selected_companies:
        url = CAREER_SITE_URLS.get(company, "")
        if not url:
            continue
        domain = url.replace("https://", "").replace("http://", "").split("/")[0]
        links[f"{company} site search"] = f"https://www.google.com/search?q=site%3A{quote_plus(domain)}+{quote_plus(query)}+jobs"
    return links
