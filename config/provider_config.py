# universal_ai/config/provider_config.py
from typing import Dict
import os
from config.settings import settings

PROVIDERS: Dict[str, Dict[str, list]] = {
    "openai": {
        "llm": ["OPENAI_API_KEY", "MODEL_NAME"],
        "embed": ["OPENAI_API_KEY", "EMBEDDING_MODEL_NAME"]
    },
    "anthropic": {
        "llm": ["ANTHROPIC_API_KEY", "MODEL_NAME"]
    },
    "groq": {
        "llm": ["GROQ_API_KEY", "MODEL_NAME"]
    },
    "azure_openai": {
        "llm": ["AZURE_OPENAI_API_KEY", "MODEL_NAME", "AZURE_ENDPOINT", "AZURE_DEPLOYMENT_NAME"]
    }
}


def load_llm_config(provider: str):
    """
    Enforce that only the chosen provider has its keys loaded.
    Nullify all unrelated provider keys.
    """
    if provider not in PROVIDERS:
        raise ValueError(f"Unknown LLM provider '{provider}'")

    for prov, keys in PROVIDERS.items():
        for key in keys.get("llm", []) + keys.get("embed", []):
            attr = key.lower()
            if prov != provider:
                if os.getenv(key):
                    if hasattr(settings, attr):
                        setattr(settings, attr, None)

            else:
                if os.getenv(attr):
                    setattr(settings, attr,os.getenv(attr))
                else:
                    raise ValueError(f"Missing required key '{key}' for provider '{provider}'")
