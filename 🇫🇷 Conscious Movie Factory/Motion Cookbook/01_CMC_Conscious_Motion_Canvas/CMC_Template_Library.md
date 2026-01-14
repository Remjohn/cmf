# CMC Template Library
## 12 Motion Canvas Scene Specifications

---

## Template Index

| # | Template ID | Sonic Arc | Visual Purpose |
|---|-------------|-----------|----------------|
| 1 | `RATING_METER_1_TO_10` | The Patient Growth | Quantify progress |
| 2 | `BEFORE_AFTER_SELF_SCORE` | The Core Transformation | Visualize change |
| 3 | `BODY_MAP_FOCUS` | The Divine Spark | Locate intuition |
| 4 | `CONFIDENCE_BAR_LIVE` | The Breakthrough | Measure courage |
| 5 | `PROGRESS_DELTA_BADGE` | The Rally | Celebrate momentum |
| 6 | `KINETIC_DEFINITION` | The Authentic Voice | Define key terms |
| 7 | `QUOTE_CARD` | The Quiet Reflection | Anchor wisdom |
| 8 | `CONSENSUS_SCORE_STACK` | The Shared Struggle | Show collective data |
| 9 | `CUTOUT_METAPHOR` | The Call to Adventure | Visualize concepts |
| 10 | `MISCONCEPTION_TRUTH` | The Confrontation | Contrast beliefs |
| 11 | `BRAND_AVATAR_FLOAT` | The Comedic Reframe | Establish presence |
| 12 | `RHYTHMIC_ABSTRACT` | The Ticking Clock | Create urgency |

---

## Template 1: RATING_METER_1_TO_10

### Purpose
Visualize a rating or score on a 1-10 scale with animated fill.

### Input Parameters
```json
{
  "score": 8,
  "label": "Energy Level",
  "color_accent": "#6A1B9A"
}
```

### Layer Structure
| Layer | Type | Z-Index | Animation |
|-------|------|---------|-----------|
| background | gradient | 0 | none |
| meter_track | rounded_rect | 1 | ENTER_FADE |
| meter_fill | animated_rect | 2 | PROGRESS_FILL (0→score*10%) |
| score_text | text | 3 | ENTER_SCALE (delayed 1.5s) |
| label_text | text | 4 | ENTER_FADE (delayed 2s) |

### Duration
4-5 seconds

### Example Output
"8/10" with horizontal bar filling to 80%

---

## Template 2: BEFORE_AFTER_SELF_SCORE

### Purpose
Split-screen comparison showing transformation.

### Input Parameters
```json
{
  "before_value": 3,
  "after_value": 8,
  "before_label": "Then",
  "after_label": "Now",
  "metric_label": "Confidence"
}
```

### Layer Structure
| Layer | Type | Z-Index | Animation |
|-------|------|---------|-----------|
| background | gradient | 0 | none |
| divider | line | 1 | ENTER_FADE |
| before_circle | circle | 2 | ENTER_SCALE |
| after_circle | circle | 3 | ENTER_SCALE (delayed 0.5s) |
| before_value | text | 4 | ENTER_FADE |
| after_value | text | 5 | ENTER_FADE (delayed 0.5s) |
| arrow | icon | 6 | SLIDE_IN (delayed 1s) |

### Duration
5-6 seconds

---

## Template 3: BODY_MAP_FOCUS

### Purpose
Highlight a body region with glowing focus area.

### Input Parameters
```json
{
  "focus_region": "heart",
  "glow_color": "#FF6B6B",
  "label": "Listen Here"
}
```

### Layer Structure
| Layer | Type | Z-Index | Animation |
|-------|------|---------|-----------|
| background | gradient | 0 | none |
| body_silhouette | svg | 1 | ENTER_FADE |
| focus_glow | radial_gradient | 2 | PULSE (loop) |
| focus_icon | icon | 3 | ENTER_SCALE |
| label_text | text | 4 | ENTER_FADE (delayed 1s) |

### Focus Regions
`head`, `heart`, `gut`, `hands`, `chest`, `solar_plexus`, `throat`

### Duration
4-5 seconds

---

## Template 4: CONFIDENCE_BAR_LIVE

### Purpose
Vertical bar chart showing courage/confidence metric.

### Input Parameters
```json
{
  "bars": [
    {"label": "Fear", "value": 30, "color": "#E53935"},
    {"label": "Courage", "value": 70, "color": "#43A047"}
  ]
}
```

### Layer Structure
| Layer | Type | Z-Index | Animation |
|-------|------|---------|-----------|
| background | gradient | 0 | none |
| bar_1 | animated_rect | 1 | PROGRESS_FILL (vertical) |
| bar_2 | animated_rect | 2 | PROGRESS_FILL (delayed 0.5s) |
| labels | text_group | 3 | ENTER_FADE |
| percentages | text_group | 4 | ENTER_SCALE |

### Duration
5-6 seconds

---

## Template 5: PROGRESS_DELTA_BADGE

### Purpose
Circular badge showing percentage change.

### Input Parameters
```json
{
  "delta_percent": 47,
  "direction": "up",
  "label": "Energy Increase"
}
```

### Layer Structure
| Layer | Type | Z-Index | Animation |
|-------|------|---------|-----------|
| background | gradient | 0 | none |
| circle_bg | circle | 1 | ENTER_SCALE |
| delta_text | text | 2 | ENTER_SCALE (delayed 0.3s) |
| arrow_icon | icon | 3 | SLIDE_IN (delayed 0.5s) |
| label_text | text | 4 | ENTER_FADE (delayed 1s) |

### Duration
3-4 seconds

---

## Template 6: KINETIC_DEFINITION

### Purpose
Word-by-word text reveal for term definitions.

### Input Parameters
```json
{
  "term": "Embodiment",
  "definition": "The practice of listening to your body's wisdom",
  "emphasis_words": ["listening", "wisdom"]
}
```

### Layer Structure
| Layer | Type | Z-Index | Animation |
|-------|------|---------|-----------|
| background | gradient | 0 | none |
| term_text | text | 1 | ENTER_SCALE |
| divider | line | 2 | SLIDE_IN |
| word_1 | text | 3 | ENTER_FADE (staggered 0.1s each) |
| word_2 | text | 4 | ENTER_FADE |
| ... | ... | ... | ... |
| emphasis_glow | overlay | 10 | PULSE (on emphasis words) |

### Duration
5-7 seconds

---

## Template 7: QUOTE_CARD

### Purpose
Centered inspirational quote with attribution.

### Input Parameters
```json
{
  "quote_text": "The body keeps the score",
  "attribution": "Bessel van der Kolk",
  "background_style": "gradient_warm"
}
```

### Layer Structure
| Layer | Type | Z-Index | Animation |
|-------|------|---------|-----------|
| background | gradient | 0 | none |
| quote_marks | icon | 1 | ENTER_FADE |
| quote_text | text | 2 | ENTER_FADE (word by word) |
| divider | line | 3 | SLIDE_IN |
| attribution | text | 4 | ENTER_FADE (delayed 2s) |

### Background Styles
`gradient_warm`, `gradient_cool`, `gradient_neutral`, `solid_dark`

### Duration
4-6 seconds

---

## Template 8: CONSENSUS_SCORE_STACK

### Purpose
Stacked horizontal bars showing collective data.

### Input Parameters
```json
{
  "categories": ["Agree", "Neutral", "Disagree"],
  "percentages": [67, 21, 12],
  "colors": ["#43A047", "#FFA726", "#E53935"]
}
```

### Layer Structure
| Layer | Type | Z-Index | Animation |
|-------|------|---------|-----------|
| background | gradient | 0 | none |
| bar_1 | animated_rect | 1 | PROGRESS_FILL |
| bar_2 | animated_rect | 2 | PROGRESS_FILL (delayed 0.3s) |
| bar_3 | animated_rect | 3 | PROGRESS_FILL (delayed 0.6s) |
| labels | text_group | 4 | ENTER_FADE |
| percentages | text_group | 5 | ENTER_SCALE |

### Duration
5-6 seconds

---

## Template 9: CUTOUT_METAPHOR

### Purpose
Icon or symbol emerging from abstract background.

### Input Parameters
```json
{
  "icon_id": "lotus",
  "metaphor_text": "Rising from the mud",
  "animation_style": "emerge"
}
```

### Layer Structure
| Layer | Type | Z-Index | Animation |
|-------|------|---------|-----------|
| background | gradient | 0 | none |
| abstract_shapes | svg_group | 1 | FLOAT (loop) |
| icon | svg | 2 | ENTER_SCALE (from center) |
| glow | radial_gradient | 3 | PULSE |
| metaphor_text | text | 4 | ENTER_FADE (delayed 1.5s) |

### Animation Styles
`emerge`, `descend`, `expand`, `pulse`

### Duration
4-5 seconds

---

## Template 10: MISCONCEPTION_TRUTH

### Purpose
Strike-through myth, reveal truth.

### Input Parameters
```json
{
  "myth_text": "Pain means something is broken",
  "truth_text": "Pain is information, not damage"
}
```

### Layer Structure
| Layer | Type | Z-Index | Animation |
|-------|------|---------|-----------|
| background | gradient | 0 | none |
| myth_text | text | 1 | ENTER_FADE |
| strikethrough | line | 2 | SLIDE_IN (after 1.5s) |
| truth_text | text | 3 | ENTER_SCALE (after 2s) |
| checkmark | icon | 4 | ENTER_SCALE (after 2.5s) |

### Duration
5-6 seconds

---

## Template 11: BRAND_AVATAR_FLOAT

### Purpose
Coach avatar floating with gentle idle motion.

### Input Parameters
```json
{
  "avatar_image_path": "brand_library/avatars/coach_01.png",
  "background_gradient": ["#1a1a2e", "#16213e"]
}
```

### Layer Structure
| Layer | Type | Z-Index | Animation |
|-------|------|---------|-----------|
| background | gradient | 0 | none |
| glow_behind | radial_gradient | 1 | PULSE |
| avatar | image | 2 | FLOAT (y ±10px, loop) |
| particle_overlay | particles | 3 | FLOAT (slow) |

### Duration
3-4 seconds (loopable)

---

## Template 12: RHYTHMIC_ABSTRACT

### Purpose
Pulsing geometric shapes creating urgency.

### Input Parameters
```json
{
  "pulse_speed": "fast",
  "shape_count": 5,
  "color_palette": ["#6A1B9A", "#00B3A6", "#E53935"]
}
```

### Layer Structure
| Layer | Type | Z-Index | Animation |
|-------|------|---------|-----------|
| background | solid | 0 | none |
| shape_1 | circle | 1 | PULSE (offset 0) |
| shape_2 | circle | 2 | PULSE (offset 0.2s) |
| shape_3 | circle | 3 | PULSE (offset 0.4s) |
| shape_4 | circle | 4 | PULSE (offset 0.6s) |
| shape_5 | circle | 5 | PULSE (offset 0.8s) |

### Pulse Speeds
`slow` (1.2s), `medium` (0.8s), `fast` (0.5s)

### Duration
4-5 seconds (loopable)

---

## Motion Token Reference

| Token | Easing | Duration | Effect |
|-------|--------|----------|--------|
| `ENTER_FADE` | easeOut | 0.3s | opacity: 0→1 |
| `ENTER_SCALE` | easeOutBack | 0.4s | scale: 0→1 |
| `EXIT_FADE` | easeIn | 0.25s | opacity: 1→0 |
| `SLIDE_IN` | easeOutCubic | 0.5s | x/y: off→on |
| `PROGRESS_FILL` | easeOutCubic | 2.0s | width/height: 0→target |
| `PULSE` | easeInOutSine | 0.6s | scale: 1→1.05→1 (loop) |
| `FLOAT` | easeInOutSine | 3.0s | y: ±10px (loop) |

---

*Library Version: 1.0.0*
