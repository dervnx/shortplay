import pytest
from unittest.mock import MagicMock

from app.core.skills_runtime import FilmStoryboarder


class TestFilmStoryboarder:
    """Tests for FilmStoryboarder."""

    def test_generate_returns_dict_with_shots(self):
        """Test that generate returns expected structure."""
        mock_result = {
            "success": True,
            "shots": [
                {
                    "shot_number": 1,
                    "description": "李明走进咖啡馆",
                    "camera_shot_type": "CU",
                    "camera_angle": "eye_level",
                    "camera_movement": "static",
                    "duration_seconds": 5,
                    "mood": "neutral",
                    "dialogue": "李明：（惊讶）王芳？好久不见！"
                }
            ],
            "raw_output": "mock"
        }

        mock_llm = MagicMock()
        storyboarder = FilmStoryboarder(llm=mock_llm)
        storyboarder.agent.run_sync = MagicMock(return_value=mock_result)

        result = storyboarder.generate_sync("script", [], [])

        assert isinstance(result, dict)
        assert "shots" in result

    def test_generate_shots_structure(self):
        """Test that generated shots have required fields."""
        mock_result = {
            "success": True,
            "shots": [
                {
                    "shot_number": 1,
                    "description": "测试镜头",
                    "camera_shot_type": "CU",
                    "duration_seconds": 5
                }
            ],
            "raw_output": "mock"
        }

        mock_llm = MagicMock()
        storyboarder = FilmStoryboarder(llm=mock_llm)
        storyboarder.agent.run_sync = MagicMock(return_value=mock_result)

        result = storyboarder.generate_sync("script", [], [])

        assert isinstance(result["shots"], list)
        if result["shots"]:
            shot = result["shots"][0]
            assert "shot_number" in shot
            assert "description" in shot

    def test_format_shot(self):
        """Test shot formatting."""
        shot = {
            "shot_number": 1,
            "description": "测试镜头",
            "camera_shot_type": "CU",
            "camera_angle": "eye_level",
            "camera_movement": "static",
            "duration_seconds": 5,
            "mood": "happy",
            "dialogue": "你好"
        }

        formatted = FilmStoryboarder.format_shot(shot)

        assert "Shot 1" in formatted
        assert "测试镜头" in formatted
        assert "CU" in formatted
        assert "5s" in formatted
        assert "happy" in formatted
        assert "你好" in formatted

    def test_format_storyboard(self):
        """Test storyboard formatting."""
        shots = [
            {"shot_number": 1, "description": "镜头1", "camera_shot_type": "CU", "duration_seconds": 5},
            {"shot_number": 2, "description": "镜头2", "camera_shot_type": "MS", "duration_seconds": 3}
        ]

        formatted = FilmStoryboarder.format_storyboard(shots)

        assert "Shot 1" in formatted
        assert "镜头1" in formatted
        assert "Shot 2" in formatted
        assert "镜头2" in formatted

    def test_format_storyboard_empty(self):
        """Test formatting empty storyboard."""
        formatted = FilmStoryboarder.format_storyboard([])
        assert formatted == "No shots generated."
