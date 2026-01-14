import os
import shutil

# Path definitions
ROOT = r"d:\Work\The Conscious Movie Factory December"
CMF_ROOT = os.path.join(ROOT, "🇫🇷 Conscious Movie Factory")
ARCHIVE = os.path.join(ROOT, "_ARCHIVE_LEGACY_V12")

# 1. DIRECTORIES TO KEEP (WHOLE FOLDERS)
KEEP_DIRS = [
    os.path.join(ROOT, "SFX_Library"),
    os.path.join(ROOT, "OUTPUTS"),
    os.path.join(ROOT, "CMF labo"),
    os.path.join(ROOT, "comfyui-workflows"), # Essential for V13 execution
    CMF_ROOT, # Keep the French folder structure itself
    os.path.join(CMF_ROOT, "inputs"),
    os.path.join(CMF_ROOT, "Motion Cookbook"),
    os.path.join(CMF_ROOT, "intelligence"),
    os.path.join(CMF_ROOT, "agents", "arc_hunters"),
    os.path.join(CMF_ROOT, "agents", "sonic"),
    os.path.join(CMF_ROOT, "agents", "_master"),
    os.path.join(CMF_ROOT, "agents", "visual"),
    os.path.join(CMF_ROOT, "output"), # output folder user mentioned
]

# 2. INDIVIDUAL FILES TO KEEP
KEEP_FILES = [
    # Master Agents
    os.path.join(ROOT, "config.yaml (The Session Truth).md"),
    os.path.join(ROOT, "GEMINI.md"),
    os.path.join(CMF_ROOT, "config.yaml (The Session Truth).md"), # Dupe check
    os.path.join(CMF_ROOT, "agents", "_master", "The Blueprint Architect (Production Planner).md"),
    os.path.join(CMF_ROOT, "agents", "_master", "The Producer (System State Manager).md"),
    
    # Visual Writers
    os.path.join(CMF_ROOT, "agents", "visual", "✍️ THE PROSE POET AGENT.md"),
    os.path.join(CMF_ROOT, "agents", "visual", "📸 THE COMPASSIONATE PHOTOGRAPHER AGENT.md"),
    os.path.join(CMF_ROOT, "agents", "visual", "🎬 THE STORYBOARD ARCHITECT v3.0 (PRIMAL EDITION).md"),
    os.path.join(CMF_ROOT, "agents", "visual", "🎨 THE C-ROLL ORCHESTRATOR AGENT.md"),
    
    # Sonic Writers
    os.path.join(CMF_ROOT, "agents", "sonic", "🎼 THE SONIC SCRIBE v2.0 (PRIMAL EDITION).md"),
    os.path.join(CMF_ROOT, "agents", "sonic", "The Sonic Sommelier (Musicologist).md"), # Check
    os.path.join(CMF_ROOT, "agents", "sonic", "The Ad-Lib Amplifier (Subconscious Audio).md"),
    
    # Commanders
    os.path.join(CMF_ROOT, "agents", "visual", "👮 THE PREMISE COMMANDER.md"),
    os.path.join(CMF_ROOT, "agents", "visual", "👮 THE SCRIPT COMMANDER.md"),
    os.path.join(CMF_ROOT, "agents", "visual", "👮 THE GMG BATCH COMMANDER.md"),
    os.path.join(CMF_ROOT, "agents", "visual", "👮 THE CAC BATCH COMMANDER.md"),
    os.path.join(CMF_ROOT, "agents", "visual", "👮 THE STORYBOARD BATCH COMMANDER.md"),
    os.path.join(CMF_ROOT, "agents", "visual", "👮 THE E-ROLL RESEARCH COMMANDER.md"),
    os.path.join(CMF_ROOT, "agents", "visual", "👮 THE ASSET COMMANDER - STATIC.md"),
    os.path.join(CMF_ROOT, "agents", "visual", "👮 THE ASSET COMMANDER - KINETIC.md"),
]

# Add Arc Hunters dynamically (27 files)
ARC_DIR = os.path.join(CMF_ROOT, "agents", "arc_hunters")
if os.path.exists(ARC_DIR):
    for f in os.listdir(ARC_DIR):
        KEEP_FILES.append(os.path.join(ARC_DIR, f))

# Normalize paths for comparison
KEEP_DIRS = [os.path.abspath(d).lower() for d in KEEP_DIRS]
KEEP_FILES = [os.path.abspath(f).lower() for f in KEEP_FILES]

def should_keep(path):
    abs_path = os.path.abspath(path).lower()
    # Check if file is explicitly kept
    if abs_path in KEEP_FILES:
        return True
    # Check if path is within a kept directory
    for d in KEEP_DIRS:
        if abs_path.startswith(d):
            return True
    return False

def archive_item(path, base_root):
    if not os.path.exists(path): return
    rel_path = os.path.relpath(path, ROOT)
    target = os.path.join(ARCHIVE, rel_path)
    os.makedirs(os.path.dirname(target), exist_ok=True)
    
    try:
        if os.path.isdir(path):
            # If it's a directory, move it if none of its contents are meant to be kept
            # (In this logic, we move the directory itself if it's not a KEEP_DIR)
            shutil.move(path, target)
        else:
            shutil.move(path, target)
    except Exception as e:
        print(f"Error moving {path}: {e}")

# EXECUTION
if not os.path.exists(ARCHIVE):
    os.makedirs(ARCHIVE)

# Walk root
for item in os.listdir(ROOT):
    item_path = os.path.join(ROOT, item)
    if item in [".agent", ".env", "_ARCHIVE_LEGACY_V12", "tools"]: continue # Skip tools and infra
    
    if not should_keep(item_path):
        archive_item(item_path, ROOT)

# Walk CMF_ROOT specifically for deeper cleanup
if os.path.exists(CMF_ROOT):
    for root_dir, subdirs, files in os.walk(CMF_ROOT, topdown=True):
        # Determine which subdirs to skip or move
        for d in list(subdirs):
            d_path = os.path.join(root_dir, d)
            if should_keep(d_path):
                continue
            else:
                archive_item(d_path, ROOT)
                subdirs.remove(d) # Don't recurse into moved directory
        
        for f in files:
            f_path = os.path.join(root_dir, f)
            if not should_keep(f_path):
                archive_item(f_path, ROOT)

print("Cleanup Complete. Legacy assets moved to _ARCHIVE_LEGACY_V12.")
