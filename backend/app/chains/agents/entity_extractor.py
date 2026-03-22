"""Entity extraction agent for short drama scripts."""

import json
from typing import Any, Dict, List

from langchain_core.prompts import ChatPromptTemplate
from langchain_core.language_models import BaseChatModel

from app.chains.agents.base import BaseAgent
from app.chains.prompts import ENTITY_EXTRACTION_PROMPT


class EntityExtractorAgent(BaseAgent):
    """Agent for extracting characters and scenes from script text."""

    def __init__(
        self,
        llm: BaseChatModel,
        system_prompt: str = "You are an expert at analyzing short drama scripts.",
    ):
        super().__init__(llm, system_prompt)

    def get_prompt_template(self) -> ChatPromptTemplate:
        return ChatPromptTemplate.from_template(ENTITY_EXTRACTION_PROMPT)

    def parse_output(self, output: str) -> Dict[str, Any]:
        """Parse JSON output from the agent.

        Args:
            output: Raw JSON string from agent

        Returns:
            Parsed dictionary with characters and scenes
        """
        try:
            # Try to parse as JSON
            result = json.loads(output)

            # Validate structure
            if not isinstance(result.get("characters", []), list):
                result["characters"] = []
            if not isinstance(result.get("scenes", []), list):
                result["scenes"] = []

            return {
                "success": True,
                "characters": result.get("characters", []),
                "scenes": result.get("scenes", []),
                "raw_output": output,
            }
        except json.JSONDecodeError:
            # If JSON parsing fails, try to extract structured data manually
            return {
                "success": False,
                "characters": self._extract_characters_fallback(output),
                "scenes": self._extract_scenes_fallback(output),
                "raw_output": output,
                "error": "Failed to parse JSON output",
            }

    def _extract_characters_fallback(self, text: str) -> List[Dict[str, str]]:
        """Fallback extraction for characters if JSON parsing fails."""
        characters = []
        lines = text.split("\n")
        for line in lines:
            if "角色" in line or "人物" in line or "character" in line.lower():
                # Try to extract name from line
                name = line.split("：")[-1].split(":")[-1].strip()
                if name:
                    characters.append({"name": name, "description": ""})
        return characters

    def _extract_scenes_fallback(self, text: str) -> List[Dict[str, str]]:
        """Fallback extraction for scenes if JSON parsing fails."""
        scenes = []
        lines = text.split("\n")
        for line in lines:
            if "场景" in line or "地点" in line or "scene" in line.lower():
                name = line.split("：")[-1].split(":")[-1].strip()
                if name:
                    scenes.append({"name": name, "description": ""})
        return scenes

    async def extract(self, script_text: str) -> Dict[str, Any]:
        """Extract entities from script text.

        Args:
            script_text: The script content to analyze

        Returns:
            Dictionary with extracted characters and scenes
        """
        return await self.run({"script_text": script_text})
