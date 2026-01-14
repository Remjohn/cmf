---
description: Motion Graphics Pipeline (GMG + CAC B-Roll)
---

# CMF PHASE 1B-MOTION: GMG + CAC Prompts

// turbo-all

**Objective:** Generate abstract motion graphics (GMG) and ambient cinema (CAC) B-Roll prompts.

**Prerequisites:**
- `{project_id}_final_script.json`
- `😎 {project_id} - The Brand Avatar 😎.md`

---

## PART A: GMG (Generative Motion Graphics)

### STEP 1: GMG COMPOSER

**Agent:** `Motion Cookbook/03_GMG_Generative_Motion_Graphics/GMG_Composer_Agent.md`
**Constitution:** `Motion Cookbook/03_GMG_Generative_Motion_Graphics/THE GMG CONSTITUTION.md`

#### 📋 MICRO TASKS
- [ ] **LOAD:** `final_script.json` + Constitution + Expert files (01-06)
- [ ] **EXECUTE:** Generate `{project_id}_GMG_PROMPTS.md`
- [ ] **VALIDATE:** Each scene has Expert# + Single Word + 3-Phase Prompts

**Expert Palette Matrix:**
| Expert | Primary Color | Accent |
|--------|--------------|--------|
| Exp 01 | Forest Green | Gold |
| Exp 02 | Grayscale | Gold |
| Exp 03 | Grayscale Materials | Gold |
| Exp 06 | **WHITE ONLY** | **NO GOLD** |

**Output:** `{project_id}_GMG_PROMPTS.md`

---

### STEP 2: GMG VISUAL ANALYST

**Agent:** `agents/phase1_writers/GMG_VISUAL_ANALYST.md`

#### 📋 MICRO TASKS
- [ ] **LOAD:** `GMG_PROMPTS.md` + Constitution
- [ ] **EXECUTE:** Generate `{project_id}_GMG_ENRICHED.md`
- [ ] **VALIDATE:** 6 GMG-specific checks per scene

**GMG Checks:**
- G1: Expert-Specific Palette
- G2: Single Word Law
- G3: Expert Routing
- G4: Expert Voice Consistency
- G5: 3-Phase Completeness
- G6: Word Count Compliance

**Output:** `{project_id}_GMG_ENRICHED.md`

---

## PART B: CAC (Conscious Ambient Cinema)

### STEP 3: CAC COMPOSER

**Agent:** `Motion Cookbook/04_CAC_Conscious_Ambient_Cinema/CAC_Composer_Agent.md`
**Metaphor Library:** `Motion Cookbook/04_CAC_Conscious_Ambient_Cinema/THE CAC METAPHOR LIBRARY.md`

#### 📋 MICRO TASKS
- [ ] **LOAD:** `final_script.json` + Metaphor Library + `Brand Avatar.md`
- [ ] **EXECUTE:** Generate `{project_id}_CAC_PROMPTS.md`
- [ ] **VALIDATE:** Each scene has Archetype# + El Shaddai Prompt (180-260 words) + Motion Spec

**El Shaddai Requirements:**
- 180-260 word prose poem
- Mundane Anchor (grounding prop)
- Sensory Stacking (Touch + Temp + Sight)
- Character Anchor injected

**Output:** `{project_id}_CAC_PROMPTS.md`

---

### STEP 4: CAC VISUAL ANALYST

**Agent:** `agents/phase1_writers/CAC_VISUAL_ANALYST.md`

#### 📋 MICRO TASKS
- [ ] **LOAD:** `CAC_PROMPTS.md` + Metaphor Library
- [ ] **EXECUTE:** Generate `{project_id}_CAC_ENRICHED.md`
- [ ] **VALIDATE:** 7 CAC-specific checks per scene

**CAC Checks:**
- C1: Metaphor Library Compliance (01-24)
- C2: Emotional Routing Accuracy
- C3: Word Count (180-260)
- C4: Mundane Anchor Presence
- C5: Sensory Stacking
- C6: El Shaddai Structure
- C7: Motion Spec Validity

**Output:** `{project_id}_CAC_ENRICHED.md`

---

## ✅ PHASE COMPLETE CHECKLIST

**GMG:**
- [ ] `{project_id}_GMG_PROMPTS.md`
- [ ] `{project_id}_GMG_ENRICHED.md`

**CAC:**
- [ ] `{project_id}_CAC_PROMPTS.md`
- [ ] `{project_id}_CAC_ENRICHED.md`

---

## 🔗 NEXT: Run `/cmf-phase1b-authorize`
