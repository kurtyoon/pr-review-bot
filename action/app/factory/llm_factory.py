from langchain_schema.language_model import BaseLanguageModel
from langchain_openai import ChatOpenAI
from langchain_google_genai import ChatGoogleGenerativeAI

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
            
            return ChatGoogleGenerativeAI(
                model=model or "gemini-1.0-pro",
                temperature=temperature,
                google_api_key=api_key,
                safety_settings={
                    "HARASSMENT": 'block_none',
                    "HATE_SPEECH": 'block_none',
                    "SEXUALLY_EXPLICIT": 'block_none',
                    "DANGEROUS_CONTENT": 'block_none',
                }
            )
        
        else:
            raise ValueError(f"Unsupported LLM provider: {llm_provider}")
