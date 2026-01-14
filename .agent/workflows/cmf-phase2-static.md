---
description: Execute Static Batch Operator (T2I/I2I Only - OpenRouter)
---

# CMF PHASE 2: STATIC ENGINEERS (OpenRouter Edition)

// turbo-all

**Objective:** Execute T2I/I2I generation using OpenRouter + Seedream 4.5. **Zero video generation.**

---

## PREREQUISITES

**ALL Phase 1 authorizations must exist:**
- [ ] `[PROJECT_ID]_SCRIPT_AUTHORIZED.md`
- [ ] `[PROJECT_ID]_STORYBOARD_AUTHORIZED.md` or `[PROJECT_ID]_PROMPTS_AUTHORIZED.md`

**Prompt files must be complete:**
- [ ] `[PROJECT_ID]_STORYBOARD_VISUAL_POETRY.md`
- [ ] `[PROJECT_ID]_GMG_PROMPTS.md`
- [ ] `[PROJECT_ID]_CAC_PROMPTS.md`

---

## STEP 1: ENVIRONMENT CHECK

Before running, verify:
```powershell
# Check Python and dependencies
python --version
pip show openai python-dotenv

# If missing, install:
pip install openai python-dotenv
```

---

## STEP 2: RUN IMAGE GENERATOR

### Option A: Generate ALL image types
```powershell
cd "d:\Work\The Conscious Movie Factory December"
python tools/cmf_image_generator.py --project "06_50-12 Monia" --type all
```

### Option B: Generate by type
```powershell
# Storyboard (A-Roll hero frames) only
python tools/cmf_image_generator.py --project "06_50-12 Monia" --type storyboard

# GMG (Motion Graphics LAST + FIRST frames) only
python tools/cmf_image_generator.py --project "06_50-12 Monia" --type gmg

# CAC (Ambient Cinema) only
python tools/cmf_image_generator.py --project "06_50-12 Monia" --type cac
```

---

## STEP 3: OUTPUT STRUCTURE

The generator creates organized folders per scene:
```
inputs/Coach Adele/06_50-12 Monia/generated_images/
├── W1/
│   ├── SC01_STORYBOARD_T2I.png
│   ├── SC01_GMG_01_LAST.png
│   ├── SC01_GMG_02_FIRST.png
│   └── SC01_CAC_T2I.png
├── W2/
│   ├── SC02_STORYBOARD_T2I.png
│   ├── SC02_GMG_01_LAST.png
│   ├── SC02_GMG_02_FIRST.png
│   └── SC02_CAC_T2I.png
├── W3/
│   └── ...
├── W4/
│   └── ...
├── W5/
│   └── ...
└── BATCH_REPORT_20260114_073000.md
```

---

## 🛑 CHECKPOINT: STATIC REVIEW

**USER ACTION REQUIRED:**

1. Open `generated_images/` folder
2. Review ALL generated images
3. Check:
   - [ ] Faces correct and recognizable?
   - [ ] Lighting consistent across scenes?
   - [ ] Brand Avatar matches description?
   - [ ] GMG LAST → FIRST logic makes sense?
   - [ ] CAC metaphors are evocative?

**DECISION:**
- **APPROVED** → Proceed to video generation
- **REJECTED** → Re-run with adjusted prompts

---

## STEP 4: BATCH FOR MULTIPLE PROJECTS

### PowerShell Batch Script
```powershell
# Run for all 5 projects
$projects = @(
    "06_50-12 Monia",
    "05_50-12 Fitou",
    "04_50-12 Nina",
    "03_50-12 Jean Pierre",
    "02_50-12 Audrey"
)

foreach ($project in $projects) {
    Write-Host ">>> Processing: $project" -ForegroundColor Cyan
    python tools/cmf_image_generator.py --project $project --type all
    Write-Host ">>> Done: $project" -ForegroundColor Green
}
```

---

## 📊 API COSTS

| Model | Price | Notes |
|-------|-------|-------|
| bytedance-seed/seedream-4.5 | ~$0.003/image | High quality, fast |

**Estimated cost per project:** ~$0.05 (15-20 images)
**5 projects/day:** ~$0.25/day

---

## DELIVERABLES CHECKLIST

- [ ] `generated_images/W1/` folder with all scene 1 images
- [ ] `generated_images/W2/` folder with all scene 2 images
- [ ] `generated_images/W3/` folder with all scene 3 images
- [ ] `generated_images/W4/` folder with all scene 4 images
- [ ] `generated_images/W5/` folder with all scene 5 images
- [ ] `BATCH_REPORT_*.md` with generation summary

---

**END OF PHASE 2: STATIC ENGINEERS (OpenRouter)**
