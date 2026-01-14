# **extending\_scenes\_guide.md**

**Purpose:** Developer guide for creating new scenes  
 **Status:** Canonical v1.0

---

## **1\. Overview**

This guide walks through creating a new scene from scratch.

**Time Estimate:** 2-4 hours for simple scene, 6-10 hours for complex

---

## **2\. Prerequisites**

Before creating a new scene, ensure you have:

* ✅ Motion Canvas project set up  
* ✅ Familiarity with TypeScript/React  
* ✅ Understanding of scene schema  
* ✅ Reviewed existing scenes

---

## **3\. Step-by-Step Process**

### **Step 1: Define Scene Concept**

**Questions to answer:**

1. What explainer/storytelling function does this serve?  
2. What parameters will it accept?  
3. What components does it need?  
4. What motion tokens will it use?  
5. How long should it be?

**Example: PERCENTAGE\_RING scene**

* **Function:** Visualize completion percentage  
* **Parameters:** percentage (0-100), label, color  
* **Components:** CircularDial, NumericLabel, TextBlock  
* **Motion Tokens:** ARC\_DRAW, NUMBER\_POP\_SOFT  
* **Duration:** 120 frames (4s)

---

### **Step 2: Create Scene Definition JSON**

**File:** `scenes/definitions/percentage_ring.json`

{  
  "scene\_id": "PERCENTAGE\_RING",  
  "version": "1.0",  
  "category": "quantitative",  
  "duration\_frames": 120,  
  "fps": 30,  
  "purpose": "Visualize completion or progress percentage",  
    
  "timing\_mode": "absolute",  
    
  "phases": \[  
    {  
      "id": "setup",  
      "frames": \[0, 24\],  
      "purpose": "Label appears"  
    },  
    {  
      "id": "fill",  
      "frames": \[24, 84\],  
      "purpose": "Ring fills to percentage"  
    },  
    {  
      "id": "emphasize",  
      "frames": \[84, 108\],  
      "purpose": "Percentage pops"  
    },  
    {  
      "id": "hold",  
      "frames": \[108, 120\],  
      "purpose": "Final hold"  
    }  
  \],  
    
  "zones": {  
    "label": {  
      "x": 0.1,  
      "y": 0.25,  
      "w": 0.8,  
      "h": 0.1  
    },  
    "ring": {  
      "x": 0.2,  
      "y": 0.4,  
      "w": 0.6,  
      "h": 0.3  
    },  
    "percentage": {  
      "x": 0.2,  
      "y": 0.75,  
      "w": 0.6,  
      "h": 0.15  
    }  
  },  
    
  "allowed\_components": \[  
    "CircularDial",  
    "NumericLabel",  
    "TextBlock",  
    "GlowEffect"  
  \],  
    
  "required\_parameters": {  
    "percentage\_value": {  
      "type": "number",  
      "range": \[0, 100\],  
      "description": "Completion percentage"  
    }  
  },  
    
  "optional\_parameters": {  
    "label\_text": {  
      "type": "string",  
      "default": "Progress",  
      "max\_length": 30  
    },  
    "ring\_color": {  
      "type": "color",  
      "default": "\#00FFD1"  
    },  
    "show\_unit": {  
      "type": "boolean",  
      "default": true  
    }  
  },  
    
  "motion\_preset": "PERCENTAGE\_RING\_V1",  
    
  "motion\_sequence": \[  
    {  
      "phase": "setup",  
      "target": "label",  
      "token": "FADE\_IN",  
      "duration": 18  
    },  
    {  
      "phase": "fill",  
      "target": "ring",  
      "token": "ARC\_DRAW",  
      "duration": 48,  
      "params": {  
        "target\_angle": "\<percentage\_angle\>"  
      }  
    },  
    {  
      "phase": "emphasize",  
      "target": "percentage",  
      "token": "NUMBER\_POP\_SOFT",  
      "duration": 18  
    }  
  \],  
    
  "validation\_rules": {  
    "percentage\_required": true,  
    "percentage\_in\_range": true,  
    "label\_max\_length": 30  
  },  
    
  "examples": \[  
    {  
      "name": "Task completion",  
      "parameters": {  
        "percentage\_value": 75,  
        "label\_text": "Tasks Complete"  
      }  
    },  
    {  
      "name": "Health goal",  
      "parameters": {  
        "percentage\_value": 85,  
        "label\_text": "Daily Goal"  
      }  
    }  
  \]  
}

---

### **Step 3: Validate Scene Definition**

python cli.py validate scene \\  
  \--file scenes/definitions/percentage\_ring.json

\# Expected output:  
\# ✅ Schema valid  
\# ✅ Phases cover full duration  
\# ✅ Zones within bounds  
\# ✅ Motion tokens exist  
\# ✅ No conflicts detected

---

### **Step 4: Create Motion Canvas Implementation**

**File:** `motion-canvas/src/scenes/percentage_ring.tsx`

import { makeScene2D } from '@motion-canvas/2d';  
import { Layout, Circle, Txt, Arc } from '@motion-canvas/2d/lib/components';  
import { createRef } from '@motion-canvas/core';  
import { easeOutCubic } from '@motion-canvas/core/lib/tweening';  
import { loadSceneConfig } from '../utils/config\_loader';  
import { applyBrandColors } from '../utils/brand\_kit';

export default makeScene2D(function\* (view) {  
  // Load configuration  
  const config \= loadSceneConfig();  
  const brand \= applyBrandColors(config.brand\_kit\_id);  
    
  // Extract parameters  
  const percentageValue \= config.parameters.percentage\_value;  
  const labelText \= config.parameters.label\_text || "Progress";  
  const ringColor \= config.parameters.ring\_color || brand.primary;  
  const showUnit \= config.parameters.show\_unit \!== false;  
    
  // Validate  
  if (percentageValue \< 0 || percentageValue \> 100\) {  
    throw new Error('percentage\_value must be 0-100');  
  }  
    
  // Create refs  
  const label \= createRef\<Txt\>();  
  const backgroundRing \= createRef\<Circle\>();  
  const progressArc \= createRef\<Arc\>();  
  const percentageText \= createRef\<Txt\>();  
    
  // Calculate dimensions  
  const ringRadius \= 200;  
  const targetAngle \= \-90 \+ (360 \* percentageValue / 100);  
    
  // Build scene  
  view.add(  
    \<Layout  
      direction="column"  
      gap={40}  
      alignItems="center"  
      y={0}  
    \>  
      {/\* Label \*/}  
      \<Txt  
        ref={label}  
        text={labelText}  
        fontSize={28}  
        fill={brand.text}  
        fontFamily="Inter-Medium"  
        opacity={0}  
      /\>  
        
      {/\* Ring container \*/}  
      \<Layout width={ringRadius \* 2 \+ 50} height={ringRadius \* 2 \+ 50}\>  
        {/\* Background circle \*/}  
        \<Circle  
          ref={backgroundRing}  
          radius={ringRadius}  
          stroke="\#2A2A2A"  
          lineWidth={16}  
        /\>  
          
        {/\* Progress arc \*/}  
        \<Arc  
          ref={progressArc}  
          radius={ringRadius}  
          startAngle={-90}  
          endAngle={-90}  
          stroke={ringColor}  
          lineWidth={16}  
          lineCap="round"  
        /\>  
      \</Layout\>  
        
      {/\* Percentage value \*/}  
      \<Txt  
        ref={percentageText}  
        text={showUnit ? \`${percentageValue}%\` : percentageValue.toString()}  
        fontSize={64}  
        fill={brand.primary}  
        fontFamily="SpaceGrotesk-Bold"  
        opacity={0}  
      /\>  
    \</Layout\>  
  );  
    
  // Animation sequence  
  // Phase 1: Setup (frames 0-24)  
  yield\* label().opacity(0, 0).to(1, 18, easeOutCubic);  
    
  // Phase 2: Fill (frames 24-84)  
  yield\* progressArc().endAngle(-90, 0).to(targetAngle, 48, easeOutCubic);  
    
  // Phase 3: Emphasize (frames 84-108)  
  yield\* percentageText().opacity(0, 0).to(1, 18, easeOutCubic);  
    
  // Phase 4: Hold (frames 108-120)  
  // (implicit \- nothing animates)  
});

---

### **Step 5: Add to Scene Registry**

**File:** `motion-canvas/src/project.ts`

import percentageRing from './scenes/percentage\_ring';

export default makeProject({  
  scenes: \[  
    // ... existing scenes  
    percentageRing,  
  \],  
});

**File:** `orchestrator/renderer.py`

SCENE\_MAP \= {  
    \# ... existing mappings  
    "PERCENTAGE\_RING": "percentage\_ring",  
}

---

### **Step 6: Create Test Configuration**

**File:** `tests/fixtures/percentage_ring/config.json`

{  
  "scene\_id": "PERCENTAGE\_RING",  
  "version": "1.0",  
  "parameters": {  
    "percentage\_value": 75,  
    "label\_text": "Test Progress",  
    "show\_unit": true  
  },  
  "brand\_kit\_id": "test\_brand",  
  "timing": {  
    "mode": "absolute",  
    "duration\_frames": 120,  
    "fps": 30  
  }  
}

---

### **Step 7: Write Tests**

**File:** `tests/scenes/test_percentage_ring.py`

import pytest  
from pathlib import Path  
import json  
from orchestrator.renderer import render\_scene

def test\_percentage\_ring\_renders():  
    """Test basic rendering"""  
    config\_path \= Path("tests/fixtures/percentage\_ring/config.json")  
    output\_dir \= Path("tests/output")  
      
    with open(config\_path) as f:  
        config \= json.load(f)  
      
    output\_path \= render\_scene(config, output\_dir)  
      
    assert output\_path.exists()  
    assert output\_path.stat().st\_size \> 0

def test\_percentage\_ring\_duration():  
    """Test output duration is correct"""  
    \# Render scene  
    output\_path \= render\_scene(test\_config, test\_output\_dir)  
      
    \# Check duration with ffprobe  
    duration \= get\_video\_duration(output\_path)  
      
    assert abs(duration \- 4.0) \< 0.1  \# 120 frames @ 30fps \= 4s ±0.1s

def test\_percentage\_ring\_invalid\_value():  
    """Test validation rejects invalid percentage"""  
    config \= {  
        "scene\_id": "PERCENTAGE\_RING",  
        "parameters": {  
            "percentage\_value": 150  \# Invalid  
        }  
    }  
      
    with pytest.raises(ValueError):  
        render\_scene(config, test\_output\_dir)

def test\_percentage\_ring\_parameters():  
    """Test different parameter combinations"""  
    test\_cases \= \[  
        {"percentage\_value": 0, "expected\_angle": \-90},  
        {"percentage\_value": 50, "expected\_angle": 90},  
        {"percentage\_value": 100, "expected\_angle": 270},  
    \]  
      
    for case in test\_cases:  
        config \= {  
            "scene\_id": "PERCENTAGE\_RING",  
            "parameters": case  
        }  
        \# Render and verify  
        \# ...

---

### **Step 8: Test Locally**

\# Test render  
python cli.py render \\  
  \--scene PERCENTAGE\_RING \\  
  \--config tests/fixtures/percentage\_ring/config.json \\  
  \--output tests/output/

\# Check result  
open tests/output/PERCENTAGE\_RING\_001.mp4

\# Run automated tests  
pytest tests/scenes/test\_percentage\_ring.py \-v

---

### **Step 9: Create Golden Master**

python cli.py golden create \\  
  \--scene PERCENTAGE\_RING \\  
  \--config tests/fixtures/percentage\_ring/config.json

\# Verify  
python cli.py test regression \--scene PERCENTAGE\_RING

---

### **Step 10: Update Documentation**

**Add to `scenes/library.json`:**

{  
  "scenes": \[  
    {  
      "scene\_id": "PERCENTAGE\_RING",  
      "name": "Percentage Ring",  
      "category": "quantitative",  
      "complexity": "simple",  
      "description": "Circular progress indicator with percentage",  
      "use\_cases": \[  
        "Task completion",  
        "Goal progress",  
        "Health metrics"  
      \],  
      "status": "production",  
      "version": "1.0"  
    }  
  \]  
}

**Update `scene_library_v1.md`:**

Add entry in appropriate section.

---

## **4\. Scene Development Checklist**

### **Design Phase**

* \[ \] Scene concept defined  
* \[ \] Parameters identified  
* \[ \] Components selected  
* \[ \] Motion tokens mapped  
* \[ \] Duration determined

### **Implementation Phase**

* \[ \] Scene definition JSON created  
* \[ \] Schema validation passes  
* \[ \] Motion Canvas scene implemented  
* \[ \] Scene registered in project  
* \[ \] Test config created

### **Testing Phase**

* \[ \] Unit tests written  
* \[ \] Integration test passes  
* \[ \] Golden master created  
* \[ \] Regression test passes  
* \[ \] Edge cases covered

### **Documentation Phase**

* \[ \] Added to scene library  
* \[ \] Examples documented  
* \[ \] Use cases described  
* \[ \] Known issues noted

---

## **5\. Common Patterns**

### **Pattern 1: Text-Heavy Scene**

// Multiple text blocks with sequential reveal  
const texts \= \[  
  createRef\<Txt\>(),  
  createRef\<Txt\>(),  
  createRef\<Txt\>()  
\];

// Render all invisible  
texts.forEach((ref, i) \=\> {  
  view.add(  
    \<Txt ref={ref} opacity={0} y={100 \+ i \* 60} /\>  
  );  
});

// Reveal sequentially  
for (let i \= 0; i \< texts.length; i++) {  
  yield\* texts\[i\]().opacity(0, 0).to(1, 18, easeOutCubic);  
  if (i \< texts.length \- 1\) {  
    yield\* waitFor(0.3); // Stagger  
  }  
}

---

### **Pattern 2: Layer-Based Scene**

// Load layer graph  
const layerGraph \= loadLayerGraph();

// Create ImageLayer for each layer  
const layers \= layerGraph.layers.map(layer \=\> {  
  const ref \= createRef\<Img\>();  
  view.add(  
    \<Img  
      ref={ref}  
      src={layer.rgba\_asset}  
      x={layer.bbox.x \* 1080}  
      y={layer.bbox.y \* 1920}  
      width={layer.bbox.w \* 1080}  
      height={layer.bbox.h \* 1920}  
      opacity={0}  
    /\>  
  );  
  return ref;  
});

// Fade in base layer first  
yield\* layers\[0\]().opacity(0, 0).to(1, 24, easeOutCubic);

// Then reveal focus layer with glow  
yield\* all(  
  layers\[1\]().opacity(0, 0).to(1, 18, easeOutCubic),  
  // Add glow effect  
);

---

### **Pattern 3: Speech-Aligned Scene**

const config \= loadSceneConfig();  
const timing \= config.timing;

let fillDuration;  
if (timing.mode \=== "speech\_aligned") {  
  const startFrame \= timing.anchors.response\_start;  
  const endFrame \= timing.anchors.response\_end;  
  fillDuration \= endFrame \- startFrame;  
} else {  
  fillDuration \= 60; // Default  
}

yield\* meter().width(0, 0).to(targetWidth, fillDuration, easeOutCubic);

---

## **6\. Debugging Tips**

### **Issue: Scene doesn't render**

**Check:**

1. Is scene registered in project.ts?  
2. Is scene ID in SCENE\_MAP?  
3. Are all imports correct?  
4. Run `npm run serve` to see preview

---

### **Issue: Animation timing off**

**Check:**

1. Frame counts add up to duration\_frames?  
2. Are motion tokens using correct durations?  
3. Use `console.log(config)` to verify parameters

---

### **Issue: Components not appearing**

**Check:**

1. Are refs created correctly?  
2. Is initial opacity 0 (if fading in)?  
3. Are bbox coordinates valid (0-1 range)?  
4. Check z-ordering

---

## **7\. Performance Optimization**

### **Minimize Re-renders**

* Don't animate every frame unnecessarily  
* Use `yield* waitFor()` instead of frame-by-frame updates

### **Reuse Components**

* Extract common patterns into shared components  
* Import from component library

### **Optimize Assets**

* Compress images before loading  
* Use appropriate resolutions (no larger than needed)

---

## **8\. Scene Variants**

To create a variant of an existing scene:

\# Copy base scene  
cp scenes/definitions/rating\_meter\_1\_to\_10.json \\  
   scenes/definitions/rating\_meter\_vertical.json

\# Modify scene\_id and parameters  
\# scene\_id: "RATING\_METER\_VERTICAL"  
\# Add: "orientation": "vertical"

\# Copy Motion Canvas implementation  
cp motion-canvas/src/scenes/rating\_meter.tsx \\  
   motion-canvas/src/scenes/rating\_meter\_vertical.tsx

\# Modify orientation logic

---

## **9\. Contributing Back**

To contribute your scene:

1. Ensure all tests pass  
2. Create golden master  
3. Document use cases  
4. Submit PR with:  
   * Scene definition JSON  
   * Motion Canvas implementation  
   * Tests  
   * Documentation updates  
   * Example renders

---

**You now know how to create production-ready scenes for Motion Cookbook.**

