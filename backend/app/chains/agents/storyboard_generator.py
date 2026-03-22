"""Storyboard generation agent for short drama shots."""

import json
from typing import Any, Dict, List, Optional

from langchain_core.prompts import ChatPromptTemplate
from langchain_core.language_models import BaseChatModel

from app.chains.agents.base import BaseAgent
from app.chains.prompts import STORYBOARD_GENERATION_PROMPT


class StoryboardGeneratorAgent(BaseAgent):
    """Agent for generating shot-by-shot storyboards from scripts."""

    def __init__(
        self,
        llm: BaseChatModel,
        system_prompt: str = "You are an expert at creating cinematic storyboards.",
    ):
        super().__init__(llm, system_prompt)

    def get_prompt_template(self) -> ChatPromptTemplate:
        return ChatPromptTemplate.from_template(STORYBOARD_GENERATION_PROMPT)

    def parse_output(self, output: str) -> Dict[str, Any]:
        """Parse JSON output from the agent.

        Args:
            output: Raw JSON string from agent

        Returns:
            Parsed dictionary with shots
        """
        try:
            result = json.loads(output)

            # Validate structure
            shots = result.get("shots", [])
            if not isinstance(shots, list):
                shots = []

            # Validate each shot
            validated_shots = []
            for shot in shots:
                validated_shot = {
                    "shot_number": shot.get("shot_number", 0),
                    "description": shot.get("description", ""),
                    "camera_shot_type": shot.get("camera_shot_type", "CU"),
                    "camera_angle": shot.get("camera_angle", "eye_level"),
                    "camera_movement": shot.get("camera_movement", "static"),
                    "duration_seconds": shot.get("duration_seconds", 5),
                    "mood": shot.get("mood", ""),
                    "dialogue": shot.get("dialogue", ""),
                }
                validated_shots.append(validated_shot)

            return {
                "success": True,
                "shots": validated_shots,
                "raw_output": output,
            }
        except json.JSONDecodeError:
            return {
                "success": False,
                "shots": [],
                "raw_output": output,
                "error": "Failed to parse JSON output",
            }

    async def generate(
        self,
        script_text: str,
        characters: List[Dict[str, str]],
        scenes: List[Dict[str, str]],
    ) -> Dict[str, Any]:
        """Generate storyboard from script.

        Args:
            script_text: The script content
            characters: List of extracted characters
            scenes: List of extracted scenes

        Returns:
            Dictionary with generated shots
        """
        # Format characters and scenes for prompt
        characters_str = "\n".join(
            [f"- {c.get('name', 'Unknown')}: {c.get('description', '')}" for c in characters]
        )
        scenes_str = "\n".join(
            [f"- {s.get('name', 'Unknown')}: {s.get('description', '')}" for s in scenes]
        )

        return await self.run({
            "script_text": script_text,
            "characters": characters_str,
            "scenes": scenes_str,
        })
