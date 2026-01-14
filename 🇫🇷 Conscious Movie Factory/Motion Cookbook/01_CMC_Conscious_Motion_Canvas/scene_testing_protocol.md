# **scene\_testing\_protocol.md**

**Purpose:** Scene validation and quality assurance  
 **Status:** Canonical v1.0

---

## **1\. Testing Philosophy**

Scenes are **infrastructure**, not creative experiments.

A scene is production-ready only when:

* ✅ Renders deterministically  
* ✅ Respects all contracts  
* ✅ Performs editorially  
* ✅ Passes all validation layers

**No exceptions.**

---

## **2\. Five Testing Layers**

### **Layer 1: Schema Validation (Static)**

### **Layer 2: Layer Graph Compatibility**

### **Layer 3: Motion Token Integrity**

### **Layer 4: Speech Alignment (if applicable)**

### **Layer 5: Editorial QA (Human)**

---

## **3\. Layer 1: Schema Validation**

**Purpose:** Ensure scene definition is structurally valid

### **Automated Checks**

npm run validate:scene \-- \\  
  \--definition schemas/scenes/body\_map\_focus.json

**Checks:**

* ✅ Conforms to JSON schema  
* ✅ `scene_id` unique and valid format  
* ✅ `version` immutable  
* ✅ `duration_frames` \> 0 and divisible by fps  
* ✅ Phases cover entire duration  
* ✅ Phases non-overlapping  
* ✅ Zones within canvas bounds (0-1)  
* ✅ `allowed_components` non-empty  
* ✅ `motion_preset` exists

**Exit Criteria:**

* Zero schema violations

**Failure Response:**

{  
  "status": "FAILED",  
  "errors": \[  
    {  
      "layer": "SCHEMA\_VALIDATION",  
      "code": "INVALID\_PHASE\_RANGE",  
      "message": "Phase 'focus' exceeds scene duration",  
      "scene\_id": "BODY\_MAP\_FOCUS",  
      "phase": "focus",  
      "frames": \[40, 200\],  
      "duration\_frames": 150  
    }  
  \]  
}

---

## **4\. Layer 2: Layer Graph Compatibility**

**Purpose:** Ensure scene can accept given layers

### **Test Command**

npm run validate:compatibility \-- \\  
  \--scene schemas/scenes/body\_map\_focus.json \\  
  \--layers data/layer\_graphs/body\_map\_001.json

**Checks:**

* ✅ Required layers present  
* ✅ Layer types compatible with allowed components  
* ✅ Layer semantics match scene requirements  
* ✅ No forbidden transforms requested  
* ✅ Z-order respected  
* ✅ All referenced layer IDs exist

**Example Test:**

test('BODY\_MAP\_FOCUS requires body and region layers', () \=\> {  
  const scene \= loadSceneDefinition('BODY\_MAP\_FOCUS');  
  const layers \= loadLayerGraph('body\_map\_001');  
    
  const compatibility \= validateCompatibility(scene, layers);  
    
  expect(compatibility.required\_layers\_present).toBe(true);  
  expect(compatibility.missing\_layers).toHaveLength(0);  
});

**Failure Response:**

{  
  "status": "INCOMPATIBLE",  
  "scene\_id": "BODY\_MAP\_FOCUS",  
  "layer\_graph\_id": "body\_map\_001",  
  "errors": \[  
    {  
      "code": "MISSING\_REQUIRED\_LAYER",  
      "message": "Scene requires 'region' semantic",  
      "required": \["body", "region"\],  
      "available": \["body", "background"\]  
    }  
  \]  
}

---

## **5\. Layer 3: Motion Token Integrity**

**Purpose:** Ensure motion logic is safe

### **Test Command**

npm run validate:tokens \-- \\  
  \--scene-config data/scene\_configs/scene\_001.json

**Checks:**

* ✅ All tokens exist in registry  
* ✅ Token versions compatible  
* ✅ Token targets exist in layer assignments  
* ✅ Token timings within scene duration  
* ✅ No conflicting tokens on same target/property  
* ✅ Token parameters valid

**Example Conflict Detection:**

test('Detects conflicting opacity tokens', () \=\> {  
  const config \= {  
    motion\_tokens: \[  
      { token\_id: 'FADE\_IN', target: 'body\_base', start\_frame: 0 },  
      { token\_id: 'PULSE\_OPACITY', target: 'body\_base', start\_frame: 10 }  
    \]  
  };  
    
  const validation \= validateTokenConflicts(config);  
    
  expect(validation.conflicts).toContainEqual({  
    type: 'PROPERTY\_CONFLICT',  
    property: 'opacity',  
    tokens: \['FADE\_IN', 'PULSE\_OPACITY'\],  
    target: 'body\_base'  
  });  
});

**Failure Response:**

{  
  "status": "FAILED",  
  "errors": \[  
    {  
      "code": "TOKEN\_CONFLICT",  
      "message": "Multiple opacity tokens on same target",  
      "target": "body\_base",  
      "property": "opacity",  
      "tokens": \["FADE\_IN", "PULSE\_OPACITY"\],  
      "frames": \[\[0, 12\], \[10, 34\]\]  
    }  
  \]  
}

---

## **6\. Layer 4: Speech Alignment (If Applicable)**

**Purpose:** Validate speech-aligned scenes

### **Test Command**

npm run validate:speech \-- \\  
  \--scene-config data/scene\_configs/scene\_002.json \\  
  \--audio tests/fixtures/interview\_audio.wav

**Checks:**

* ✅ Required anchors provided or computable  
* ✅ Anchors monotonic (start \< peak \< end)  
* ✅ Anchors within scene duration  
* ✅ Confidence ≥ threshold (default 0.7)  
* ✅ Fallback behavior defined

**Test Cases:**

test('Speech anchors are monotonic', () \=\> {  
  const anchors \= { response\_start: 42, response\_peak: 78, response\_end: 118 };  
  expect(anchors.response\_start \< anchors.response\_peak).toBe(true);  
  expect(anchors.response\_peak \< anchors.response\_end).toBe(true);  
});

test('Falls back to absolute timing if confidence low', () \=\> {  
  const anchors \= { confidence: 0.5 };  
  const resolved \= resolveAnchors(anchors, scene);  
    
  expect(resolved).toEqual(scene.default\_anchors);  
});

**Failure Response:**

{  
  "status": "WARNING",  
  "message": "Speech anchors below confidence threshold",  
  "confidence": 0.62,  
  "threshold": 0.70,  
  "action": "Using fallback absolute timing"  
}

---

## **7\. Layer 5: Editorial QA**

**Purpose:** Human validation of visual quality

### **Checklist**

**Rendering:**

* ✅ Frame count matches specification  
* ✅ Duration accurate (±1 frame tolerance)  
* ✅ No dropped frames  
* ✅ No visual artifacts  
* ✅ Alpha channel correct (if applicable)

**Legibility:**

* ✅ Text readable at 1080×1920  
* ✅ Minimum font size 20px (labels), 32px (values)  
* ✅ Contrast ratio ≥ 4.5:1  
* ✅ No visual crowding

**Motion Quality:**

* ✅ Smooth animation (no jank)  
* ✅ Proper easing  
* ✅ Clear visual hierarchy  
* ✅ No unnecessary motion  
* ✅ Emphasis at correct moments

**Brand Compliance:**

* ✅ Colors match brand kit  
* ✅ Typography consistent  
* ✅ Motion intensity appropriate  
* ✅ Overall feel on-brand

**Editorial Feel:**

* ✅ Would this make someone stop scrolling?  
* ✅ Does it clarify or distract?  
* ✅ Feels professional, not amateurish  
* ✅ Appropriate pacing

### **QA Workflow**

\# 1\. Render test scene  
npm run render:test \-- \\  
  \--scene BODY\_MAP\_FOCUS \\  
  \--config tests/fixtures/body\_map\_test\_001.json \\  
  \--output qa/body\_map\_focus\_test.mp4

\# 2\. Human review  
\# \- Watch at 0.5x, 1x, 2x speeds  
\# \- Check on mobile device  
\# \- Compare to golden master

\# 3\. Mark result  
npm run qa:mark \-- \\  
  \--scene BODY\_MAP\_FOCUS \\  
  \--status \[PASS|NEEDS\_REVISION|FAIL\]

---

## **8\. Golden Master Testing**

### **Purpose**

Golden master renders ensure regression-free updates.

### **Process**

**1\. Create Golden Master:**

npm run render:golden \-- \\  
  \--scene BODY\_MAP\_FOCUS \\  
  \--config tests/fixtures/golden/body\_map\_focus.json \\  
  \--output tests/golden/body\_map\_focus.mp4

**2\. Generate Hash:**

sha256sum tests/golden/body\_map\_focus.mp4 \> tests/golden/body\_map\_focus.sha256

**3\. Store Metadata:**

{  
  "scene\_id": "BODY\_MAP\_FOCUS",  
  "version": "1.0",  
  "golden\_render\_date": "2026-01-04",  
  "config\_hash": "a3f7b2e9...",  
  "video\_hash": "b4e8c3d1...",  
  "frame\_count": 150,  
  "duration\_seconds": 5.0  
}

**4\. Regression Test:**

npm run test:regression \-- \\  
  \--scene BODY\_MAP\_FOCUS \\  
  \--golden tests/golden/body\_map\_focus.mp4

**Comparison:**

* Frame-by-frame diff  
* Structural similarity index (SSIM)  
* Pixel difference tolerance: \< 0.5%

---

## **9\. Batch Testing**

Test all scenes at once:

npm run test:all-scenes

**Output:**

✓ CUTOUT\_METAPHOR (1/16)          \[PASS\]  
✓ BEFORE\_AFTER\_SPLIT (2/16)       \[PASS\]  
✗ BODY\_MAP\_FOCUS (3/16)           \[FAIL \- Layer compatibility\]  
✓ BLUEPRINT\_FLOW (4/16)           \[PASS\]  
...

Summary:  
  Passed:  14/16  
  Failed:  2/16  
  Warnings: 1

---

## **10\. Continuous Integration**

### **Pre-commit Checks**

\# .git/hooks/pre-commit

npm run validate:all-scenes  
if \[ $? \-ne 0 \]; then  
  echo "Scene validation failed. Commit rejected."  
  exit 1  
fi

### **CI Pipeline**

\# .github/workflows/scene-tests.yml

name: Scene Tests  
on: \[push, pull\_request\]

jobs:  
  validate:  
    runs-on: ubuntu-latest  
    steps:  
      \- uses: actions/checkout@v3  
      \- name: Install dependencies  
        run: npm install  
      \- name: Schema validation  
        run: npm run test:schemas  
      \- name: Token validation  
        run: npm run test:tokens  
      \- name: Render test scenes  
        run: npm run test:render  
      \- name: Compare to golden masters  
        run: npm run test:regression

---

## **11\. Performance Testing**

### **Render Time Benchmarks**

npm run bench:scenes

**Target Metrics:**

| Scene | Max Render Time (CPU) | Max Render Time (GPU) |
| ----- | ----- | ----- |
| Simple (\< 100 layers) | 30s | 15s |
| Medium (100-200 layers) | 60s | 30s |
| Complex (200+ layers) | 90s | 45s |

**Failure:** Scene exceeds max render time

---

## **12\. Test Fixtures**

### **Organization**

/tests/fixtures/  
  /body\_map\_focus/  
    config.json           \# Scene configuration  
    layer\_graph.json      \# Test layers  
    expected\_output.mp4   \# Golden master  
    expected\_output.sha256  
  /rating\_meter/  
    config.json  
    audio\_sample.wav      \# For speech-aligned tests  
    ...

### **Fixture Requirements**

Each fixture must include:

* ✅ Valid scene configuration  
* ✅ Compatible layer graph  
* ✅ Golden master render  
* ✅ Expected metadata  
* ✅ Audio sample (if speech-aligned)

---

## **13\. Error Classification**

| Severity | Response | Example |
| ----- | ----- | ----- |
| CRITICAL | Block release | Schema violation |
| ERROR | Fix required | Missing required layer |
| WARNING | Review needed | Low confidence anchors |
| INFO | Monitor | Performance slower than expected |

---

## **14\. Test Coverage Requirements**

Before scene is production-ready:

* ✅ Schema validation: 100%  
* ✅ Compatibility tests: All layer combinations  
* ✅ Token conflict detection: Edge cases covered  
* ✅ Speech alignment: With and without anchors  
* ✅ Golden master: Exists and passes  
* ✅ Editorial QA: Human approved  
* ✅ Performance: Within benchmarks  
* ✅ Regression: Passes on re-render

---

## **15\. CLI Command Reference**

\# Validate single scene  
npm run validate:scene \-- \--scene BODY\_MAP\_FOCUS

\# Test compatibility  
npm run validate:compatibility \-- \--scene ... \--layers ...

\# Token integrity  
npm run validate:tokens \-- \--config ...

\# Speech alignment  
npm run validate:speech \-- \--config ... \--audio ...

\# Render test  
npm run render:test \-- \--scene ... \--config ...

\# Create golden master  
npm run render:golden \-- \--scene ... \--config ...

\# Regression test  
npm run test:regression \-- \--scene ...

\# Full test suite  
npm run test:all-scenes

\# Performance benchmark  
npm run bench:scenes

---

## **16\. References**

* `scene_schema.md` \- Scene structure requirements  
* `layer_graph_schema.md` \- Layer validation rules  
* `motion_tokens.md` \- Token definitions  
* `scene_library_v1.md` \- Scene catalog

