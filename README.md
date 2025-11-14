# 🔌 Universal LLM Adapters

> A flexible, provider-agnostic abstraction layer for seamless integration with multiple LLM providers

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

Switch between OpenAI, Azure OpenAI, Anthropic, Groq, and Ollama with a single line of configuration. No code changes required.

## ✨ Why Use This?

- **🔄 Provider Agnostic**: Write once, run anywhere - switch providers by changing one environment variable
- **🎯 Unified Interface**: Same API across all providers - no need to learn multiple SDKs
- **⚡ Streaming Ready**: Built-in streaming support for real-time responses
- **🔒 Type Safe**: Fully typed with Python type hints for better IDE support
- **🐳 Production Ready**: Async support, error handling, and timeout configuration
- **💰 Cost Optimized**: Easy A/B testing and fallback strategies between providers

## 🚀 Quick Start

### Installation

```bash
pip install openai anthropic groq aiohttp python-dotenv pydantic-settings
```

### Setup

1. **Clone or copy the adapter structure:**
```
your_project/
├── adapters/
│   ├── openai_llm_adapter.py
│   ├── azure_openai_llm_adapter.py
│   ├── anthropic_llm_adapter.py
│   ├── groq_llm_adapter.py
│   └── ollama_llm_adapter.py
├── config/
│   ├── settings.py
│   ├── provider_config.py
│   └── factory.py
├── interfaces/
│   └── llm_interface.py
└── .env
```

2. **Configure your `.env` file:**
```bash
# Choose your provider (openai, azure_openai, anthropic, groq, ollama)
LLM_PROVIDER=openai

# Add your API key
OPENAI_API_KEY=sk-...
MODEL_NAME=gpt-4
```

3. **Start using it:**
```python
from config.factory import load_llm_adapter

llm = load_llm_adapter()
response = await llm.generate("Explain quantum computing simply")
print(response)
```

That's it! Change `LLM_PROVIDER` in `.env` to switch providers instantly.

## 📖 Usage Examples

### Basic Text Generation

```python
from config.factory import load_llm_adapter

async def main():
    llm = load_llm_adapter()
    
    response = await llm.generate(
        prompt="Write a haiku about coding",
        max_tokens=100,
        temperature=0.8
    )
    print(response)
```

### Streaming Responses

```python
async def stream_example():
    llm = load_llm_adapter()
    
    stream = await llm.generate(
        prompt="Tell me a story about AI",
        stream=True,
        max_tokens=500
    )
    
    async for chunk in stream:
        print(chunk, end="", flush=True)
```

### Chat Conversations

```python
async def chat_example():
    llm = load_llm_adapter()
    
    messages = [
        {"role": "system", "content": "You are a helpful coding assistant."},
        {"role": "user", "content": "How do I reverse a string in Python?"}
    ]
    
    response = await llm.generate(prompt=messages)
    print(response)
```

### Multi-Provider Strategy

```python
async def multi_provider():
    # Use fast model for simple tasks
    fast_llm = load_llm_adapter("groq")
    quick_answer = await fast_llm.generate("What is 2+2?")
    
    # Use smart model for complex reasoning
    smart_llm = load_llm_adapter("openai")
    detailed = await smart_llm.generate("Explain quantum entanglement")
    
    # Use local model for privacy-sensitive data
    local_llm = load_llm_adapter("ollama")
    private = await local_llm.generate("Analyze this confidential report...")
```

## ⚙️ Configuration

### Environment Variables

Create a `.env` file with your provider settings:

```bash
# === Core Configuration ===
LLM_PROVIDER=openai

# === OpenAI ===
OPENAI_API_KEY=sk-proj-...
MODEL_NAME=gpt-4

# === Azure OpenAI ===
AZURE_OPENAI_API_KEY=your-key
AZURE_OPENAI_ENDPOINT=https://your-resource.openai.azure.com/
AZURE_OPENAI_API_VERSION=2024-02-15-preview
AZURE_DEPLOYMENT_NAME=gpt-4

# === Anthropic ===
ANTHROPIC_API_KEY=sk-ant-...
ANTHROPIC_MODEL_NAME=claude-3-5-sonnet-20241022

# === Groq ===
GROQ_API_KEY=gsk_...
GROQ_MODEL_NAME=llama-3.1-70b-versatile

# === Ollama (Local) ===
OLLAMA_URL=http://localhost:11434
OLLAMA_MODEL_NAME=llama2
```

### Runtime Provider Selection

```python
# Use environment default
llm = load_llm_adapter()

# Override at runtime
openai_llm = load_llm_adapter("openai")
claude_llm = load_llm_adapter("anthropic")
```

## 🎯 Real-World Use Cases

### 1. **Development → Production Pipeline**
```python
# .env.development
LLM_PROVIDER=ollama  # Free local testing

# .env.production  
LLM_PROVIDER=azure_openai  # Enterprise deployment

# Code stays identical!
llm = load_llm_adapter()
```

### 2. **Cost Optimization**
```python
def get_provider_for_task(complexity: str):
    """Route to cheapest provider that meets requirements"""
    if complexity == "simple":
        return load_llm_adapter("groq")  # Fast & affordable
    elif complexity == "medium":
        return load_llm_adapter("openai")  # Balanced
    else:
        return load_llm_adapter("anthropic")  # Maximum quality
```

### 3. **Automatic Fallback**
```python
async def generate_with_fallback(prompt: str):
    """Try multiple providers if one fails"""
    for provider in ["openai", "anthropic", "groq"]:
        try:
            llm = load_llm_adapter(provider)
            return await llm.generate(prompt)
        except Exception as e:
            logging.warning(f"{provider} failed: {e}")
            continue
    raise Exception("All providers unavailable")
```

### 4. **A/B Testing**
```python
async def compare_models(prompt: str):
    """Test same prompt across providers"""
    results = {}
    for provider in ["openai", "anthropic", "groq"]:
        llm = load_llm_adapter(provider)
        results[provider] = await llm.generate(prompt)
    return results
```

## 🏗️ Architecture

```
┌─────────────────────────────────────────┐
│         Your Application Code           │
└──────────────┬──────────────────────────┘
               │
               ▼
┌─────────────────────────────────────────┐
│      LLM Interface (Abstract)           │
│  - generate(prompt, stream, **kwargs)   │
└──────────────┬──────────────────────────┘
               │
       ┌───────┴───────┬─────────┬──────────┐
       ▼               ▼         ▼          ▼
   ┌────────┐    ┌─────────┐ ┌──────┐  ┌────────┐
   │ OpenAI │    │Anthropic│ │ Groq │  │ Ollama │
   └────────┘    └─────────┘ └──────┘  └────────┘
```

**Key Components:**
- **Interface Layer**: Abstract base defining the contract
- **Adapter Layer**: Provider-specific implementations
- **Config Layer**: Environment validation & provider factory
- **Factory Pattern**: Returns correct adapter based on config

## 📊 Provider Comparison

| Provider | Streaming | Chat Format | Local | Best For |
|----------|:---------:|:-----------:|:-----:|----------|
| **OpenAI** | ✅ | ✅ | ❌ | General purpose, GPT-4 |
| **Azure OpenAI** | ✅ | ✅ | ❌ | Enterprise, compliance |
| **Anthropic** | ✅ | ✅ | ❌ | Long context, Claude |
| **Groq** | ✅ | ✅ | ❌ | Speed, cost-effective |
| **Ollama** | ✅ | ❌ | ✅ | Privacy, offline use |

## 🛡️ Error Handling

```python
from openai import OpenAIError
from anthropic import APIError as AnthropicError

try:
    response = await llm.generate(prompt)
except OpenAIError as e:
    print(f"OpenAI error: {e}")
except AnthropicError as e:
    print(f"Anthropic error: {e}")
except Exception as e:
    print(f"Unexpected error: {e}")
```

## 🤝 Contributing

Contributions are welcome! To add a new provider:

1. **Create adapter** in `adapters/` implementing `LLMInterface`
2. **Add config validation** in `config/provider_config.py`
3. **Register in factory** in `config/factory.py`
4. **Update documentation** with provider details

## 📋 Requirements

- Python 3.8+
- openai
- anthropic
- groq
- aiohttp
- python-dotenv
- pydantic-settings

## 🐛 Troubleshooting

**Provider not loading?**
```python
from config.provider_config import load_llm_config
from config.settings import settings

# Validate configuration
load_llm_config(settings.llm_provider)
```

**Streaming not working?**
- Ensure `stream=True` parameter is passed
- Verify provider supports streaming (check table above)
- Check network connectivity for cloud providers

**Import errors?**
- Verify all dependencies are installed: `pip install -r requirements.txt`
- Check Python path includes the adapter directory

### Acknowledgments

Built to solve the common pain point of provider lock-in in LLM applications. Inspired by the need for flexibility in production GenAI systems.
