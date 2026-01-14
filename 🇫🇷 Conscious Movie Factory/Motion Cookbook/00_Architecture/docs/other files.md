---

# **📄 motion\_tokens.md**

\# motion\_tokens.md  
\*\*Purpose:\*\* Canonical motion vocabulary    
\*\*Status:\*\* Locked v1.0  

\---

\#\# 1\. What Is a Motion Token?

A Motion Token is a \*\*named, reusable, deterministic animation primitive\*\*.

Motion Tokens:  
\- Encapsulate animation logic  
\- Abstract timing & easing  
\- Are composable  
\- Never depend on content semantics

They are the \*\*only allowed animation units\*\* in the system.

\---

\#\# 2\. Core Principles

1\. No freeform animation  
2\. No ad-hoc keyframes  
3\. No AI-generated motion  
4\. Tokens are versioned  
5\. Tokens are predictable

\---

\#\# 3\. Motion Token Schema

\`\`\`json  
{  
  "token\_id": "FADE\_IN\_UP",  
  "version": "1.0",  
  "category": "entrance",  
  "duration\_frames": 18,  
  "easing": "easeOutCubic",  
  "properties": {  
    "opacity": \[0, 1\],  
    "translateY": \[24, 0\]  
  },  
  "constraints": {  
    "requires\_alpha": false,  
    "max\_scale": 1.0  
  }  
}

---

## **4\. Motion Token Categories**

### **4.1 Entrance**

* FADE\_IN  
* FADE\_IN\_UP  
* SLIDE\_IN\_LEFT  
* SCALE\_IN\_SOFT

### **4.2 Exit**

* FADE\_OUT  
* SLIDE\_OUT\_DOWN  
* SCALE\_OUT

### **4.3 Emphasis**

* PULSE\_SCALE  
* GLOW\_FLASH  
* UNDERLINE\_DRAW  
* BORDER\_TRACE

### **4.4 Focus / Camera**

* CAMERA\_PUSH  
* CAMERA\_PAN  
* CAMERA\_REFRAME

### **4.5 Looping / Ambient**

* FLOAT\_SLOW  
* DRIFT\_VERTICAL  
* BREATHING\_OPACITY

---

## **5\. Token Composition Rules**

Allowed:

* Sequential chaining  
* Parallel execution  
* Phase-bound execution

Forbidden:

* Token overlap without explicit grouping  
* Runtime mutation  
* Content-aware easing

---

## **6\. Timing Model**

Tokens execute in:

* Scene phases  
* Absolute frame ranges  
* Deterministic order

Tokens never calculate timing dynamically.

---

## **7\. Token Governance**

* Tokens are immutable  
* New behavior → new token version  
* Deprecated tokens remain supported

---

## **8\. Why This Matters**

Motion Tokens:

* Prevent animation drift  
* Enable reuse  
* Make debugging possible  
* Preserve brand consistency

Without tokens, automation collapses.

---

\---

\# 📄 scene\_library\_v1.md

\`\`\`markdown  
\# scene\_library\_v1.md  
\*\*Purpose:\*\* Canonical scene inventory    
\*\*Version:\*\* v1.0    
\*\*Scene Count:\*\* 16  

\---

\#\# 1\. Scene Families

Scenes are grouped by \*\*narrative function\*\*, not visuals.

\---

\#\# 2\. Storytelling Scenes

\#\#\# SCENE\_01 — CUTOUT\_METAPHOR  
\- Purpose: Symbolic storytelling  
\- Duration: 150f  
\- Core tokens: FADE\_IN, CAMERA\_PUSH, GLOW\_FLASH  
\- Inputs: 1–2 cutout images

\---

\#\#\# SCENE\_02 — BEFORE\_AFTER\_MATCH  
\- Purpose: Contrast / transformation  
\- Duration: 120f  
\- Core tokens: MATCH\_CUT, FADE\_OVERLAY  
\- Inputs: 2 images

\---

\#\#\# SCENE\_03 — ARCHETYPE\_FORESHADOW  
\- Purpose: Mythic framing  
\- Duration: 150f  
\- Core tokens: FLOAT\_SLOW, VIGNETTE\_FADE  
\- Inputs: 1 illustrated image

\---

\#\# 3\. Explainer Scenes

\#\#\# SCENE\_04 — BODY\_MAP\_FOCUS  
\- Purpose: Explain body-based concepts  
\- Duration: 150f  
\- Core tokens: CAMERA\_PUSH, REGION\_GLOW  
\- Inputs: layered body image

\---

\#\#\# SCENE\_05 — BLUEPRINT\_FLOW  
\- Purpose: Step-by-step explanation  
\- Duration: 180f  
\- Core tokens: LINE\_DRAW, TEXT\_REVEAL  
\- Inputs: 3–5 text steps

\---

\#\#\# SCENE\_06 — CHART\_REVEAL  
\- Purpose: Data storytelling  
\- Duration: 150f  
\- Core tokens: BAR\_GROW, NUMBER\_POP  
\- Inputs: numeric values

\---

\#\# 4\. Emphasis Scenes

\#\#\# SCENE\_07 — AFFIRMATION\_WORD  
\- Purpose: Emotional anchor  
\- Duration: 120f  
\- Core tokens: FADE\_IN, GLOW\_SOFT  
\- Inputs: single word

\---

\#\#\# SCENE\_08 — MISCONCEPTION\_TRUTH  
\- Purpose: Paradigm shift  
\- Duration: 150f  
\- Core tokens: TEXT\_STRIKE, COVER\_REVEAL  
\- Inputs: 2 text layers

\---

\#\#\# SCENE\_09 — KINETIC\_NUMBER  
\- Purpose: Impact statistic  
\- Duration: 90f  
\- Core tokens: SCALE\_POP, IMPACT\_SHAKE  
\- Inputs: number \+ label

\---

\#\# 5\. Social / Meme Scenes

\#\#\# SCENE\_10 — QUIZ\_OVERLAY  
\- Purpose: Engagement  
\- Duration: 150f  
\- Core tokens: OPTION\_POP, HIGHLIGHT\_CORRECT  
\- Inputs: question \+ answers

\---

\#\#\# SCENE\_11 — POLL\_CARD  
\- Purpose: Interaction prompt  
\- Duration: 120f  
\- Core tokens: SLIDE\_IN, BAR\_FILL  
\- Inputs: poll options

\---

\#\# 6\. Avatar / Presence Scenes

\#\#\# SCENE\_12 — BRAND\_AVATAR\_FLOAT  
\- Purpose: Authority presence  
\- Duration: 150f  
\- Core tokens: FLOAT\_SLOW, CAMERA\_PUSH  
\- Inputs: avatar cutout

\---

\#\#\# SCENE\_13 — QUOTE\_CARD  
\- Purpose: Credibility  
\- Duration: 150f  
\- Core tokens: FADE\_IN, UNDERLINE\_DRAW  
\- Inputs: quote \+ author

\---

\#\#\# SCENE\_14 — FUTURE\_SELF  
\- Purpose: Aspirational framing  
\- Duration: 150f  
\- Core tokens: GLOW\_RIM, CAMERA\_SLOW\_PUSH  
\- Inputs: cutout portrait

\---

\#\# 7\. Montage Scenes

\#\#\# SCENE\_15 — RHYTHMIC\_ABSTRACT  
\- Purpose: Energy build  
\- Duration: 120f  
\- Core tokens: BEAT\_CUT, GLITCH\_FLASH  
\- Inputs: 4–6 clips

\---

\#\#\# SCENE\_16 — DREAM\_STATE  
\- Purpose: Vision casting  
\- Duration: 180f  
\- Core tokens: DISSOLVE\_LONG, SPEED\_RAMP\_SOFT  
\- Inputs: cinematic B-roll

\---

---

\# 📄 brand\_kit\_schema.md

\`\`\`markdown  
\# brand\_kit\_schema.md  
\*\*Purpose:\*\* Brand consistency contract    
\*\*Status:\*\* Required  

\---

\#\# 1\. What Is a Brand Kit?

A Brand Kit defines \*\*visual constraints\*\*, not aesthetics.

It limits choice to preserve identity.

\---

\#\# 2\. Brand Kit Schema

\`\`\`json  
{  
  "brand\_id": "coach\_alpha",

  "colors": {  
    "primary": "\#00FFD1",  
    "secondary": "\#1B1B1B",  
    "accent": "\#FFD700"  
  },

  "fonts": {  
    "headline": "Inter-Bold",  
    "body": "Inter-Regular",  
    "number": "SpaceGrotesk-Bold"  
  },

  "motion\_preferences": {  
    "intensity": "medium",  
    "camera\_usage": "allowed",  
    "glow\_allowed": true  
  },

  "backgrounds": {  
    "default": "dark\_gradient",  
    "alternatives": \["grid", "blur"\]  
  }  
}

---

## **3\. Enforcement Rules**

* Scenes must consume brand tokens  
* No hardcoded colors  
* No font overrides  
* Motion intensity respected

---

## **4\. Brand Compatibility Layer**

Scene \+ Brand Kit must be compatible:

* If not → fallback variant  
* Never auto-adjust silently

---

## **5\. Versioning**

Brand Kits are versioned.  
Scenes declare compatibility ranges.

---

## **6\. Why This Matters**

Without Brand Kits:

* Automation destroys identity  
* Output feels generic  
* Clients churn

With them:

* Every scene feels intentional  
* Scale doesn’t dilute quality

---

# **1\. Why the current “quiz template” is weak**

The quiz scenes we listed before fail because they:

* Assume **static attention** (viewer reads)  
* Assume **answers are known upfront**  
* Are **UI-centric**, not *human-centric*  
* Ignore **performance, reaction, hesitation, social proof**

Goal.com–style content works because:

* The **human is the focal point**  
* Graphics *react* to what the human says  
* The animation feels like **broadcast graphics**, not “quiz cards”

So we need to redefine the category entirely.

---

# **2\. Correct category: “Live Response Overlay Scenes”**

This is NOT a quiz.

This is a **response visualization scene**.

Think:

* Interviews  
* Ratings  
* Progress check-ins  
* Confidence scores  
* Before/after self-assessment  
* Opinion meters

These are **post-hoc animated explainers**, not interactive quizzes.

---

# **3\. New Scene Family (replace Quiz / Poll)**

## **🎤 RESPONSE & PROGRESS SCENES (NEW FAMILY)**

These scenes assume:

* A-roll already exists (interview, talking head, street response)  
* We **visualize meaning**, not ask questions  
* Timing is driven by **speech beats**, not UI steps

This aligns perfectly with Motion Canvas.

---

# **4\. Canonical High-Performance Scene Types (Goal.com style)**

I’ll give you **6 strong replacements**, all reusable for coaches.

---

## **SCENE A — RATING METER (1–10)**

### **Example**

Client says:  
“I’d say I’m at a 7 right now.”

### **Visual**

* Horizontal or circular scale (1–10)  
* Needle / fill animates **to 7**  
* Number pops last  
* Subtle glow at current level

### **Why it works**

* Visualizes progress instantly  
* Feels broadcast-grade  
* Extremely reusable

### **Motion Canvas strengths used**

* Deterministic number animation  
* Smooth easing  
* Emphasis tokens

---

## **SCENE B — BEFORE / AFTER SELF-SCORE**

### **Example**

“Before coaching I was a 3\. Now I’m an 8.”

### **Visual**

* Split scale  
* Left side fills to 3 (muted color)  
* Right side fills to 8 (brand color)  
* Divider slides between

### **Emotion**

Transformation, proof, credibility

---

## **SCENE C — CONFIDENCE BAR (LIVE REVEAL)**

### **Example**

“How confident do you feel right now?”

Client answers verbally.

### **Visual**

* Bar starts empty  
* Fills slowly while they speak  
* Locks at final value

This **tracks human pacing**, not UI timing.

---

## **SCENE D — REACTION EMPHASIS (QUOTE \+ EMPHASIS)**

### **Example**

“That changed everything for me.”

### **Visual**

* Key phrase extracted  
* Animated underline or glow  
* Subtle zoom on speaker cutout  
* No “quiz” UI at all

This is closer to Vox / MagnetsMedia.

---

## **SCENE E — PROGRESS DELTA (▲ \+3, \+5)**

### **Example**

“I improved by 4 points.”

### **Visual**

* Old value → new value  
* Delta badge floats up (+4)  
* Color-coded improvement

Extremely powerful for coaches.

---

## **SCENE F — CONSENSUS STACK (MULTIPLE PEOPLE)**

### **Example**

3–5 interview clips:  
“7”  
“8”  
“6”

### **Visual**

* Vertical stack of numbers  
* Average animates at end  
* “Avg: 7.0” emphasized

This is **Goal.com DNA**.

---

# **5\. Why this fits your system perfectly**

These scenes:

✅ Are **rigid** in structure  
✅ Are **parameterized**  
✅ Are **semantic**, not interactive  
✅ Require no guessing from AI  
✅ Feel premium and editorial

They’re also:

* 100% deterministic  
* 100% reusable  
* 100% brand-safe

---

# **6\. How Motion Canvas shines here (specifically)**

Motion Canvas is excellent at:

* **Numeric interpolation**  
* **Meter / bar animation**  
* **Camera push synced to beats**  
* **Layered overlays on A-roll**  
* **Broadcast-style motion systems**

This is *exactly* what Vox / Goal / MagnetsMedia do:

Simple graphics, perfect timing, strong hierarchy.

No generative video needed.

---

# **7\. Revised Scene Taxonomy (important)**

Replace:  
❌ Quiz scenes  
❌ Poll scenes

With:  
✅ Response Visualization Scenes  
✅ Progress & Rating Scenes  
✅ Interview Overlay Scenes

These are **editorial graphics**, not quizzes.

---

# **8\. Updated “Top 16 Scenes” (corrected)**

I’ll only list the **relevant ones** here:

1. Rating Meter (1–10)  
2. Before / After Score  
3. Confidence Bar  
4. Progress Delta  
5. Reaction Emphasis  
6. Consensus Stack  
7. Blueprint Explainer  
8. Body Map Focus  
9. Cutout Metaphor  
10. Misconception → Truth  
11. Affirmation Word  
12. Quote Card  
13. Brand Avatar Float  
14. Future Self Portrait  
15. Rhythmic Abstract  
16. Dream State Montage

This list is **far stronger commercially**.

---

# **9\. Key insight (this is important)**

You are not building:

“Quiz animations”

You are building:

**Editorial response graphics for short-form video**

That’s why Goal.com, Vox, MagnetsMedia win.

They don’t ask viewers to think.  
They **show meaning instantly**.

---

## **If you want next**

I strongly recommend we:

1. Rewrite the quiz scenes in `scene_library_v1.md`  
2. Define **Rating / Meter motion tokens**  
3. Create a **Response Scene Schema**  
4. Map **speech beats → animation triggers**

Say the word and we’ll lock that layer properly.

Absolutely — below is a **clean, production-grade rewrite** of the quiz-related parts of `scene_library_v1.md`, replacing weak “quiz / poll” scenes with **editorial, Goal.com–style response visualization scenes**.

This rewrite **preserves the integrity of the library** while upgrading it to something that actually performs in real content pipelines.

---

## **🔁 REWRITE — `scene_library_v1.md` (Quiz / Poll Section)**

### **❌ REMOVE (deprecated)**

The following scenes are **deprecated** and should be removed from v1:

* `SCENE_10 — QUIZ_OVERLAY`  
* `SCENE_11 — POLL_CARD`

Reason:

These scenes are UI-driven, attention-fragile, and misaligned with interview-based, coach-centric content. They do not map well to editorial motion graphics standards (Goal.com, Vox, MagnetsMedia).

---

## **✅ ADD — RESPONSE & PROGRESS SCENES (New Family)**

### **5\. Response & Progress Scenes**

**Purpose:** Visualize human answers, progress, confidence, and transformation in interview and testimonial content.

These scenes assume:

* A-roll (interview / talking head / street response) already exists  
* Graphics **react to meaning**, not interaction  
* Timing aligns with speech beats, not UI steps

---

### **SCENE\_10 — RATING\_METER\_1\_TO\_10**

**Purpose:**  
Visualize a self-reported score (progress, confidence, clarity, satisfaction).

**Duration:** 120–150 frames

**Core Motion Tokens:**

* METER\_FILL\_SMOOTH  
* NUMBER\_POP\_SOFT  
* GLOW\_ACCENT\_HOLD

**Inputs:**

* `rating_value` (1–10)  
* `label` (optional, e.g. “Confidence”)  
* `orientation` (horizontal | circular)

**Visual Description:**  
A clean broadcast-style scale animates from 0 to the reported value.  
The number appears last, locking attention.

**Primary Use Cases:**

* Client check-ins  
* Progress testimonials  
* Self-assessment clips

---

### **SCENE\_11 — BEFORE\_AFTER\_SELF\_SCORE**

**Purpose:**  
Demonstrate transformation using self-reported before/after scores.

**Duration:** 150 frames

**Core Motion Tokens:**

* SPLIT\_REVEAL  
* METER\_FILL\_DELAYED  
* DELTA\_HIGHLIGHT

**Inputs:**

* `before_value` (1–10)  
* `after_value` (1–10)  
* `metric_label` (e.g. “Confidence”)

**Visual Description:**  
Two scales or meters appear sequentially:

* “Before” fills first (muted)  
* “After” fills second (brand color)  
  A delta indicator reinforces improvement.

**Primary Use Cases:**

* Coaching results  
* Case studies  
* Sales proof clips

---

### **SCENE\_12 — CONFIDENCE\_BAR\_LIVE\_REVEAL**

**Purpose:**  
Visualize confidence or certainty while a subject speaks.

**Duration:** 120–150 frames

**Core Motion Tokens:**

* BAR\_FILL\_PROGRESSIVE  
* HOLD\_AND\_LOCK  
* SOFT\_GLOW\_PULSE

**Inputs:**

* `final_value` (1–10)  
* `label` (e.g. “How confident do you feel?”)

**Visual Description:**  
The bar fills gradually, mimicking the rhythm of speech, then locks at the final value.

**Primary Use Cases:**

* Interviews  
* Reflection moments  
* Emotional beats

---

### **SCENE\_13 — PROGRESS\_DELTA\_BADGE**

**Purpose:**  
Highlight the magnitude of improvement or change.

**Duration:** 90–120 frames

**Core Motion Tokens:**

* NUMBER\_TRANSITION  
* DELTA\_POP\_UP  
* IMPACT\_EMPHASIS

**Inputs:**

* `start_value`  
* `end_value`  
* `delta_unit` (points, %, steps)

**Visual Description:**  
The old value transitions to the new value, followed by a floating delta badge (e.g. “+4”).

**Primary Use Cases:**

* Testimonials  
* Program results  
* Quick proof beats

---

### **SCENE\_14 — REACTION\_EMPHASIS\_QUOTE**

**Purpose:**  
Emphasize a powerful spoken phrase or reaction.

**Duration:** 120–150 frames

**Core Motion Tokens:**

* TEXT\_HIGHLIGHT\_DRAW  
* CAMERA\_PUSH\_SUBTLE  
* UNDERLINE\_TRACE

**Inputs:**

* `highlight_phrase`  
* `speaker_name` (optional)

**Visual Description:**  
Key words from the spoken sentence appear as kinetic typography, subtly synced with the speaker’s presence.

**Primary Use Cases:**

* Emotional reactions  
* Breakthrough statements  
* Memorable soundbites

---

### **SCENE\_15 — CONSENSUS\_SCORE\_STACK**

**Purpose:**  
Show collective agreement or average sentiment from multiple people.

**Duration:** 150–180 frames

**Core Motion Tokens:**

* STACK\_REVEAL  
* NUMBER\_POP\_STAGGER  
* AVERAGE\_EMPHASIS

**Inputs:**

* `scores[]` (array of 3–6 values)  
* `metric_label`  
* `show_average` (boolean)

**Visual Description:**  
Scores appear sequentially in a vertical or radial stack.  
An average score animates in last.

**Primary Use Cases:**

* Street interviews  
* Group testimonials  
* Social proof content

---

### **SCENE\_16 — RESPONSE\_CALLOUT\_LOWER\_THIRD**

**Purpose:**  
Editorial-style annotation of an interview response.

**Duration:** 90–120 frames

**Core Motion Tokens:**

* LOWER\_THIRD\_SLIDE  
* TEXT\_REVEAL\_SOFT  
* HOLD\_STABLE

**Inputs:**

* `response_text`  
* `context_label` (e.g. “Client Feedback”)

**Visual Description:**  
A clean lower-third callout appears, framing the response without distracting from the speaker.

**Primary Use Cases:**

* Interviews  
* Documentary-style shorts  
* Authority-building content

---

## **🔑 Why This Rewrite Is Strong**

These scenes:

* Feel **broadcast-grade**, not templated  
* Center **human responses**, not UI interaction  
* Are perfect for **coaching, testimonials, interviews**  
* Map cleanly to **Motion Canvas strengths**  
* Are deterministic and reusable

This is **Goal.com / Vox / MagnetsMedia DNA**, not TikTok gimmicks.

---

Perfect — below are **fully updated, canonical rewrites** of the three documents you requested.  
These are **drop-in replacements**, not patches.

They explicitly support **Goal.com / Vox / interview-driven graphics**, while preserving determinism.

---

# **📄 motion\_tokens.md (UPDATED)**

\# motion\_tokens.md  
\*\*Purpose:\*\* Canonical motion vocabulary    
\*\*Status:\*\* Locked v1.1 (Response Visualization Enabled)

\---

\#\# 1\. Definition

A Motion Token is a \*\*deterministic, reusable animation primitive\*\* that encodes  
how something moves — never \*what\* it represents.

Tokens:  
\- Are authored once  
\- Are versioned  
\- Are composable  
\- Never depend on semantics, content, or AI inference

\---

\#\# 2\. Core Principles (Unchanged)

1\. No freeform animation  
2\. No AI-generated motion  
3\. No runtime mutation  
4\. All motion is declarative  
5\. All motion is reviewable

\---

\#\# 3\. Motion Token Schema

\`\`\`json  
{  
  "token\_id": "METER\_FILL\_SMOOTH",  
  "version": "1.0",  
  "category": "quantitative",  
  "duration\_frames": 30,  
  "easing": "easeOutCubic",  
  "properties": {  
    "fill\_ratio": \[0, "\<TARGET\>"\]  
  },  
  "constraints": {  
    "min\_target": 0,  
    "max\_target": 1  
  }  
}

`<TARGET>` is resolved **before render**, never during animation.

---

## **4\. Token Categories (Expanded)**

### **4.1 Entrance**

* FADE\_IN  
* FADE\_IN\_UP  
* SLIDE\_IN\_LEFT  
* LOWER\_THIRD\_SLIDE

---

### **4.2 Exit**

* FADE\_OUT  
* SLIDE\_OUT\_DOWN

---

### **4.3 Emphasis**

* PULSE\_SCALE  
* GLOW\_FLASH  
* UNDERLINE\_TRACE  
* IMPACT\_SHAKE\_SOFT

---

### **4.4 Camera**

* CAMERA\_PUSH\_SUBTLE  
* CAMERA\_SLOW\_PUSH  
* CAMERA\_REFRAME

---

### **4.5 Ambient / Loop**

* FLOAT\_SLOW  
* DRIFT\_VERTICAL  
* BREATHING\_OPACITY

---

## **5\. Quantitative / Editorial Tokens (NEW)**

These tokens power **Goal.com–style response graphics**.

---

### **METER\_FILL\_SMOOTH**

* Animates a scale or meter to a target value  
* Linear spatial motion, eased temporally

---

### **BAR\_FILL\_PROGRESSIVE**

* Gradual bar fill aligned to speech beats  
* Supports pause and lock

---

### **NUMBER\_POP\_SOFT**

* Final number reveal  
* Slight scale \+ opacity emphasis

---

### **DELTA\_POP\_UP**

* Floating delta indicator (e.g. \+4)  
* Vertical rise \+ fade

---

### **STACK\_REVEAL\_STAGGER**

* Sequential reveal of multiple numeric values  
* Used for consensus stacks

---

### **AVERAGE\_EMPHASIS**

* Highlights derived value (mean, median)  
* Glow \+ scale emphasis

---

## **6\. Token Composition Rules**

Allowed:

* Sequential chaining (e.g. fill → number pop)  
* Parallel execution (e.g. bar fill \+ glow)  
* Phase-bound execution

Forbidden:

* Overlapping quantitative tokens on same layer  
* Dynamic retiming  
* Conditional easing

---

## **7\. Speech Alignment Compatibility**

Certain tokens are **speech-aligned capable**:

Speech-aligned compatible tokens:

* BAR\_FILL\_PROGRESSIVE  
* METER\_FILL\_SMOOTH  
* NUMBER\_POP\_SOFT

They may accept:

* `start_frame`  
* `lock_frame`

But **never** calculate them internally.

---

## **8\. Governance**

* Tokens are immutable  
* Any behavioral change \= new version  
* Deprecated tokens remain renderable

---

## **9\. Why This Matters**

These additions enable:

* Interview overlays  
* Progress visualization  
* Broadcast-style graphics

Without sacrificing determinism.

---

\---

\# 📄 scene\_schema.md (UPDATED)

\`\`\`markdown  
\# scene\_schema.md  
\*\*Purpose:\*\* Formal definition of a Scene    
\*\*Status:\*\* Canonical v1.1 (Speech-Aligned)

\---

\#\# 1\. Scene Definition (Unchanged)

A Scene is a \*\*fixed motion structure\*\* with parameterized content.

\---

\#\# 2\. New Concept: Timing Modes

Scenes now declare a \*\*timing mode\*\*.

\`\`\`json  
"timing\_mode": "absolute"

---

## **3\. Supported Timing Modes**

### **3.1 ABSOLUTE (Default)**

* Fixed frame ranges  
* Fully deterministic  
* No dependency on audio

Used for:

* Explainers  
* Charts  
* Blueprint scenes

---

### **3.2 SPEECH\_ALIGNED (NEW)**

Used when:

* Scene overlays interview A-roll  
* Motion should align with spoken response

Key properties:

* Motion start/end frames are **externally provided**  
* Scene structure remains rigid  
* Animation does NOT analyze audio

---

## **4\. Speech-Aligned Scene Schema**

{  
  "scene\_id": "RATING\_METER\_1\_TO\_10",  
  "version": "1.1",  
  "duration\_frames": 150,  
  "fps": 30,

  "timing\_mode": "speech\_aligned",

  "speech\_hooks": {  
    "start\_anchor": "response\_start",  
    "lock\_anchor": "response\_end"  
  },

  "zones": {  
    "overlay": { "x": 0.1, "y": 0.75, "w": 0.8, "h": 0.15 }  
  },

  "allowed\_components": \[  
    "Meter",  
    "NumericLabel",  
    "GlowEffect"  
  \],

  "motion\_preset": "RATING\_METER\_V1"  
}

---

## **5\. Speech Hooks**

Speech hooks are **labels**, not logic.

Examples:

* response\_start  
* response\_peak  
* response\_end

They are resolved **before render**.

---

## **6\. Validation Rules (Expanded)**

Speech-aligned scenes must:

* Receive resolved frame anchors  
* Fall back to absolute timing if unavailable  
* Never access raw audio

---

## **7\. Why This Matters**

This allows:

* Human-paced graphics  
* Interview overlays  
* Editorial feel

Without compromising determinism.

---

\---

* 

---

\---

\# 📄 speech\_anchor\_taxonomy.md

\`\`\`markdown  
\# speech\_anchor\_taxonomy.md  
\*\*Purpose:\*\* Canonical temporal anchor vocabulary    
\*\*Status:\*\* Locked v1.0  

\---

\#\# 1\. Definition

Speech Anchors are \*\*named temporal markers\*\* extracted from spoken audio.

They:  
\- Represent timing only  
\- Contain no semantic meaning  
\- Are resolved before render

\---

\#\# 2\. Anchor Design Rules

1\. Anchors are labels, not logic  
2\. Anchors are monotonic  
3\. Anchors are optional  
4\. Anchors never overlap meaningfully

\---

\#\# 3\. Core Anchor Types

\#\#\# response\_start  
First audible speech onset.

\---

\#\#\# response\_peak  
Point of maximum emphasis or energy.

\---

\#\#\# response\_end  
End of the spoken response.

\---

\#\#\# pause\_mid  
Notable silence inside a response.

\---

\#\#\# hesitation  
Detectable verbal hesitation (um, uh).

(Used sparingly.)

\---

\#\# 4\. Extended Anchors (Optional)

\#\#\# escalation\_point  
Where speech accelerates or intensifies.

\---

\#\#\# resolution\_point  
Where speaker concludes thought emotionally.

\---

\#\# 5\. Anchor Output Schema

\`\`\`json  
{  
  "anchors": {  
    "response\_start": 38,  
    "response\_peak": 74,  
    "response\_end": 121  
  }  
}

Frames are relative to scene duration.

---

## **6\. Usage Rules**

* Scenes may request anchors  
* Anchors must be resolved or ignored  
* No scene may require more than 3 anchors

---

## **7\. Why This Matters**

This taxonomy:

* Enables human-paced motion  
* Avoids emotional inference  
* Preserves deterministic animation

---

\---

\# 📄 interview\_scene\_variants.md

\`\`\`markdown  
\# interview\_scene\_variants.md  
\*\*Purpose:\*\* Canonical interview overlay patterns    
\*\*Status:\*\* v1.0  

\---

\#\# 1\. Design Philosophy

Interview scenes:  
\- Serve the speaker  
\- Visualize meaning, not performance  
\- Enhance clarity without distraction

\---

\#\# 2\. Variant Categories

\---

\#\# 3\. Rating & Progress Variants

\#\#\# VARIANT\_A — SINGLE\_SCORE  
\- Meter fills once  
\- Number locks at end  
\- Used for quick check-ins

\---

\#\#\# VARIANT\_B — BEFORE\_AFTER  
\- Two sequential meters  
\- Delta emphasized  
\- Used for transformation stories

\---

\#\#\# VARIANT\_C — LIVE\_FILL  
\- Progressive fill during speech  
\- Locks at response\_end

\---

\#\# 4\. Reaction & Emphasis Variants

\#\#\# VARIANT\_D — KEY\_PHRASE  
\- Extracted phrase appears  
\- Underline or glow  
\- Synced to response\_peak

\---

\#\#\# VARIANT\_E — LOWER\_THIRD\_CALLOUT  
\- Editorial annotation  
\- Minimal motion  
\- Used in documentary tone

\---

\#\# 5\. Social Proof Variants

\#\#\# VARIANT\_F — CONSENSUS\_STACK  
\- Multiple scores  
\- Average emphasized  
\- Used for street interviews

\---

\#\#\# VARIANT\_G — DELTA\_ONLY  
\- Shows improvement only  
\- Minimal context  
\- High-impact beat

\---

\#\# 6\. Scene Selection Guidelines

| Content Type | Preferred Variant |  
|------------|------------------|  
| Testimonials | BEFORE\_AFTER |  
| Interviews | LIVE\_FILL |  
| Street Vox | CONSENSUS\_STACK |  
| Emotional Beats | KEY\_PHRASE |  
| Authority Content | LOWER\_THIRD |

\---

\#\# 7\. Why This Matters

These variants allow:  
\- Editorial flexibility  
\- Strong pacing  
\- Brand-safe reuse

Without fragmenting the scene library.

\---

---

# **📦 FULL DOCUMENT INVENTORY (Production Readiness)**

### **Core Architecture**

* ✅ architecture.md  
* ✅ scene\_schema.md  
* ✅ layer\_graph\_schema.md

### **Motion System**

* ✅ motion\_tokens.md  
* ✅ quantitative\_component\_library.md

### **Scene System**

* ✅ scene\_library\_v1.md  
* ✅ interview\_scene\_variants.md

### **AI Governance**

* ✅ agent\_contracts.md  
* ✅ speech\_anchor\_taxonomy.md

### **Brand & Styling**

* ✅ brand\_kit\_schema.md

### **Conceptual Completeness**

You now have:

* Deterministic motion  
* Safe AI boundaries  
* Scene reuse  
* Speech-aligned overlays  
* Brand enforcement  
* Editorial-grade output

**Yes — you are ready to start production.**

No missing foundational documents.

---

# **🧠 Pillow & SAM 3 — Necessary or Not?**

## **Pillow (Python Imaging Library)**

### **Verdict: OPTIONAL (Utility Only)**

Use Pillow only for:

* Image resizing  
* Cropping  
* Format normalization  
* Simple alpha cleanup

Do **not** use Pillow for:

* Layer extraction  
* Semantic segmentation  
* Anything “intelligent”

It’s a **support tool**, not a core dependency.

---

## **SAM 3 (Segment Anything Model)**

### **Verdict: USEFUL, NOT REQUIRED FOR v1**

SAM 3 is valuable for:

* Body maps  
* Complex diagrams  
* Organic shapes  
* Maps, anatomy, illustrations

But:

* Qwen Image Layered already covers most needs  
* Many scenes only require **manual or AI-assisted cutouts**  
* Over-reliance increases infra complexity

### **Recommendation:**

* Support SAM 3 as an **optional enhancement**  
* Gate it behind:  
  * “complex image” detection  
  * Or explicit scene requirements

---

Perfect.  
These three documents **close the loop** between design, engineering, QA, and scale economics.

Below are **fully written, production-grade specs** you can drop straight into your repo.

---

# **📄 motion\_canvas\_component\_library.md**

\# motion\_canvas\_component\_library.md  
\*\*Purpose:\*\* Canonical Motion Canvas component inventory    
\*\*Status:\*\* Locked v1.0  

\---

\#\# 1\. Definition

Components are \*\*renderable building blocks\*\* implemented in Motion Canvas.

They:  
\- Consume Layer Graph data  
\- Accept motion tokens  
\- Enforce spatial constraints  
\- Contain no AI logic

\---

\#\# 2\. Component Design Rules

1\. One visual responsibility per component  
2\. No implicit animation  
3\. All motion via tokens  
4\. Responsive to container size  
5\. Deterministic render only

\---

\#\# 3\. Core Component Inventory

\---

\#\#\# 3.1 ImageLayer

\*\*Purpose:\*\*    
Render RGBA image layers.

\*\*Props:\*\*  
\- src  
\- bbox  
\- opacity  
\- scale

\---

\#\#\# 3.2 CutoutLayer

\*\*Purpose:\*\*    
Render subject cutouts with optional glow or outline.

\*\*Props:\*\*  
\- src  
\- outline\_color  
\- glow\_strength

\---

\#\#\# 3.3 TextBlock

\*\*Purpose:\*\*    
Render headline or body text.

\*\*Props:\*\*  
\- text  
\- font  
\- align  
\- max\_lines

\---

\#\#\# 3.4 NumericLabel

\*\*Purpose:\*\*    
Render numbers with strong hierarchy.

\*\*Props:\*\*  
\- value  
\- format  
\- unit

\---

\#\#\# 3.5 Meter

\*\*Purpose:\*\*    
Render horizontal or circular meters.

\*\*Props:\*\*  
\- value\_range  
\- current\_value  
\- orientation

\---

\#\#\# 3.6 ProgressBar

\*\*Purpose:\*\*    
Render progressive bars.

\*\*Props:\*\*  
\- current\_value  
\- max\_value

\---

\#\#\# 3.7 DeltaBadge

\*\*Purpose:\*\*    
Render improvement indicators.

\*\*Props:\*\*  
\- delta\_value  
\- polarity

\---

\#\#\# 3.8 StackGroup

\*\*Purpose:\*\*    
Render stacked values or labels.

\*\*Props:\*\*  
\- values\[\]  
\- layout

\---

\#\#\# 3.9 GlowEffect

\*\*Purpose:\*\*    
Visual emphasis without motion.

\*\*Props:\*\*  
\- color  
\- intensity

\---

\#\#\# 3.10 CameraRig

\*\*Purpose:\*\*    
Global camera transformations.

\*\*Props:\*\*  
\- zoom  
\- pan  
\- anchor

\---

\#\# 4\. Composition Rules

\- Components may be nested  
\- Parent controls layout  
\- Children inherit transforms  
\- CameraRig applies last

\---

\#\# 5\. Performance Constraints

\- No component may trigger re-layout per frame  
\- No dynamic font loading at runtime  
\- All assets preloaded

\---

\#\# 6\. Why This Matters

This library:  
\- Makes Motion Canvas predictable  
\- Simplifies debugging  
\- Enables scale  
\- Keeps animation reviewable

\---

