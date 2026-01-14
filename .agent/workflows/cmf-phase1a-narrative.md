---
description: Quote Mining & Premise Composition
---

# CMF PHASE 1A-NARRATIVE: Quote Mining → Composition

// turbo-all

**Objective:** Extract quotes, enrich with V3 data, compose premise, authorize arc.

**Prerequisites:**
- `{project_id}_strategy_brief.json`
- `{project_id}_transcript_clean.md`
- `😎 {project_id} - The Brand Avatar 😎.md`

---

## THE 4-AGENT PIPELINE

```
🔎 HUNTER → 📊 ANALYST → ✍️ COMPOSER → ⚔️ COMMANDER
```

---

## STEP 1: ARC HUNTER (Quote Extraction)

**Agent:** Route to specific Hunter based on `strategy_brief.selected_arc`
**Location:** `agents/phase1_writers/hunters/`

#### 📋 MICRO TASKS
- [ ] **PLAN:** Extract 24-32 raw quotes using arc-specific rules
- [ ] **LOAD:** `transcript_clean.md` + `strategy_brief.json`
- [ ] **EXECUTE:** Generate `{project_id}_Quote_Manifest.md`
- [ ] **VALIDATE:** 24-32 quotes with `functional_tag` + `viral_score`

**Hunter Routing:**
| Arc | Hunter File |
|-----|-------------|
| Witness | `🔎 THE WITNESS HUNTER.md` |
| Breakthrough | `🔎 THE BREAKTHROUGH HUNTER.md` |
| Shared Struggle | `🔎 THE SHARED STRUGGLE HUNTER.md` |
| ... | (13 total) |

**Output:** `{project_id}_Quote_Manifest.md`

---

## STEP 2: ARC ANALYST (V3 Enrichment)

**Agent:** Route to specific Analyst based on arc
**Location:** `agents/phase1_writers/analysts/`

#### 📋 MICRO TASKS
- [ ] **PLAN:** Enrich quotes with V3 narrative coherence data
- [ ] **LOAD:** `Quote_Manifest.md` + `strategy_brief.json`
- [ ] **EXECUTE:** Generate `{project_id}_Quote_Manifest_Enriched.md`
- [ ] **VALIDATE:** All quotes tagged with THEMATIC_FIT, PACING, POLARITY, GLUE

**V3 Enrichment Tags:**
- `THEMATIC_FIT` (0-100)
- `PACING_CLASS` (STACCATO/LEGATO)
- `POLARITY_CATEGORIES`
- `PHILOSOPHICAL_WEIGHT` (0-10)
- `GLUE_SCORE` (0-100)
- `HIGH_AFFINITY_SEQUENCES`

**Output:** `{project_id}_Quote_Manifest_Enriched.md`

---

## STEP 3: STORY COMPOSER (Premise Assembly)

**Agent:** Route to specific Composer based on arc
**Location:** `agents/phase1_writers/composers/`

#### 📋 MICRO TASKS
- [ ] **PLAN:** Assemble best quotes into 60-90s premise
- [ ] **LOAD:** `Quote_Manifest_Enriched.md` + `strategy_brief.json`
- [ ] **EXECUTE:** Generate `{project_id}_premise_analysis.json`
- [ ] **VALIDATE:** Duration 60-90s. Arc rules applied. JSON valid.

**Composition Rules:**
- Max 3 quotes per cluster (if stacking)
- Favor punchy 3-5s fragments over 12s blocks
- Enforce 60-90 second total duration

**Output:** `{project_id}_premise_analysis.json`

---

## STEP 4: ARC COMMANDER (Premise Authorization)

**Agent:** Route to specific Commander based on arc
**Location:** `agents/commanders/arc_commanders/`

#### 📋 MICRO TASKS
- [ ] **PLAN:** Validate premise using 14 boolean checks (10 arc + 4 V3)
- [ ] **LOAD:** `premise_analysis.json` + `Quote_Manifest_Enriched.md`
- [ ] **EXECUTE:** Generate `{project_id}_[ARC]_AUTHORIZED.md`
- [ ] **VALIDATE:** Quality score ≥75. All critical checks PASS.

**14-Point Checklist:**
| # | Check | Type |
|---|-------|------|
| 1-10 | Arc-Specific Rules | Boolean |
| 11 | Template Match | V3 |
| 12 | Bookend Check | V3 |
| 13 | Beat Map | V3 |
| 14 | Narrative Coherence | V3 |

**Authorization Thresholds:**
- **≥75:** ✅ AUTHORIZED
- **<75:** ❌ REJECTION_NOTE.md with fixes

**Output:** `{project_id}_[ARC]_AUTHORIZED.md`

---

## ✅ PHASE COMPLETE CHECKLIST

- [ ] `{project_id}_Quote_Manifest.md`
- [ ] `{project_id}_Quote_Manifest_Enriched.md`
- [ ] `{project_id}_premise_analysis.json`
- [ ] `{project_id}_[ARC]_AUTHORIZED.md` (Quality ≥75)

---

## 🔗 NEXT: `/cmf-phase1a-script`
