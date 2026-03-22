"""Prompt templates for LangChain agents."""

# Entity Extraction Prompt
ENTITY_EXTRACTION_PROMPT = """You are an expert at analyzing short drama scripts and extracting structured information.

Your task is to analyze the following script text and extract:
1. **Characters**: All characters mentioned in the script, with their names and brief descriptions
2. **Scenes**: All locations/settings where the story takes place

## Rules:
- Extract characters with their full names and distinguishing characteristics
- Identify scenes as distinct locations (e.g., "咖啡厅", "办公室", "街道")
- Provide character names in Chinese or original form
- Scene names should be descriptive and concise

## Output Format:
Return a JSON object with:
- "characters": List of character objects with "name" and "description"
- "scenes": List of scene objects with "name" and "description"

## Script Text:
{script_text}

## Extraction Result:
"""

# Storyboard Generation Prompt
STORYBOARD_GENERATION_PROMPT = """You are an expert at creating shot-by-shot storyboards for short dramas.

Your task is to analyze the script and create a detailed storyboard with individual shots.

## Rules:
- Break down the story into clear, concise shots
- Each shot should describe: camera angle, movement, and action
- Include dialogue/action description for each shot
- Maintain narrative continuity across shots
- Typical short drama: 20-40 shots per chapter

## Output Format:
Return a JSON object with:
- "shots": List of shot objects containing:
  - "shot_number": Sequential number
  - "description": What happens in this shot
  - "camera_shot_type": ECU/CU/MCU/MS/MLS/LS/ELS
  - "camera_angle": eye_level/high_angle/low_angle/bird_eye/dutch/over_shoulder
  - "camera_movement": static/pan/tilt/dolly_in/dolly_out/track/crane/handheld/steadicam/zoom_in/zoom_out
  - "duration_seconds": Estimated duration (2-10 seconds typical)
  - "mood": mood/atmosphere description
  - "dialogue": Key dialogue if any

## Script Text:
{script_text}

## Characters (for reference):
{characters}

## Scenes (for reference):
{scenes}

## Storyboard Result:
"""

# Shot Frame Prompt Generation
SHOT_FRAME_PROMPT = """You are an expert at creating detailed image generation prompts for short drama shots.

Your task is to generate a detailed prompt for creating the key frame image of a shot.

## Rules:
- Describe the scene vividly with specific details
- Include character appearances and positions
- Specify lighting, atmosphere, and mood
- Use cinematic composition terminology
- Keep prompts under 500 characters

## Shot Description:
{shot_description}

## Character Details:
{character_details}

## Scene Details:
{scene_details}

## Output:
Return a JSON object with:
- "prompt": The image generation prompt
- "negative_prompt": Things to avoid in the image

## Image Prompt Result:
"""

# Consistency Check Prompt
CONSISTENCY_CHECK_PROMPT = """You are an expert at checking consistency in short drama scripts.

Your task is to analyze the script and identify:
1. Character appearance inconsistencies
2. Scene/location contradictions
3. Timeline issues
4. Logical errors

## Script Text:
{script_text}

## Characters:
{characters}

Return a JSON object with:
- "issues": List of consistency issues found
- "warnings": List of potential problems
- "suggestions": Recommended fixes
"""
