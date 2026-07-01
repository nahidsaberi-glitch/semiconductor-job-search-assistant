import io
import streamlit as st

def extract_resume_text(uploaded_file) -> str:
    if uploaded_file is None:
        return ""

    filename = uploaded_file.name.lower()
    data = uploaded_file.read()

    if filename.endswith(".txt"):
        return data.decode("utf-8", errors="ignore")

    if filename.endswith(".pdf"):
        try:
            from pypdf import PdfReader
            reader = PdfReader(io.BytesIO(data))
            return "\n".join([(p.extract_text() or "") for p in reader.pages])
        except Exception as e:
            st.warning(f"Could not read PDF resume: {e}")
            return ""

    if filename.endswith(".docx"):
        try:
            import docx
            document = docx.Document(io.BytesIO(data))
            return "\n".join([p.text for p in document.paragraphs])
        except Exception as e:
            st.warning(f"Could not read DOCX resume: {e}")
            return ""

    st.warning("Unsupported file type. Please upload .txt, .pdf, or .docx.")
    return ""
