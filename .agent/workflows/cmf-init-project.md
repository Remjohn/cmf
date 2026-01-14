---
description: Initialize a new CMF project folder with automation scripts
---

# /cmf-init-project: Project Initialization

Use this workflow when you have a new transcript and are starting a brand new project.

## STEP 1: PREPARATION
1. Ensure your transcript (.srt or .txt) is ready.
2. Ensure you know the Coach folder name (Default: "Coach Adele").

## STEP 2: RUN THE FACTORY

**Option A: Default (Coach Adele)**
```powershell
python tools/create_project.py --transcript "path/to/transcript.srt"
```

**Option B: Specific Coach (16+ Coaches Supported)**
```powershell
python tools/create_project.py --transcript "path/to/transcript.srt" --coach "Coach Jean"
```

*Example:*
`python tools/create_project.py --transcript "14_160-01 Law of Attraction.srt" --coach "Coach Sarah"`

**(Note: If the Coach folder doesn't exist, it will be created automatically.)**

## STEP 3: VERIFY AND RUN
1. The tool will print the location of your new folder.
2. `cd` into that new folder.
3. Run `.\RUN_PIPELINE.ps1` to start production immediately!

---
**TIP:** If you add multiple projects at once, you can run `python tools/generate_automator.py --all` to scan and add scripts to all folders that are missing them.
