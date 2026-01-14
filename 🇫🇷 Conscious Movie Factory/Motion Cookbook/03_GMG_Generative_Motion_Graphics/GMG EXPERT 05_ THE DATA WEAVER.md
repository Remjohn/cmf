

# **GMG EXPERT 05: THE DATA WEAVER**

System Role: The Analyst, The Proof, The "Hero Object," The Product Reveal.

Visual Lineage: Apple Keynote Product Reveals, Minority Report (Pre-Cog Interface), Linear.app Landing Pages, High-End Fintech Dashboards (Robinhood/Revolut), Territory Studio FUI.

Core Physics Engine: "The Cinematic Boot-Sequence" (A structured timeline of Arrival $\\to$ Ignition $\\to$ Context).

---

## **1\. CORE PHILOSOPHY: THE "PRODUCT REVEAL"**

The Data Weaver operates on the principle of "Tangible Value."

We do not treat data or concepts as "Paperwork." We treat them as Luxury Products. Whether it is a Chart, a Battery Icon, a Shield, or a Sync Button, we film it like it is the new iPhone.

### **1.1 The "Hero Asset" Mandate**

We reject the "Full Dashboard." A screen full of numbers is noise.

* **The Constraint:** We render **One Single Key Object**.  
  * *It could be:* A Line Graph (Growth).  
  * *It could be:* A Battery (Energy).  
  * *It could be:* A Shield (Protection).  
  * *It could be:* A Chain Link (Connection).  
* **The Isolation:** This object floats in the center of the Deep Void. It has thickness, glass refraction, and casts a soft colored shadow. It is an object, not a drawing.

### **1.2 The "Dark-to-Light" Drama**

Premium aesthetics rely on **Contrast of State**.

* **State A (The Void):** The scene starts in darkness. The object is either missing or a dim silhouette.  
* **State B (The Arrival):** The object enters with momentum (Swipe In).  
* **State C (The Ignition):** The object *turns on*. It is not lit by a lamp; it **IS** the light source. The Neon Bar glows; the Glass edges catch the light.  
* **State D (The Context):** Only *after* the object is lit does the Text appear.

---

## **2\. THE VISUAL ARCHITECTURE (DESIGN TOKENS)**

To prevent "Generic UI," every prompt is built from these rigid tokens.

### **2.1 Dimensionality (The Floating Interface)**

The world is a 3D space where elements float on invisible layers.

* **Plane 0 (The Void):** Deep Matte Black (\#050505).  
* **Plane 1 (The Aura):** A soft, diffused "Ambient Blob" of the Brand Color moving slowly behind the glass. This creates the "Glow" behind the UI.  
* **Plane 2 (The Glass):** The Container. A rounded rectangle with a white frosted border and background blur.  
* **Plane 3 (The Data/Object):** The Content. Floating slightly *above* the glass (Z-axis separation).

### **2.2 The Palette (The Dark Mode Triad)**

We enforce a strict "Dark Mode" aesthetic.

1. **The Void:** Rich Black (\#050505).  
2. **The Material (Neutral):** Frosted Glass, Brushed Steel, or Dark Grey Matte Plastic.  
3. **The Signal (Brand Accent):** The Brand\_Accent (e.g., Golden Yellow \#FFC727) is used **exclusively** for the **Active State**.  
   * *The Trend Line:* Golden Yellow.  
   * *The Battery Fill:* Golden Yellow.  
   * *The Glow:* Golden Yellow.

### **2.3 The Texture (The "Retina" Token)**

We must explicitly define the **Resolution**.

* **Sharpness:** "Sub-pixel perfect," "Anti-aliased," "Retina Display."  
* **No Noise:** Unlike the other experts, this expert is **CLEAN**. No film grain. No grunge. The "Premium" feel comes from *perfection*.

---

## **3\. THE MOTION PHYSICS ENGINE (BOOT SEQUENCE)**

We do not animate "Fades." We animate **"Arrival."** We use **Explicit Timestamps** to choreograph the 3-Act structure.

### **3.1 The Sequence (Timeline)**

* **\[00:00-00:01\] The Swipe In:** The object enters the frame from the bottom or scales up from zero. It uses **"Overshoot Physics"** (it goes slightly too far and snaps back).  
* **\[00:01-00:02\] The Ignition:** The internal lights turn on. The glass catches the refraction. The Brand Accent glows.  
* **\[00:02-00:03\] The Reveal:** The Typography slides out from behind the object or types on.  
* **\[00:03-00:05\] The Float:** The object settles into a gentle, rhythmic "Sine Wave" float (up and down) to show it is alive.

### **3.2 The "Spring" Physics**

Digital objects have imaginary mass.

* **The Pop:** When a widget appears, it overshoots slightly and settles back (Elastic Interpolation).  
* **The Slide:** Panels slide in with "Friction." They start fast and end slow.

### **3.3 The "Text Interaction"**

Typography provides the Label for the Product.

* **Constraint:** **ONE KEY METRIC** or **ONE LABEL**. ("+50%", "100%", "SYNCED").  
* **Placement:** The text usually sits *below* or *inside* the object. It must be crisp, white, and sans-serif (San Francisco / Inter / Poppins).

---

## **4\. THE "REVERSE-LINEAR" WORKFLOW**

We generate the **Final Lit State** first, then turn off the lights.

### **Step A: The Product Frame (Last Frame \- T2I)**

* **Goal:** The "Result."  
* **Word Count:** **90-110 Words.**  
* **Content:** Describes the "Hero Object" in its final, fully lit state.  
* **Details:** Focus on materials (frosted glass, neon light), specific lighting (internal glow), and exact text placement.  
* **Composition:** Centered, floating, with padding on all sides.

### **Step B: The Darkroom Frame (First Frame \- I2I)**

* **Goal:** The "Void."  
* **Operation:** **Blackout.**  
  * **Remove the Object:** Or make it a very faint, dark silhouette (5% opacity).  
  * **Remove the Text:** The void is empty.  
  * **Remove the Light:** No glow. Pitch black.

### **Step C: The Sequence (Motion \- I2V)**

* **Goal:** The "Boot Up."  
* **Prompting:** Use the Timestamp Protocol to command the Swipe, The Light, and The Text.

---

## **5\. TEST PROMPTS (THE "AUDREY" SCRIPT)**

Here are **2 Test Examples** applying the **"Cinematic Boot-Sequence"** logic.

### **Test Set 1: "The Recovery" (Battery)**

Context: "I'm surprised to see I can recover in a second."

Concept: A premium "Energy Cell" booting up to 100%.

#### **1\. LAST FRAME (Text-to-Image / Z-Image Turbo)**

**\[OBJECT\]:** A macro 3D render of a "Hero Battery" widget floating in the center of a deep black void. The battery is encased in a premium frosted glass capsule with rounded corners and a brushed steel rim. **\[STATE\]:** Inside the glass, a thick vertical column of neon light is filled to the absolute top, glowing with intense **Golden Yellow \[\#FFC727\]** bioluminescence. **\[TYPOGRAPHY\]:** A crisp, bright white number "**100%**" floats directly in the center of the glowing bar, rendered in a bold geometric sans-serif font. **\[LIGHTING\]:** The internal yellow light casts a soft, volumetric glow onto the surrounding black void, highlighting the refraction in the glass edges. **\[QUALITY\]:** Retina resolution, sub-pixel perfect, Apple design aesthetic.

#### **2\. FIRST FRAME (Image-to-Image / Qwen Edit)**

**BLACKOUT:** Remove the Battery object completely. The screen is a pitch-black void. There is no light, no glass, no text. (Optionally: Leave a tiny, faint grey outline of the battery frame, 5% opacity, at the very bottom of the screen).

#### **3\. MOTION PROMPT (I2V / Wan 2.2)**

**\[00:00-00:01\]:** SWIPE IN. The glass battery widget slides up rapidly from the bottom, overshooting slightly and snapping into the center. **\[00:01-00:02\]:** IGNITION. The neon bar inside fills instantly from bottom to top with bright Golden Yellow light. **\[00:02-00:03\]:** REVEAL. The text "**100%**" pops onto the screen with a scale bounce. **\[00:03-00:05\]:** FLOAT. The fully lit battery bobs gently up and down (sine wave) while the light pulses.

---

### **Test Set 2: "The Collaboration" (Sync)**

Context: "Collaborating with a Coach... she doesn't let go."

Concept: Two distinct rings fusing into one "Unbreakable" link.

#### **1\. LAST FRAME (Text-to-Image / Z-Image Turbo)**

**\[OBJECT\]:** A high-fidelity 3D render of two interlocking metallic rings floating in a deep black void. The rings are made of polished chrome but are fused at the intersection point by a glowing band of **Golden Yellow \[\#FFC727\]** energy. **\[TYPOGRAPHY\]:** Directly below the rings, the single word "**SYNCED**" is displayed in wide, tracking-spaced white sans-serif text. **\[ATMOSPHERE\]:** The golden energy creates a "lens flare" effect that streaks horizontally across the dark background. **\[DETAILS\]:** The rings are perfectly symmetrical, floating with a shallow depth of field (blurred edges). **\[QUALITY\]:** 8K resolution, octane render, photorealistic materials, clean UI aesthetic.

#### **2\. FIRST FRAME (Image-to-Image / Qwen Edit)**

**BLACKOUT:** Remove the rings and the text. The screen is a pitch-black void. (Optionally: Two faint, dark grey rings are visible at the far left and right edges of the screen, disconnected).

#### **3\. MOTION PROMPT (I2V / Wan 2.2)**

**\[00:00-00:01\]:** CONVERGE. Two dark metallic rings fly in from the left and right edges, colliding in the center with a heavy magnetic impact. **\[00:01-00:02\]:** FUSION. The moment they touch, a blinding Golden Yellow light ignites at the connection point. **\[00:02-00:03\]:** REVEAL. The word "**SYNCED**" slides up from below the rings. **\[00:03-00:05\]:** FLOAT. The locked rings rotate slowly and bob gently in the void.

---

## **6\. IMMUTABLE CONSISTENCY GUARDRAILS**

1. **The "Boot Sequence" Law:** The animation MUST follow the order: **Position $\\to$ Light $\\to$ Text.** Never show the text before the object is lit.  
2. **The "No Spreadsheet" Law:** Never render a grid of numbers. Abstract the data into **Shapes** (Lines, Circles, Bars, Objects).  
3. **The "Rounded Corner" Law:** All UI elements must have rounded corners (Radius 20px+). Sharp corners look cheap and dated.  
4. **The "English Only" Law:** Do not let the AI generate small labels. Keep text to **Big Numbers** or **Single Words**.  
5. **The "Clean Glass" Law:** Ensure the glass texture is smooth (frosted), not cracked or dirty. Perfection is the goal.

This architecture ensures **Expert 05** delivers visuals that feel like **High-Value Product Reveals**, making the data feel like the star of the show.

