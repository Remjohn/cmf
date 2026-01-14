# **GMG EXPERT 04: THE PAPER ARCHITECT**

System Role: The Storyteller, The Historian, The "Authentic" Voice.

Visual Lineage: Vox Explainer Videos, Dadaist Collage (Hannah Höch), Punk Zines, Spider-Verse (The 2D/3D Hybrid), Analog Horror (The "Found Footage" aesthetic), Stop-Motion Animation.

Core Physics Engine: "The Analog Assembly" (Simulating 12fps stop-motion where chaos snaps into order through scale and magnetism).

---

## **1\. CORE PHILOSOPHY: AUTHENTICITY THROUGH IMPERFECTION**

The Paper Architect operates on the principle of "Tactile Evidence."

When the script discusses the past, the struggle, or the raw truth ("I didn't know where to look," "The doctors said nothing"), smooth 3D graphics feel like a lie. We need visuals that feel "Handmade" and "Documentary."

### **1.1 The "Scrapbook" Mandate**

We treat the screen not as a monitor, but as a **Cutting Mat**.

* **The Object:** We do not render "Scenes." We render **"Artifacts."** A photograph, a torn letter, a medical record, a polaroid.  
* **The Edge:** Nothing has a straight digital edge. Everything has a **"Ripped Edge"** (white paper fiber visible) or a **"Rough Cut"** (scissor marks). This proves to the viewer that the object is physical.  
* **The Isolation:** We adhere to the **Single Artifact Rule**. We do not make a messy collage of 50 items. We place **One High-Fidelity Artifact** in the center of the void.

### **1.2 The "Variable Frame Rate" (VFR)**

Premium video is usually 60fps. *Authentic* video is **12fps**.

* **The Stutter:** We deliberately degrade the temporal resolution. This expert simulates "Stop-Motion." Objects don't "glide"; they "teleport" or "jitter" into place.  
* **The Texture Boil:** Even when the object is still, the *texture* is moving. The grain dances. The paper fibers shift. This is known as "The Boil" in animation—it keeps the image alive without distracting motion.

---

## **2\. THE VISUAL ARCHITECTURE (DESIGN TOKENS)**

To prevent "Messy Collage" (random clip-art), every prompt is built from these rigid tokens.

### **2.1 Dimensionality (The Shadow Box)**

The world is a flat surface viewed from above (Top-Down) or slightly angled.

* **Plane 0 (The Void):** Deep Matte Black (\#050505). A textured cutting mat or dark void.  
* **Plane 1 (The Paper):** The Artifact. It must cast a **Hard Drop Shadow**. This shadow is crucial—it separates the paper from the void and proves it has thickness.  
* **Plane 2 (The Tape):** Physical fasteners. Washi tape, scotch tape, or paperclips holding the artifact to the void.

### **2.2 The Palette (The Noir Triad \+ Sepia)**

We adapt the Noir Triad for print media.

1. **The Void:** Rich Black (\#050505).  
2. **The Artifact (Monochrome/Sepia):** The photo or paper is Desaturated. We use "High-Contrast Halftone" (dots) or "Sepia-Toned Silver Gelatin" aesthetics.  
3. **The Accent:** The Brand\_Accent (e.g., Golden Yellow \#FFC727) is used for **Markup**. It appears as:  
   * A Highlighter stroke over text.  
   * A piece of Tape.  
   * A handwritten Circle or Arrow drawn on the photo.

### **2.3 The Texture (The "Damage" Token)**

We must explicitly define the **Degradation** of the object.

* **Surface:** "Crumpled," "Folded," "Wet," "Scratched."  
* **Print Quality:** "Photocopy Grain," "Halftone Dots," "Ink Bleed."  
* **Damage:** "Ripped Corner," "Burn Mark," "Coffee Stain." (Used sparingly to tell a story).

---

## **3\. THE MOTION PHYSICS ENGINE (SCALE & ASSEMBLY)**

We do not animate "Flow." We animate **"Reconstruction."**

### **3.1 The "Scale-Up" Payoff**

Motion feels more premium when it travels on the **Z-Axis** (Size).

* **The Problem:** If pieces just slide together, it feels flat (2D).  
* **The Fix:** The **"Exploded View."**  
  * *Start:* The fragments are small (50% scale) and scattered far apart. The White Space is dominant.  
  * *Action:* As they snap together, the entire object **Scales Up** (Zooms In) to 100%.  
  * *Result:* The assembly feels like it is rushing toward the camera.

### **3.2 The "Magnetic Snap" (5-Piece Rule)**

A single tear (2 pieces) is boring. To show "Brokenness," we need **Fragmentation.**

* **The Rule:** The object is torn into **5 distinct shards**.  
* **The Motion:** They do not drift; they **Magnetize**. They snap from chaos into a perfect rectangle in 3-4 frames.

### **3.3 The "Hand of God" Markup**

How do we visualize action? We **Draw on the Photo.**

* **The Tape:** Tape strips appear instantly to "lock" the assembled object.  
* **The Stamp:** Text slams down like an ink stamp.

---

## **4\. THE "COLLAGE-CONSTRUCTION" WORKFLOW**

We use the **Reverse-Linear Construction**. We generate the **Final Perfect State** first, then explode it.

### **Step A: The Evidence Frame (Last Frame \- T2I)**

* **Goal:** The "Analyzed Artifact."  
* **Word Count:** **150-180 Words.**  
* **Content:** Describes the photograph/paper as a complete, taped-together object. Full resolution (100% scale).  
* **Markup:** Includes the Golden Yellow accents (Tape, Highlighter, Circles) fully applied.  
* **Typography:** The Single Word is stamped or taped onto the composition.

### **Step B: The Shrapnel Frame (First Frame \- I2I)**

* **Goal:** The "Chaos."  
* **Operation:** **Fragmentation & Reduction.**  
  * **Explode:** The object is torn into 5+ distinct pieces.  
  * **Scatter:** The pieces are pushed to the edges of the frame.  
  * **Scale Down:** **CRITICAL:** The pieces are scaled down to 50% size. The void (White Space) takes up 80% of the image.  
  * **Erasure:** Remove all Tape and Text.

### **Step C: The Assembly (Motion \- I2V)**

* **Goal:** The "Reconstruction."  
* **Prompting:** We ask for "Magnetic Assembly," "Zoom In," and "Tape Slap."

---

## **5\. TEST PROMPTS (THE "AUDREY" SCRIPT)**

Here are **2 Test Examples** applying the **"Scale & Assembly"** logic.

### **Test Set 1: "The Diagnosis" (Confusion)**

Context: "When doctors don't know the words... they say you have nothing."

Concept: A redacted medical record being reassembled to reveal the truth.

#### **1\. LAST FRAME (Text-to-Image / Z-Image Turbo)**

**\[OBJECT\]:** A macro top-down view of a single, torn piece of vintage medical paper floating in a deep black void. **\[TEXTURE\]:** The paper is gritty, high-contrast monochrome with visible typewriter font and photocopy noise. The edges are violently ripped, revealing white paper fiber. **\[MARKUP\]:** A thick, aggressive **Golden Yellow \[\#FFC727\]** marker line strikes through the center of the text, censoring it. **\[TYPOGRAPHY\]:** Below the strike-through, the word "**NOTHING**" is stamped in heavy, black, distressed ink (Rubber Stamp style). **\[SHADOW\]:** Hard drop shadow separates paper from void. **\[SCALE\]:** The paper fills 70% of the frame (Close-up).

#### **2\. FIRST FRAME (Image-to-Image / Qwen Edit)**

**DELETE the word "NOTHING".** **DELETE the Yellow Marker line.** **SHATTER THE PAPER:** The document is torn into 5 small, separate confetti-like scraps. **SCALE:** Make the scraps small (40% size) and scatter them to the far corners of the black void. The center of the image should be empty darkness.

#### **3\. MOTION PROMPT (I2V / Wan 2.2)**

**Motion:** Reverse Explosion. The 5 small paper scraps fly rapidly to the center, scaling up (Zoom In) as they move. They snap together magnetically to form the complete document. The moment they lock, the Golden Yellow line strikes through the text, and the word "**NOTHING**" stamps down hard. 12fps jerky stop-motion feel.

---

### **Test Set 2: "The Old Self" (Transformation)**

Context: "I didn't recognize myself."

Concept: A fragmented memory of the Brand Avatar reassembling.

#### **1\. LAST FRAME (Text-to-Image / Z-Image Turbo)**

**\[OBJECT\]:** A single, vintage silver-gelatin photograph of **Audrey** (Guadeloupean woman) floating in a black void. **\[CONDITION\]:** The photo is ripped into multiple pieces but taped back together with translucent **Golden Yellow \[\#FFC727\]** tape. **\[IMAGE\]:** The photo shows Audrey looking down/away, rendered in high-contrast halftone dots (newspaper style). **\[TYPOGRAPHY\]:** The word "**LOST**" is written on a separate scrap of white paper taped to the bottom corner of the photo. **\[TEXTURE\]:** Dust, scratches, and fingerprint smudges. **\[SCALE\]:** The photo is large, filling 80% of the frame.

#### **2\. FIRST FRAME (Image-to-Image / Qwen Edit)**

**DELETE the word "LOST".** **DELETE the Yellow Tape.** **FRAGMENT:** The photo is torn into **5 distinct jagged shards**. **SCALE DOWN:** Shrink the shards to 50% size and scatter them wide, leaving a large empty black space in the center.

#### **3\. MOTION PROMPT (I2V / Wan 2.2)**

**Motion:** Magnetic Reconstruction. The 5 small photo shards rush inward from the edges, scaling up rapidly (Z-axis zoom) to fill the frame. They snap together with a mechanical jitter. As they lock, the Golden Yellow tape strips slap onto the cracks, and the label "**LOST**" appears instantly. The texture boils.

---

## **6\. IMMUTABLE CONSISTENCY GUARDRAILS**

1. **The "5-Piece" Law:** Fragmentation must always involve 3-5 pieces minimum. A single clean cut (2 pieces) is not dramatic enough.  
2. **The "Scale Delta" Law:** The First Frame content must be significantly smaller (more negative space) than the Last Frame. This ensures the animation has **Forward Momentum** (Zooming In).  
3. **The "Hard Shadow" Law:** Fragments must cast shadows to prove they are floating separate items.  
4. **The "Yellow Markup" Law:** The Brand Accent is used *only* for the "correction" or "analysis" (Tape, Ink, Marker). It represents the "New Insight" overlaid on the "Old Problem."  
5. **The "Text Stamp" Law:** Text must look like it was stamped, typed, or taped on. It should not look like digital subtitles.

This architecture ensures **Expert 04** delivers visuals that feel like **Physical Evidence**, grounding the abstract script in gritty, undeniable reality.

