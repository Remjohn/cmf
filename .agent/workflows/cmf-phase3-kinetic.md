---
description: Execute Kinetic Batch Operator (I2V Only - Zero New Images)
---

# CMF PHASE 3: KINETIC ENGINEERS

// turbo-all

**Objective:** Execute I2V generation. **Zero new image generation allowed.**

---

## PREREQUISITES
**Phase 2 authorization must exist:**
- [ ] `[PROJECT_ID]_STATIC_AUTHORIZED.md`

**All source images must be approved:**
- [ ] All `_01_T2I.png` files reviewed
- [ ] All `_02_FIRST.png` files reviewed (GMG)

---

## STEP 1: KINETIC PLANNING

**Agent:** `agents/phase3_kinetic/THE KINETIC BATCH OPERATOR.md`

1. Read ALL approved images from `04_assets/generative/`
2. Enter PLANNING MODE:
   - Assign motion physics (Wan 2.2 settings)
   - Map I2V prompts to source images
   - Verify Static Review Checkpoint passed
3. Output: `[PROJECT_ID]_KINETIC_BATCH_PLAN.md`

---

## STEP 2: I2V EXECUTION

**Tool:** Wan 2.2 / Running Hub API

### For B-Roll & CAC:
- Input: `_01_T2I.png`
- Output: `_03_MOV.mp4`

### For GMG:
- Input: `_02_FIRST.png` (animate from Void to Goal)
- Output: `_03_MOV.mp4`

**Naming Convention:**
```
04_assets/generative/
├── [PROJECT_ID]_SC01_BROLL_03_MOV.mp4
├── [PROJECT_ID]_SC02_CAC_03_MOV.mp4
├── [PROJECT_ID]_SC03_GMG_03_MOV.mp4
```

---

## STEP 3: MOTION QUALITY CHECK

**Automated Checks:**
- [ ] Video duration matches spec (5-6 seconds)?
- [ ] Motion is smooth (no jitter)?
- [ ] Subject stays consistent?

---

## 👮 COMMANDER CHECK: THE ASSET COMMANDER - KINETIC
**Agent:** `agents/commanders/THE ASSET COMMANDER - KINETIC.md`

- [ ] Input images were authorized?
- [ ] All planned videos exist?
- [ ] Naming convention followed?
- **IF PASS:** Issue `[PROJECT_ID]_KINETIC_AUTHORIZED.md`

---

## ⛔ PHASE 3 COMPLETE

**The following now exist:**
- [ ] All `_03_MOV.mp4` files
- [ ] `[PROJECT_ID]_KINETIC_AUTHORIZED.md`

---

## DELIVERABLES CHECKLIST

- [ ] `[PROJECT_ID]_KINETIC_BATCH_PLAN.md`
- [ ] All `_03_MOV.mp4` files
- [ ] `[PROJECT_ID]_KINETIC_AUTHORIZED.md`

---

## NEXT STEPS

With all assets generated, proceed to:
- **Phase 4:** VFX Fabrication
- **Phase 5:** Audio Assembly
- **Phase 6:** Manual Finishing

---

**END OF PHASE 3: KINETIC ENGINEERS**
