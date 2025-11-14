from dataclasses import dataclass
import logging
import os
from typing import Any, AsyncGenerator, Dict, List, Optional, Union
from groq import AsyncGroq
from groq import GroqError
from interfaces.llm_interface import LLMInterface

logger = logging.getLogger(__name__)

@dataclass
class GROQ_CONFIG:
    MODEL_NAME: str = os.getenv("GROQ_MODEL_NAME")
    GROQ_API_KEY: str = os.getenv("GROQ_API_KEY")

class GroqLLMAdapter(LLMInterface):
    def __init__(self):
        self.config = GROQ_CONFIG()
        self.client = AsyncGroq(api_key=self.config.GROQ_API_KEY, timeout=30)
        self.default_model = self.config.MODEL_NAME
        print("groq called >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")

    async def generate(
        self,
        prompt: Union[str, List[Dict[str, str]]],
        model: Optional[str] = None,
        stream: bool = False,
        **kwargs
    ) -> Union[str, AsyncGenerator[str, None]]:
        model = model or self.default_model
        messages = [{"role": "user", "content": prompt}] if isinstance(prompt, str) else prompt

        try:
            if stream:
                async def streamer():
                    async with self.client.chat.completions.stream(
                        model=model,
                        messages=messages,
                        **kwargs
                    ) as stream_resp:
                        async for chunk in stream_resp:
                            if chunk.choices and chunk.choices[0].delta:
                                content = chunk.choices[0].delta.content
                                if content:
                                    yield content
                return streamer() 
            else:
                resp = await self.client.chat.completions.create(model=model, messages=messages, **kwargs)
                return resp.choices[0].message.content.strip()
        except GroqError as e:
            logger.error(f"[Groq] API error: {e}")
            raise
        except Exception as e:
            logger.exception(f"[Groq] Unexpected error: {e}")
            raise
