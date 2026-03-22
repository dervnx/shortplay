"""MiniMax LLM provider integration."""

from typing import Optional, Dict, Any
import os

from langchain_openai import ChatOpenAI
from langchain_core.language_models import BaseChatModel

from app.core.config import settings


class MiniMaxLLM(ChatOpenAI):
    """MiniMax chat model compatible with OpenAI API."""

    def __init__(
        self,
        model: str = "MiniMax-Text-01",
        api_key: Optional[str] = None,
        api_base: str = "https://api.minimax.chat/v1",
        **kwargs,
    ):
        api_key = api_key or os.getenv("MINIMAX_API_KEY", "")
        super().__init__(
            model=model,
            openai_api_key=api_key,
            openai_api_base=api_base,
            **kwargs,
        )


class MiniMaxProvider:
    """Provider for MiniMax LLM models."""

    _instance: Optional["MiniMaxProvider"] = None

    def __init__(self):
        self.api_key = settings.MINIMAX_API_KEY if hasattr(settings, "MINIMAX_API_KEY") else os.getenv("MINIMAX_API_KEY", "")
        self.api_base = settings.MINIMAX_API_BASE if hasattr(settings, "MINIMAX_API_BASE") else "https://api.minimax.chat/v1"
        self.model_name = settings.MINIMAX_MODEL if hasattr(settings, "MINIMAX_MODEL") else "MiniMax-Text-01"

    @classmethod
    def get_instance(cls) -> "MiniMaxProvider":
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    def get_llm(self, model: Optional[str] = None, **kwargs) -> BaseChatModel:
        """Get configured LLM instance.

        Args:
            model: Optional model name override
            **kwargs: Additional arguments for ChatOpenAI

        Returns:
            Configured ChatOpenAI instance
        """
        return MiniMaxLLM(
            model=model or self.model_name,
            api_key=self.api_key,
            api_base=self.api_base,
            **kwargs,
        )

    def get_text_llm(self, **kwargs) -> BaseChatModel:
        """Get LLM for text generation tasks."""
        return self.get_llm(**kwargs)

    def get_vision_llm(self, **kwargs) -> BaseChatModel:
        """Get LLM for vision tasks (if supported)."""
        # MiniMax vision support may vary
        return self.get_llm(**kwargs)


# Global provider instance
minimax_provider = MiniMaxProvider.get_instance()


def get_minimax_llm(**kwargs) -> BaseChatModel:
    """Convenience function to get MiniMax LLM."""
    return minimax_provider.get_llm(**kwargs)
