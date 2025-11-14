from adapters.openai_llm_adapter import OpenAILLMAdapter
from adapters.groq_llm_adapter import GroqLLMAdapter
from adapters.anthropic_llm_adapter import AnthropicLLMAdapter
from adapters.ollama_llm_adapter import OllamaLLMAdapter
from adapters.azure_openai_llm_adapter import AzureOpenAILLMAdapter
from config.settings import settings

def load_llm_adapter(provider: str=None):
    if not provider:
        provider = settings.llm_provider

    print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>provider    ",provider) 
    input(">>>")
    provider = provider.lower()
    if provider == "openai":
        return OpenAILLMAdapter()
    elif provider == "azure_openai":
        return AzureOpenAILLMAdapter()
    elif provider == "groq":
        return GroqLLMAdapter()
    elif provider == "anthropic":
        return AnthropicLLMAdapter()
    elif provider == "ollama":
        return OllamaLLMAdapter()
    else:
        raise ValueError(f"Unsupported LLM provider: {provider}")
