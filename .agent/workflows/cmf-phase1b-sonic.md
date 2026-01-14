---
description: Sonic Engineering (Music prompts for Suno/Udio)
---

# CMF PHASE 1B-SONIC: Music Engineering

// turbo-all

**Objective:** Generate music prompts for the project soundtrack.

**Prerequisites:**
- `{project_id}_SCRIPT_AUTHORIZED.md` (from Phase 1)
- `{project_id}_final_script.json`
- `Tribe_Soul_Profile.md` (Coach-level file)

---

## STEP 1: SONIC SOMMELIER (Genre Pairing)

**Agent:** `agents/sonic/The Sonic Sommelier (Musicologist).md`
**Guide:** `intelligence/guides/🎶 The Sonic Sommelier.md`

#### 📋 MICRO TASKS
- [ ] **LOAD:** `final_script.json` + `Tribe_Soul_Profile.md` + `Genre Library.txt`
- [ ] **EXECUTE:** Generate `{project_id}_sonic_sommelier_brief.md`
- [ ] **VALIDATE:** Contains BPM Range + Genre Blend + Cultural Insight + Reference Artists

**Actions:**
1. Load Cultural Data (Tribe Soul Profile)
2. Analyze Narrative Emotional Arc
3. Select "Vintage" (BPM + Genre + Instruments to Avoid)
4. Generate Sourcing Brief

**Output:** `{project_id}_sonic_sommelier_brief.md`

---

## STEP 2: SONIC SCRIBE (Suno Prompt)

**Agent:** `agents/sonic/The Sonic Scribe (Composer).md`

#### 📋 MICRO TASKS
- [ ] **LOAD:** `sonic_sommelier_brief.md` + `final_script.json`
- [ ] **EXECUTE:** Generate `{project_id}_sonic_scribe_output.md`
- [ ] **VALIDATE:** Contains Suno V5 Prompt + Song Structure Tags + Style Descriptors

**Actions:**
1. Translate Emotional Arc → Song Structure (`[Intro]`, `[Verse]`, `[Chorus]`)
2. Add Style Descriptors from Sommelier Brief
3. Add "Sonic Vacuum" commands (silence breaks)
4. Final Assembly: Complete Suno.ai prompt

**Output:** `{project_id}_sonic_scribe_output.md`

---

## ✅ PHASE COMPLETE CHECKLIST

- [ ] `{project_id}_sonic_sommelier_brief.md` exists
- [ ] `{project_id}_sonic_scribe_output.md` exists

---

## 🔗 NEXT: Run in parallel with:
- `/cmf-phase1b-storyboard`
- `/cmf-phase1b-motion`

Then run: `/cmf-phase1b-authorize`
