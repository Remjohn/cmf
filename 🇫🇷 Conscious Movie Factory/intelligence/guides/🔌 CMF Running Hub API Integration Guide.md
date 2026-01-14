# 🔌 CMF Running Hub API Integration Guide

**Version:** 1.0  
**Last Updated:** 2025-12-10  
**Compliance:** CMF Visual Engine ✅

---

## 📋 Overview

This guide documents the integration of the **CMF Visual Engine** with the **Running Hub API** for automated image and video generation. Running Hub provides cloud-based access to the AI models required for the CMF production pipeline.

### Supported Models

| Model | Purpose | CMF Function |
|-------|---------|--------------|
| **Z-Image-Turbo** | Text-to-Image | Generate END Frames (Hero Frames / Source Truth) |
| **Qwen-Image-Edit-2509** | Image Editing | Generate START Frames (Reverse Engineering) |
| **Qwen-Edit-2509-Light-Migration** | Lighting Transfer | Apply Atmospheric Lighting Presets |
| **Wan 2.2** | Image-to-Video | Animate keyframe pairs (Kinetic Engine) |

---

## 🔐 API Configuration

### Environment Variable Setup

Set your Running Hub API key as an environment variable:

**Windows (PowerShell):**
```powershell
$env:RUNNINGHUB_API_KEY = "31220af16a9b4af097038c4206a1a122"
```

**Windows (Command Prompt):**
```cmd
set RUNNINGHUB_API_KEY=31220af16a9b4af097038c4206a1a122
```

**Linux/macOS:**
```bash
export RUNNINGHUB_API_KEY="31220af16a9b4af097038c4206a1a122"
```

### Persistent Configuration (Recommended)

Add to your system environment variables or create a `.env` file in your project:
```
RUNNINGHUB_API_KEY=31220af16a9b4af097038c4206a1a122
```

---

## 📡 API Endpoints & Parameters

### 1. Z-Image-Turbo (Text-to-Image)

**Purpose:** Generate high-fidelity Hero Frames using the 5-Block Visual Anchor Architecture.

**Endpoint:** `https://api.runninghub.ai/v1/z-image-turbo`

**Method:** POST

**Headers:**
```
Authorization: Bearer $RUNNINGHUB_API_KEY
Content-Type: application/json
```

**Request Body:**
```json
{
  "prompt": "[5-BLOCK VISUAL ANCHOR PROMPT]",
  "negative_prompt": "No studio lighting, no perfect skin, no airbrushing, no fantasy elements, no cinematic teal/orange, no multiple people, no complex hand manipulations, no stock photo aesthetic, no morphing",
  "width": 1920,
  "height": 1080,
  "seed": 12345,
  "num_inference_steps": 30,
  "guidance_scale": 7.5
}
```

**Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `prompt` | string | ✅ | Full 5-Block Visual Anchor prompt |
| `negative_prompt` | string | ✅ | Exclusion terms for relatability |
| `width` | integer | ❌ | Output width (default: 1024) |
| `height` | integer | ❌ | Output height (default: 1024) |
| `seed` | integer | ❌ | Fixed seed for consistency across frames |
| `num_inference_steps` | integer | ❌ | Quality steps (default: 30) |
| `guidance_scale` | float | ❌ | Prompt adherence (default: 7.5) |

**Response:**
```json
{
  "status": "success",
  "output": {
    "image_url": "https://...",
    "seed_used": 12345
  }
}
```

---

### 2. Qwen-Image-Edit-2509 (Image Editing)

**Purpose:** Generate START Frames by reverse-engineering END Frames. Maintains pixel-perfect character consistency.

**Endpoint:** `https://api.runninghub.ai/v1/qwen-image-edit`

**Method:** POST

**Request Body:**
```json
{
  "image": "[BASE64_ENCODED_IMAGE or IMAGE_URL]",
  "prompt": "[QWEN-EDIT SURGICAL INSTRUCTION]",
  "negative_prompt": "morphing, distortion, identity change, facial structure change",
  "watermark": false
}
```

**Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `image` | string | ✅ | Base64 or URL of END Frame |
| `prompt` | string | ✅ | Qwen-Edit Reverse Engineering protocol |
| `negative_prompt` | string | ❌ | Prevent unwanted modifications |
| `watermark` | boolean | ❌ | Add watermark (default: false) |

**Prompt Structure (Qwen-Edit Protocol):**
```
[1. REFERENCE ANCHOR]
"The input image shows [Subject Description]. The lighting is [Current Lighting]."

[2. SURGICAL INSTRUCTION]
"Edit Instruction: Modify ONLY [Target Area]. Keep [Invariant Elements] unchanged."

[3. THE CHANGE]
"Change [Feature A] to [Feature B]."

[4. NEGATIVE CONSTRAINTS]
"Do not change the facial structure. Do not change clothing. No morphing."
```

---

### 3. Qwen-Edit-2509-Light-Migration (The Atmosphere Engine)

**Purpose:** Apply Structural Lighting Changes using "L-Roll" (Lighting Reference Images). Handles re-lighting, day-to-night conversion, and volumetrics.

**Endpoint:** `https://api.runninghub.ai/v1/qwen-lighting`

**Method:** POST

**Request Body:**
```json
{
  "image": "[BASE64_OF_SOURCE_FRAME]",
  "light_reference": "[BASE64_OF_L_ROLL_IMAGE]",
  "prompt": "[DIRECTIONAL_CUE]",
  "trigger": "参考色调，移除图1原有的光照并参考图2的光照和色调对图1重新照明",
  "batch_size": 4
}
```

**Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `image` | string | ✅ | Base asset to re-light |
| `light_reference` | string | ✅ | **L-Roll Image** (Dictates physics/texture) |
| `prompt` | string | ✅ | Directional cue (e.g., "Light from top right") |
| `trigger` | string | ✅ | Mandatory Chinese trigger phrase |
| `batch_size` | integer | ✅ | **Must be 4** (Mitigates randomness) |

**⚠️ Critical Protocols:**
1.  **Reference over Prompt:** The L-Roll image does 90% of the work. The prompt only sets direction.
2.  **Match Domains:** Use Indoor L-Roll for Indoor scenes, Outdoor L-Roll for Outdoor scenes.
3.  **De-Lighting:** To make an image look authentic (D-Roll), use `04_soft_window_overcast.jpg`.

**L-Roll Library (Lighting References):**
1.  **Epiphany:** `01_tyndall_beams.jpg` (God Rays/Volumetrics)
2.  **Prison/Anxiety:** `02_venetian_blinds.jpg` (Striped Shadows)
3.  **Cyberpunk:** `03_neon_cyan_magenta.jpg` (Future/Tech)
4.  **De-Lighting:** `04_soft_window_overcast.jpg` (Authentic/Raw)
5.  **Community:** `05_campfire_warmth.jpg` (Warm/Safe)
6.  **Truth:** `06_harsh_noir_spotlight.jpg` (High Contrast/Noir)

---

### 4. Wan 2.2 (Image-to-Video)

**Purpose:** Animate paired keyframes using the Kinetic Prompt Architecture.

**Endpoint:** `https://api.runninghub.ai/v1/wan-i2v`

**Method:** POST

**Request Body:**
```json
{
  "start_image": "[BASE64_OF_START_FRAME]",
  "end_image": "[BASE64_OF_END_FRAME]",
  "prompt": "[KINETIC PROMPT]",
  "negative_prompt": "morphing, melting face, extra limbs, disappearing objects, jerky transition, cartoon physics",
  "duration": 4,
  "fps": 24,
  "resolution": "1080p"
}
```

**Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `start_image` | string | ✅ | Base64 of START Frame |
| `end_image` | string | ✅ | Base64 of END Frame |
| `prompt` | string | ✅ | Kinetic Prompt (camera + action) |
| `negative_prompt` | string | ✅ | Quality control exclusions |
| `duration` | integer | ❌ | Video length in seconds (default: 4) |
| `fps` | integer | ❌ | Frames per second (default: 24) |
| `resolution` | string | ❌ | Output resolution (default: 1080p) |

**Kinetic Prompt Structure:**
```
[1. INPUT CONTEXT]
"Reference shows [Subject] in [Environment]. Vibe is [Mood]."

[2. CAMERA DYNAMICS]
"Camera Movement: [Technique]. Camera Physics: [Weight]."

[3. SUBJECT ACTION]
"Primary Action: [Main verb]. Micro-Movement: [Nuance]. Timing: [Pacing]."

[4. ATMOSPHERIC MOTION]
"Background: [Dynamics]."

[5. ANCHOR]
"Maintain: [Locked details]."
```

---

## 🔄 CMF Production Pipeline

### Complete Workflow

```
┌─────────────────────────────────────────────────────────────┐
│  STEP 1: Generate END Frames (Hero Frames)                  │
│  Model: Z-Image-Turbo                                       │
│  Input: 5-Block Visual Anchor Prompt                        │
│  Output: [Song]_Cut[X.X]_END.png                           │
└─────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────┐
│  STEP 2: Generate START Frames (Reverse Engineering)        │
│  Model: Qwen-Image-Edit-2509                                │
│  Input: END Frame + Surgical Edit Instruction               │
│  Output: [Song]_Cut[X.X]_START.png                         │
└─────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────┐
│  STEP 3: Apply Atmospheric Lighting (Optional)              │
│  Model: Qwen-Edit-2509-Light-Migration                      │
│  Input: Frame + Light Reference + Preset Description        │
│  Output: Relit frame                                        │
└─────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────┐
│  STEP 4: Generate Video Clips                               │
│  Model: Wan 2.2 (I2V)                                       │
│  Input: START + END Frames + Kinetic Prompt                 │
│  Output: [Song]_Cut[X.X]_VIDEO.mp4                         │
└─────────────────────────────────────────────────────────────┘
```

---

## 🛠️ Example cURL Commands

### Generate Hero Frame (END Frame)
```bash
curl -X POST https://api.runninghub.ai/v1/z-image-turbo \
  -H "Authorization: Bearer $RUNNINGHUB_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "Subject: Baseem, 30yo Middle Eastern male, short boxed beard, weary eyes, wearing a heather-grey textured t-shirt. Action: Baseem is smiling, Golden Hour Wrap Light. Framing: Medium close-up. Aesthetic: Shot on iPhone, grainy film. No studio lighting, no perfect skin.",
    "negative_prompt": "studio lighting, perfect skin, airbrushing, fantasy, stock photo",
    "width": 1920,
    "height": 1080,
    "seed": 42
  }'
```

### Reverse-Engineer START Frame
```bash
curl -X POST https://api.runninghub.ai/v1/qwen-image-edit \
  -H "Authorization: Bearer $RUNNINGHUB_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "image": "https://your-storage.com/Song_Cut1.1_END.png",
    "prompt": "The input image shows Baseem smiling in golden light. Edit Instruction: Modify ONLY the facial expression and lighting. Keep clothing folds, hair strands, camera angle unchanged. Change the confident smile to an anxious grimace. Change lighting to cold blue, Blade-Through-Shadows preset. Do not change facial structure.",
    "negative_prompt": "morphing, identity change"
  }'
```

### Apply Atmospheric Lighting (L-Roll Protocol)
```bash
curl -X POST https://api.runninghub.ai/v1/qwen-lighting \
  -H "Authorization: Bearer $RUNNINGHUB_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "image": "[BASE64_SOURCE]",
    "light_reference": "[BASE64_L_ROLL_TYNDALL]",
    "prompt": "Light source from top right. Holy atmosphere.",
    "trigger": "参考色调，移除图1原有的光照并参考图2的光照和色调对图1重新照明",
    "batch_size": 4
  }'
```

### Generate Video Clip
```bash
curl -X POST https://api.runninghub.ai/v1/wan-i2v \
  -H "Authorization: Bearer $RUNNINGHUB_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "start_image": "[BASE64_START]",
    "end_image": "[BASE64_END]",
    "prompt": "Reference shows anxious man in cold blue light. Camera: Slow push-in, smooth dolly. Action: Subject lifts gaze from hands. Blinks slowly. Jaw unclenches. Micro-movement: Chest rises with deep breath. Maintain: Scar on cheek, hoodie texture.",
    "negative_prompt": "morphing, melting, extra limbs, jerky",
    "duration": 5,
    "fps": 24
  }'
```

---

## ⚠️ Error Handling

| Error Code | Meaning | Solution |
|------------|---------|----------|
| 401 | Invalid API key | Check `RUNNINGHUB_API_KEY` |
| 429 | Rate limit exceeded | Wait and retry |
| 400 | Invalid parameters | Check prompt format |
| 503 | Model unavailable | Retry after delay |

---

## 📁 File Naming Convention

```
[Song Title]_Cut[Scene.Cut]_[Type].extension

Examples:
- ReveilDuCoeur_Cut1.1_END.png
- ReveilDuCoeur_Cut1.1_START.png
- ReveilDuCoeur_Cut1.1_VIDEO.mp4
```

---

## 📚 Reference Documents

- [🔶🎬 CMF Visual Engine: Master Technical Architecture](file:///d:/Work/The%20Conscious%20Movie%20Factory%20December/🔶🎬%20The%20CMF%20Visual%20Engine_%20Master%20Technical%20Architecture%20&%20Kinetic%20Protocols%20🎬🔶.md)
- [🌞🎵 Virtual Director V5.0 - Song-First Edition](file:///d:/Work/The%20Conscious%20Movie%20Factory%20December/🇫🇷%20Conscious%20Movie%20Factory/intelligence/guides/🌞🎵%20The%20Virtual%20Director%20&%20Storyboard%20Architect%20-%20Song-First%20Edition.md)
- [🌞 CMF Master Execution Workflow V12](file:///d:/Work/The%20Conscious%20Movie%20Factory%20December/🇫🇷%20Conscious%20Movie%20Factory/intelligence/guides/🌞%20CMF%20Master%20Execution%20Workflow%20V12.md)

---

**Compliance:** CMF Visual Engine ✅ | Running Hub API ✅ | Sub-Plan 3 Integration ✅
