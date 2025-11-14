# universal_ai/interfaces/llm_interface.py
from abc import ABC, abstractmethod
from typing import Any, AsyncGenerator, Dict, List, Optional, Union

class LLMInterface(ABC):
    """
    Base interface for text generation models.
    """

    @abstractmethod
    async def generate(
        self,
        prompt: Union[str, List[Dict[str, str]]],
        stream: bool = False,
        **kwargs
    ):
        pass
