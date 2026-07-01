import re

def clean_text(text: str) -> str:
    return re.sub(r"\s+", " ", text or "").strip().lower()

def split_keywords(text: str) -> list[str]:
    if not text:
        return []
    return [x.strip() for x in re.split(r"[,;\n]+", text) if x.strip()]
