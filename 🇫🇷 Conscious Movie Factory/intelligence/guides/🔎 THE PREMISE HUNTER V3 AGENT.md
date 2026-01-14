# 🔎 THE PREMISE HUNTER V3 — Frame-First Protocol

## System Overview

The Premise Hunter V3 is a **Frame-First, Context-Clustered** script extraction algorithm designed to find viral potential while maintaining context and relevance. It replaces the hook-hunting approach with an intelligent content mapping system.

**Key Principle:**
> "Frames are more important than hooks. Hooks without frames create confusion. Frames with hooks create traction."

---

## Algorithm Phases

```
┌─────────────────────────────────────────────────────────────────────┐
│  PHASE 1: SOURCE ANALYSIS          (Classify & Map)                │
│  ↓                                                                   │
│  PHASE 2: FRAME DISCOVERY           (Find the Unified Message)     │
│  ↓                                                                   │
│  PHASE 3: CONTEXT CLUSTER BUILDING  (Group Related Content)        │
│  ↓                                                                   │
│  PHASE 4: VIRAL MOMENT MINING       (Find Hooks WITHIN Clusters)   │
│  ↓                                                                   │
│  PHASE 5: SCRIPT COMPOSITION        (Assemble Final Script)        │
│  ↓                                                                   │
│  PHASE 6: VALIDATION                (Score & Verify)               │
└─────────────────────────────────────────────────────────────────────┘
```

---

## PHASE 1: SOURCE ANALYSIS

### 1.1 Input Classification

For each source material, determine:

| Field | Options | Impact on Strategy |
|-------|---------|-------------------|
| **Content Type** | Testimonial, Coach Solo, Interview, Mixed | Determines quote extraction approach |
| **Speaker** | Client, Coach, Both | Affects voice consistency |
| **Source Count** | Single, Multi-Source Fusion | Determines clustering complexity |
| **Raw Length** | <10min, 10-30min, 30-60min, >60min | Affects depth of extraction |

### 1.2 Source Metadata Template

```json
{
  "sources": [
    {
      "source_id": "S1",
      "title": "Matthis Testimonial Interview",
      "content_type": "testimonial",
      "speaker": "client",
      "duration_minutes": 43,
      "language": "French",
      "key_topics": ["anxiety", "liver detox", "grief", "transformation"]
    }
  ],
  "fusion_mode": false,
  "expected_output_duration": 60
}
```

### 1.3 Extraction Strategy Decision Tree

```
IF source_count == 1:
    IF content_type == "testimonial":
        → PREFER continuous segments (natural flow)
        → ALLOW scattered if continuous unavailable
    ELIF content_type == "coach_solo":
        → ALLOW thematic extraction (jumping between topics)
    ELIF content_type == "interview":
        → ALLOW answer-hopping (scattered by design)

IF source_count > 1:
    → REQUIRE context clustering (fusion mode)
    → NO continuous segment expectation
```

---

## PHASE 2: FRAME DISCOVERY

### 2.1 The Frame Discovery Protocol

**Objective:** Before hunting for viral moments, establish the UNIFIED MESSAGE that will contextualize everything.

**Chain of Thought Prompting:**

```markdown
## Step 1: Surface Analysis
Read the entire transcript(s) and answer:
- What is the MAIN TOPIC being discussed?
- What TRANSFORMATION or INSIGHT is being described?
- Who is the PROTAGONIST of this story (coach, client, or both)?

## Step 2: Audience Alignment
Consider the TARGET AUDIENCE and answer:
- What does this audience ALREADY BELIEVE?
- What do they WANT TO HEAR?
- What PAIN are they experiencing?

## Step 3: Frame Formulation
Combine insights into a FRAME STATEMENT using this template:

"This content is about [TOPIC] which shows how [MECHANISM] leads to [OUTCOME]. 
The audience will understand that [KEY INSIGHT]."

## Step 4: Frame Validation
Score the frame (1-10) on:
- CLARITY: Is it immediately understandable? 
- RELEVANCE: Does it match audience pain?
- DIFFERENTIATION: Is this different from generic advice?
- COACH CENTRALITY: Is the coach's method visible?
```

### 2.2 Frame Examples

| Content Type | Bad Frame (Hook-First) | Good Frame (Frame-First) |
|--------------|------------------------|---------------------------|
| Matthis Testimonial | "A man dealing with grief after his father's death" | "Holistic transformation (body+mind+emotions) through Adèle's detox program" |
| Coach Philosophy | "Why you should eat differently" | "The hidden link between liver health and emotional processing" |
| Multi-Source Fusion | "Various people share struggles" | "The pattern of how chronic fatigue is actually unprocessed emotion" |

### 2.3 Frame Output

```json
{
  "frame_statement": "This content shows how Adèle's holistic detox program addresses not just physical symptoms but the emotional roots of chronic fatigue, particularly unprocessed grief stored in the liver.",
  "frame_components": {
    "topic": "Holistic health transformation",
    "mechanism": "Liver detox + emotional release",
    "outcome": "Increased energy, emotional resilience",
    "key_insight": "Physical symptoms often have emotional origins"
  },
  "frame_validation_score": {
    "clarity": 8,
    "relevance": 9,
    "differentiation": 7,
    "coach_centrality": 9,
    "total": 33,
    "max": 40
  }
}
```

---

## PHASE 3: CONTEXT CLUSTER BUILDING

### 3.1 The Five Core Clusters

Every effective short-form script needs these narrative elements:

| Cluster ID | Name | Function | Required? |
|------------|------|----------|-----------|
| C1 | **HOOK** | Pattern interrupt / Grab attention | ✅ Required |
| C2 | **PROBLEM** | Pain identification / Symptom description | ✅ Required |
| C3 | **MECHANISM** | Unique solution / Differentiator | ✅ Required |
| C4 | **PROOF** | Results / Validation / Credibility | ✅ Required |
| C5 | **CLOSE** | Call to action / Empowerment | 🟡 Optional |

### 3.2 Cluster Building Protocol

**For Each Cluster:**

```markdown
## Step 1: Quote Mining
Scan all sources for quotes that serve this cluster's FUNCTION.
Extract 3-5 candidate quotes per cluster.

## Step 2: Thematic Coherence Check
For each candidate quote, ask:
- Does this quote AMPLIFY the established FRAME?
- Does this quote SERVE the cluster's FUNCTION?
- Can this quote STAND ALONE or does it need context?

## Step 3: Quote Scoring
Score each quote (1-10) on:
- VIRAL POTENTIAL: Surprise × Emotion × Specificity
- FRAME ALIGNMENT: Does it reinforce or distract from frame?
- STANDALONE CLARITY: Understandable without surrounding context?
- FLOW POTENTIAL: Can it connect smoothly to adjacent clusters?

## Step 4: Quote Selection
Select the TOP 1-2 quotes per cluster based on scores.
```

### 3.3 Context Cluster Template

```json
{
  "cluster_id": "C2",
  "cluster_name": "PROBLEM",
  "function": "Identify the pain, describe symptoms, create recognition",
  "quotes": [
    {
      "quote_id": "Q2A",
      "text": "Moi j'suis un grand anxieux de base, j'ai toujours été très contrôlé par mon mental",
      "source_id": "S1",
      "timestamp": "3:32",
      "scores": {
        "viral_potential": 7,
        "frame_alignment": 9,
        "standalone_clarity": 8,
        "flow_potential": 8
      },
      "total_score": 32
    },
    {
      "quote_id": "Q2B",
      "text": "C'était beaucoup de fatigue chronique, fatigue dans les muscles, brouillard mental",
      "source_id": "S1",
      "timestamp": "6:12",
      "scores": {
        "viral_potential": 6,
        "frame_alignment": 9,
        "standalone_clarity": 9,
        "flow_potential": 9
      },
      "total_score": 33
    }
  ],
  "selected_quote": "Q2B",
  "selection_rationale": "Higher standalone clarity and flow potential, maintains frame without needing additional context"
}
```

---

## PHASE 4: VIRAL MOMENT MINING

### 4.1 The Viral Trinity (Within Frame)

Now that we have clusters, identify which moments have VIRAL POTENTIAL:

| Element | Definition | Score 1-20 |
|---------|------------|------------|
| **SURPRISE** | Challenges assumptions, unexpected twist | "This should make the viewer say 'Wait, what?'" |
| **EMOTION** | Visceral feeling (shame, pride, relief, fear) | "This should make the viewer FEEL something" |
| **SPECIFICITY** | Tangible, sensory, concrete details | "This uses specific numbers, names, or descriptions" |

### 4.2 Viral Moment Identification

```markdown
## For Each Cluster, Ask:

### SURPRISE CHECK
- Does this quote contain an UNEXPECTED PERSPECTIVE?
- Does it CONTRADICT common wisdom?
- Does it reveal something HIDDEN or COUNTERINTUITIVE?

### EMOTION CHECK
- What SPECIFIC EMOTION does this evoke?
- Is the emotion VISCERAL (felt in the body)?
- Is there VULNERABILITY or COURAGE displayed?

### SPECIFICITY CHECK
- Are there NUMBERS (7/10, 3 months, $500)?
- Are there NAMES or PLACES?
- Are there SENSORY DETAILS (sounds, feelings, sights)?
```

### 4.3 Viral Score Calculation

```
VIRAL_SCORE = (SURPRISE × EMOTION × SPECIFICITY) / 100

Example:
- Quote: "La détox du foie, un organe très concerné par la gestion des émotions"
- SURPRISE: 14 (liver-emotion connection is unexpected)
- EMOTION: 12 (creates curiosity, not visceral)
- SPECIFICITY: 10 (names specific organ)
- VIRAL_SCORE = (14 × 12 × 10) / 100 = 16.8

Interpretation:
- 0-10: Low viral potential (informational only)
- 10-20: Moderate potential (interesting but not shareable)
- 20-30: High potential (likely to cause engagement)
- 30+: Exceptional (likely viral element)
```

---

## PHASE 5: SCRIPT COMPOSITION

### 5.1 Cluster Assembly Order

Standard order (can be modified based on arc):

```
1. HOOK (C1)     → 0-8 seconds
2. PROBLEM (C2)  → 8-20 seconds
3. MECHANISM (C3)→ 20-35 seconds
4. PROOF (C4)    → 35-50 seconds
5. CLOSE (C5)    → 50-60 seconds
```

### 5.2 Transition Coherence

Between each cluster, verify:

```markdown
## Transition Check
For each adjacent cluster pair (C[n] → C[n+1]):
- Is there LOGICAL FLOW? (Does the next thought follow naturally?)
- Is there TONAL CONSISTENCY? (Do emotions transition smoothly?)
- Is there SPEAKER CONSISTENCY? (Same voice or clear handoff?)

If any check fails, consider:
- Adding a BRIDGE quote between clusters
- Reordering clusters
- Selecting different quote from pool
```

### 5.3 Script Output Format

```json
{
  "script_metadata": {
    "frame": "Holistic transformation through Adèle's detox program",
    "total_duration_seconds": 60,
    "source_fusion": false,
    "sonic_arc_recommendation": "1. The Core Transformation"
  },
  "script_sequence": [
    {
      "position": 1,
      "cluster": "HOOK",
      "timestamp": "0:00-0:08",
      "selected_quote": {
        "text": "Avec Adèle on travaille sur la détox, pas seulement du corps mais sur la détox de l'esprit, la détox émotionnelle",
        "source": "S1",
        "original_timestamp": "21:47"
      },
      "viral_score": 18.4,
      "scene_builder_code": "HOOK-2-B-1"
    }
  ]
}
```

---

## PHASE 6: VALIDATION

### 6.1 Final Validation Checklist

Run these checks on the completed script:

| Check | Criteria | Pass/Fail |
|-------|----------|-----------|
| **Frame Integrity** | Does every quote reinforce the established frame? | ✅/❌ |
| **Coach Presence** | Is the coach mentioned at least TWICE (open/close)? | ✅/❌ |
| **Viral Minimum** | Is there at least ONE quote with viral score >20? | ✅/❌ |
| **Flow Test** | Read aloud - does it flow naturally? | ✅/❌ |
| **Duration Check** | Is total duration 55-65 seconds? | ✅/❌ |
| **Specificity Check** | Is there at least ONE specific number/name? | ✅/❌ |

### 6.2 Quality Score Calculation

```
SCRIPT_QUALITY = (
    Frame_Integrity_Score +
    Coach_Presence_Score +
    Average_Viral_Score +
    Flow_Score +
    Specificity_Score
) / 5

Interpretation:
- 0-40: Needs major revision
- 40-60: Acceptable, minor improvements possible
- 60-80: Good quality script
- 80-100: Excellent, ready for production
```

### 6.3 Red Flags (Automatic Rejection)

If ANY of these are true, the script must be revised:

- ❌ Frame is unclear or constantly shifting
- ❌ Coach is mentioned ZERO times
- ❌ NO quote scores above 10 on viral potential
- ❌ Script opens with grief/death without context (hook-bombing)
- ❌ Total duration <50s or >70s

---

## APPENDIX A: Chain of Thought Conditioning Template

Use this template when prompting for script extraction:

```markdown
# Context
You are analyzing [SOURCE_TYPE] content from [COACH_NAME].
The target audience is [AUDIENCE_DESCRIPTION].
The goal is to create a 60-second script that [OBJECTIVE].

# Instructions
Follow this exact sequence:

## Step 1: Frame Discovery
First, read the entire transcript and identify:
- The MAIN TOPIC (what is this about?)
- The UNIQUE MECHANISM (what makes this different?)
- The TARGET EMOTION (how should viewers feel?)

Write your frame statement before proceeding.

## Step 2: Context Cluster Mapping
Identify quotes that serve each of these functions:
- HOOK: What grabs attention?
- PROBLEM: What pain is being described?
- MECHANISM: What solution is offered?
- PROOF: What results are shared?
- CLOSE: What action is encouraged?

For each quote, note the timestamp and explain why it fits.

## Step 3: Viral Scoring
For each selected quote, score:
- SURPRISE (1-20): How unexpected is this?
- EMOTION (1-20): How visceral is this?
- SPECIFICITY (1-20): How concrete is this?

Calculate: (S × E × Sp) / 100

## Step 4: Assembly
Order your selected quotes and verify:
- Does the flow feel natural?
- Is the coach present at start AND end?
- Is total duration approximately 60 seconds?

## Step 5: Final Validation
Run through the validation checklist and report your quality score.
```

---

## APPENDIX B: Multi-Source Fusion Protocol

When combining multiple sources:

### B.1 Source Weighting

```
PRIMARY_SOURCE: The main voice (typically coach or featured client)
SUPPORTING_SOURCES: Additional perspectives (other clients, experts)

Weight distribution:
- Primary: 60-70% of quotes
- Supporting: 30-40% of quotes
```

### B.2 Voice Transition Rules

```
When transitioning between speakers:
- ADD visual transition (whip pan, cut to new person)
- MAINTAIN thematic continuity
- NEVER cut mid-sentence across speakers
- PREFER natural pause points

Example of GOOD fusion:
[Coach]: "The liver stores unprocessed emotions..."
[Client A]: "I didn't believe it until..."
[Client B]: "The results were immediate..."

Example of BAD fusion:
[Coach]: "The liver..."
[Client A]: "...made me realize..."
[Client B]: "...seven kilos in..."
```

---

## APPENDIX C: Example Application - Matthis

### Input
- Single source testimonial (43 minutes)
- Speaker: Client (Matthis)
- Content Type: Testimonial interview
- Language: French

### Frame Discovery
```
FRAME: "Holistic transformation through liver detox addresses the 
emotional roots of chronic fatigue, showing how physical healing 
unlocks emotional resilience."
```

### Context Clusters Built

| Cluster | Selected Quote | Viral Score |
|---------|----------------|-------------|
| HOOK | "Avec Adèle on travaille sur la détox, pas seulement du corps..." | 18.4 |
| PROBLEM | "Moi j'suis un grand anxieux de base... fatigue chronique..." | 14.2 |
| MECHANISM | "La détox du foie, un organe très concerné par la gestion des émotions" | 16.8 |
| PROOF | "J'ai perdu mon père... ça a joué sur le fait d'accueillir cette épreuve..." | 24.6 |
| CLOSE | "Avec Adèle on peut aller loin... ce côté brut, c'est ça qui m'a plu" | 12.4 |

### Final Script Quality Score: 72/100 (Good)

---

**END OF PROTOCOL**
