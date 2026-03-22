"""Film entity extraction skill for short drama scripts."""

from typing import Any, Dict, List, Optional

from app.chains.agents.entity_extractor import EntityExtractorAgent
from app.chains.providers.minimax import get_minimax_llm


class FilmEntityExtractor:
    """Skill for extracting entities (characters, scenes) from film scripts.

    This skill analyzes short drama script text and extracts structured
    information about characters and scenes.
    """

    def __init__(self, llm=None):
        """Initialize the entity extractor.

        Args:
            llm: Optional LLM instance. If not provided, uses MiniMax.
        """
        self.llm = llm or get_minimax_llm()
        self.agent = EntityExtractorAgent(llm=self.llm)

    async def extract(self, script_text: str) -> Dict[str, Any]:
        """Extract entities from script text.

        Args:
            script_text: The script content to analyze

        Returns:
            Dictionary containing:
            - characters: List of {"name": str, "description": str}
            - scenes: List of {"name": str, "description": str}
        """
        result = await self.agent.extract(script_text)
        return result

    def extract_sync(self, script_text: str) -> Dict[str, Any]:
        """Synchronous version of extract."""
        result = self.agent.run_sync({"script_text": script_text})
        return result

    @staticmethod
    def format_characters(characters: List[Dict[str, str]]) -> str:
        """Format characters list for display.

        Args:
            characters: List of character dictionaries

        Returns:
            Formatted string
        """
        if not characters:
            return "No characters found."
        return "\n".join([
            f"- {c.get('name', 'Unknown')}: {c.get('description', '')}"
            for c in characters
        ])

    @staticmethod
    def format_scenes(scenes: List[Dict[str, str]]) -> str:
        """Format scenes list for display.

        Args:
            scenes: List of scene dictionaries

        Returns:
            Formatted string
        """
        if not scenes:
            return "No scenes found."
        return "\n".join([
            f"- {s.get('name', 'Unknown')}: {s.get('description', '')}"
            for s in scenes
        ])
