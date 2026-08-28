from langchain_ollama.llms import OllamaLLM
import os

class _QWEN:
    
    def connect_model(self):
        return OllamaLLM(base_url = os.getenv("OLLAMA_BASE_URL"), model = os.getenv("OLLAMA_REASON_MODEL"))

reason_model = _QWEN().connect_model()