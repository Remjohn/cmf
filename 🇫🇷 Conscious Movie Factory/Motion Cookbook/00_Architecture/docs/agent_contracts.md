# **agent\_contracts.md**

**Purpose:** AI agent interfaces and boundaries  
 **Status:** Canonical v1.0

---

## **1\. Agent Philosophy**

### **Core Principle**

**AI prepares, Motion Canvas animates.**

AI agents:

* ✅ Analyze and interpret  
* ✅ Generate and extract assets  
* ✅ Label and structure data  
* ✅ Fill scene parameters

AI agents **never**:

* ❌ Choose motion tokens  
* ❌ Define animation timing  
* ❌ Create easing curves  
* ❌ Modify scene structure  
* ❌ Generate video directly

---

## **2\. Agent Contract Template**

Every agent follows this interface:

### **2.1 Input/Output**

* **Input:** JSON via `stdin`  
* **Output:** JSON via `stdout`  
* **Errors:** JSON via `stderr`  
* **Exit Codes:** 0 \= success, non-zero \= failure

### **2.2 Standard Schema**

{  
  "agent\_id": "LayerExtractor",  
  "version": "1.0",  
  "input\_schema": {...},  
  "output\_schema": {...},  
  "timeout\_seconds": 60,  
  "retry\_policy": "3x\_exponential",  
  "failure\_modes": \[...\]  
}

---

## **3\. Agent Inventory**

### **3.1 ContextAnalyzer**

**File:** `/src/agents/context_analyzer.py`

**Purpose:** Interpret user intent and extract key concepts

**Input:**

{  
  "script": "In today's video, we'll explore how your gut is your second brain...",  
  "notes": "Body map concept, intuition theme",  
  "target\_audience": "health coaches"  
}

**Output:**

{  
  "topic": "gut-brain connection",  
  "intent": "explain",  
  "key\_concepts": \["intuition", "gut\_health", "nervous\_system"\],  
  "emotional\_tone": "educational",  
  "suggested\_visual\_themes": \["body\_anatomy", "connection", "clarity"\],  
  "confidence": 0.92  
}

**Execution:**

echo '{"script": "..."}' | python agents/context\_analyzer.py

---

### **3.2 ScenePlanner**

**File:** `/src/agents/scene_planner.py`

**Purpose:** Select appropriate scenes based on context

**Input:**

{  
  "context": {  
    "topic": "gut-brain connection",  
    "intent": "explain",  
    "key\_concepts": \["intuition", "gut\_health"\]  
  },  
  "available\_scenes": \["BODY\_MAP\_FOCUS", "KINETIC\_DEFINITION", "STEP\_BREAKDOWN"\],  
  "constraints": {  
    "min\_scenes": 5,  
    "max\_scenes": 7  
  }  
}

**Output:**

{  
  "selected\_scenes": \[  
    {  
      "scene\_id": "BODY\_MAP\_FOCUS",  
      "priority": 1,  
      "rationale": "Perfect for anatomical explanation",  
      "confidence": 0.95  
    },  
    {  
      "scene\_id": "KINETIC\_DEFINITION",  
      "priority": 2,  
      "rationale": "Define 'gut-brain axis'",  
      "confidence": 0.88  
    }  
  \]  
}

**Decision Logic:**

1. Match key concepts to scene semantics  
2. Ensure variety (no duplicate scene types)  
3. Prioritize by confidence and relevance  
4. Respect constraints

---

### **3.3 ImageGenerator**

**File:** `/src/agents/image_generator.py`

**Purpose:** Generate missing images (optional)

**Input:**

{  
  "prompt": "minimalist line art illustration of human body with gut region highlighted",  
  "style": "clean, medical diagram",  
  "aspect\_ratio": "9:16",  
  "model": "qwen\_image\_2512"  
}

**Output:**

{  
  "image\_path": "data/generated/body\_diagram\_001.png",  
  "width": 1080,  
  "height": 1920,  
  "generation\_time\_ms": 4200,  
  "model\_used": "qwen\_image\_2512"  
}

**Models Available:**

* `qwen_image_2512` \- General purpose  
* `nanobanana_pro` \- Complex diagrams/maps  
* `zimage_turbo` \- Fast stylized

---

### **3.4 LayerExtractor**

**File:** `/src/agents/layer_extractor.py`

**Purpose:** Decompose images into RGBA layers

**Input:**

{  
  "source\_image": "assets/body\_diagram.png",  
  "method": "qwen\_layered",  
  "output\_dir": "data/layer\_graphs/body\_map\_001/"  
}

**Output:**

{  
  "layer\_graph\_id": "body\_map\_001",  
  "layers": \[  
    {  
      "layer\_id": "body\_base",  
      "src": "data/layer\_graphs/body\_map\_001/body\_base.png",  
      "bbox": {"x": 0.1, "y": 0.15, "w": 0.8, "h": 0.7},  
      "extraction\_confidence": 0.98  
    },  
    {  
      "layer\_id": "gut\_region",  
      "src": "data/layer\_graphs/body\_map\_001/gut\_region.png",  
      "bbox": {"x": 0.42, "y": 0.48, "w": 0.18, "h": 0.22},  
      "extraction\_confidence": 0.92  
    }  
  \],  
  "total\_layers": 4,  
  "processing\_time\_ms": 3420  
}

**Methods:**

* `qwen_layered` \- Automatic layer extraction  
* `sam3` \- Segmentation-based  
* `manual` \- User-provided layers

**File Output:**

data/layer\_graphs/body\_map\_001/  
  body\_base.png  
  gut\_region.png  
  heart\_region.png  
  brain\_region.png

---

### **3.5 SemanticLabeler**

**File:** `/src/agents/semantic_labeler.py`

**Purpose:** Assign semantic tags to layers

**Input:**

{  
  "layer\_graph\_id": "body\_map\_001",  
  "layers": \[  
    {  
      "layer\_id": "gut\_region",  
      "src": "data/layer\_graphs/body\_map\_001/gut\_region.png",  
      "bbox": {"x": 0.42, "y": 0.48, "w": 0.18, "h": 0.22}  
    }  
  \],  
  "context": {  
    "topic": "gut-brain connection"  
  }  
}

**Output:**

{  
  "labeled\_layers": \[  
    {  
      "layer\_id": "gut\_region",  
      "semantics": \["gut", "digestive", "intuition", "nervous\_system"\],  
      "confidence": 0.91,  
      "primary\_semantic": "gut"  
    }  
  \]  
}

**Labeling Process:**

1. Visual analysis (Qwen3-VL / Wan VLM)  
2. Spatial analysis (position, size)  
3. Context alignment (topic keywords)  
4. Taxonomy matching (standard semantic tags)

---

### **3.6 SpeechAnalyzer**

**File:** `/src/agents/speech_analyzer.py`

**Purpose:** Extract temporal anchors from audio/transcript

**Input:**

{  
  "audio": "data/audio/response\_clip.wav",  
  "transcript": "I'd say I'm at about a seven right now",  
  "scene\_duration\_frames": 150,  
  "fps": 30  
}

**Output:**

{  
  "anchors": {  
    "response\_start": 42,  
    "response\_peak": 78,  
    "response\_end": 118  
  },  
  "confidence": 0.87,  
  "detected\_pauses": \[65, 102\],  
  "speech\_rate": "normal"  
}

**Techniques:**

* VAD (Voice Activity Detection)  
* Prosody analysis  
* Transcript alignment  
* Pause detection

**Fallback:** If confidence \< 0.7, return `null` anchors.

---

### **3.7 ParameterFiller**

**File:** `/src/agents/parameter_filler.py`

**Purpose:** Fill scene parameters from context \+ layers

**Input:**

{  
  "scene\_id": "BODY\_MAP\_FOCUS",  
  "layer\_graph": {...},  
  "context": {  
    "topic": "gut-brain connection",  
    "key\_concepts": \["intuition"\]  
  },  
  "brand\_kit": {  
    "colors": {"primary": "\#00FFD1"}  
  }  
}

**Output:**

{  
  "scene\_config": {  
    "scene\_id": "BODY\_MAP\_FOCUS",  
    "layer\_assignments": {  
      "background": "body\_base",  
      "primary": "gut\_region"  
    },  
    "parameters": {  
      "headline\_text": "Your intuition lives here",  
      "subtext": "The gut-brain connection",  
      "highlight\_color": "\#00FFD1"  
    }  
  }  
}

**Filling Logic:**

1. Match layers to scene zones by semantics  
2. Generate text from key concepts  
3. Apply brand colors  
4. Validate completeness

---

## **4\. Agent Execution Model**

### **4.1 Sequential Execution**

\# 1\. Analyze context  
cat input.json | python agents/context\_analyzer.py \> context.json

\# 2\. Plan scenes  
cat context.json | python agents/scene\_planner.py \> plan.json

\# 3\. Extract layers  
cat plan.json | python agents/layer\_extractor.py \> layers.json

\# 4\. Label semantics  
cat layers.json | python agents/semantic\_labeler.py \> labeled.json

\# 5\. Fill parameters  
cat labeled.json | python agents/parameter\_filler.py \> scene\_configs.json

### **4.2 Orchestrated Execution**

**File:** `/src/orchestrator/pipeline.ts`

async function runPipeline(input: UserInput): Promise\<SceneConfig\[\]\> {  
  const context \= await runAgent('context\_analyzer', input);  
  const plan \= await runAgent('scene\_planner', context);  
  const layers \= await runAgent('layer\_extractor', plan);  
  const labeled \= await runAgent('semantic\_labeler', layers);  
  const configs \= await runAgent('parameter\_filler', labeled);  
  return configs;  
}

---

## **5\. Agent Validation**

### **5.1 Schema Validation**

Every agent output is validated against its schema.

import { z } from 'zod';

const LayerExtractorOutputSchema \= z.object({  
  layer\_graph\_id: z.string(),  
  layers: z.array(z.object({  
    layer\_id: z.string(),  
    src: z.string(),  
    bbox: z.object({  
      x: z.number().min(0).max(1),  
      y: z.number().min(0).max(1),  
      w: z.number().min(0).max(1),  
      h: z.number().min(0).max(1)  
    })  
  }))  
});

const result \= LayerExtractorOutputSchema.safeParse(agentOutput);  
if (\!result.success) {  
  throw new AgentValidationError(result.error);  
}

---

## **6\. Error Handling**

### **6.1 Agent Error Output**

{  
  "error": "LAYER\_EXTRACTION\_FAILED",  
  "message": "SAM3 segmentation timeout",  
  "agent\_id": "layer\_extractor",  
  "input\_hash": "a3f7b2e9...",  
  "timestamp": "2026-01-04T12:34:56Z"  
}

### **6.2 Failure Modes**

| Agent | Failure Mode | Response |
| ----- | ----- | ----- |
| ContextAnalyzer | Invalid script | Request clarification |
| ScenePlanner | No matching scenes | Use fallback scenes |
| ImageGenerator | Generation failed | Prompt user for image |
| LayerExtractor | Extraction timeout | Skip layering, use whole image |
| SemanticLabeler | Low confidence | Use generic labels |
| SpeechAnalyzer | No speech detected | Use absolute timing |
| ParameterFiller | Missing layers | Skip scene |

---

## **7\. Retry Policies**

### **7.1 Exponential Backoff**

def retry\_agent(agent\_func, max\_retries=3):  
    for attempt in range(max\_retries):  
        try:  
            return agent\_func()  
        except Exception as e:  
            if attempt \== max\_retries \- 1:  
                raise  
            time.sleep(2 \*\* attempt)  \# 1s, 2s, 4s

### **7.2 Timeout Enforcement**

import signal

def timeout\_handler(signum, frame):  
    raise TimeoutError("Agent exceeded timeout")

signal.signal(signal.SIGALRM, timeout\_handler)  
signal.alarm(60)  \# 60 second timeout

try:  
    result \= run\_agent(input\_data)  
finally:  
    signal.alarm(0)

---

## **8\. Agent Testing**

### **8.1 Unit Tests**

\# tests/agents/test\_context\_analyzer.py

def test\_context\_analyzer\_basic():  
    input\_data \= {"script": "Today we'll talk about habits..."}  
    output \= context\_analyzer.process(input\_data)  
      
    assert output\['topic'\] is not None  
    assert output\['intent'\] in \['explain', 'emphasize', 'storytelling'\]  
    assert output\['confidence'\] \>= 0.5

### **8.2 Integration Tests**

\# Test full pipeline  
npm run test:pipeline \-- \\  
  \--input tests/fixtures/body\_map\_example.json \\  
  \--expected tests/fixtures/body\_map\_expected.json

---

## **9\. Agent Monitoring**

### **9.1 Metrics**

Track for each agent:

* **Execution time** (median, p95, p99)  
* **Success rate** (%)  
* **Retry rate** (%)  
* **Confidence scores** (distribution)

### **9.2 Logging**

{  
  "timestamp": "2026-01-04T12:34:56Z",  
  "agent\_id": "layer\_extractor",  
  "input\_hash": "a3f7b2e9...",  
  "execution\_time\_ms": 3420,  
  "status": "success",  
  "output\_layers": 4,  
  "confidence": 0.95  
}

---

## **10\. Agent Boundaries (Critical)**

### **What Agents CAN Do:**

* ✅ Analyze images and text  
* ✅ Generate images  
* ✅ Extract and segment layers  
* ✅ Assign semantic labels  
* ✅ Match layers to scene requirements  
* ✅ Fill text and numeric parameters  
* ✅ Detect speech timing

### **What Agents CANNOT Do:**

* ❌ Choose motion tokens  
* ❌ Define animation curves  
* ❌ Set easing functions  
* ❌ Determine timing  
* ❌ Modify scene structure  
* ❌ Generate video frames  
* ❌ Make aesthetic decisions about motion

**Why This Matters:** Violating these boundaries introduces non-determinism and breaks quality guarantees.

---

## **11\. Agent Development Workflow**

### **Adding a New Agent**

1. **Define contract** in this document  
2. **Create schema** in `/schemas/agents/`  
3. **Implement** in `/src/agents/`  
4. **Add tests** in `/tests/agents/`  
5. **Update orchestrator** to call agent  
6. **Document** in agent inventory above

---

## **12\. References**

* `architecture.md` \- Overall system design  
* `scene_schema.md` \- Scene structure agents fill  
* `layer_graph_schema.md` \- Layer structure agents produce  
* `speech_anchor_taxonomy.md` \- Speech analysis output format

# **agent\_contracts.md \- COMPLETE AGENT I/O SPECIFICATIONS**

## **Add to Section 3: Complete Agent Inventory**

### **3.8 AssetValidator**

**File:** /src/agents/asset\_validator.py

**Purpose:** Check asset availability and quality before processing

**Input:**

{  
  "plan": {  
    "selected\_scenes": \[  
      {"scene\_id": "BODY\_MAP\_FOCUS", "priority": 1}  
    \]  
  },  
  "assets": {  
    "user\_provided": \[  
      "data/assets/body\_diagram.png"  
    \],  
    "required\_by\_scenes": \[  
      {"scene\_id": "BODY\_MAP\_FOCUS", "requires": \["body\_image"\]}  
    \]  
  }  
}

**Output:**

{  
  "agent\_id": "AssetValidator",  
  "output": {  
    "validation\_status": "pass",  
    "available\_assets": \[  
      {  
        "asset\_id": "body\_diagram",  
        "path": "data/assets/body\_diagram.png",  
        "type": "image/png",  
        "dimensions": {"width": 2048, "height": 2048},  
        "file\_size\_mb": 3.2,  
        "quality\_score": 0.92  
      }  
    \],  
    "missing\_assets": \[\],  
    "warnings": \[  
      {  
        "asset\_id": "body\_diagram",  
        "warning": "Image resolution higher than needed (2048px \> 1920px)",  
        "recommendation": "Will be downscaled"  
      }  
    \]  
  }  
}

**Validation Checks:**

* File exists and readable  
* Format supported (PNG, JPEG, WebP)  
* Dimensions adequate (min 1080px shortest side)  
* Not corrupted  
* Reasonable file size (\<50MB)

---

### **3.9 TextSynthesizer**

**File:** /src/agents/text\_synthesizer.py

**Purpose:** Generate concise explainer copy when needed

**Input:**

{  
  "context": {  
    "topic": "gut-brain connection",  
    "key\_concepts": \["intuition", "nervous\_system"\]  
  },  
  "text\_type": "headline",  
  "max\_length": 50,  
  "tone": "educational"  
}

**Output:**

{  
  "agent\_id": "TextSynthesizer",  
  "output": {  
    "generated\_text": "Your intuition lives in your gut",  
    "character\_count": 33,  
    "confidence": 0.88,  
    "alternatives": \[  
      "The gut-brain axis explained",  
      "Your second brain: the gut"  
    \]  
  }  
}

**Text Types Supported:**

* headline (5-50 chars)  
* subtext (10-100 chars)  
* definition (50-200 chars)  
* label (3-20 chars)

---

### **3.10 SceneConfigBuilder**

**File:** /src/agents/scene\_config\_builder.py

**Purpose:** Combine all agent outputs into final scene configurations

**Input:**

{  
  "selected\_scenes": \[...\],  
  "layer\_graphs": {...},  
  "labeled\_layers": {...},  
  "filled\_parameters": {...},  
  "brand\_kit\_id": "default\_brand"  
}

**Output:**

{  
  "agent\_id": "SceneConfigBuilder",  
  "output": {  
    "scene\_configs": \[  
      {  
        "scene\_id": "RATING\_METER\_1\_TO\_10",  
        "version": "1.0",  
        "config\_id": "config\_001",  
        "layer\_graph\_id": null,  
        "brand\_kit\_id": "default\_brand",  
        "parameters": {  
          "rating\_value": 7,  
          "label\_text": "Confidence Level",  
          "min\_value": 0,  
          "max\_value": 10  
        },  
        "timing": {  
          "mode": "absolute",  
          "duration\_frames": 150,  
          "fps": 30  
        },  
        "output\_path": "data/rendered/RATING\_METER\_1\_TO\_10\_001.mp4"  
      }  
    \],  
    "build\_timestamp": "2026-01-04T14:22:10Z"  
  }  
}

---

### **3.11 MotionTokenResolver**

**File:** /src/agents/motion\_token\_resolver.py

**Purpose:** Validate and resolve motion token references

**Input:**

{  
  "scene\_config": {  
    "scene\_id": "RATING\_METER\_1\_TO\_10",  
    "motion\_preset": "RATING\_METER\_V1"  
  },  
  "motion\_token\_library": "config/motion\_tokens.json"  
}

**Output:**

{  
  "agent\_id": "MotionTokenResolver",  
  "output": {  
    "resolved\_tokens": \[  
      {  
        "token\_id": "FADE\_IN",  
        "version": "1.0",  
        "target": "label",  
        "duration\_frames": 18,  
        "easing": "easeOutCubic",  
        "properties": {"opacity": \[0, 1\]}  
      },  
      {  
        "token\_id": "METER\_FILL\_SMOOTH",  
        "version": "1.0",  
        "target": "meter",  
        "duration\_frames": 30,  
        "easing": "easeOutCubic",  
        "properties": {"fill\_ratio": \[0, 0.7\]}  
      }  
    \],  
    "conflicts": \[\],  
    "validation\_status": "pass"  
  }  
}

---

### **3.12 OutputValidator**

**File:** /src/agents/output\_validator.py

**Purpose:** Final validation before marking pipeline complete

**Input:**

{  
  "rendered\_scenes": \[  
    {  
      "scene\_id": "RATING\_METER\_1\_TO\_10",  
      "output\_path": "data/rendered/RATING\_METER\_1\_TO\_10\_001.mp4",  
      "expected\_duration\_seconds": 5.0  
    }  
  \]  
}

**Output:**

{  
  "agent\_id": "OutputValidator",  
  "output": {  
    "validation\_results": \[  
      {  
        "scene\_id": "RATING\_METER\_1\_TO\_10",  
        "file\_exists": true,  
        "file\_size\_mb": 2.3,  
        "duration\_seconds": 5.0,  
        "duration\_match": true,  
        "dimensions": {"width": 1080, "height": 1920},  
        "codec": "h264",  
        "bitrate\_kbps": 3500,  
        "corrupted": false,  
        "validation\_status": "pass"  
      }  
    \],  
    "overall\_status": "pass",  
    "failed\_scenes": \[\],  
    "warnings": \[\]  
  }  
}

**Validation Checks:**

* File exists  
* Duration within tolerance (±0.1s)  
* Not corrupted (can open with ffprobe)  
* Correct dimensions  
* Reasonable file size  
* Valid codec

---

## **Complete Agent Pipeline Flow**

graph TD  
    A\[User Input\] \--\> B\[ContextAnalyzer\]  
    B \--\> C\[ScenePlanner\]  
    C \--\> D\[AssetValidator\]  
    D \--\> E{Assets OK?}  
    E \--\>|No| F\[ImageGenerator\]  
    E \--\>|Yes| G\[LayerExtractor\]  
    F \--\> G  
    G \--\> H\[SemanticLabeler\]  
    H \--\> I\[TextSynthesizer\]  
    I \--\> J\[ParameterFiller\]  
    J \--\> K\[SceneConfigBuilder\]  
    K \--\> L\[MotionTokenResolver\]  
    L \--\> M\[Renderer\]  
    M \--\> N\[OutputValidator\]  
    N \--\> O{All Pass?}  
    O \--\>|Yes| P\[Deliver Scenes\]  
    O \--\>|No| Q\[Retry/Report\]

---

## **Agent Execution Times (Typical)**

| Agent | Time (avg) | Parallelizable |
| ----- | ----- | ----- |
| ContextAnalyzer | 0.5s | No |
| ScenePlanner | 0.3s | No |
| AssetValidator | 0.2s | No |
| ImageGenerator | 4-8s | Yes (per image) |
| LayerExtractor | 3-6s | Yes (per image) |
| SemanticLabeler | 1-2s | Yes (per layer) |
| TextSynthesizer | 0.5-1s | Yes (per text) |
| ParameterFiller | 0.2s | No |
| SceneConfigBuilder | 0.1s | No |
| MotionTokenResolver | 0.1s | No |
| Renderer | 20-45s | Yes (per scene) |
| OutputValidator | 0.3s | Yes (per scene) |

---

## **Retry Policies by Agent**

### **No Retry**

* ScenePlanner (deterministic)  
* AssetValidator (file operations)  
* ParameterFiller (deterministic)  
* SceneConfigBuilder (deterministic)

### **Limited Retry (3x)**

* ContextAnalyzer (may have transient API failures)  
* ImageGenerator (API rate limits)  
* LayerExtractor (model timeouts)  
* SemanticLabeler (model timeouts)  
* TextSynthesizer (API failures)

### **Render-Specific (1x)**

* Renderer (expensive, rarely fails)  
* OutputValidator (no retry, just report)

