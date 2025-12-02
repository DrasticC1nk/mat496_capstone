
import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

PROJECT_ROOT = Path(__file__).parent.parent

LLM_PROVIDER = os.getenv("LLM_PROVIDER", "openai")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4-turbo-preview")
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY", "")
ANTHROPIC_MODEL = os.getenv("ANTHROPIC_MODEL", "claude-3-sonnet-20240229")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "llama2")
OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")

STARTING_HEALTH = int(os.getenv("STARTING_HEALTH", "100"))
STARTING_GOLD = int(os.getenv("STARTING_GOLD", "50"))
MAX_INVENTORY_SIZE = int(os.getenv("MAX_INVENTORY_SIZE", "20"))
SAVE_DIRECTORY = PROJECT_ROOT / os.getenv("SAVE_DIRECTORY", "saves")

VECTOR_STORE_PATH = PROJECT_ROOT / os.getenv("VECTOR_STORE_PATH", "data/vector_store")
EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "sentence-transformers/all-MiniLM-L6-v2")

DEBUG_MODE = os.getenv("DEBUG_MODE", "false").lower() == "true"
LANGCHAIN_TRACING_V2 = os.getenv("LANGCHAIN_TRACING_V2", "false").lower() == "true"

SAVE_DIRECTORY.mkdir(parents=True, exist_ok=True)
VECTOR_STORE_PATH.parent.mkdir(parents=True, exist_ok=True)


def get_llm():
    if LLM_PROVIDER == "openai":
        from langchain_openai import ChatOpenAI
        return ChatOpenAI(
            api_key=OPENAI_API_KEY,
            model=OPENAI_MODEL,
            temperature=0.7
        )
    elif LLM_PROVIDER == "anthropic":
        from langchain_anthropic import ChatAnthropic
        return ChatAnthropic(
            api_key=ANTHROPIC_API_KEY,
            model=ANTHROPIC_MODEL,
            temperature=0.7
        )
    elif LLM_PROVIDER == "ollama":
        from langchain_community.llms import Ollama
        return Ollama(
            model=OLLAMA_MODEL,
            base_url=OLLAMA_BASE_URL
        )
    else:
        raise ValueError(f"Unknown LLM provider: {LLM_PROVIDER}")


def get_embeddings():
    from langchain_community.embeddings import HuggingFaceEmbeddings
    return HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL)
