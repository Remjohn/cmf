# Scene Type → Workflow Routing Table
## C-Roll Generation Mapping

---

## Primary Routing Rules

### Rule 1: Quantitative Content → CMC
If the scene contains numeric data (ratings, scores, percentages, comparisons), 
route to CMC for deterministic visualization.

### Rule 2: Existing Assets → CGM
If the scene requires composition with existing assets (celebrities, avatars, icons), 
route to CGM for asset-based composition.

### Rule 3: Abstract Concepts → GMG
If the scene visualizes abstract ideas, metaphors, or transformations,
route to GMG for AI-generated imagery.

### Rule 4: Emotional Peaks → CAC
If the scene represents an emotional climax or ambient moment,
route to CAC for poetic cinemagraphs.

---

## Complete Routing Table

| Scene Type | Primary | Secondary | Rationale |
|------------|---------|-----------|-----------|
| `SCORE_REVEAL` | CMC | GMG | Numeric data, bar/meter animation |
| `RATING_METER` | CMC | — | Pure quantitative, 1-10 scale |
| `BEFORE_AFTER` | CMC | CGM | Comparison requires precision |
| `BODY_MAP` | CMC | CAC | Anatomical focus, could be ambient |
| `PERCENTAGE_DELTA` | CMC | — | Numeric change visualization |
| `KINETIC_DEFINITION` | CMC | CAC | Text animation, could be poetic |
| `QUOTE_CELEBRITY` | CGM | CAC | Requires celebrity cutout |
| `QUOTE_PRESENTER` | CGM | — | Requires avatar cutout |
| `ICON_HEADER` | CGM | GMG | Icon + avatar composition |
| `SPLIT_HEADER` | CGM | GMG | Real image + avatar split |
| `IMMERSIVE_PRESENTER` | CGM | — | Avatar in environment |
| `CINEMATIC_B_ROLL` | CGM | GMG | Full-frame image |
| `LIVING_PORTRAIT` | CGM | CAC | Pre-animated idle loop |
| `ABSTRACT_CONCEPT` | GMG | CAC | Pure AI visualization |
| `TRANSFORMATION` | GMG | CAC | Change/growth imagery |
| `METAPHOR_VISUAL` | GMG | CAC | Symbolic representation |
| `ENERGY_VISUALIZATION` | GMG | — | Dynamic abstract |
| `COSMIC_SCALE` | GMG | CAC | Vast perspective |
| `AMBIENT_INTERLUDE` | CAC | GMG | Breathing space |
| `EMOTIONAL_PEAK` | CAC | GMG | Climactic moment |
| `POETIC_MOMENT` | CAC | — | Pure visual poetry |
| `WATER_EMERGENCE` | CAC | — | Specific metaphor |
| `CATHEDRAL_LIGHT` | CAC | — | Specific metaphor |

---

## Decision Tree

```
                    ┌─── Contains numbers/data? ────────> CMC
                    │
                    ├─── Requires celebrity/avatar? ───> CGM
                    │
Scene Type ─────────├─── Abstract/conceptual? ─────────> GMG
                    │
                    ├─── Emotional peak/ambient? ──────> CAC
                    │
                    └─── Unclear? ─────────────────────> GMG (default)
```

---

## Output Configuration

### CMC Outputs
```
04_assets/c_roll/CMC/[PROJECT]_[SCENE]_CMC_[TEMPLATE]_[A|B].mp4
```

### CGM Outputs
```
04_assets/c_roll/CGM/[PROJECT]_[SCENE]_CGM_[ARCHETYPE]_[A|B].mp4
```

### GMG Outputs
```
04_assets/c_roll/GMG/[PROJECT]_[SCENE]_GMG_[TEMPLATE]_[A|B].mp4
```

### CAC Outputs
```
04_assets/c_roll/CAC/[PROJECT]_[SCENE]_CAC_[METAPHOR]_[A|B].mp4
```

---

## Expected Output Per Scene

| Scenario | Primary Variants | Secondary Variants | Total |
|----------|------------------|-------------------|-------|
| Primary only | 2 | 0 | 2 |
| Primary + Secondary | 2 | 2 | 4 |
| All workflows (special) | 2 | 2 + 2 + 2 | 8 |

**Standard**: 2-4 options per scene  
**Maximum**: 8 options per scene (for key moments)

---

*Version: 1.0.0*
