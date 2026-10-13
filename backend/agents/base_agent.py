from abc import ABC

class base_agent(ABC):
    def sanitize_text(self, text: str) -> str:
        """Removes null bytes and invalid characters."""
        if isinstance(text, str):
            return text.replace("\x00", "").replace("\u0000", "")
        
        return text

    def sanitize_messages(self, messages):
        """Recursively cleans text inside LangChain message objects or dicts."""
        cleaned = []
        for msg in messages:
            if hasattr(msg, "content") and isinstance(msg.content, str):
                msg.content = self.sanitize_text(msg.content)
            elif isinstance(msg, dict) and "content" in msg:
                msg["content"] = self.sanitize_text(msg["content"])
            cleaned.append(msg)
        return cleaned