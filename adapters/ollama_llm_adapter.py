from dataclasses import dataclass
import logging
import os
import aiohttp
from typing import Any, AsyncGenerator, Dict, List, Optional, Union
from interfaces.llm_interface import LLMInterface

logger = logging.getLogger(__name__)

@dataclass
class OLLAMA_CONFIG:
    MODEL_NAME: str = os.getenv("OLLAMA_MODEL_NAME")
    OLLAMA_URL: str = os.getenv("OLLAMA_URL")

class OllamaLLMAdapter(LLMInterface):
    """
    Adapter for local Ollama models running on an Ollama server.
    """

    def __init__(self):
        self.config = OLLAMA_CONFIG()
        self.base_url = self.config.OLLAMA_URL
        self.default_model = self.config.MODEL_NAME
        print("ollama called >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")

    async def generate(
        self,
        prompt: Union[str, List[Dict[str, str]]],
        model: Optional[str] = None,
        stream: bool = False,
        **kwargs
    ):
        model = model or self.default_model
        content = prompt if isinstance(prompt, str) else prompt[-1]["content"]

        try:
            async with aiohttp.ClientSession() as session:
                payload = {
                    "model": model,
                    "prompt": content,
                    "stream": stream,
                    **kwargs
                }

                async with session.post(f"{self.base_url}/api/generate", json=payload) as resp:
                    # Handle streaming
                    if stream:
                        async def streamer():
                            async for line in resp.content:
                                if not line:
                                    continue
                                decoded = line.decode("utf-8").strip()
                                if decoded:
                                    yield decoded
                        return streamer()

                    # Non-streamed full response
                    result = await resp.json()
                    return result.get("response", "").strip()

        except aiohttp.ClientError as e:
            logger.error(f"[Ollama] HTTP connection error: {e}")
            raise
        except Exception as e:
            logger.exception(f"[Ollama] Unexpected error: {e}")
            raise
