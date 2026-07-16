import os

API_KEY = os.getenv("OPENAI_API_KEY")

try:
    import streamlit as st
    if not API_KEY:
        API_KEY = st.secrets.get("OPENAI_API_KEY")
except Exception:
    pass

if not API_KEY:
    raise RuntimeError(
        "OPENAI_API_KEY is missing. Set this key in Streamlit Secrets or your environment."
    )

BASE_URL = os.getenv("BASE_URL", "")  # empty -> use official OpenAI endpoint when not set
MODEL_NAME = os.getenv("MODEL_NAME", "llama-3.3-70b-versatile")