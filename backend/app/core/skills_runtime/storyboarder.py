"""Film storyboard generation skill for short drama shots."""

from typing import Any, Dict, List, Optional

from app.chains.agents.storyboard_generator import StoryboardGeneratorAgent
from app.chains.providers.minimax import get_minimax_llm


class FilmStoryboarder:
    """Skill for generating shot-by-shot storyboards from film scripts.

    This skill takes script text and extracted entities to create
    detailed storyboard with individual shots.
    """

    def __init__(self, llm=None):
        """Initialize the storyboarder.

        Args:
            llm: Optional LLM instance. If not provided, uses MiniMax.
        """
        self.llm = llm or get_minimax_llm()
        self.agent = StoryboardGeneratorAgent(llm=self.llm)

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
            Dictionary containing:
            - shots: List of shot dictionaries
        """
        result = await self.agent.generate(script_text, characters, scenes)
        return result

    def generate_sync(
        self,
        script_text: str,
        characters: List[Dict[str, str]],
        scenes: List[Dict[str, str]],
    ) -> Dict[str, Any]:
        """Synchronous version of generate."""
        result = self.agent.run_sync({
            "script_text": script_text,
            "characters": characters,
            "scenes": scenes,
        })
        return result

    @staticmethod
    def format_shot(shot: Dict[str, Any]) -> str:
        """Format a single shot for display.

        Args:
            shot: Shot dictionary

        Returns:
            Formatted string
        """
        lines = [
            f"Shot {shot.get('shot_number', '?')}: {shot.get('description', '')}",
            f"  Camera: {shot.get('camera_shot_type', 'CU')} / {shot.get('camera_angle', 'eye_level')} / {shot.get('camera_movement', 'static')}",
            f"  Duration: {shot.get('duration_seconds', 5)}s",
        ]
        if shot.get('mood'):
            lines.append(f"  Mood: {shot.get('mood')}")
        if shot.get('dialogue'):
            lines.append(f"  Dialogue: {shot.get('dialogue')}")
        return "\n".join(lines)

    @staticmethod
    def format_storyboard(shots: List[Dict[str, Any]]) -> str:
        """Format entire storyboard for display.

        Args:
            shots: List of shot dictionaries

        Returns:
            Formatted string
        """
        if not shots:
            return "No shots generated."
        return "\n\n".join([
            FilmStoryboarder.format_shot(shot)
            for shot in shots
        ])
