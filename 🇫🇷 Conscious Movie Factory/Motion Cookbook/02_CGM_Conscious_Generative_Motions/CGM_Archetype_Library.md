# CGM Archetype Library
## 12 Asset-Based Composition Patterns

---

## Archetype Index

| # | Archetype ID | Sonic Arc | Required Assets |
|---|--------------|-----------|-----------------|
| 1 | `QUOTE_CARD_CELEBRITY` | The Quiet Reflection | Celebrity cutout, quote |
| 2 | `QUOTE_CARD_PRESENTER` | The Authentic Voice | Avatar cutout, quote |
| 3 | `ICON_HEADER` | The Divine Spark | Icon, avatar |
| 4 | `ICON_HEADER_SOLO` | The Call to Adventure | Icon only |
| 5 | `SPLIT_HEADER` | The Breakthrough | E-Roll image, avatar |
| 6 | `SPLIT_HEADER_TEXT` | The Core Transformation | E-Roll image, headline |
| 7 | `IMMERSIVE_PRESENTER` | The Comedic Reframe | Avatar, full background |
| 8 | `IMMERSIVE_SCENE` | The Rally | Full background, text overlay |
| 9 | `CINEMATIC_B_ROLL` | The Ticking Clock | D-Roll/E-Roll image |
| 10 | `CINEMATIC_QUOTE` | The Shared Struggle | D-Roll image, quote |
| 11 | `LIVING_PORTRAIT` | The Patient Growth | Pre-animated video, quote |
| 12 | `DUAL_PRESENCE` | The Confrontation | Two cutouts |

---

## Archetype 1: QUOTE_CARD_CELEBRITY

### Purpose
Famous person cutout with inspirational quote.

### Required Assets
| Asset | Source | Required |
|-------|--------|----------|
| `celebrity_cutout` | D-Roll | ✓ |
| `gradient_background` | Brand Library | ✓ |
| `glow_overlay` | Generated | Optional |

### Layout JSON
```json
{
  "archetype": "QUOTE_CARD_CELEBRITY",
  "layers": [
    {"id": "bg", "type": "gradient", "z": 0, "colors": ["#1a1a2e", "#16213e"]},
    {"id": "glow", "type": "image", "z": 1, "blend": "screen", "opacity": 0.4},
    {"id": "celebrity", "type": "image", "z": 4, "position": {"x": "center", "y": 800}, "scale": 0.8},
    {"id": "quote", "type": "text", "z": 7, "font": "Playfair Display", "size": 48, "position": {"y": 300}},
    {"id": "attribution", "type": "text", "z": 8, "font": "Inter", "size": 28, "position": {"y": 520}}
  ]
}
```

### Animation Strategy
**First Frame**: Zoom out 10%, opacity 70%  
**Last Frame**: Full composition  
**Model**: VEO 3.1

---

## Archetype 2: QUOTE_CARD_PRESENTER

### Purpose
Coach/presenter avatar with their own quote.

### Required Assets
| Asset | Source | Required |
|-------|--------|----------|
| `avatar_cutout` | Brand Library | ✓ |
| `gradient_background` | Brand Library | ✓ |

### Layout JSON
```json
{
  "archetype": "QUOTE_CARD_PRESENTER",
  "layers": [
    {"id": "bg", "type": "gradient", "z": 0},
    {"id": "avatar", "type": "image", "z": 4, "position": {"x": "center", "y": 850}},
    {"id": "quote", "type": "text", "z": 7, "position": {"y": 280}},
    {"id": "name", "type": "text", "z": 8, "position": {"y": 500}}
  ]
}
```

---

## Archetype 3: ICON_HEADER

### Purpose
Large thematic icon above, presenter below.

### Required Assets
| Asset | Source | Required |
|-------|--------|----------|
| `icon` | Brand Library | ✓ |
| `avatar_cutout` | Brand Library | ✓ |
| `headline` | Script | ✓ |

### Layout JSON
```json
{
  "archetype": "ICON_HEADER",
  "layers": [
    {"id": "bg", "type": "gradient", "z": 0},
    {"id": "icon", "type": "image", "z": 2, "position": {"y": 400}, "scale": 1.2},
    {"id": "headline", "type": "text", "z": 5, "position": {"y": 700}},
    {"id": "avatar", "type": "image", "z": 6, "position": {"y": 1200}, "scale": 0.7}
  ]
}
```

---

## Archetype 4: ICON_HEADER_SOLO

### Purpose
Icon-focused without presenter (concept visualization).

### Required Assets
| Asset | Source | Required |
|-------|--------|----------|
| `icon` | Brand Library | ✓ |
| `headline` | Script | ✓ |

### Layout JSON
```json
{
  "archetype": "ICON_HEADER_SOLO",
  "layers": [
    {"id": "bg", "type": "gradient", "z": 0},
    {"id": "glow", "type": "radial", "z": 1},
    {"id": "icon", "type": "image", "z": 3, "position": {"y": 600}, "scale": 1.5},
    {"id": "headline", "type": "text", "z": 5, "position": {"y": 1100}}
  ]
}
```

---

## Archetype 5: SPLIT_HEADER

### Purpose
Real-world image in top half, presenter in bottom.

### Required Assets
| Asset | Source | Required |
|-------|--------|----------|
| `top_image` | E-Roll | ✓ |
| `avatar_cutout` | Brand Library | ✓ |

### Layout JSON
```json
{
  "archetype": "SPLIT_HEADER",
  "split_ratio": 0.5,
  "layers": [
    {"id": "top_image", "type": "image", "z": 0, "crop": {"y": 0, "h": 960}},
    {"id": "bottom_bg", "type": "gradient", "z": 1, "region": {"y": 960, "h": 960}},
    {"id": "avatar", "type": "image", "z": 4, "position": {"y": 1300}},
    {"id": "divider", "type": "line", "z": 5, "y": 960}
  ]
}
```

---

## Archetype 6: SPLIT_HEADER_TEXT

### Purpose
Real image top, headline text bottom (no avatar).

### Required Assets
| Asset | Source | Required |
|-------|--------|----------|
| `top_image` | E-Roll | ✓ |
| `headline` | Script | ✓ |
| `subhead` | Script | Optional |

### Layout JSON
```json
{
  "archetype": "SPLIT_HEADER_TEXT",
  "layers": [
    {"id": "top_image", "type": "image", "z": 0},
    {"id": "bottom_bg", "type": "gradient", "z": 1},
    {"id": "headline", "type": "text", "z": 4, "font_size": 56},
    {"id": "subhead", "type": "text", "z": 5, "font_size": 32}
  ]
}
```

---

## Archetype 7: IMMERSIVE_PRESENTER

### Purpose
Presenter integrated into full-frame background.

### Required Assets
| Asset | Source | Required |
|-------|--------|----------|
| `avatar_cutout` | Brand Library | ✓ |
| `background_image` | E-Roll/Generated | ✓ |

### Layout JSON
```json
{
  "archetype": "IMMERSIVE_PRESENTER",
  "layers": [
    {"id": "background", "type": "image", "z": 0, "fill": "cover"},
    {"id": "overlay", "type": "gradient", "z": 1, "opacity": 0.3},
    {"id": "avatar", "type": "image", "z": 4, "position": {"x": 270, "y": 1100}},
    {"id": "text", "type": "text", "z": 6, "position": {"x": 600, "y": 400}}
  ]
}
```

---

## Archetype 8: IMMERSIVE_SCENE

### Purpose
Full background with floating text (no presenter).

### Required Assets
| Asset | Source | Required |
|-------|--------|----------|
| `background_image` | E-Roll/D-Roll | ✓ |
| `text_overlay` | Script | ✓ |

### Layout JSON
```json
{
  "archetype": "IMMERSIVE_SCENE",
  "layers": [
    {"id": "background", "type": "image", "z": 0, "fill": "cover"},
    {"id": "darken", "type": "overlay", "z": 1, "color": "#000", "opacity": 0.4},
    {"id": "text", "type": "text", "z": 4, "position": {"y": 960}, "align": "center"}
  ]
}
```

---

## Archetype 9: CINEMATIC_B_ROLL

### Purpose
Full-frame cinematic image with minimal/no text.

### Required Assets
| Asset | Source | Required |
|-------|--------|----------|
| `image` | D-Roll/E-Roll | ✓ |
| `caption` | Script | Optional |

### Layout JSON
```json
{
  "archetype": "CINEMATIC_B_ROLL",
  "layers": [
    {"id": "image", "type": "image", "z": 0, "fill": "cover"},
    {"id": "vignette", "type": "overlay", "z": 2},
    {"id": "caption", "type": "text", "z": 4, "position": {"y": 1700}, "size": 24}
  ]
}
```

---

## Archetype 10: CINEMATIC_QUOTE

### Purpose
Cinematic image with overlaid quote.

### Required Assets
| Asset | Source | Required |
|-------|--------|----------|
| `image` | D-Roll | ✓ |
| `quote` | Script | ✓ |

### Layout JSON
```json
{
  "archetype": "CINEMATIC_QUOTE",
  "layers": [
    {"id": "image", "type": "image", "z": 0},
    {"id": "darken", "type": "gradient", "z": 1, "direction": "bottom", "opacity": 0.6},
    {"id": "quote", "type": "text", "z": 4, "position": {"y": 1200}},
    {"id": "attribution", "type": "text", "z": 5}
  ]
}
```

---

## Archetype 11: LIVING_PORTRAIT

### Purpose
Pre-animated idle loop with quote overlay.

### Required Assets
| Asset | Source | Required |
|-------|--------|----------|
| `living_portrait_video` | Pre-animated | ✓ |
| `quote` | Script | ✓ |

### Special Handling
This archetype uses a pre-animated RGBA video as the subject layer. No additional I2V animation needed for the subject.

### Layout JSON
```json
{
  "archetype": "LIVING_PORTRAIT",
  "layers": [
    {"id": "bg", "type": "gradient", "z": 0},
    {"id": "portrait_video", "type": "video", "z": 4, "loop": true},
    {"id": "quote", "type": "text", "z": 7},
    {"id": "grain", "type": "overlay", "z": 10}
  ]
}
```

---

## Archetype 12: DUAL_PRESENCE

### Purpose
Two figures/cutouts in composition (contrast, dialogue).

### Required Assets
| Asset | Source | Required |
|-------|--------|----------|
| `cutout_left` | D-Roll/Brand | ✓ |
| `cutout_right` | D-Roll/Brand | ✓ |

### Layout JSON
```json
{
  "archetype": "DUAL_PRESENCE",
  "layers": [
    {"id": "bg", "type": "gradient", "z": 0},
    {"id": "left_cutout", "type": "image", "z": 3, "position": {"x": 200}},
    {"id": "right_cutout", "type": "image", "z": 4, "position": {"x": 700}},
    {"id": "vs_text", "type": "text", "z": 6, "content": "VS", "position": {"x": "center"}}
  ]
}
```

---

## Animation Strategies

| Strategy | First Frame Effect | Best For |
|----------|-------------------|----------|
| `zoom_out` | Scale 90%, opacity 70% | Reveals, entrances |
| `fade_in` | All layers 50% opacity | Gentle entrances |
| `text_hidden` | Text layer removed | Text reveals |
| `position_shift` | Elements offset 50px | Movement |
| `blur_to_sharp` | Gaussian blur applied | Focus transitions |

---

## Asset Pool Paths

```
Brand Library/
├── avatars/
├── icons/
├── gradients/
└── overlays/

D-Roll Pool/
├── celebrities/
├── locations/
└── objects/

E-Roll Pool/
├── stock/
├── youtube_stills/
└── editorial/
```

---

*Library Version: 1.0.0*
