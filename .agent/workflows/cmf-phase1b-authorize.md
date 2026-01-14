---
description: Final Visual Authorization (Visual Commander)
---

# CMF PHASE 1B-AUTHORIZE: Visual Commander

// turbo-all

**Objective:** Final quality gate for all visual prompts before image generation.

**Prerequisites (ALL must exist):**
- `{project_id}_STORYBOARD_AUTHORIZED.md`
- `{project_id}_GMG_ENRICHED.md`
- `{project_id}_CAC_ENRICHED.md`
- `😎 {project_id} - The Brand Avatar 😎.md`

---

## STEP 1: VISUAL COMMANDER (Final Authorization)

**Agent:** `agents/phase1_writers/THE VISUAL COMMANDER AGENT.md`

#### 📋 MICRO TASKS
- [ ] **LOAD:** All ENRICHED files + `Brand Avatar.md`
- [ ] **EXECUTE:** Generate `{project_id}_PROMPTS_AUTHORIZED.md`
- [ ] **VALIDATE:** Visual Fidelity Score ≥ 90

---

## THE 15-POINT COMPLIANCE CHECKLIST

### TIER 1: CRITICAL (10 pts each)
| # | Check |
|---|-------|
| 1 | Character Anchor present in EVERY prompt? |
| 2 | Physical DNA verbatim match across all scenes? |
| 3 | Emotional Arc Progression visible? |

### TIER 2: STRUCTURAL (7 pts each)
| # | Check |
|---|-------|
| 4 | No T-Codes/V-Codes in prose? |
| 5 | No system terminology? |
| 6 | GMG: Expert-Specific Palette? |
| 7 | GMG: Single Word Law? |
| 8 | Expert Voice Consistency? |

### TIER 3: DENSITY (5 pts each)
| # | Check |
|---|-------|
| 9 | Word count compliance? |
| 10 | CAC: Mundane Anchor present? |
| 11 | CAC: Sensory Stacking? |
| 12 | Camera/Lens specs present? |
| 13 | "Hyper-realistic" ending? |

### TIER 4: MOTION (3-5 pts each)
| # | Check |
|---|-------|
| 14 | I2I Deconstruction logic? |
| 15 | I2V Physics verbs? |

---

## AUTHORIZATION THRESHOLDS

| Score | Verdict | Action |
|-------|---------|--------|
| **90-100** | ✅ AUTHORIZED | Ready for Phase 2 |
| **75-89** | ⚠️ CONDITIONAL | Auto-fixes applied |
| **50-74** | ❌ REJECTED | Return to Analyst |
| **<50** | 🚫 CRITICAL | Return to Architect |

---

## ✅ PHASE COMPLETE

**Output:** `{project_id}_PROMPTS_AUTHORIZED.md`

**Visual Fidelity Score:** Must be ≥ 90

---

## 🔗 NEXT PHASE

All visual prompts are now authorized. Proceed to:
- `/cmf-eroll` (E-Roll Research)
- `/cmf-phase2-static` (Image Generation)
