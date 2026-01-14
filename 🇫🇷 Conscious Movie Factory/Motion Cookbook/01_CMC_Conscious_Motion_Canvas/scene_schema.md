# **📄 scene\_schema.md**

\# scene\_schema.md  
\*\*Purpose:\*\* Formal definition of a Scene    
\*\*Status:\*\* Canonical  

\---

\#\# 1\. What Is a Scene?

A Scene is a \*\*fixed motion structure\*\* designed to communicate a specific narrative or explanatory beat.

A Scene is:  
\- Rigid in time  
\- Rigid in spatial topology  
\- Flexible only in content parameters

\---

\#\# 2\. Scene Invariants

Every Scene MUST define:

\- Total duration (frames)  
\- Temporal phases  
\- Spatial zones  
\- Allowed component types  
\- Motion presets

These invariants never change at runtime.

\---

\#\# 3\. Scene Schema (Logical)

\`\`\`json  
{  
  "scene\_id": "BODY\_MAP\_FOCUS",  
  "version": "1.0",  
  "duration\_frames": 150,  
  "fps": 30,

  "purpose": "explain",

  "phases": \[  
    {  
      "id": "establish",  
      "frames": \[0, 40\]  
    },  
    {  
      "id": "focus",  
      "frames": \[40, 110\]  
    },  
    {  
      "id": "reinforce",  
      "frames": \[110, 150\]  
    }  
  \],

  "zones": {  
    "background": { "x": 0, "y": 0, "w": 1, "h": 1 },  
    "primary":    { "x": 0.15, "y": 0.25, "w": 0.7, "h": 0.4 },  
    "secondary":  { "x": 0.15, "y": 0.7,  "w": 0.7, "h": 0.2 }  
  },

  "allowed\_components": \[  
    "ImageLayer",  
    "TextBlock",  
    "RegionHighlight",  
    "Arrow",  
    "GlowEffect"  
  \],

  "motion\_preset": "EXPLAINER\_FOCUS\_V1"  
}

---

## **4\. Scene Parameters (Runtime)**

{  
  "scene\_id": "BODY\_MAP\_FOCUS",  
  "parameters": {  
    "headline\_text": "Your intuition lives here",  
    "focus\_region\_id": "gut",  
    "highlight\_color": "\#00FFD1"  
  }  
}

Parameters:

* Fill content slots  
* Select variants  
* Never alter structure

---

## **5\. Scene Validation Rules**

A Scene Instance MUST:

* Use only allowed components  
* Respect zone boundaries  
* Respect phase timing  
* Use valid Layer Graph references

Invalid instances are rejected.

---

## **6\. Scene Versioning**

Any structural change requires:

* New scene version  
* Backward compatibility guarantees

Scenes are immutable once published.

**scene\_schema.md \- COMPLETE EXAMPLES SECTION**

## **Add Section 8: Complete Scene Definitions**

### **Example 1: RATING\_METER\_1\_TO\_10 (Simple)**

{

  "scene\_id": "RATING\_METER\_1\_TO\_10",

  "version": "1.0",

  "category": "response\_visualization",

  "duration\_frames": 150,

  "fps": 30,

  "purpose": "Visualize self-reported numeric rating",


  "timing\_mode": "absolute",


  "phases": \[

    {

      "id": "setup",

      "frames": \[0, 30\],

      "purpose": "Label appears"

    },

    {

      "id": "fill",

      "frames": \[30, 90\],

      "purpose": "Meter fills to value"

    },

    {

      "id": "emphasize",

      "frames": \[90, 120\],

      "purpose": "Number pops and holds"

    },

    {

      "id": "hold",

      "frames": \[120, 150\],

      "purpose": "Final frame hold"

    }

  \],


  "zones": {

    "label": {

      "x": 0.1,

      "y": 0.3,

      "w": 0.8,

      "h": 0.1,

      "anchor": "top-center"

    },

    "meter": {

      "x": 0.1,

      "y": 0.45,

      "w": 0.8,

      "h": 0.15,

      "anchor": "center"

    },

    "value": {

      "x": 0.1,

      "y": 0.65,

      "w": 0.8,

      "h": 0.2,

      "anchor": "center"

    }

  },


  "allowed\_components": \[

    "TextBlock",

    "HorizontalMeter",

    "NumericLabel",

    "GlowEffect"

  \],


  "required\_parameters": {

    "rating\_value": {

      "type": "number",

      "range": \[0, 10\],

      "default": null

    },

    "min\_value": {

      "type": "number",

      "default": 0

    },

    "max\_value": {

      "type": "number",

      "default": 10

    },

    "label\_text": {

      "type": "string",

      "default": "Rating"

    }

  },


  "optional\_parameters": {

    "show\_ticks": {

      "type": "boolean",

      "default": true

    },

    "orientation": {

      "type": "enum",

      "values": \["horizontal", "circular"\],

      "default": "horizontal"

    }

  },


  "motion\_preset": "RATING\_METER\_V1",


  "motion\_sequence": \[

    {

      "phase": "setup",

      "target": "label",

      "token": "FADE\_IN",

      "duration": 18

    },

    {

      "phase": "fill",

      "target": "meter",

      "token": "METER\_FILL\_SMOOTH",

      "duration": 30,

      "params": {

        "target\_value": "\<rating\_value\>"

      }

    },

    {

      "phase": "emphasize",

      "target": "value",

      "token": "NUMBER\_POP\_SOFT",

      "duration": 18

    }

  \],


  "validation\_rules": {

    "rating\_value\_required": true,

    "rating\_value\_in\_range": true,

    "label\_text\_max\_length": 30

  }

}

---

### **Example 2: BODY\_MAP\_FOCUS (Complex)**

{

  "scene\_id": "BODY\_MAP\_FOCUS",

  "version": "1.0",

  "category": "explainer",

  "duration\_frames": 180,

  "fps": 30,

  "purpose": "Explain body-based concepts with region emphasis",


  "timing\_mode": "absolute",


  "phases": \[

    {

      "id": "establish",

      "frames": \[0, 40\],

      "purpose": "Full body visible"

    },

    {

      "id": "focus",

      "frames": \[40, 130\],

      "purpose": "Region highlighted and labeled"

    },

    {

      "id": "reinforce",

      "frames": \[130, 180\],

      "purpose": "Headline appears with glow"

    }

  \],


  "zones": {

    "background": {

      "x": 0,

      "y": 0,

      "w": 1,

      "h": 1,

      "z\_index": 0

    },

    "body\_container": {

      "x": 0.1,

      "y": 0.15,

      "w": 0.8,

      "h": 0.7,

      "z\_index": 1

    },

    "headline": {

      "x": 0.1,

      "y": 0.88,

      "w": 0.8,

      "h": 0.1,

      "z\_index": 3

    }

  },


  "allowed\_components": \[

    "ImageLayer",

    "RegionHighlight",

    "TextBlock",

    "GlowEffect",

    "Arrow"

  \],


  "required\_parameters": {

    "layer\_graph\_id": {

      "type": "string",

      "description": "ID of layer graph containing body layers"

    },

    "focus\_region\_id": {

      "type": "string",

      "description": "Which layer to emphasize (e.g. 'gut\_region')"

    },

    "headline\_text": {

      "type": "string",

      "max\_length": 50

    }

  },


  "optional\_parameters": {

    "highlight\_color": {

      "type": "color",

      "default": "\#00FFD1"

    },

    "show\_arrow": {

      "type": "boolean",

      "default": false

    }

  },


  "layer\_requirements": {

    "required\_semantics": \["body", "region"\],

    "min\_layers": 2,

    "max\_layers": 10

  },


  "motion\_preset": "EXPLAINER\_FOCUS\_V1",


  "motion\_sequence": \[

    {

      "phase": "establish",

      "targets": \["body\_base"\],

      "token": "FADE\_IN",

      "duration": 24

    },

    {

      "phase": "focus",

      "targets": \["\<focus\_region\_id\>"\],

      "tokens": \[

        {

          "token": "CAMERA\_PUSH\_SUBTLE",

          "duration": 36

        },

        {

          "token": "GLOW\_ACCENT\_HOLD",

          "duration": 60,

          "delay": 12

        }

      \]

    },

    {

      "phase": "reinforce",

      "targets": \["headline"\],

      "token": "FADE\_IN\_UP",

      "duration": 24

    }

  \]

}

---

## **Add Section 9: Speech Alignment Example**

### **RATING\_METER\_1\_TO\_10 (Speech-Aligned Variant)**

{

  "scene\_id": "RATING\_METER\_1\_TO\_10",

  "version": "1.1",

  "timing\_mode": "speech\_aligned",


  "speech\_hooks": {

    "required\_anchors": \["response\_start", "response\_end"\],

    "optional\_anchors": \["response\_peak"\],

    "anchor\_ranges": {

      "response\_start": \[0, 150\],

      "response\_peak": \[20, 130\],

      "response\_end": \[40, 150\]

    },

    "fallback\_mode": "absolute"

  },


  "motion\_sequence": \[

    {

      "phase": "dynamic",

      "anchor\_start": "response\_start",

      "anchor\_end": "response\_end",

      "targets": \["meter"\],

      "token": "BAR\_FILL\_PROGRESSIVE",

      "lock\_at": "response\_end"

    },

    {

      "phase": "dynamic",

      "anchor\_trigger": "response\_end",

      "offset\_frames": 6,

      "targets": \["value"\],

      "token": "NUMBER\_POP\_SOFT",

      "duration": 18

    }

  \]

}

**Concrete Example Values:**

{

  "anchors": {

    "response\_start": 42,

    "response\_peak": 78,

    "response\_end": 118

  }

}

This means:

* Meter starts filling at frame 42  
* Continues filling until frame 118  
* Number pops at frame 124 (118 \+ 6 offset)

