"""
CMF Smart Project Factory
Creates a new project folder from a transcript file, copies the template, and installs automation.

Usage:
    python tools/create_project.py --transcript "path/to/transcript.srt"
"""

import os
import shutil
import argparse
from pathlib import Path
import sys

# Import the automator generator
sys.path.append(os.path.dirname(__file__))
import generate_automator

BASE_PATH = r"d:\Work\The Conscious Movie Factory December"
INPUTS_ROOT = Path(BASE_PATH) / "🇫🇷 Conscious Movie Factory" / "inputs"
TEMPLATE_PATH = INPUTS_ROOT / "_TEMPLATE_PROJECT"

def create_project(transcript_path, coach_name="Coach Adele"):
    transcript = Path(transcript_path)
    if not transcript.exists():
        print(f"🛑 Error: Transcript not found at {transcript}")
        return

    # 1. Project ID from Filename (e.g., "14_160-01 Title.srt" -> "14_160-01 Title")
    project_id = transcript.stem
    print(f"🏗️  Initializing Project: {project_id}")

    # 2. Target Directory
    coach_dir = INPUTS_ROOT / coach_name
    if not coach_dir.exists():
        print(f"🆕 Coach folder '{coach_name}' does not exist. Creating it...")
        coach_dir.mkdir(parents=True, exist_ok=True)
        
    target_dir = coach_dir / project_id
    
    if target_dir.exists():
        print(f"⚠️  Warning: Project folder already exists at {target_dir}")
        print("   Skipping creation to prevent overwriting. Use manual check if needed.")
    else:
        # 3. Copy Template
        print(f"📂 Creating folder structure in inputs/{coach_name}/...")
        try:
            shutil.copytree(TEMPLATE_PATH, target_dir)
        except Exception as e:
            print(f"🛑 Error copying template: {e}")
            return

    # 4. Copy Transcript (Keep original filename)
    target_transcript = target_dir / transcript.name
    if not target_transcript.exists():
        print(f"📜 Copying transcript...")
        shutil.copy2(transcript, target_transcript)
    
    # 5. Install Automation Pipeline
    print(f"🤖 Installing Automator (RUN_PIPELINE.ps1)...")
    generate_automator.generate_script(project_id)

    print(f"\n✅ SUCCESS! Project '{project_id}' is ready.")
    print(f"👉 Go there: cd \"{target_dir}\"")
    print(f"👉 Run it:   .\RUN_PIPELINE.ps1")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="CMF Smart Project Factory")
    parser.add_argument("--transcript", required=True, help="Path to the .srt or .txt transcript file")
    parser.add_argument("--coach", default="Coach Adele", help="Name of the coach folder (default: Coach Adele)")
    
    args = parser.parse_args()
    
    create_project(args.transcript, args.coach)
