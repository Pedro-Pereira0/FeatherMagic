from langchain_groq import ChatGroq

import os
from dotenv import load_dotenv

load_dotenv()

class _Groq:
    
    def connect_model(self):
        return ChatGroq(model = os.getenv("GROQ_MODEL"), api_key = os.getenv("GROQ_API_KEY"))

reason_model_groq = _Groq().connect_model()