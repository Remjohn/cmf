# 🔮 E-Roll Cultural DNA Research System

## **⚠️ MANDATORY WORKFLOW - NO SHORTCUTS**

> [!CAUTION]
> **DO NOT GENERATE SEARCH QUERIES WITHOUT A DEEP RESEARCH REPORT.**
> Generic queries like "ladder climbing success" or "breakthrough celebration" are FORBIDDEN.
> Every query MUST reference a VERIFIED cultural source from the Deep Research Report.

---

## **The 5-Phase Locked Workflow**

```
┌─────────────────────────────────────────────────────────────────┐
│ PHASE 1: INPUT GATHERING                                        │
│ ─────────────────────────                                       │
│ ✓ Read final_script.json                                        │
│ ✓ Read Tribe Soul Profile                                       │
│ ✓ Read Brand Avatar (if exists)                                 │
└─────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│ PHASE 2: 12 INTROSPECTION QUESTIONS                             │
│ ────────────────────────────────────                            │
│ Answer each question FROM THE CULTURAL PERSPECTIVE              │
│ NOT from the script themes                                      │
└─────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│ PHASE 3: DEEP RESEARCH (BROWSER) ★ MANDATORY ★                  │
│ ───────────────────────────────────────────────                 │
│ Use browser to find REAL, VERIFIABLE cultural references        │
│ Find: Named people, documented events, specific sources         │
│ NO AI hallucinations. REAL URLs. REAL sources.                  │
└─────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│ PHASE 4: DEEP RESEARCH REPORT                                   │
│ ─────────────────────────────                                   │
│ Output: [project_id]_ERoll_Deep_Research_Report.md              │
│ Must contain: Source URLs, Named references, Cultural context   │
│ ★ NO QUERIES UNTIL THIS REPORT IS COMPLETE ★                    │
└─────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│ PHASE 5: SEARCH QUERY GENERATION                                │
│ ────────────────────────────────                                │
│ Output: [project_id]_ERoll_Search_Queries.json                  │
│ Each query MUST cite its source from the Deep Research Report   │
└─────────────────────────────────────────────────────────────────┘
```

---

## **Phase 1: Input Gathering**

### Required Files

| File | Location | Purpose |
|------|----------|---------|
| `final_script.json` | `inputs/[Coach]/[Project]/` | Script themes to ground in culture |
| `Tribe Soul Profile` | `inputs/[Coach]/` | Cultural DNA of the audience |
| `Brand Avatar` | `inputs/[Coach]/` | Coach positioning (if exists) |

### What to Extract

**From Script:**
- Key transformation themes (e.g., "Spectator → Créateur")
- Emotional states (before/after)
- Specific words or phrases used

**From Tribe Soul Profile:**
- `tribe_slang` - Insider language codes
- `shared_heroes` - Named heroes/elders
- `common_enemies` - Documented opposition
- `inside_jokes` - Cultural humor patterns

---

## **Phase 2: The 12 Introspection Questions**

> [!IMPORTANT]
> Answer these questions about THE CULTURE, not the script.
> If your answer is generic (e.g., "ladder" instead of "Kinkeliba"), you're doing it wrong.

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
7. Who are the living or ancestral figures this audience reveres? (NAMED)
8. What archetypes (healer, warrior, mother) resonate with this tribe?

### Opposition, Wounds & Enemy
9. What systems, forces, or ideas threatened or tried to erase this culture?
10. What shared wounds or traumas bind this community together?

### Shared Emotional Truths
11. What collective emotions (pride, grief, longing, reclamation) define this tribe?
12. What future vision or aspiration unites this community?

---

## **Phase 3: Deep Research (MANDATORY)**

> [!CAUTION]
> You MUST use browser-based research to find REAL references.
> DO NOT hallucinate sources. DO NOT use generic concepts.

### Research Targets Per Angle

For each of the 6 angles, use browser to find:
- **2-3 NAMED references** (people, brands, events, works)
- **Source URLs** where you verified the reference
- **Cultural context** explaining why this resonates

### Example Deep Research Output

**ANGLE 4: Heroes & Elders**
| Reference | Source | Why It Resonates |
|-----------|--------|------------------|
| Fatima Douba | secretsdediongoma.com | Afro-holistic naturopath bridging ancestral wisdom |
| Frantz Fanon | Peau Noire Masques Blancs | Intellectual hero who named medical racism |
| Youssouf Fofana | maisonchateaurouge.com | Creator who remixed French symbols with African textiles |

**ANGLE 5: Opposition & Enemy**
| Reference | Source | Why It Resonates |
|-----------|--------|------------------|
| Syndrome Méditerranéen | France Inter article | Documented medical bias against Black patients |
| Alimentation Blanche | Afro-Cooking Magazine | The "poison fade" of European diet |

---

## **Phase 4: Deep Research Report**

### Output File
**Location:** `inputs/[Coach]/[Project]/[project_id]_ERoll_Deep_Research_Report.md`

### Required Structure

```markdown
# E-Roll Deep Research Report: [Project Name]

## Tribe Profile Summary
- Audience: [Description from Soul Profile]
- Key Cultural Codes: [From slang/heroes/enemies]

## ANGLE 1: Language, Codes & Signals
### Verified References
1. **[Reference Name]** - Source: [URL] - Relevance: [Why]
2. **[Reference Name]** - Source: [URL] - Relevance: [Why]

## ANGLE 2: Aesthetics & Symbols
### Verified References
...

[Continue for all 6 angles]

## Research Sources Used
- [URL 1]
- [URL 2]
...
```

---

## **Phase 5: Search Query Generation**

> [!IMPORTANT]
> ONLY generate queries AFTER the Deep Research Report is complete.
> EVERY query must cite its source from the report.

### Output File
**Location:** `inputs/[Coach]/[Project]/[project_id]_ERoll_Search_Queries.json`

### Required JSON Structure

```json
{
    "project_id": "[project_id]",
    "framework": "Cultural_DNA_6_Angles",
    "deep_research_conducted": true,
    "deep_research_report": "[path_to_report.md]",
    "queries": [
        {
            "angle": "ANGLE_1_LANGUAGE_CODES",
            "queries": [
                {
                    "query": "[CULTURALLY SPECIFIC QUERY]",
                    "why": "[Connection to audience identity]",
                    "source": "[From Deep Research Report]"
                }
            ]
        }
    ]
}
```

### Query Quality Checklist

| ❌ WRONG (Generic) | ✅ RIGHT (Culturally Specific) |
|-------------------|-------------------------------|
| "ladder climbing success" | "Maison Château Rouge Youssouf Fofana Bogolan" |
| "herbal cleanse detox" | "Kinkeliba thé longue vie African morning ritual" |
| "breakthrough celebration" | "S'enjailler celebration Ivorian diaspora France" |
| "divine light awakening" | "Retour aux Sources Ifa Yoruba spirituality France" |
| "man on stage performing" | "African diaspora spoken word poetry Paris performance" |
| "mental fog confusion" | "syndrome méditerranéen racisme médical France" |

---

## **The 6 Cultural Angles**

### ANGLE 1: Language, Codes & Signals
*"Who sounds like US"*

- Insider slang and greetings
- Call-and-response patterns
- Visual codes only insiders recognize
- **Example:** "S'enjailler" (Ivorian slang for resilience through joy)

### ANGLE 2: Aesthetics & Symbols
*"What looks like US"*

- Clothing, textiles, patterns
- Sacred symbols and adornments
- Cultural color palettes
- **Example:** "Bogolan mudcloth pattern" (Maison Château Rouge)

### ANGLE 3: Rituals & Behaviors
*"What we do that others don't"*

- Daily and ceremonial practices
- Preparation and cleansing rituals
- Sacred space creation
- **Example:** "Bain de feuilles with Djeka leaves"

### ANGLE 4: Heroes, Elders & Icons
*"Who represents US at our best"*

- NAMED spiritual leaders and teachers
- NAMED influencers and icons
- Ancestral figures
- **Example:** "Fatima Douba naturopathe afro-holistique"

### ANGLE 5: Opposition, Wounds & Enemy
*"What we survived or still resist"*

- Documented systems of harm
- Shared wounds and traumas
- Symbols of resistance
- **Example:** "Syndrome Méditerranéen" (France Inter documented)

### ANGLE 6: Shared Emotional Truths
*"What we feel together"*

- Pride, grief, longing, reclamation
- Future visions and aspirations
- Solidarity and community
- **Example:** "Retour aux Sources" spiritual movement

---

## **Validation Checklist**

Before generating queries, verify:

- [ ] Deep Research Report exists and is complete
- [ ] Each angle has 2-3 NAMED, VERIFIED references
- [ ] No generic concepts (ladder, light, breakthrough)
- [ ] Every query cites a source from the Deep Research Report
- [ ] Queries use specific cultural terms, not script themes

---

## **Common Mistakes to Avoid**

| Mistake | Why It's Wrong | How to Fix |
|---------|----------------|------------|
| Skipping Deep Research | Queries become generic clichés | ALWAYS use browser to verify |
| Using script themes as queries | "breakthrough triumph" has no cultural DNA | Ground in Tribe Soul Profile |
| Generic queries | "man on stage" returns random stock | Use specific: "African diaspora spoken word Paris" |
| No source citation | Can't verify cultural relevance | Every query needs source from report |
| "Fort Monroe" type sources | Wrong cultural context | Research finds RIGHT archives |

---

## **Output Files Summary**

| Phase | Output File | Description |
|-------|-------------|-------------|
| Phase 4 | `[project_id]_ERoll_Deep_Research_Report.md` | Verified cultural references |
| Phase 5 | `[project_id]_ERoll_Search_Queries.json` | 24 queries with source citations |
| Execution | `04_assets/e-roll/` | Downloaded images |

---

## **E-Roll is IMAGES ONLY**

**✅ HIGH VALUE:**
- Archival photography
- Documentary stills
- Scientific diagrams
- Book covers (named authors)
- Cultural artifacts
- Named brand imagery

**❌ LOW VALUE:**
- Random faces (stock)
- Watermarked previews
- Generic "person smiling" type
- Scene-based illustrations

**Blocked Stock Sites:** Shutterstock, Vecteezy, Dreamstime, Getty, iStock, Alamy, Depositphotos, 123RF, etc.
