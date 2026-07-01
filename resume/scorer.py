from config import CAREER_PATHS, COMPANY_BOOSTS, BAY_AREA_TERMS
from utils.text import clean_text, split_keywords

def build_keywords(selected_paths: list[str], custom_keywords: str) -> list[str]:
    keywords = []
    for path in selected_paths:
        keywords.extend(CAREER_PATHS.get(path, []))
    keywords.extend(split_keywords(custom_keywords))
    return list(dict.fromkeys([k for k in keywords if k]))

def keyword_score(resume_text: str, job_text: str, selected_paths: list[str], custom_keywords: str):
    resume = clean_text(resume_text)
    job = clean_text(job_text)
    keywords = build_keywords(selected_paths, custom_keywords)
    matched, missing = [], []

    for kw in keywords:
        kw_l = kw.lower()
        if kw_l in job:
            if kw_l in resume:
                matched.append(kw)
            else:
                missing.append(kw)

    if not matched and not missing:
        return 0, [], []

    score = int(100 * len(matched) / max(1, len(matched) + len(missing)))
    return score, matched, missing

def company_boost(company: str, title: str = "", description: str = ""):
    text = clean_text(f"{company} {title} {description}")
    for target, boost in COMPANY_BOOSTS.items():
        if target in text:
            return boost, target.title()
    return 0, ""

def work_mode_from_text(job_text: str) -> str:
    text = clean_text(job_text)
    if "remote" in text:
        return "Remote"
    if "hybrid" in text:
        return "Hybrid"
    if "onsite" in text or "on-site" in text or "on site" in text:
        return "Onsite"
    return "Not specified"

def is_bay_area(location: str, description: str = "") -> bool:
    text = clean_text(location + " " + description)
    return any(term in text for term in BAY_AREA_TERMS)

def has_excluded_keywords(job_text: str, exclude_keywords: str) -> bool:
    text = clean_text(job_text)
    excluded = split_keywords(exclude_keywords)
    return any(clean_text(word) in text for word in excluded)

def add_scores(job: dict, resume_text: str, selected_paths: list[str], custom_keywords: str) -> dict:
    job_text = f"{job['title']} {job['company']} {job['location']} {job['description']}"
    base_score, matched, missing = keyword_score(resume_text, job_text, selected_paths, custom_keywords)
    boost, boosted_company = company_boost(job["company"], job["title"], job["description"])
    job["base_match_score"] = base_score
    job["company_boost"] = boost
    job["boosted_company"] = boosted_company
    job["final_score"] = min(100, base_score + boost)
    job["work_mode"] = work_mode_from_text(job_text)
    job["bay_area_match"] = "Yes" if is_bay_area(job["location"], job["description"]) else "No"
    job["matched_keywords"] = ", ".join(matched[:15])
    job["missing_keywords"] = ", ".join(missing[:15])
    job["status"] = "Not applied"
    job["notes"] = ""
    return job
