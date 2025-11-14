from dataclasses import dataclass
import logging
import os
from typing import Any, AsyncGenerator, Dict, List, Optional, Union
from anthropic import AsyncAnthropic, APIError as AnthropicError
from interfaces.llm_interface import LLMInterface

logger = logging.getLogger(__name__)

@dataclass
class ANTHROPIC_CONFIG:
    MODEL_NAME: str = os.getenv("ANTHROPIC_MODEL_NAME")
    ANTHROPIC_API_KEY: str = os.getenv("ANTHROPIC_API_KEY")

class AnthropicLLMAdapter(LLMInterface):
    def __init__(self):
        self.config = ANTHROPIC_CONFIG()
        self.client = AsyncAnthropic(api_key=self.config.ANTHROPIC_API_KEY, timeout=30)
        self.default_model = self.config.MODEL_NAME
        

    async def generate(
        self,
        prompt: Union[str, List[Dict[str, str]]],
        model: Optional[str] = None,
        stream: bool = False,
        **kwargs
    ):
        model = model or self.default_model
        # Anthropic expects a list of messages, but for simple cases we just pass user text
        content = prompt if isinstance(prompt, str) else prompt[-1]["content"]

        try:
            if stream:
                # ✅ define nested async generator so outer function can return normally
                async def streamer():
                    async with self.client.messages.stream(
                        model=model,
                        messages=[{"role": "user", "content": content}],
                        **kwargs
                    ) as stream_resp:
                        async for event in stream_resp:
                            # Each stream event may contain a token delta
                            if event.type == "content_block_delta":
                                delta = event.delta
                                if delta:
                                    yield delta
                return streamer()

            else:
                # Non-streamed inference
                resp = await self.client.messages.create(
                    model=model,
                    messages=[{"role": "user", "content": content}],
                    **kwargs
                )
                # Claude responses are structured as a list of text blocks
                if resp.content and len(resp.content) > 0:
                    return resp.content[0].text.strip()
                return ""

        except AnthropicError as e:
            logger.error(f"[Anthropic] API error: {e}")
            raise
        except Exception as e:
            logger.exception(f"[Anthropic] Unexpected error: {e}")
            raise
