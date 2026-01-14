# CMF Project Template

## Naming Convention
`XX_160-YY NAME`

Where:
- `XX` = Video sequence number (01-160)
- `160` = Monthly target (160 videos/month)
- `YY` = Client batch number
- `NAME` = Subject/Client name

**Example:** `01_160-01 Matthis`, `45_160-03 Sophie`

---

## Required Inputs (YOU PROVIDE)

| File | Description |
|------|-------------|
| `🎙️ [PROJECT_ID] - TRANSCRIPT [NAME].md` | Raw interview/coaching session |
| `[Subject]-avatar.png` | Screenshot of subject (PNG/JPG) |
| `[Coach]-avatar.jpeg` | Screenshot of coach (optional) |

---

## Pipeline Outputs (AUTO-GENERATED)

### Sub-Plan 1: Script Foundation
- `[PROJECT_ID]_premise_analysis.json`
- `[PROJECT_ID]_final_script.json`

### Sub-Plan 2: Sonic + Visual
- `[PROJECT_ID]_sonic_sourcing_brief.json`
- `[PROJECT_ID]_sonic_scribe_output.md`
- `[PROJECT_ID]_STORYBOARD_PRIMAL.md`
- `😎 [PROJECT_ID] - Brand Avatars.md`

### Sub-Plan 3: Assets + Assembly
- `D-Roll Intelligence Plan.md`
- `E-Roll Intelligence Plan.md`
- `🎯 [PROJECT_ID] - PRODUCTION BIBLE.md`
- `04_assets/` (generated visuals)
- `[PROJECT_ID]_fullVideo_[NAME].mp4` (final output)

---

## How to Use

1. **Copy this folder** and rename to your project code (e.g., `01_160-01 Matthis`)
2. **Add transcript** to the TRANSCRIPT.md file
3. **Add avatar images** (subject required, coach optional)
4. **Run `/cmf-execute`** to start the pipeline
