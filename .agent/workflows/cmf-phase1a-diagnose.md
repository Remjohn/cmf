---
description: Story Diagnosis & Brand Avatar (Setup Phase)
---

# CMF PHASE 1A-DIAGNOSE: Setup & Discovery

// turbo-all

**Objective:** Diagnose the arc type and establish visual identity.

**Prerequisites:**
- `{project_id}_transcript_clean.md`
- Avatar image (PNG/JPG)

---

## STEP 1: STORY DOCTOR (Arc Diagnosis)

**Agent:** `agents/phase1_writers/THE STORY DOCTOR.md`
**Guide:** `intelligence/guides/🎯 ARC SELECTION GUIDE.md`

#### 📋 MICRO TASKS
- [ ] **PLAN:** Analyze transcript to detect arc type
- [ ] **LOAD:** `{project_id}_transcript_clean.md`
- [ ] **EXECUTE:** Generate `{project_id}_strategy_brief.json`
- [ ] **VALIDATE:** Contains `selected_arc` + `unified_frame_statement` + `protagonist_voice`

**13 Supported Arcs:**
| # | Arc | Use When |
|---|-----|----------|
| 1 | The Witness | Testimonial validation |
| 2 | The Breakthrough | Transformation story |
| 3 | The Shared Struggle | Empathy building |
| 4 | The Confrontation | Challenge/opposition |
| 5 | The Core Transformation | Identity shift |
| 6 | The Warning | Prevention message |
| 7 | The Rally | Collective movement |
| 8 | The Divine Spark | Spiritual awakening |
| 9 | The Call to Adventure | Invitation/invitation |
| 9b | The Ticking Clock | Urgency/scarcity |
| 10 | The Comedic Reframe | Satire/humor |
| 11 | The Sacred Return | Integration/homecoming |
| 12 | The Quiet Reflection | Wisdom/contemplation |

**Output:** `{project_id}_strategy_brief.json`

---

## STEP 2: BRAND AVATAR BUILDER (Visual DNA)

**Agent:** `agents/phase1_writers/THE BRAND AVATAR BUILDER.md`

#### 📋 MICRO TASKS
- [ ] **PLAN:** Extract physical DNA from avatar image
- [ ] **LOAD:** Avatar image + `strategy_brief.json`
- [ ] **EXECUTE:** Generate `😎 {project_id} - The Brand Avatar 😎.md`
- [ ] **VALIDATE:** Contains PHYSICAL DNA block (Skin, Hair, Build, Features)

**Critical Output Fields:**
```markdown
## PHYSICAL DNA (INVARIANT)
- **Skin:** [Exact tone, e.g., "Light brown to caramel, warm undertones"]
- **Hair:** [Texture, style, color]
- **Build:** [Body type, posture]
- **Features:** [Face shape, distinguishing marks]
```

**Output:** `😎 {project_id} - The Brand Avatar 😎.md`

---

## ✅ PHASE COMPLETE CHECKLIST

- [ ] `{project_id}_strategy_brief.json` exists
- [ ] `😎 {project_id} - The Brand Avatar 😎.md` exists

---

## 🔗 NEXT: `/cmf-phase1a-narrative`
