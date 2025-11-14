# universal_ai/adapters/openai_llm_adapter.py
from dataclasses import dataclass
import logging
import os
from typing import Any, AsyncGenerator, Dict, List, Optional, Union
from openai import AsyncOpenAI
from openai import OpenAIError
from interfaces.llm_interface import LLMInterface

logger = logging.getLogger(__name__)

@dataclass
class OPENAI_CONFIG:
    MODEL_NAME: str = os.getenv("MODEL_NAME")
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY")

class OpenAILLMAdapter(LLMInterface):
    def __init__(self):
        self.config = OPENAI_CONFIG()
        self.client = AsyncOpenAI(api_key=self.config.OPENAI_API_KEY, timeout=30)
        self.default_model = self.config.MODEL_NAME
        print("openai called >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")

    async def generate(
        self,
        prompt: Union[str, List[Dict[str, str]]],
        model: Optional[str] = None,
        stream: bool = False,
        **kwargs
    ):
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
        except OpenAIError as e:
            logger.error(f"[OpenAI] API error: {e}")
            raise
        except Exception as e:
            logger.exception(f"[OpenAI] Unexpected error: {e}")
            raise
