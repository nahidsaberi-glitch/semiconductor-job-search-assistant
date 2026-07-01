# Semiconductor Career Assistant

Version 3.1 now uses **Native Career Connectors** instead of SerpAPI/Google site search.

## What changed in v3.0

- Removed the SerpAPI dependency for company career-site search.
- Added direct native connector architecture:
  - `career_connectors/workday.py`
  - `career_connectors/greenhouse.py`
  - `career_connectors/lever.py`
  - `career_connectors/sitime.py`
  - `career_connectors/native.py`
- Added connector mapping in `config.py` under `NATIVE_CAREER_CONNECTORS`.
- First enabled companies:
  - Intel — Workday
  - KLA — Workday
  - NVIDIA — Workday
  - SiTime — SiTime public job listing page

## Install

```bash
pip install -r requirements.txt
```

## Run

```bash
streamlit run app.py
```

## Optional Adzuna source

Adzuna is still supported as an optional broad job board source. Add these to Streamlit secrets only if you want Adzuna:

```toml
ADZUNA_APP_ID = "your_id"
ADZUNA_APP_KEY = "your_key"
```

Native career connectors do **not** need SerpAPI and do **not** need a Google search API key. If you still see a SERPAPI_KEY message, you are running the old extracted folder; delete it and extract this v3.1 zip into a new folder.

## Adding another company

Add an entry to `NATIVE_CAREER_CONNECTORS` in `config.py`.

Example Workday company:

```python
"Company Name": {
    "type": "workday",
    "base_url": "https://company.wd1.myworkdayjobs.com",
    "tenant": "company",
    "site": "External",
    "site_url": "https://company.wd1.myworkdayjobs.com/External",
}
```

Example Greenhouse company:

```python
"Company Name": {
    "type": "greenhouse",
    "board_token": "companytoken",
}
```

Example Lever company:

```python
"Company Name": {
    "type": "lever",
    "account": "companyaccount",
}
```
