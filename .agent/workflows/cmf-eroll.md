---
description: Execute the full E-Roll Cultural DNA image procurement workflow
---

# CMF E-ROLL: CULTURAL DNA RESEARCH (V15 - Micro Task Architecture)

// turbo-all

**Objective:** Procure culturally-specific E-Roll images using the locked 5-Phase Deep Research workflow.

**Prerequisite:** Run `/cmf-phase1-visual` FIRST. This workflow requires:
- `{project_id}_final_script.json`
- `Tribe_Soul_Profile.md` (at Coach level)
- `😎 {project_id} - The Brand Avatar 😎.md` (if exists)

**Critical Reference:** `intelligence/guides/🔮 E-Roll Research Planning Generator.md`

> [!CAUTION]
> **DO NOT GENERATE SEARCH QUERIES WITHOUT A DEEP RESEARCH REPORT.**
> Generic queries like "ladder climbing success" are FORBIDDEN.
> Every query MUST reference a VERIFIED cultural source.

---

## STEP 1: INPUT GATHERING

#### 📋 MICRO TASK LIST: 1A_INPUT_GATHER
- [ ] **PLAN:** I will extract cultural DNA themes from project inputs.
- [ ] **LOAD:** I have read `final_script.json` + `Tribe_Soul_Profile.md` + `Brand Avatar.md`.
- [ ] **EXECUTE:** I have extracted: Transformation themes, Tribe slang, Heroes, Enemies.
- [ ] **VALIDATE:** I have cultural grounding (NOT just script themes).

**Actions:**
1. Read `final_script.json` - Extract transformation journey themes
2. Read `Tribe_Soul_Profile.md` - Extract `tribe_slang`, `shared_heroes`, `common_enemies`
3. Read `Brand Avatar.md` - Coach positioning context

---

## STEP 2: 12 INTROSPECTION QUESTIONS

#### 📋 MICRO TASK LIST: 2A_INTROSPECTION
- [ ] **PLAN:** I will answer 12 questions FROM THE CULTURAL PERSPECTIVE.
- [ ] **LOAD:** I have internalized the Tribe Soul Profile cultural context.
- [ ] **EXECUTE:** I have answered all 12 questions with cultural specifics.
- [ ] **VALIDATE:** Answers contain NAMED references (not "ladder" or "light").

> [!IMPORTANT]
> Answer about THE CULTURE, not the script.
> If your answer is generic (e.g., "ladder"), you're doing it wrong.

**The 12 Questions (6 Angles × 2 each):**

### Language & Codes
1. What words, slang, or greetings identify "insiders" in this culture?
2. What visual signals or gestures would only insiders recognize?

### Aesthetics & Symbols
3. What colors, textures, or styles define this culture's visual identity?
4. What sacred symbols, adornments, or objects carry deep meaning?

### Rituals & Behaviors
5. What daily or ceremonial practices define this community?
6. What preparation or cleansing rituals are sacred to this culture?

### Heroes, Elders & Icons
7. Who are the NAMED figures this audience reveres (living or ancestral)?
8. What archetypes (healer, warrior, mother) resonate with this tribe?

### Opposition, Wounds & Enemy
9. What systems threatened or tried to erase this culture?
10. What shared wounds or traumas bind this community together?

### Shared Emotional Truths
11. What collective emotions (pride, grief, reclamation) define this tribe?
12. What future vision or aspiration unites this community?

---

## STEP 3: DEEP RESEARCH (MANDATORY - USE BROWSER)

#### 📋 MICRO TASK LIST: 3A_DEEP_RESEARCH
- [ ] **PLAN:** I will use BROWSER to find REAL, VERIFIABLE cultural references.
- [ ] **LOAD:** I have my 12 answered introspection questions.
- [ ] **EXECUTE:** I have found 2-3 NAMED references per angle with URLs.
- [ ] **VALIDATE:** Every reference is VERIFIABLE (real person, event, brand, URL).

> [!CAUTION]
> You MUST use browser-based research. DO NOT hallucinate sources.

**For each of 6 angles, find:**
- 2-3 NAMED references (people, brands, events, works)
- Source URLs where you verified the reference
- Cultural context explaining why this resonates

**Example Research Output:**
| Angle | Reference | Source | Why It Resonates |
|-------|-----------|--------|------------------|
| Heroes | Fatima Douba | secretsdediongoma.com | Afro-holistic naturopath bridging ancestral wisdom |
| Opposition | Syndrome Méditerranéen | France Inter article | Documented medical bias against Black patients |
| Aesthetics | Maison Château Rouge | maisonchateaurouge.com | Remixed French symbols with African textiles |

---

## STEP 4: DEEP RESEARCH REPORT

#### 📋 MICRO TASK LIST: 4A_RESEARCH_REPORT
- [ ] **PLAN:** I will compile all verified references into a structured report.
- [ ] **LOAD:** I have my research findings from Phase 3.
- [ ] **EXECUTE:** I have generated `{project_id}_ERoll_Deep_Research_Report.md`.
- [ ] **VALIDATE:** Report contains: Tribe Summary + 6 Angles + Source URLs.

**Output:** `inputs/{project_folder}/{project_id}_ERoll_Deep_Research_Report.md`

**Required Structure:**
```markdown
# E-Roll Deep Research Report: [Project Name]

## Tribe Profile Summary
- Audience: [Description from Soul Profile]
- Key Cultural Codes: [From slang/heroes/enemies]

## ANGLE 1: Language, Codes & Signals
### Verified References
1. **[Reference Name]** - Source: [URL] - Relevance: [Why]
2. **[Reference Name]** - Source: [URL] - Relevance: [Why]

[Continue for all 6 angles]

## Research Sources Used
- [URL 1]
- [URL 2]
```

> [!IMPORTANT]
> **NO QUERIES UNTIL THIS REPORT IS COMPLETE**

---

## STEP 5: SEARCH QUERY GENERATION

#### 📋 MICRO TASK LIST: 5A_QUERY_GEN
- [ ] **PLAN:** I will generate 24 queries (6 angles × 4 each) from the Report.
- [ ] **LOAD:** I have read `ERoll_Deep_Research_Report.md`.
- [ ] **EXECUTE:** I have generated `{project_id}_ERoll_Search_Queries.json`.
- [ ] **VALIDATE:** Every query cites source from Report. No generic terms.

**Output:** `inputs/{project_folder}/{project_id}_ERoll_Search_Queries.json`

**Query Quality Check:**
| ❌ WRONG (Generic) | ✅ RIGHT (Culturally Specific) |
|-------------------|-------------------------------|
| "ladder climbing success" | "Maison Château Rouge Youssouf Fofana Bogolan" |
| "herbal cleanse detox" | "Kinkeliba thé longue vie African morning ritual" |
| "breakthrough celebration" | "S'enjailler celebration Ivorian diaspora France" |
| "divine light awakening" | "Retour aux Sources Ifa Yoruba spirituality France" |

**JSON Structure:**
```json
{
    "project_id": "{project_id}",
    "framework": "Cultural_DNA_6_Angles",
    "deep_research_conducted": true,
    "queries": [
        {
            "angle": "ANGLE_1_LANGUAGE_CODES",
            "scene_code": "ANG1_01",
            "query": "[CULTURALLY SPECIFIC QUERY]",
            "source": "[From Deep Research Report]"
        }
    ]
}
```

---

## STEP 6: E-ROLL COMMANDER CHECK

**Agent:** `agents/commanders/THE E-ROLL RESEARCH COMMANDER.md`

#### 📋 MICRO TASK LIST: 6A_EROLL_COMMANDER
- [ ] **PLAN:** I will audit research ancestry + query specificity.
- [ ] **LOAD:** I have read `ERoll_Search_Queries.json` + `ERoll_Deep_Research_Report.md`.
- [ ] **EXECUTE:** I have generated `{project_id}_EROLL_AUTHORIZED.md`.
- [ ] **VALIDATE:** Ancestry Check + Specificity Check passed.

**Commander Checklist (from Guide):**
- [ ] Deep Research Report exists and is complete?
- [ ] Each angle has 2-3 NAMED, VERIFIED references?
- [ ] No generic concepts (ladder, light, breakthrough)?
- [ ] Every query cites a source from the Deep Research Report?
- [ ] Queries use specific cultural terms, not script themes?

**IF PASS:** Issue `{project_id}_EROLL_AUTHORIZED.md`
**IF FAIL:** Issue `REJECTION_NOTE.md` with specific fixes

---

## STEP 7: IMAGE HUNT (EXECUTION)

#### 📋 MICRO TASK LIST: 7A_IMAGE_HUNT
- [ ] **PLAN:** I will execute 24 image downloads using the queries.
- [ ] **LOAD:** I have read `EROLL_AUTHORIZED.md` + `ERoll_Search_Queries.json`.
- [ ] **EXECUTE:** I have run `image_hunter.py` for all 24 queries.
- [ ] **VALIDATE:** 24 images downloaded to `04_assets/e-roll/`.

**Execute for all 24 queries:**
```bash
python tools/image_hunter.py \
  --query "[QUERY]" \
  --output_dir "{PROJECT}/04_assets/e-roll" \
  --scene_code "ANG{N}_{M}" \
  --project_id "{PROJECT_ID}" \
  --count 1 \
  --sources outscraper
```

**Scene Code Mapping:**
- ANG1_01 through ANG1_04 (Language)
- ANG2_01 through ANG2_04 (Aesthetics)
- ANG3_01 through ANG3_04 (Rituals)
- ANG4_01 through ANG4_04 (Heroes)
- ANG5_01 through ANG5_04 (Opposition)
- ANG6_01 through ANG6_04 (Emotional)

---

## ⛔ E-ROLL GATE

**ALL the following must exist before completion:**
- [ ] `{project_id}_ERoll_Deep_Research_Report.md`
- [ ] `{project_id}_ERoll_Search_Queries.json`
- [ ] `{project_id}_EROLL_AUTHORIZED.md`
- [ ] `04_assets/e-roll/` contains 24 images

---

## DELIVERABLES CHECKLIST

- [ ] `{project_id}_ERoll_Deep_Research_Report.md`
- [ ] `{project_id}_ERoll_Search_Queries.json`
- [ ] `{project_id}_EROLL_AUTHORIZED.md`
- [ ] 24 images in `04_assets/e-roll/` (ANG1-6 × 4 each)

---

## OUTPUT STRUCTURE

```
{PROJECT}/
├── {project_id}_ERoll_Deep_Research_Report.md
├── {project_id}_ERoll_Search_Queries.json
├── {project_id}_EROLL_AUTHORIZED.md
└── 04_assets/
    └── e-roll/
        ├── {project_id}_ANG1_01_IMG_01.jpg
        ├── {project_id}_ANG1_01_IMG_manifest.json
        └── ... (24 images + manifests)
```

---

**END OF CMF E-ROLL COMMAND (V15)**
