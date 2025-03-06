import os

class Config:
    def __init__(self):

        self.setting = {
            # General Settings
            "model": "gpt-4o-mini",
            "temperature": 0.3,
            "verbose": False,
            "open_api_key": os.getenv("OPENAI_API_KEY"),
        }

    def get(self, key, default=None):
        return self.setting.get(key, default)
