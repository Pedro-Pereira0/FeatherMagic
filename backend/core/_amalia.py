from langchain_ollama.llms import OllamaLLM
import os

class _Amalia:

    def connect_model(self):
        return OllamaLLM(base_url = os.getenv("OLLAMA_BASE_URL"), model = os.getenv("OLLAMA_WRITING_MODEL"))

writer_model = _Amalia().connect_model()