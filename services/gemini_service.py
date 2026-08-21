# import json
# from google import genai

# from config.config import GEMINI_API_KEY, MODEL_NAME
# from utils.prompts import SYSTEM_PROMPT


# class GeminiService:

#     def __init__(self):
#         if not GEMINI_API_KEY:
#             raise ValueError("GEMINI_API_KEY is missing.")

#         self.client = genai.Client(
#             api_key=GEMINI_API_KEY
#         )

#     def generate_command(self, user_command, dataframe):

#         columns = list(dataframe.columns)

#         sample_data = dataframe.head(5).to_dict(
#             orient="records"
#         )

#         prompt = f"""
# {SYSTEM_PROMPT}

# DATAFRAME COLUMNS:
# {columns}

# SAMPLE DATA:
# {sample_data}

# USER COMMAND:
# {user_command}

# Return ONLY valid JSON.
# """

#         response = self.client.models.generate_content(
#             model=MODEL_NAME,
#             contents=prompt
#         )

#         text = response.text.strip()

#         # Remove markdown fences if Gemini returns them
#         if text.startswith("```"):
#             text = text.replace("```json", "")
#             text = text.replace("```", "")

#         return json.loads(text)


import json
from google import genai
from config.config import GEMINI_API_KEY, MODEL_NAME
from utils.prompts import SYSTEM_PROMPT

class GeminiService:
    def __init__(self):
        if not GEMINI_API_KEY:
            raise ValueError("GEMINI_API_KEY is missing in .env")
        self.client = genai.Client(api_key=GEMINI_API_KEY)

    def generate_command(self, user_command: str, dataframe, prefer_vba: bool = False):
        columns = list(dataframe.columns)
        sample_data = dataframe.head(5).to_dict(orient="records")

        preference = "Prefer Excel VBA code." if prefer_vba else "Prefer Pandas code."

        prompt = f"""
{SYSTEM_PROMPT}

{preference}

DATAFRAME COLUMNS:
{columns}

SAMPLE DATA (first 5 rows):
{sample_data}

USER COMMAND (may come from voice transcription):
{user_command}

Return ONLY valid JSON.
"""

        response = self.client.models.generate_content(
            model=MODEL_NAME,
            contents=prompt
        )

        text = response.text.strip()

        # Clean markdown fences if present
        if text.startswith("```"):
            text = text.replace("```json", "").replace("```", "").strip()

        return json.loads(text)