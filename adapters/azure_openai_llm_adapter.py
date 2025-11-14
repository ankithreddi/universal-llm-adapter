from dataclasses import dataclass
import logging
import os
from typing import Any, AsyncGenerator, Dict, List, Optional, Union
from openai import AsyncAzureOpenAI
from openai import OpenAIError
from interfaces.llm_interface import LLMInterface
from dotenv import load_dotenv
# load_dotenv()

load_dotenv(override=True)
logger = logging.getLogger(__name__)

@dataclass
class AZURE_OPENAI_CONFIG:
    AZURE_API_KEY: str = os.getenv("AZURE_OPENAI_API_KEY")
    AZURE_API_BASE: str = os.getenv("AZURE_OPENAI_ENDPOINT")  # e.g. "https://your-resource-name.openai.azure.com/"
    AZURE_API_VERSION: str = os.getenv("AZURE_OPENAI_API_VERSION")
    AZURE_DEPLOYMENT_NAME: str = os.getenv("AZURE_DEPLOYMENT_NAME")  # Model deployment name

class AzureOpenAILLMAdapter(LLMInterface):
    """
    Adapter for Azure OpenAI Service.
    Compatible with your LLMInterface and usage pattern.
    """

    def __init__(self):
        self.config = AZURE_OPENAI_CONFIG()
        print(self.config)
        if not all([self.config.AZURE_API_KEY, self.config.AZURE_API_BASE, self.config.AZURE_DEPLOYMENT_NAME]):
            raise ValueError("Missing required Azure OpenAI environment variables.")

        self.client = AsyncAzureOpenAI(
            api_key=self.config.AZURE_API_KEY,
            azure_endpoint=self.config.AZURE_API_BASE,
            api_version=self.config.AZURE_API_VERSION,
            timeout=30,
        )
        self.default_deployment = self.config.AZURE_DEPLOYMENT_NAME
        print("azure openai called >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")

    async def generate(
        self,
        prompt: Union[str, List[Dict[str, str]]],
        model: Optional[str] = None,
        stream: bool = False,
        **kwargs
    ):
        """
        Generate text response from Azure OpenAI chat model.
        """
        deployment_name = model or self.default_deployment
        messages = [{"role": "user", "content": prompt}] if isinstance(prompt, str) else prompt

        try:
            if stream:
                async def streamer():
                    async with self.client.chat.completions.stream(
                        model=deployment_name,  # deployment_name acts like model
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
                resp = await self.client.chat.completions.create(
                    model=deployment_name,
                    messages=messages,
                    **kwargs
                )
                return resp.choices[0].message.content.strip()

        except OpenAIError as e:
            logger.error(f"[Azure OpenAI] API error: {e}")
            raise
        except Exception as e:
            logger.exception(f"[Azure OpenAI] Unexpected error: {e}")
            raise
