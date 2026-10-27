import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI

load_dotenv()


def get_llm(temperature: float = 0.1, **kwargs) -> ChatGoogleGenerativeAI:
    api_key = os.getenv("GOOGLE_API_KEY", "").strip()
    model_name = os.getenv("GEMINI_MODEL_NAME", "gemini-2.5-flash")
    if not api_key or api_key == "your_gemini_api_key_here":
        raise RuntimeError(
            "GOOGLE_API_KEY is missing in .env. Please set a valid Gemini API key."
        )
    return ChatGoogleGenerativeAI(
        model=model_name,
        google_api_key=api_key,
        temperature=temperature,
        timeout=60,
        max_retries=2,
    )