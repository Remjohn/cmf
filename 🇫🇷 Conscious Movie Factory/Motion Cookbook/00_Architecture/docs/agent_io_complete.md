# **agent\_io\_complete.md**

**Purpose:** Complete I/O specifications for all 12 agents  
 **Status:** Canonical reference v1.0

---

## **Overview**

This document provides complete input/output schemas for all 12 agents in the Motion Cookbook pipeline.

---

## **1\. ContextAnalyzer ✅**

**Purpose:** Interpret user intent and extract key concepts

**Input Schema:**

{  
  "script": "string (required)",  
  "topic": "string (optional)",  
  "intent": "enum: explain|emphasize|storytelling|social\_proof (optional)",  
  "metadata": {  
    "speaker\_name": "string (optional)",  
    "video\_type": "string (optional)"  
  }  
}

**Output Schema:**

{  
  "agent\_id": "ContextAnalyzer",  
  "version": "1.0",  
  "output": {  
    "topic": "string",  
    "intent": "enum",  
    "ratings\_detected": \[  
      {  
        "value": "number",  
        "context": "current|before|after"  
      }  
    \],  
    "key\_concepts": \["string\[\]"\],  
    "emotional\_tone": "string",  
    "confidence": "number (0-1)"  
  }  
}

---

## **2\. ScenePlanner ✅**

**Purpose:** Select appropriate scenes based on context

**Input Schema:**

{  
  "output": {  
    "topic": "string",  
    "intent": "enum",  
    "ratings\_detected": "array",  
    "key\_concepts": "string\[\]"  
  },  
  "constraints": {  
    "min\_scenes": "number (default: 5)",  
    "max\_scenes": "number (default: 7)",  
    "force\_scenes": "string\[\] (optional)"  
  },  
  "available\_scenes": "string\[\] (optional)"  
}

**Output Schema:**

{  
  "agent\_id": "ScenePlanner",  
  "version": "1.0",  
  "output": {  
    "selected\_scenes": \[  
      {  
        "scene\_id": "string",  
        "priority": "number",  
        "rationale": "string",  
        "confidence": "number (0-1)"  
      }  
    \],  
    "analyzed\_context": "object (passed through)"  
  }  
}

---

## **3\. AssetValidator 🚧**

**Purpose:** Validate asset availability and quality

**Input Schema:**

{  
  "plan": {  
    "selected\_scenes": "array"  
  },  
  "assets": {  
    "user\_provided": \["string\[\] (paths)"\],  
    "required\_by\_scenes": \[  
      {  
        "scene\_id": "string",  
        "requires": "string\[\]"  
      }  
    \]  
  }  
}

**Output Schema:**

{  
  "agent\_id": "AssetValidator",  
  "version": "1.0",  
  "output": {  
    "validation\_status": "pass|partial|fail",  
    "available\_assets": \[  
      {  
        "asset\_id": "string",  
        "path": "string",  
        "type": "string (mime type)",  
        "dimensions": {"width": "number", "height": "number"},  
        "file\_size\_mb": "number",  
        "quality\_score": "number (0-1)"  
      }  
    \],  
    "missing\_assets": \["string\[\]"\],  
    "warnings": \[  
      {  
        "asset\_id": "string",  
        "warning": "string",  
        "recommendation": "string"  
      }  
    \]  
  }  
}

**Validation Rules:**

* File exists and readable  
* Supported format (PNG, JPEG, WebP, MP4)  
* Minimum dimensions: 1080px (shortest side)  
* Maximum file size: 50MB  
* Not corrupted (can be opened)

---

## **4\. ImageGenerator 📋**

**Purpose:** Generate missing images using AI models

**Input Schema:**

{  
  "missing\_assets": \["string\[\] (asset descriptions)"\],  
  "prompts": \[  
    {  
      "asset\_id": "string",  
      "prompt": "string",  
      "style": "string",  
      "aspect\_ratio": "string (default: 9:16)",  
      "model": "enum: qwen\_image\_2512|nanobanana\_pro|zimage\_turbo"  
    }  
  \],  
  "context": {  
    "topic": "string",  
    "key\_concepts": "string\[\]"  
  }  
}

**Output Schema:**

{  
  "agent\_id": "ImageGenerator",  
  "version": "1.0",  
  "output": {  
    "generated\_images": \[  
      {  
        "asset\_id": "string",  
        "path": "string",  
        "model\_used": "string",  
        "prompt\_used": "string",  
        "dimensions": {"width": "number", "height": "number"},  
        "generation\_time\_ms": "number",  
        "success": "boolean"  
      }  
    \],  
    "failed\_generations": \[  
      {  
        "asset\_id": "string",  
        "error": "string",  
        "retry\_recommended": "boolean"  
      }  
    \]  
  }  
}

**Supported Models:**

* qwen\_image\_2512: General purpose, high quality  
* nanobanana\_pro: Complex diagrams, maps, technical  
* zimage\_turbo: Fast, stylized content

---

## **5\. LayerExtractor 🚧**

**Purpose:** Decompose images into RGBA layers

**Input Schema:**

{  
  "assets": \[  
    {  
      "asset\_id": "string",  
      "path": "string",  
      "method": "enum: qwen\_layered|sam3|manual (default: qwen\_layered)"  
    }  
  \],  
  "output\_dir": "string (default: data/layer\_graphs/)"  
}

**Output Schema:**

{  
  "agent\_id": "LayerExtractor",  
  "version": "1.0",  
  "output": {  
    "layer\_graphs": \[  
      {  
        "graph\_id": "string",  
        "source\_asset": "string",  
        "extraction\_method": "string",  
        "extraction\_confidence": "number (0-1)",  
        "layers": \[  
          {  
            "layer\_id": "string",  
            "rgba\_asset": "string (path)",  
            "bbox": {  
              "x": "number (0-1)",  
              "y": "number (0-1)",  
              "w": "number (0-1)",  
              "h": "number (0-1)"  
            },  
            "z\_index": "number",  
            "type": "enum: image|region|cutout",  
            "extraction\_confidence": "number (0-1)"  
          }  
        \],  
        "processing\_time\_ms": "number"  
      }  
    \],  
    "failed\_extractions": \[  
      {  
        "asset\_id": "string",  
        "error": "string",  
        "fallback\_strategy": "use\_whole\_image|skip|retry"  
      }  
    \]  
  }  
}

**Extraction Methods:**

* qwen\_layered: Automatic layering (default)  
* sam3: High-quality segmentation  
* manual: User-provided layers

---

## **6\. SemanticLabeler 🚧**

**Purpose:** Assign semantic tags to layers

**Input Schema:**

{  
  "layer\_graphs": \[  
    {  
      "graph\_id": "string",  
      "layers": \[  
        {  
          "layer\_id": "string",  
          "rgba\_asset": "string",  
          "bbox": "object"  
        }  
      \]  
    }  
  \],  
  "context": {  
    "topic": "string",  
    "key\_concepts": "string\[\]"  
  }  
}

**Output Schema:**

{  
  "agent\_id": "SemanticLabeler",  
  "version": "1.0",  
  "output": {  
    "labeled\_layer\_graphs": \[  
      {  
        "graph\_id": "string",  
        "layers": \[  
          {  
            "layer\_id": "string",  
            "semantics": \["string\[\]"\],  
            "confidence": "number (0-1)",  
            "primary\_semantic": "string",  
            "allowed\_transforms": \["string\[\]"\]  
          }  
        \]  
      }  
    \],  
    "low\_confidence\_layers": \[  
      {  
        "graph\_id": "string",  
        "layer\_id": "string",  
        "confidence": "number",  
        "warning": "string"  
      }  
    \]  
  }  
}

**Semantic Taxonomy:**

* body, anatomy, region  
* person, speaker, subject  
* background, foreground  
* gut, brain, heart (body-specific)  
* hub, node, connection (diagram-specific)  
* cause, effect, problem, solution (concept-specific)

---

## **7\. TextSynthesizer 📋**

**Purpose:** Generate concise explainer copy

**Input Schema:**

{  
  "context": {  
    "topic": "string",  
    "key\_concepts": "string\[\]",  
    "intent": "string"  
  },  
  "text\_requests": \[  
    {  
      "type": "enum: headline|subtext|definition|label",  
      "max\_length": "number",  
      "tone": "enum: educational|emotional|neutral",  
      "required\_concepts": "string\[\] (optional)"  
    }  
  \]  
}

**Output Schema:**

{  
  "agent\_id": "TextSynthesizer",  
  "version": "1.0",  
  "output": {  
    "generated\_texts": \[  
      {  
        "type": "string",  
        "text": "string",  
        "character\_count": "number",  
        "confidence": "number (0-1)",  
        "alternatives": \["string\[\]"\]  
      }  
    \]  
  }  
}

**Text Types:**

* headline: 5-50 characters, punchy  
* subtext: 10-100 characters, explanatory  
* definition: 50-200 characters, formal  
* label: 3-20 characters, concise

---

## **8\. ParameterFiller ✅**

**Purpose:** Fill scene parameters from context \+ layers

**Input Schema:**

{  
  "selected\_scenes": \["array"\],  
  "layer\_graphs": \["array"\],  
  "labeled\_layers": \["array"\],  
  "context": "object",  
  "brand\_kit\_id": "string"  
}

**Output Schema:**

{  
  "agent\_id": "ParameterFiller",  
  "version": "1.0",  
  "output": {  
    "filled\_scenes": \[  
      {  
        "scene\_id": "string",  
        "parameters": "object (scene-specific)",  
        "layer\_assignments": "object (optional)",  
        "completeness": "number (0-1)",  
        "missing\_params": \["string\[\]"\],  
        "warnings": \["string\[\]"\]  
      }  
    \]  
  }  
}

---

## **9\. SceneConfigBuilder ✅**

**Purpose:** Combine all outputs into final scene configs

**Input Schema:**

{  
  "filled\_scenes": \["array"\],  
  "layer\_graphs": \["array"\],  
  "brand\_kit\_id": "string",  
  "timing\_mode": "enum: absolute|speech\_aligned (default: absolute)",  
  "speech\_anchors": "object (optional)"  
}

**Output Schema:**

{  
  "agent\_id": "SceneConfigBuilder",  
  "version": "1.0",  
  "output": {  
    "scene\_configs": \[  
      {  
        "scene\_id": "string",  
        "version": "string",  
        "config\_id": "string (UUID)",  
        "layer\_graph\_id": "string (optional)",  
        "brand\_kit\_id": "string",  
        "parameters": "object",  
        "timing": {  
          "mode": "string",  
          "duration\_frames": "number",  
          "fps": "number",  
          "anchors": "object (optional)"  
        },  
        "output\_path": "string"  
      }  
    \],  
    "build\_timestamp": "string (ISO 8601)"  
  }  
}

---

## **10\. MotionTokenResolver ✅**

**Purpose:** Validate and resolve motion token references

**Input Schema:**

{  
  "scene\_configs": \["array"\],  
  "motion\_token\_library": "string (path, default: config/motion\_tokens.json)"  
}

**Output Schema:**

{  
  "agent\_id": "MotionTokenResolver",  
  "version": "1.0",  
  "output": {  
    "resolved\_configs": \[  
      {  
        "scene\_id": "string",  
        "resolved\_tokens": \[  
          {  
            "token\_id": "string",  
            "version": "string",  
            "target": "string",  
            "duration\_frames": "number",  
            "easing": "string",  
            "properties": "object"  
          }  
        \],  
        "conflicts": \["string\[\]"\],  
        "validation\_status": "pass|warning|fail"  
      }  
    \]  
  }  
}

**Validation Checks:**

* All tokens exist in library  
* No conflicting tokens on same target  
* Token durations fit within scene duration  
* Parameters are valid

---

## **11\. SpeechAnalyzer 📋**

**Purpose:** Extract temporal anchors from audio

**Input Schema:**

{  
  "audio": "string (path, required)",  
  "transcript": "string (optional)",  
  "scene\_duration\_frames": "number (required)",  
  "fps": "number (default: 30)"  
}

**Output Schema:**

{  
  "agent\_id": "SpeechAnalyzer",  
  "version": "1.0",  
  "output": {  
    "anchors": {  
      "response\_start": "number (frame)",  
      "response\_peak": "number (frame)",  
      "response\_end": "number (frame)",  
      "pause\_mid": "number (frame, optional)"  
    },  
    "confidence": "number (0-1)",  
    "speech\_segments": \[  
      {  
        "start": "number (seconds)",  
        "end": "number (seconds)",  
        "duration": "number (seconds)"  
      }  
    \],  
    "detected\_pauses": \["number\[\] (seconds)"\],  
    "energy\_peaks": \["number\[\] (seconds)"\]  
  }  
}

**Fallback:** If no speech detected or confidence \< 0.7, returns empty anchors.

---

## **12\. OutputValidator ✅**

**Purpose:** Final validation of rendered outputs

**Input Schema:**

{  
  "rendered\_scenes": \[  
    {  
      "scene\_id": "string",  
      "output\_path": "string",  
      "expected\_duration\_seconds": "number"  
    }  
  \]  
}

**Output Schema:**

{  
  "agent\_id": "OutputValidator",  
  "version": "1.0",  
  "output": {  
    "validation\_results": \[  
      {  
        "scene\_id": "string",  
        "file\_exists": "boolean",  
        "file\_size\_mb": "number",  
        "duration\_seconds": "number",  
        "duration\_match": "boolean",  
        "dimensions": {"width": "number", "height": "number"},  
        "codec": "string",  
        "bitrate\_kbps": "number",  
        "corrupted": "boolean",  
        "validation\_status": "pass|fail"  
      }  
    \],  
    "overall\_status": "pass|partial|fail",  
    "failed\_scenes": \["string\[\]"\],  
    "warnings": \["string\[\]"\]  
  }  
}

---

## **Agent Dependencies**

ContextAnalyzer  
  ↓  
ScenePlanner  
  ↓  
AssetValidator  
  ├──→ ImageGenerator (if assets missing)  
  └──→ LayerExtractor  
        ↓  
      SemanticLabeler  
        ↓  
      TextSynthesizer (parallel)  
        ↓  
      ParameterFiller  
        ↓  
      SceneConfigBuilder  
        ↓  
      MotionTokenResolver  
        ↓  
      (Renderer \- external)  
        ↓  
      OutputValidator

---

## **Error Handling Standards**

All agents must follow this error format:

{  
  "error": "ERROR\_CODE",  
  "message": "Human-readable description",  
  "agent\_id": "string",  
  "input\_hash": "string",  
  "timestamp": "string (ISO 8601)"  
}

**Common Error Codes:**

* INVALID\_INPUT  
* SCHEMA\_VALIDATION\_FAILED  
* PROCESSING\_TIMEOUT  
* EXTERNAL\_API\_FAILURE  
* INSUFFICIENT\_CONFIDENCE  
* MISSING\_DEPENDENCY

---

