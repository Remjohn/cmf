"""
CMF OpenRouter Image Generator
Generates images using OpenRouter API with bytedance-seed/seedream-4.5

Usage:
    python cmf_image_generator.py --project "06_50-12 Monia" --type storyboard
    python cmf_image_generator.py --project "06_50-12 Monia" --type gmg
    python cmf_image_generator.py --project "06_50-12 Monia" --type cac
    python cmf_image_generator.py --project "06_50-12 Monia" --type all
"""

import os
import json
import base64
import argparse
import re
from pathlib import Path
from datetime import datetime
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configuration
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
MODEL = "bytedance-seed/seedream-4.5"
BASE_PATH = Path(r"d:\Work\The Conscious Movie Factory December\🇫🇷 Conscious Movie Factory\inputs")
OUTPUT_BASE = Path(r"d:\Work\The Conscious Movie Factory December\🇫🇷 Conscious Movie Factory\outputs")

# Initialize OpenRouter client
client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=OPENROUTER_API_KEY,
)


def generate_image(prompt: str, output_path: Path) -> bool:
    """
    Generate an image using OpenRouter's Seedream 4.5 model.
    
    Args:
        prompt: The text prompt for image generation
        output_path: Where to save the generated image
        
    Returns:
        True if successful, False otherwise
    """
    try:
        print(f"  → Generating: {output_path.name}...")
        
        response = client.chat.completions.create(
            extra_headers={
                "HTTP-Referer": "https://consciousmovie.factory",
                "X-Title": "Conscious Movie Factory",
            },
            model=MODEL,
            modalities=["image", "text"],
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )
        
        # Extract the image from response
        message = response.choices[0].message
        
        # The image is returned as base64 data URL
        if hasattr(message, 'content') and message.content:
            # Parse the base64 image data
            for part in message.content if isinstance(message.content, list) else [message.content]:
                if isinstance(part, dict) and part.get('type') == 'image':
                    image_data = part.get('image', {}).get('data', '')
                    if image_data:
                        # Decode and save
                        image_bytes = base64.b64decode(image_data)
                        output_path.parent.mkdir(parents=True, exist_ok=True)
                        with open(output_path, 'wb') as f:
                            f.write(image_bytes)
                        print(f"  ✓ Saved: {output_path}")
                        return True
                elif isinstance(part, str) and part.startswith('data:image'):
                    # Handle data URL format
                    header, data = part.split(',', 1)
                    image_bytes = base64.b64decode(data)
                    output_path.parent.mkdir(parents=True, exist_ok=True)
                    with open(output_path, 'wb') as f:
                        f.write(image_bytes)
                    print(f"  ✓ Saved: {output_path}")
                    return True
        
        print(f"  ✗ No image in response")
        return False
        
    except Exception as e:
        print(f"  ✗ Error: {e}")
        return False


def parse_storyboard_prompts(project_path: Path) -> list:
    """Parse STORYBOARD_VISUAL_POETRY.md to extract prompts per scene."""
    storyboard_file = project_path / f"{project_path.name}_STORYBOARD_VISUAL_POETRY.md"
    
    if not storyboard_file.exists():
        print(f"  ✗ Storyboard file not found: {storyboard_file}")
        return []
    
    prompts = []
    content = storyboard_file.read_text(encoding='utf-8')
    
    # Split by scene markers (W1, W2, W3, W4, W5 or SCENE)
    scene_pattern = r'(?:##\s*(?:W\d|SCENE\s*\d|Scene\s*\d).*?)(?=##\s*(?:W\d|SCENE\s*\d|Scene\s*\d)|$)'
    scenes = re.findall(scene_pattern, content, re.DOTALL | re.IGNORECASE)
    
    if not scenes:
        # Try to split by horizontal rules or double newlines
        scenes = content.split('---')
    
    for i, scene_content in enumerate(scenes, 1):
        if len(scene_content.strip()) > 50:  # Minimum prompt length
            prompts.append({
                'scene_id': f'W{i}',
                'type': 'STORYBOARD',
                'prompt': scene_content.strip(),
                'output_name': f'SC{i:02d}_STORYBOARD_T2I.png'
            })
    
    return prompts


def parse_gmg_prompts(project_path: Path) -> list:
    """Parse GMG_PROMPTS.md to extract prompts per scene (LAST and FIRST frames)."""
    gmg_file = project_path / f"{project_path.name}_GMG_PROMPTS.md"
    
    if not gmg_file.exists():
        print(f"  ✗ GMG file not found: {gmg_file}")
        return []
    
    prompts = []
    content = gmg_file.read_text(encoding='utf-8')
    
    # Look for LAST FRAME and FIRST FRAME sections
    scene_pattern = r'##\s*(?:GMG\s*)?SCENE[:\s]*(\w+)'
    scenes = re.split(scene_pattern, content, flags=re.IGNORECASE)
    
    # Parse in pairs (scene_id, content)
    for i in range(1, len(scenes), 2):
        if i + 1 < len(scenes):
            scene_id = scenes[i].strip()
            scene_content = scenes[i + 1]
            
            # Extract LAST FRAME prompt
            last_match = re.search(r'(?:LAST\s*FRAME|T2I\s*PROMPT)[:\s]*(.+?)(?=FIRST\s*FRAME|I2I|MOTION|##|$)', 
                                   scene_content, re.DOTALL | re.IGNORECASE)
            if last_match:
                prompts.append({
                    'scene_id': scene_id,
                    'type': 'GMG_LAST',
                    'prompt': last_match.group(1).strip(),
                    'output_name': f'SC{len(prompts)//2 + 1:02d}_GMG_01_LAST.png'
                })
            
            # Extract FIRST FRAME prompt (for I2I - we'll use text-to-image for now)
            first_match = re.search(r'(?:FIRST\s*FRAME|I2I\s*PROMPT)[:\s]*(.+?)(?=MOTION|##|$)', 
                                    scene_content, re.DOTALL | re.IGNORECASE)
            if first_match:
                prompts.append({
                    'scene_id': scene_id,
                    'type': 'GMG_FIRST',
                    'prompt': first_match.group(1).strip(),
                    'output_name': f'SC{len(prompts)//2 + 1:02d}_GMG_02_FIRST.png'
                })
    
    return prompts


def parse_cac_prompts(project_path: Path) -> list:
    """Parse CAC_PROMPTS.md to extract prompts per scene."""
    cac_file = project_path / f"{project_path.name}_CAC_PROMPTS.md"
    
    if not cac_file.exists():
        print(f"  ✗ CAC file not found: {cac_file}")
        return []
    
    prompts = []
    content = cac_file.read_text(encoding='utf-8')
    
    # Look for EL SHADDAI PROMPT sections
    scene_pattern = r'##\s*(?:CAC\s*)?SCENE[:\s]*(\w+)'
    scenes = re.split(scene_pattern, content, flags=re.IGNORECASE)
    
    for i in range(1, len(scenes), 2):
        if i + 1 < len(scenes):
            scene_id = scenes[i].strip()
            scene_content = scenes[i + 1]
            
            # Extract the main T2I prompt (El Shaddai)
            prompt_match = re.search(r'(?:EL\s*SHADDAI|T2I\s*PROMPT)[:\s]*(.+?)(?=MOTION\s*SPEC|##|$)', 
                                     scene_content, re.DOTALL | re.IGNORECASE)
            if prompt_match:
                prompts.append({
                    'scene_id': scene_id,
                    'type': 'CAC',
                    'prompt': prompt_match.group(1).strip(),
                    'output_name': f'SC{len(prompts) + 1:02d}_CAC_T2I.png'
                })
    
    return prompts


def run_batch(project_id: str, prompt_type: str = 'all'):
    """
    Run batch image generation for a project.
    
    Args:
        project_id: Project identifier (e.g., "06_50-12 Monia")
        prompt_type: 'storyboard', 'gmg', 'cac', or 'all'
    """
    print(f"\n{'='*60}")
    print(f"CMF IMAGE GENERATOR - OpenRouter + Seedream 4.5")
    print(f"{'='*60}")
    print(f"Project: {project_id}")
    print(f"Type: {prompt_type}")
    print(f"{'='*60}\n")
    
    # Find project path
    project_path = None
    for coach_folder in BASE_PATH.iterdir():
        if coach_folder.is_dir():
            for project_folder in coach_folder.iterdir():
                if project_id in project_folder.name:
                    project_path = project_folder
                    break
    
    if not project_path:
        print(f"✗ Project not found: {project_id}")
        return
    
    print(f"Project Path: {project_path}")
    
    # Create output directory
    output_dir = project_path / "generated_images"
    output_dir.mkdir(exist_ok=True)
    
    # Collect prompts based on type
    all_prompts = []
    
    if prompt_type in ['storyboard', 'all']:
        print("\n[1] Parsing Storyboard prompts...")
        storyboard_prompts = parse_storyboard_prompts(project_path)
        all_prompts.extend(storyboard_prompts)
        print(f"    Found {len(storyboard_prompts)} prompts")
    
    if prompt_type in ['gmg', 'all']:
        print("\n[2] Parsing GMG prompts...")
        gmg_prompts = parse_gmg_prompts(project_path)
        all_prompts.extend(gmg_prompts)
        print(f"    Found {len(gmg_prompts)} prompts")
    
    if prompt_type in ['cac', 'all']:
        print("\n[3] Parsing CAC prompts...")
        cac_prompts = parse_cac_prompts(project_path)
        all_prompts.extend(cac_prompts)
        print(f"    Found {len(cac_prompts)} prompts")
    
    if not all_prompts:
        print("\n✗ No prompts found to process!")
        return
    
    print(f"\n{'='*60}")
    print(f"GENERATING {len(all_prompts)} IMAGES")
    print(f"{'='*60}\n")
    
    # Generate images
    success_count = 0
    fail_count = 0
    
    for i, prompt_data in enumerate(all_prompts, 1):
        print(f"\n[{i}/{len(all_prompts)}] {prompt_data['type']} - {prompt_data['scene_id']}")
        
        # Create scene-specific folder
        scene_folder = output_dir / prompt_data['scene_id']
        scene_folder.mkdir(exist_ok=True)
        
        output_path = scene_folder / prompt_data['output_name']
        
        if generate_image(prompt_data['prompt'], output_path):
            success_count += 1
        else:
            fail_count += 1
    
    # Summary
    print(f"\n{'='*60}")
    print(f"GENERATION COMPLETE")
    print(f"{'='*60}")
    print(f"✓ Success: {success_count}")
    print(f"✗ Failed: {fail_count}")
    print(f"Output: {output_dir}")
    print(f"{'='*60}\n")
    
    # Write batch report
    report_path = output_dir / f"BATCH_REPORT_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write(f"# CMF Image Generation Report\n\n")
        f.write(f"**Project:** {project_id}\n")
        f.write(f"**Date:** {datetime.now().isoformat()}\n")
        f.write(f"**Model:** {MODEL}\n\n")
        f.write(f"## Results\n")
        f.write(f"- Success: {success_count}\n")
        f.write(f"- Failed: {fail_count}\n\n")
        f.write(f"## Generated Files\n")
        for prompt_data in all_prompts:
            status = "✓" if (output_dir / prompt_data['scene_id'] / prompt_data['output_name']).exists() else "✗"
            f.write(f"- {status} {prompt_data['output_name']}\n")


def main():
    parser = argparse.ArgumentParser(description='CMF OpenRouter Image Generator')
    parser.add_argument('--project', '-p', required=True, help='Project ID (e.g., "06_50-12 Monia")')
    parser.add_argument('--type', '-t', choices=['storyboard', 'gmg', 'cac', 'all'], 
                        default='all', help='Type of prompts to process')
    
    args = parser.parse_args()
    run_batch(args.project, args.type)


if __name__ == '__main__':
    main()
