import pytest
from unittest.mock import AsyncMock, MagicMock, patch

from app.core.skills_runtime import FilmEntityExtractor


class TestFilmEntityExtractor:
    """Tests for FilmEntityExtractor."""

    def test_extract_returns_dict_with_characters_and_scenes(self, sample_script):
        """Test that extract returns expected structure."""
        import json

        mock_result = {
            "success": True,
            "characters": [
                {"name": "李明", "description": "男主角"},
                {"name": "王芳", "description": "女主角"}
            ],
            "scenes": [
                {"name": "咖啡馆内", "description": "室内场景"},
                {"name": "咖啡馆外", "description": "室外场景"}
            ],
            "raw_output": "mock raw output"
        }

        # Create mock response with .content attribute
        mock_response = MagicMock()
        mock_response.content = json.dumps(mock_result)

        # Mock the LLM's invoke method
        mock_llm = MagicMock()
        mock_llm.invoke = MagicMock(return_value=mock_response)

        extractor = FilmEntityExtractor(llm=mock_llm)
        result = extractor.extract_sync(sample_script)

        assert isinstance(result, dict)
        assert "characters" in result
        assert "scenes" in result

    def test_extract_characters_structure(self, sample_script):
        """Test that extracted characters have required fields."""
        import json

        mock_result = {
            "success": True,
            "characters": [
                {"name": "李明", "description": "男主角"}
            ],
            "scenes": [],
            "raw_output": ""
        }

        mock_response = MagicMock()
        mock_response.content = json.dumps(mock_result)

        mock_llm = MagicMock()
        mock_llm.invoke = MagicMock(return_value=mock_response)

        extractor = FilmEntityExtractor(llm=mock_llm)
        result = extractor.extract_sync(sample_script)

        assert isinstance(result["characters"], list)
        if result["characters"]:
            char = result["characters"][0]
            assert "name" in char
            assert isinstance(char["name"], str)

    def test_extract_scenes_structure(self, sample_script):
        """Test that extracted scenes have required fields."""
        import json

        mock_result = {
            "success": True,
            "characters": [],
            "scenes": [
                {"name": "咖啡馆内", "description": "室内场景"}
            ],
            "raw_output": ""
        }

        mock_response = MagicMock()
        mock_response.content = json.dumps(mock_result)

        mock_llm = MagicMock()
        mock_llm.invoke = MagicMock(return_value=mock_response)

        extractor = FilmEntityExtractor(llm=mock_llm)
        result = extractor.extract_sync(sample_script)

        assert isinstance(result["scenes"], list)
        if result["scenes"]:
            scene = result["scenes"][0]
            assert "name" in scene
            assert isinstance(scene["name"], str)

    def test_format_characters(self):
        """Test characters formatting."""
        characters = [
            {"name": "李明", "description": "男主角"},
            {"name": "王芳", "description": "女主角"}
        ]

        formatted = FilmEntityExtractor.format_characters(characters)

        assert "李明" in formatted
        assert "男主角" in formatted
        assert "王芳" in formatted

    def test_format_characters_empty(self):
        """Test formatting empty characters list."""
        formatted = FilmEntityExtractor.format_characters([])
        assert formatted == "No characters found."

    def test_format_scenes(self):
        """Test scenes formatting."""
        scenes = [
            {"name": "咖啡馆内", "description": "室内场景"}
        ]

        formatted = FilmEntityExtractor.format_scenes(scenes)

        assert "咖啡馆内" in formatted
        assert "室内场景" in formatted

    def test_format_scenes_empty(self):
        """Test formatting empty scenes list."""
        formatted = FilmEntityExtractor.format_scenes([])
        assert formatted == "No scenes found."