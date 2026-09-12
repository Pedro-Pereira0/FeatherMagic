from langchain_ollama import ChatOllama
import os
from dotenv import load_dotenv

load_dotenv()

class _QWEN:
    
    def connect_model(self):
        return ChatOllama(base_url = os.getenv("OLLAMA_BASE_URL"), model = os.getenv("OLLAMA_REASON_MODEL"))

reason_model_qwen = _QWEN().connect_model()