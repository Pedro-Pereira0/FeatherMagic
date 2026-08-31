from langchain_google_genai import ChatGoogleGenerativeAI

import os
from dotenv import load_dotenv

load_dotenv()

class _Gemini:
    
    def connect_model(self):
        return ChatGoogleGenerativeAI(model = os.getenv("GEMINI_MODEL"), google_api_key = os.getenv("GEMINI_API_KEY"))

reason_model_gemini = _Gemini().connect_model()