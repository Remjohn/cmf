# CGM Layout JSON Schema
## PosterCopilot Composition Specification

---

## Schema Overview

All CGM compositions are defined using this JSON schema. The schema follows PosterCopilot principles for predictable, reproducible frame composition.

---

## Root Schema

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "title": "CGM Layout Specification",
  "type": "object",
  "required": ["layout_id", "archetype", "canvas", "layers"],
  "properties": {
    "layout_id": {
      "type": "string",
      "description": "Unique identifier: [PROJECT]_[SCENE]_CGM_[ARCHETYPE]"
    },
    "archetype": {
      "type": "string",
      "enum": [
        "QUOTE_CARD_CELEBRITY", "QUOTE_CARD_PRESENTER",
        "ICON_HEADER", "ICON_HEADER_SOLO",
        "SPLIT_HEADER", "SPLIT_HEADER_TEXT",
        "IMMERSIVE_PRESENTER", "IMMERSIVE_SCENE",
        "CINEMATIC_B_ROLL", "CINEMATIC_QUOTE",
        "LIVING_PORTRAIT", "DUAL_PRESENCE"
      ]
    },
    "canvas": {
      "type": "object",
      "properties": {
        "width": {"type": "integer", "const": 1080},
        "height": {"type": "integer", "const": 1920}
      }
    },
    "layers": {
      "type": "array",
      "items": {"$ref": "#/$defs/layer"}
    },
    "animation_config": {
      "$ref": "#/$defs/animation_config"
    }
  }
}
```

---

## Layer Types

### Image Layer

```json
{
  "id": "celebrity_cutout",
  "type": "image",
  "z_index": 4,
  "source": "d_roll/celebrity_maya_angelou_001.png",
  "position": {
    "x": "center",
    "y": 800
  },
  "scale": 0.8,
  "opacity": 1.0,
  "blend_mode": "normal"
}
```

### Gradient Layer

```json
{
  "id": "background",
  "type": "gradient",
  "z_index": 0,
  "direction": "vertical",
  "colors": ["#1a1a2e", "#16213e"],
  "stops": [0, 1]
}
```

### Text Layer

```json
{
  "id": "quote_text",
  "type": "text",
  "z_index": 7,
  "content": "The body keeps the score",
  "font": "Playfair Display",
  "font_weight": "bold",
  "font_size": 48,
  "color": "#ffffff",
  "position": {
    "x": "center",
    "y": 300
  },
  "max_width": 900,
  "align": "center",
  "line_height": 1.3
}
```

### Overlay Layer

```json
{
  "id": "glow_overlay",
  "type": "overlay",
  "z_index": 1,
  "source": "generated/glow_soft_gold.png",
  "blend_mode": "screen",
  "opacity": 0.4
}
```

### Video Layer (Living Portrait)

```json
{
  "id": "portrait_video",
  "type": "video",
  "z_index": 4,
  "source": "living_portraits/audrey_idle_01.mp4",
  "loop": true,
  "position": {"x": "center", "y": 700}
}
```

---

## Position Values

| Value | Meaning |
|-------|---------|
| `"center"` | Centered on axis |
| `integer` | Pixel offset from origin |
| `"left"` | 0 + safe_margin |
| `"right"` | canvas_width - element_width - safe_margin |
| `"top"` | 0 + safe_margin |
| `"bottom"` | canvas_height - element_height - safe_margin |

---

## Blend Modes

| Mode | Pillow Equivalent | Use Case |
|------|-------------------|----------|
| `normal` | Alpha composite | Standard layering |
| `multiply` | ImageChops.multiply | Darken |
| `screen` | ImageChops.screen | Lighten, glows |
| `overlay` | Custom | Contrast |
| `soft_light` | Custom | Subtle grading |

---

## Animation Config

```json
{
  "animation_config": {
    "model": "Wan 2.2",
    "strategy": "zoom_out",
    "first_frame_path": "outputs/frames/CGM/first/scene_001.png",
    "last_frame_path": "outputs/frames/CGM/scene_001.png",
    "duration_seconds": 5.0,
    "fps": 30
  }
}
```

### Strategies

| Strategy | First Frame Transform |
|----------|----------------------|
| `zoom_out` | Scale 0.9, opacity 0.7 |
| `fade_in` | Opacity 0.5 all layers |
| `text_hidden` | Remove text layers |
| `position_shift` | Offset elements 50px |

---

## Complete Example

```json
{
  "layout_id": "audrey_005_CGM_QUOTE_CARD_CELEBRITY",
  "archetype": "QUOTE_CARD_CELEBRITY",
  "version": "1.0.0",
  "canvas": {
    "width": 1080,
    "height": 1920
  },
  "layers": [
    {
      "id": "background",
      "type": "gradient",
      "z_index": 0,
      "direction": "vertical",
      "colors": ["#1a1a2e", "#16213e"]
    },
    {
      "id": "glow_overlay",
      "type": "overlay",
      "z_index": 1,
      "source": "generated/glow_soft_gold.png",
      "blend_mode": "screen",
      "opacity": 0.4
    },
    {
      "id": "celebrity_cutout",
      "type": "image",
      "z_index": 4,
      "source": "d_roll/celebrity_maya_angelou_001.png",
      "position": {"x": "center", "y": 800},
      "scale": 0.8
    },
    {
      "id": "quote_text",
      "type": "text",
      "z_index": 7,
      "content": "We delight in the beauty of the butterfly, but rarely admit the changes it has gone through to achieve that beauty.",
      "font": "Playfair Display",
      "font_size": 48,
      "color": "#ffffff",
      "position": {"x": "center", "y": 300},
      "max_width": 900,
      "align": "center"
    },
    {
      "id": "attribution",
      "type": "text",
      "z_index": 8,
      "content": "— Maya Angelou",
      "font": "Inter",
      "font_weight": "semibold",
      "font_size": 28,
      "color": "#b0b0b0",
      "position": {"x": "center", "y": 520}
    }
  ],
  "animation_config": {
    "model": "Wan 2.2",
    "strategy": "zoom_out",
    "duration_seconds": 5.0,
    "fps": 30
  }
}
```

---

## Validation Rules

1. **canvas** must be exactly 1080×1920
2. **z_index** must be unique per layer
3. **source** paths must exist or be flagged for generation
4. **font** must be from approved list
5. **text** content must fit within max_width
6. **opacity** must be 0.0-1.0
7. **colors** must be valid hex codes

---

## Approved Fonts

| Font | Weight | Use |
|------|--------|-----|
| `Inter` | Regular, SemiBold, Bold | Body, labels |
| `Playfair Display` | Regular, Bold | Quotes, headlines |
| `Montserrat` | SemiBold, Bold | Emphasis |

---

*Schema Version: 1.0.0*
