import os
import streamlit as st
from dotenv import load_dotenv

load_dotenv()

def get_secret(name: str) -> str:
    if name in os.environ:
        return os.environ[name]
    try:
        return st.secrets[name]
    except Exception:
        return ""
