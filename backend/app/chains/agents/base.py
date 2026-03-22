"""Base agent class for LangChain agents."""

from abc import ABC, abstractmethod
from typing import Any, Dict, Optional

from langchain_core.language_models import BaseChatModel
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage
from langchain_core.prompts import ChatPromptTemplate


class BaseAgent(ABC):
    """Abstract base class for all agents."""

    def __init__(
        self,
        llm: BaseChatModel,
        system_prompt: Optional[str] = None,
    ):
        """Initialize the agent.

        Args:
            llm: The language model to use
            system_prompt: Optional system prompt override
        """
        self.llm = llm
        self.system_prompt = system_prompt

    @abstractmethod
    def get_prompt_template(self) -> ChatPromptTemplate:
        """Return the prompt template for this agent."""
        pass

    @abstractmethod
    def parse_output(self, output: str) -> Dict[str, Any]:
        """Parse the agent's output into a structured format."""
        pass

    async def run(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Run the agent with given input.

        Args:
            input_data: Dictionary containing input parameters

        Returns:
            Dictionary containing the agent's response
        """
        prompt = self.get_prompt_template()
        messages = prompt.format_messages(**input_data)

        response = await self.llm.ainvoke(messages)
        return self.parse_output(response.content)

    def run_sync(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Synchronous version of run."""
        prompt = self.get_prompt_template()
        messages = prompt.format_messages(**input_data)
        response = self.llm.invoke(messages)
        return self.parse_output(response.content)
