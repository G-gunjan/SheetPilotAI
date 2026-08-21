import os
from dotenv import load_dotenv

load_dotenv()
try:
    import streamlit as st

    GEMINI_API_KEY = st.secrets.get(
        "GEMINI_API_KEY",
        os.getenv("GEMINI_API_KEY")
    )
except Exception:
    # Local fallback
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")


MODEL_NAME = "gemini-2.5-flash"

APP_NAME = "SheetPilot AI – Voice Macro Builder"