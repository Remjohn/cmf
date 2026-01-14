---
description: Storyboard Pipeline (A-Roll Hero Frames)
---

# CMF PHASE 1B-STORYBOARD: A-Roll Visual Prompts

// turbo-all

**Objective:** Generate photorealistic hero frame prompts for the main A-Roll footage.

**Prerequisites:**
- `{project_id}_SCRIPT_AUTHORIZED.md`
- `{project_id}_final_script.json`
- `😎 {project_id} - The Brand Avatar 😎.md`

---

## THE 5-AGENT PIPELINE

```
🎬 ARCHITECT → 🔍 ANALYST → 📸 PHOTOGRAPHER → ✍️ POET → ⚔️ COMMANDER
```

---

## STEP 1: STORYBOARD ARCHITECT (Primal Analysis)

**Agent:** `agents/phase1_writers/THE STORYBOARD ARCHITECT v3.0 (PRIMAL EDITION).md`

#### 📋 MICRO TASKS
- [ ] **LOAD:** `final_script.json` + `Brand Avatar.md`
- [ ] **EXECUTE:** Generate `{project_id}_STORYBOARD_PRIMAL.md`
- [ ] **VALIDATE:** Each scene has T-Code + V-Code + Arc Beat + PRIMAL Analysis

**Output:** `{project_id}_STORYBOARD_PRIMAL.md`

---

## STEP 2: VISUAL ANALYST (Validation)

**Agent:** `agents/phase1_writers/THE VISUAL ANALYST AGENT.md`

#### 📋 MICRO TASKS
- [ ] **LOAD:** `STORYBOARD_PRIMAL.md` + `Brand Avatar.md`
- [ ] **EXECUTE:** Generate `{project_id}_STORYBOARD_ENRICHED.md`
- [ ] **VALIDATE:** 8-point validation complete

**8-Point Validation:**
1. T-Code Consistency
2. V-Code Hierarchy
3. **CHARACTER ANCHOR IMMUTABILITY** ⚠️ CRITICAL
4. SPR Coherence
5. Environment Logic
6. Timestamp Accuracy
7. Arc Progression
8. Uniqueness Check

**Output:** `{project_id}_STORYBOARD_ENRICHED.md`

---

## STEP 3: COMPASSIONATE PHOTOGRAPHER (Structure)

**Agent:** `agents/phase1_writers/THE COMPASSIONATE PHOTOGRAPHER AGENT.md`

#### 📋 MICRO TASKS
- [ ] **LOAD:** `STORYBOARD_ENRICHED.md` + `Brand Avatar.md`
- [ ] **EXECUTE:** Generate `{project_id}_STORYBOARD_STRUCTURED.md`
- [ ] **VALIDATE:** Each scene has SPR (16 words) + 6-Block Structure

**6-Block Output per Scene:**
- `[PRIMING (SPR)]`
- `[CHARACTER ANCHOR]`
- `[CINEMATIC COMPOSITION]`
- `[MATERIAL PHYSICS]`
- `[LIGHT BEHAVIOR]`
- `[THE NARRATIVE MOMENT]`

**Output:** `{project_id}_STORYBOARD_STRUCTURED.md`

---

## STEP 4: PROSE POET (Final Translation)

**Agent:** `agents/phase1_writers/THE PROSE POET AGENT.md`

#### 📋 MICRO TASKS
- [ ] **LOAD:** `STORYBOARD_STRUCTURED.md` + `Brand Avatar.md`
- [ ] **EXECUTE:** Generate `{project_id}_STORYBOARD_VISUAL_POETRY.md`
- [ ] **VALIDATE:** NO headers in output. Biological hook first. "Hyper-realistic" ending.

**6-Paragraph Pure Prose Structure:**
1. BIOLOGICAL HOOK + CHARACTER
2. CAMERA + FRAMING
3. FULL BODY + GESTURE
4. LIGHT + ATMOSPHERE
5. NARRATIVE + SUBTEXT
6. TECHNICAL GROUNDING

**Output:** `{project_id}_STORYBOARD_VISUAL_POETRY.md`

---

## STEP 5: STORYBOARD COMMANDER (Authorization)

**Agent:** `agents/commanders/THE STORYBOARD BATCH COMMANDER.md`

#### 📋 MICRO TASKS
- [ ] **LOAD:** `STORYBOARD_VISUAL_POETRY.md` + `Brand Avatar.md`
- [ ] **EXECUTE:** Generate `{project_id}_STORYBOARD_AUTHORIZED.md`
- [ ] **VALIDATE:** Avatar verbatim. Tone consistent. No codes visible.

**Output:** `{project_id}_STORYBOARD_AUTHORIZED.md`

---

## ✅ PHASE COMPLETE CHECKLIST

- [ ] `{project_id}_STORYBOARD_PRIMAL.md`
- [ ] `{project_id}_STORYBOARD_ENRICHED.md`
- [ ] `{project_id}_STORYBOARD_STRUCTURED.md`
- [ ] `{project_id}_STORYBOARD_VISUAL_POETRY.md`
- [ ] `{project_id}_STORYBOARD_AUTHORIZED.md`

---

## 🔗 NEXT: Run `/cmf-phase1b-authorize`
