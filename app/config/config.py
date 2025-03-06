import os

class Config:
    def __init__(self):

        self.setting = {
            # General Settings
            "llm_provider": os.getenv("LLM_PROVIDER", "openai"),
            "model": os.getenv("MODEL_NAME", "gpt-4o-mini"),
            "temperature": float(os.getenv("TEMPERATURE", "0.3")),
            "verbose": os.getenv("VERBOSE", "False").lower() == "true",

            # API Keys
            "open_api_key": os.getenv("OPENAI_API_KEY"),
            "google_api_key": os.getenv("GOOGLE_API_KEY"),
        }

    def get(self, key, default=None):
        return self.setting.get(key, default)
