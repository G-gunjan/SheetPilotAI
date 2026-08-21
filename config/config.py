
# import os
# from dotenv import load_dotenv

# load_dotenv(dotenv_path=r"D:\SheetPilotAI\.env")

# GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# MODEL_NAME = "gemini-2.5-flash"
# APP_NAME = "SheetPilot AI"

# print("Key loaded:", GEMINI_API_KEY is not None)
# print("Key length:", len(GEMINI_API_KEY) if GEMINI_API_KEY else 0)
# print("Key starts with:", GEMINI_API_KEY[:5] if GEMINI_API_KEY else "NONE")

import os
from dotenv import load_dotenv

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
MODEL_NAME = "gemini-2.5-flash"
APP_NAME = "SheetPilot AI – Voice Macro Builder"