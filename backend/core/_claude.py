from langchain_anthropic import ChatAnthropic
import os

from dotenv import load_dotenv

load_dotenv()


class _Claude:
    def connect_model(self):
        return ChatAnthropic(model = os.getenv("CLAUDE_MODEL"), api_key = os.getenv("CLAUDE_API_KEY"))

reason_model_claude = _Claude().connect_model()