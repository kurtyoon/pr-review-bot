from langchain_core.language_models.base import BaseLanguageModel
from langchain_openai import ChatOpenAI
from langchain_google_genai import ChatGoogleGenerativeAI
from google.generativeai.types.safety_types import HarmCategory, HarmBlockThreshold

class LLMFactory:

    @staticmethod
    def create_llm(config) -> BaseLanguageModel:
        llm_provider = config.get("llm_provider", "openai").lower()
        model = config.get("model")
        temperature = config.get("temperature", 0.3)

        if llm_provider == "openai":
            api_key = config.get("openai_api_key")

            if not api_key:
                raise ValueError("OpenAI API key is not set")
            
            return ChatOpenAI(
                model=model or "gpt-4o-mini",
                temperature=temperature,
                openai_api_key=api_key
            )
        
        elif llm_provider == "google":
            api_key = config.get("google_api_key")

            if not api_key:
                raise ValueError("Google API key is not set")
            
            safety_settings = {
                HarmCategory.HARASSMENT: HarmBlockThreshold.NONE,
                HarmCategory.HATE_SPEECH: HarmBlockThreshold.NONE,
                HarmCategory.SEXUALLY_EXPLICIT: HarmBlockThreshold.NONE,
                HarmCategory.DANGEROUS_CONTENT: HarmBlockThreshold.NONE
            }
            
            return ChatGoogleGenerativeAI(
                model=model or "gemini-1.0-pro",
                temperature=temperature,
                google_api_key=api_key,
                safety_settings=safety_settings
            )
        
        else:
            raise ValueError(f"Unsupported LLM provider: {llm_provider}")
