---
description: Script Assembly & Authorization
---

# CMF PHASE 1A-SCRIPT: Final Script Production

// turbo-all

**Objective:** Assemble final script and authorize for production.

**Prerequisites:**
- `{project_id}_premise_analysis.json`
- `{project_id}_[ARC]_AUTHORIZED.md`
- `{project_id}_transcript_clean.md` (for timestamp verification)

---

## THE 2-AGENT PIPELINE

```
✍️ SCRIPT ASSEMBLY → ⚔️ SCRIPT COMMANDER
```

---

## STEP 1: SCRIPT ASSEMBLY

**Agent:** Route to specific Composer based on arc
**Location:** `agents/phase1_writers/composers/`

#### 📋 MICRO TASKS
- [ ] **PLAN:** Format premise quotes into Conscious Arc structure
- [ ] **LOAD:** `premise_analysis.json` + `[ARC]_AUTHORIZED.md`
- [ ] **EXECUTE:** Generate `{project_id}_final_script.json`
- [ ] **VALIDATE:** JSON valid. Timestamps present. HOOK→CTA structure.

**Conscious Arc Structure:**
```json
{
  "scenes": [
    {"id": "W1_HOOK", "quote": "...", "start": "00:00", "end": "00:05"},
    {"id": "W2_PROBLEM", "quote": "...", "start": "...", "end": "..."},
    {"id": "W3_MECHANISM", "quote": "...", "start": "...", "end": "..."},
    {"id": "W4_PROOF", "quote": "...", "start": "...", "end": "..."},
    {"id": "W5_CLOSE", "quote": "...", "start": "...", "end": "..."}
  ]
}
```

**Output:** `{project_id}_final_script.json`

---

## STEP 2: SCRIPT COMMANDER (Final Authorization)

**Agent:** Route to specific Commander based on arc
**Location:** `agents/commanders/arc_commanders/`

#### 📋 MICRO TASKS
- [ ] **PLAN:** Validate script for production readiness
- [ ] **LOAD:** `final_script.json` + `transcript_clean.md`
- [ ] **EXECUTE:** Generate `{project_id}_SCRIPT_AUTHORIZED.md`
- [ ] **VALIDATE:** All 4 checks PASS

**4-Point Script Checklist:**
| # | Check | Fail Behavior |
|---|-------|---------------|
| 1 | **Timestamp Citation** | Every quote has source timestamp? |
| 2 | **Voice Fidelity** | Does it sound like the person? |
| 3 | **Arc Match** | Follows selected arc structure? |
| 4 | **JSON Valid** | Formatting correct? |

**Output:** `{project_id}_SCRIPT_AUTHORIZED.md`

---

## ✅ PHASE COMPLETE CHECKLIST

- [ ] `{project_id}_final_script.json`
- [ ] `{project_id}_SCRIPT_AUTHORIZED.md`

---

## ⛔ PHASE 1A GATE COMPLETE

**ALL must exist before Phase 1B:**
- [ ] `{project_id}_strategy_brief.json`
- [ ] `😎 {project_id} - The Brand Avatar 😎.md`
- [ ] `{project_id}_[ARC]_AUTHORIZED.md`
- [ ] `{project_id}_SCRIPT_AUTHORIZED.md`

---

## 🔗 NEXT: Run in parallel:
- `/cmf-phase1b-sonic`
- `/cmf-phase1b-storyboard`
- `/cmf-phase1b-motion`

Then: `/cmf-phase1b-authorize`
