import pandas as pd
import streamlit as st

from config import TARGET_COMPANIES, CAREER_PATHS
from export.excel import to_excel_bytes
from job_sources.adzuna import search_adzuna, normalize_adzuna_job
from job_sources.queries import build_queries, make_search_links, make_google_site_search_links
from career_connectors.native import search_native_company, companies_with_native_connectors
from resume.parser import extract_resume_text
from resume.scorer import add_scores, has_excluded_keywords, is_bay_area
from utils.secrets import get_secret
from utils.parallel import run_parallel

st.set_page_config(page_title="Semiconductor Career Assistant", page_icon="🔎", layout="wide")

st.title("🔎 Semiconductor Career Assistant")
st.caption("Version 3.1 — Native Career Connectors + optional Adzuna search. No SerpAPI needed.")

with st.sidebar:
    st.header("Search Setup")
    location = st.text_input("Location", value="San Jose, CA")

    selected_paths = st.multiselect(
        "Career paths",
        options=list(CAREER_PATHS.keys()),
        default=[
            "DFT / Test Engineering",
            "Product Engineering",
            "Validation Engineering",
            "Reliability Engineering",
            "Manufacturing / NPI"
        ]
    )

    selected_companies = st.multiselect(
        "Target companies",
        options=TARGET_COMPANIES,
        default=[
            "Intel", "AMD", "NVIDIA", "Apple", "KLA", "Applied Materials",
            "Lam Research", "SiTime", "Micron", "Texas Instruments",
            "Advantest", "Teradyne", "Cadence", "Synopsys", "Keysight"
        ]
    )

    custom_keywords = st.text_area(
        "Custom keywords",
        value="scan, ATPG, MBIST, JTAG, wafer sort, ATE, Python, JMP, SQL",
        help="Add keywords separated by commas or new lines."
    )

    exclude_keywords = st.text_area(
        "Exclude keywords",
        value="intern, internship, manager, director",
        help="Jobs containing these words will be removed."
    )

    st.subheader("Sources")
    use_adzuna = st.checkbox("Search Adzuna", value=True)
    use_company_sites = st.checkbox("Search official company career feeds (native connectors)", value=True)

    st.subheader("Filters")
    bay_area_only = st.checkbox("Bay Area only", value=False)
    remote_only = st.checkbox("Remote only", value=False)
    hybrid_only = st.checkbox("Hybrid only", value=False)

    st.subheader("Search controls")
    include_company_queries = st.checkbox("Include company-specific searches", value=True)
    results_per_query = st.slider("Results per query", min_value=5, max_value=50, value=10, step=5)
    max_queries = st.slider("Maximum searches to run", min_value=10, max_value=200, value=100, step=10)

st.subheader("Resume")
uploaded_resume = st.file_uploader("Upload resume", type=["txt", "pdf", "docx"])
uploaded_text = extract_resume_text(uploaded_resume)

resume_text = st.text_area(
    "Paste or edit resume text",
    value=uploaded_text,
    height=220,
    placeholder="Paste your resume here..."
)

tab1, tab2, tab3, tab4 = st.tabs(["Search Jobs", "Search Links", "Manual Job Match", "Tracker"])

with tab1:
    st.markdown("### Search and rank jobs")

    if use_company_sites:
        supported = companies_with_native_connectors()
        unsupported = [c for c in selected_companies if c not in supported]
        st.success(f"Native career connectors enabled for: {', '.join([c for c in selected_companies if c in supported]) or 'none selected'}. No SerpAPI key is required.")
        if unsupported:
            st.caption(f"Not yet native-connected: {', '.join(unsupported[:12])}{'...' if len(unsupported) > 12 else ''}")

    if st.button("Search Jobs"):
        if not resume_text.strip():
            st.warning("Please upload or paste your resume first.")
        elif not selected_paths:
            st.warning("Please select at least one career path.")
        elif not use_adzuna and not use_company_sites:
            st.warning("Please select at least one job source.")
        else:
            queries = build_queries(selected_paths, selected_companies, include_company_queries)[:max_queries]
            st.write(f"Running {len(queries)} searches...")
            all_jobs = []

            search_errors = []
            progress_text = st.empty()
            progress_bar = st.progress(0)

            def _search_native(task):
                company, query = task
                jobs = search_native_company(
                    company=company,
                    query=query,
                    location=location,
                    limit=min(results_per_query, 20),
                )
                return company, query, jobs

            with st.spinner("Searching jobs..."):
                # Keep Adzuna sequential and unchanged. This avoids touching API-key behavior.
                for query in queries:
                    if use_adzuna:
                        if get_secret("ADZUNA_APP_ID") and get_secret("ADZUNA_APP_KEY"):
                            try:
                                raw_jobs = search_adzuna(query, location, results_per_page=results_per_query)
                                for raw in raw_jobs:
                                    all_jobs.append(normalize_adzuna_job(raw, query))
                            except Exception as e:
                                search_errors.append(f"Adzuna search failed for '{query}': {e}")
                        else:
                            search_errors.append("Adzuna is selected, but ADZUNA_APP_ID or ADZUNA_APP_KEY is missing.")
                            break

                # Step 1 upgrade: search native company feeds in parallel.
                if use_company_sites:
                    native_tasks = [(company, query) for query in queries for company in selected_companies]

                    def _update_native_progress(completed, total, task):
                        progress_text.write(f"Searching official company feeds... {completed}/{total}")
                        progress_bar.progress(completed / total)

                    native_results, native_errors = run_parallel(
                        native_tasks,
                        _search_native,
                        max_workers=12,
                        progress_callback=_update_native_progress,
                    )

                    for _company, _query, jobs in native_results:
                        all_jobs.extend(jobs)

                    for msg in native_errors:
                        search_errors.append(f"Native connector failed: {msg}")

            progress_text.empty()
            progress_bar.empty()

            if search_errors:
                with st.expander("Search warnings"):
                    for msg in search_errors[:25]:
                        st.warning(msg)
                    if len(search_errors) > 25:
                        st.caption(f"{len(search_errors) - 25} more warnings hidden.")

            scored_jobs = []
            for job in all_jobs:
                job_text = f"{job['title']} {job['company']} {job['location']} {job['description']}"
                if has_excluded_keywords(job_text, exclude_keywords):
                    continue
                if bay_area_only and not is_bay_area(job["location"], job["description"]):
                    continue
                if remote_only and "remote" not in job_text.lower():
                    continue
                if hybrid_only and "hybrid" not in job_text.lower():
                    continue
                scored_jobs.append(add_scores(job, resume_text, selected_paths, custom_keywords))

            if not scored_jobs:
                st.warning("No jobs found. Try fewer filters, broader location, or another source.")
            else:
                df = pd.DataFrame(scored_jobs).drop_duplicates(subset=["title", "company", "location", "apply_link"])
                df = df.sort_values(by="final_score", ascending=False)

                st.success(f"Found {len(df)} unique jobs after filters.")
                display_cols = [
                    "final_score", "base_match_score", "company_boost", "source",
                    "title", "company", "location", "work_mode", "bay_area_match",
                    "source_query", "matched_keywords", "missing_keywords",
                    "apply_link", "status", "notes"
                ]
                st.dataframe(df[display_cols], use_container_width=True, hide_index=True)

                st.download_button(
                    "Download Excel",
                    to_excel_bytes(df),
                    "semiconductor_career_results_v3_0.xlsx",
                    "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                )
                st.download_button(
                    "Download CSV",
                    df.to_csv(index=False).encode("utf-8"),
                    "semiconductor_career_results_v3_0.csv",
                    "text/csv"
                )

                st.markdown("### Top matches")
                for _, row in df.head(10).iterrows():
                    with st.expander(f"{row['final_score']}% — {row['title']} — {row['company']}"):
                        st.write(f"**Source:** {row['source']}")
                        st.write(f"**Location:** {row['location']}")
                        st.write(f"**Work mode:** {row['work_mode']}")
                        st.write(f"**Source query:** {row['source_query']}")
                        st.write(f"**Matched keywords:** {row['matched_keywords']}")
                        st.write(f"**Missing keywords:** {row['missing_keywords']}")
                        st.write(f"**Apply:** {row['apply_link']}")
                        st.write(row["description"][:1500] + "...")

with tab2:
    st.markdown("### Search links")
    search_phrase = st.text_input("Search phrase", value="product engineer semiconductor validation DFT reliability")
    for name, link in make_search_links(search_phrase, location, selected_companies).items():
        st.markdown(f"- [{name}]({link})")
    st.markdown("### Manual company career search links — fallback only")
    for name, link in make_google_site_search_links(search_phrase, selected_companies).items():
        st.markdown(f"- [{name}]({link})")

with tab3:
    st.markdown("### Manual job match")
    pasted_job = st.text_area("Paste a job description", height=240)
    if st.button("Score Manual Job"):
        if not resume_text.strip() or not pasted_job.strip():
            st.warning("Please paste both resume and job description.")
        else:
            temp_job = {
                "title": "Manual Job", "company": "", "location": "",
                "description": pasted_job, "apply_link": "",
                "source_query": "manual", "source": "manual",
                "created": "", "salary_min": "", "salary_max": "",
            }
            scored = add_scores(temp_job, resume_text, selected_paths, custom_keywords)
            st.metric("Match Score", f"{scored['final_score']}%")
            st.write("**Matched keywords:**", scored["matched_keywords"] or "None found")
            st.write("**Missing keywords:**", scored["missing_keywords"] or "None found")

with tab4:
    st.markdown("### Application tracker template")
    tracker_df = pd.DataFrame([{
        "Company": "", "Job Title": "", "Apply Link": "", "Date Found": "",
        "Date Applied": "", "Status": "Not applied", "Recruiter": "",
        "Follow-up Date": "", "Notes": ""
    }])
    st.dataframe(tracker_df, use_container_width=True, hide_index=True)
    st.download_button(
        "Download blank tracker as Excel",
        to_excel_bytes(tracker_df, sheet_name="Application Tracker"),
        "semiconductor_application_tracker.xlsx",
        "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
