# **📄 layer\_graph\_schema.md**

\`\`\`markdown  
\# layer\_graph\_schema.md  
\*\*Purpose:\*\* Canonical visual representation    
\*\*Status:\*\* Core Contract  

\---

\#\# 1\. What Is a Layer Graph?

A Layer Graph represents \*\*all visual elements\*\* as independent, semantically labeled RGBA layers.

It is the bridge between:  
\- AI perception  
\- Deterministic motion rendering

\---

\#\# 2\. Design Principles

\- Every visible element is a layer  
\- Every layer has meaning  
\- No layer contains baked motion  
\- Transparency is first-class

\---

\#\# 3\. Layer Graph Schema (Logical)

\`\`\`json  
{  
  "graph\_id": "body\_map\_v3",  
  "canvas": {  
    "width": 1080,  
    "height": 1920,  
    "aspect\_ratio": "9:16"  
  },

  "layers": \[  
    {  
      "layer\_id": "body\_base",  
      "type": "image",  
      "rgba\_asset": "body\_base.png",  
      "z\_index": 0,  
      "bbox": { "x": 0, "y": 0, "w": 1, "h": 1 },  
      "semantics": \["body", "human", "base"\],  
      "allowed\_transforms": \["scale", "opacity"\]  
    },  
    {  
      "layer\_id": "gut\_region",  
      "type": "region",  
      "rgba\_asset": "gut\_mask.png",  
      "z\_index": 2,  
      "bbox": { "x": 0.42, "y": 0.48, "w": 0.18, "h": 0.22 },  
      "semantics": \["gut", "intuition", "nervous\_system"\],  
      "allowed\_transforms": \["scale", "opacity", "outline", "glow"\]  
    }  
  \]  
}

**layer\_graph\_schema.md \- COMPLETE EXAMPLES**

## **Add Section 10: Complete Layer Graph Examples**

### **Example 1: Simple Speaker Cutout (2 layers)**

{  
  "graph\_id": "speaker\_cutout\_001",  
  "source\_image": "data/assets/speaker\_headshot.png",  
  "canvas": {  
    "width": 1080,  
    "height": 1920,  
    "aspect\_ratio": "9:16"  
  },  
  "extraction\_method": "manual",  
  "extraction\_confidence": 1.0,  
  "created\_at": "2026-01-04T12:34:56Z",  
    
  "layers": \[  
    {  
      "layer\_id": "background",  
      "type": "image",  
      "rgba\_asset": "data/layer\_graphs/speaker\_cutout\_001/background.png",  
      "z\_index": 0,  
      "bbox": {  
        "x": 0,  
        "y": 0,  
        "w": 1,  
        "h": 1  
      },  
      "semantics": \["background", "neutral"\],  
      "allowed\_transforms": \["opacity", "blur"\],  
      "extraction\_confidence": 1.0  
    },  
    {  
      "layer\_id": "speaker",  
      "type": "cutout",  
      "rgba\_asset": "data/layer\_graphs/speaker\_cutout\_001/speaker.png",  
      "z\_index": 1,  
      "bbox": {  
        "x": 0.25,  
        "y": 0.15,  
        "w": 0.5,  
        "h": 0.7  
      },  
      "semantics": \["person", "speaker", "foreground"\],  
      "allowed\_transforms": \["scale", "opacity", "position", "glow"\],  
      "extraction\_confidence": 1.0  
    }  
  \]  
}

**Visual Representation:**

Layer Stack (z-index):  
┌────────────────────┐  
│   speaker (z=1)    │ ← RGBA cutout, transparent background  
│                    │   bbox: x:0.25, y:0.15, w:0.5, h:0.7  
├────────────────────┤  
│ background (z=0)   │ ← Solid or gradient  
│                    │   bbox: full canvas  
└────────────────────┘

**File Structure:**

data/layer\_graphs/speaker\_cutout\_001/  
├── graph.json          \# This JSON  
├── background.png      \# 1080x1920 RGBA  
└── speaker.png         \# 540x1344 RGBA (cropped to bbox)

---

### **Example 2: Body Map with Regions (5 layers)**

{  
  "graph\_id": "body\_map\_gut\_001",  
  "source\_image": "data/assets/body\_diagram.png",  
  "canvas": {  
    "width": 1080,  
    "height": 1920  
  },  
  "extraction\_method": "qwen\_layered",  
  "extraction\_confidence": 0.87,  
  "created\_at": "2026-01-04T13:22:10Z",  
    
  "layers": \[  
    {  
      "layer\_id": "body\_base",  
      "type": "image",  
      "rgba\_asset": "data/layer\_graphs/body\_map\_gut\_001/body\_base.png",  
      "z\_index": 0,  
      "bbox": {  
        "x": 0.1,  
        "y": 0.15,  
        "w": 0.8,  
        "h": 0.7  
      },  
      "semantics": \["body", "anatomy", "base"\],  
      "allowed\_transforms": \["opacity", "scale"\],  
      "extraction\_confidence": 0.98  
    },  
    {  
      "layer\_id": "gut\_region",  
      "type": "region",  
      "rgba\_asset": "data/layer\_graphs/body\_map\_gut\_001/gut\_region.png",  
      "z\_index": 2,  
      "bbox": {  
        "x": 0.42,  
        "y": 0.48,  
        "w": 0.18,  
        "h": 0.22  
      },  
      "semantics": \["gut", "digestive", "intuition", "nervous\_system"\],  
      "allowed\_transforms": \["scale", "opacity", "glow", "outline"\],  
      "extraction\_confidence": 0.92,  
      "parent\_layer": "body\_base"  
    },  
    {  
      "layer\_id": "brain\_region",  
      "type": "region",  
      "rgba\_asset": "data/layer\_graphs/body\_map\_gut\_001/brain\_region.png",  
      "z\_index": 2,  
      "bbox": {  
        "x": 0.44,  
        "y": 0.18,  
        "w": 0.14,  
        "h": 0.12  
      },  
      "semantics": \["brain", "cognition", "thinking"\],  
      "allowed\_transforms": \["scale", "opacity", "glow", "outline"\],  
      "extraction\_confidence": 0.95,  
      "parent\_layer": "body\_base"  
    },  
    {  
      "layer\_id": "heart\_region",  
      "type": "region",  
      "rgba\_asset": "data/layer\_graphs/body\_map\_gut\_001/heart\_region.png",  
      "z\_index": 2,  
      "bbox": {  
        "x": 0.40,  
        "y": 0.35,  
        "w": 0.12,  
        "h": 0.10  
      },  
      "semantics": \["heart", "emotion", "feeling"\],  
      "allowed\_transforms": \["scale", "opacity", "glow", "outline"\],  
      "extraction\_confidence": 0.88,  
      "parent\_layer": "body\_base"  
    },  
    {  
      "layer\_id": "overlay\_glow",  
      "type": "fx",  
      "rgba\_asset": "data/layer\_graphs/body\_map\_gut\_001/overlay\_glow.png",  
      "z\_index": 5,  
      "bbox": {  
        "x": 0,  
        "y": 0,  
        "w": 1,  
        "h": 1  
      },  
      "semantics": \["effect", "glow", "overlay"\],  
      "allowed\_transforms": \["opacity"\],  
      "extraction\_confidence": 1.0  
    }  
  \],  
    
  "relationships": \[  
    {  
      "type": "parent\_child",  
      "parent": "body\_base",  
      "children": \["gut\_region", "brain\_region", "heart\_region"\]  
    }  
  \]  
}

**Visual Representation:**

Layer Stack:  
┌────────────────────┐  
│ overlay\_glow (z=5) │ ← FX layer (full canvas)  
├────────────────────┤  
│ brain\_region (z=2) │ ← Small bbox, top of body  
│ heart\_region (z=2) │ ← Medium bbox, chest  
│ gut\_region (z=2)   │ ← Medium bbox, abdomen  
├────────────────────┤  
│ body\_base (z=0)    │ ← Full body silhouette  
└────────────────────┘

Bounding Box Visualization (0-1 normalized):

y:0.0  ┌──────────────────────┐  
       │                      │  
y:0.18 │     \[brain\_region\]   │  
       │                      │  
y:0.35 │     \[heart\_region\]   │  
       │                      │  
y:0.48 │     \[gut\_region\]     │  
       │                      │  
y:0.85 │                      │  
       └──────────────────────┘  
      x:0.1              x:0.9

---

### **Example 3: Complex Diagram (City Map, 12 layers)**

{  
  "graph\_id": "city\_system\_flow\_001",  
  "source\_image": "data/assets/city\_diagram.png",  
  "canvas": {  
    "width": 1080,  
    "height": 1920  
  },  
  "extraction\_method": "sam3",  
  "extraction\_confidence": 0.79,  
    
  "layers": \[  
    {  
      "layer\_id": "map\_base",  
      "type": "image",  
      "z\_index": 0,  
      "bbox": {"x": 0, "y": 0, "w": 1, "h": 1},  
      "semantics": \["map", "geography", "base"\]  
    },  
    {  
      "layer\_id": "downtown\_hub",  
      "type": "region",  
      "z\_index": 2,  
      "bbox": {"x": 0.35, "y": 0.4, "w": 0.3, "h": 0.2},  
      "semantics": \["hub", "downtown", "center", "density"\]  
    },  
    {  
      "layer\_id": "residential\_north",  
      "type": "region",  
      "z\_index": 2,  
      "bbox": {"x": 0.2, "y": 0.1, "w": 0.6, "h": 0.25},  
      "semantics": \["residential", "suburbs", "housing"\]  
    },  
    {  
      "layer\_id": "industrial\_south",  
      "type": "region",  
      "z\_index": 2,  
      "bbox": {"x": 0.15, "y": 0.65, "w": 0.7, "h": 0.25},  
      "semantics": \["industrial", "warehouse", "logistics"\]  
    },  
    {  
      "layer\_id": "transit\_line\_1",  
      "type": "path",  
      "z\_index": 3,  
      "path\_data": "M 0.5,0.2 L 0.5,0.5 L 0.6,0.7",  
      "semantics": \["transit", "connection", "flow"\]  
    },  
    {  
      "layer\_id": "transit\_line\_2",  
      "type": "path",  
      "z\_index": 3,  
      "path\_data": "M 0.3,0.4 L 0.5,0.5 L 0.7,0.4",  
      "semantics": \["transit", "connection", "flow"\]  
    },  
    {  
      "layer\_id": "bottleneck\_point",  
      "type": "icon",  
      "z\_index": 4,  
      "bbox": {"x": 0.48, "y": 0.48, "w": 0.04, "h": 0.04},  
      "semantics": \["bottleneck", "problem", "congestion"\]  
    }  
  \],  
    
  "relationships": \[  
    {  
      "type": "connects",  
      "from": "residential\_north",  
      "to": "downtown\_hub",  
      "via": "transit\_line\_1"  
    },  
    {  
      "type": "connects",  
      "from": "downtown\_hub",  
      "to": "industrial\_south",  
      "via": "transit\_line\_1"  
    }  
  \]  
}

---

## **Add Section 11: BBox Calculation Logic**

### **How Bounding Boxes Are Calculated**

**Input:** Layer extraction identifies a region in pixel space  
 **Output:** Normalized bbox (0-1 coordinates)

**Algorithm:**

def calculate\_bbox(layer\_pixels, canvas\_width, canvas\_height):  
    """  
    Convert pixel coordinates to normalized bbox  
    """  
    \# Find non-transparent pixel bounds  
    y\_coords, x\_coords \= np.where(layer\_pixels\[:, :, 3\] \> 0\)  
      
    if len(x\_coords) \== 0:  
        return None  \# Empty layer  
      
    \# Get pixel bounds  
    x\_min, x\_max \= x\_coords.min(), x\_coords.max()  
    y\_min, y\_max \= y\_coords.min(), y\_coords.max()  
      
    \# Normalize to 0-1  
    bbox \= {  
        "x": x\_min / canvas\_width,  
        "y": y\_min / canvas\_height,  
        "w": (x\_max \- x\_min) / canvas\_width,  
        "h": (y\_max \- y\_min) / canvas\_height  
    }  
      
    return bbox

**Example:**

Canvas: 1080×1920  
Layer occupies pixels: x\[378-648\], y\[921-1344\]

Calculation:  
x \= 378 / 1080 \= 0.35  
y \= 921 / 1920 \= 0.48  
w \= (648 \- 378\) / 1080 \= 0.25  
h \= (1344 \- 921\) / 1920 \= 0.22

Result:  
{"x": 0.35, "y": 0.48, "w": 0.25, "h": 0.22}

### **Validation Rules**

* All bbox values must be in range \[0, 1\]  
* x \+ w ≤ 1  
* y \+ h ≤ 1  
* w \> 0, h \> 0  
* Minimum w: 0.05 (5% of canvas)  
* Minimum h: 0.05 (5% of canvas)

---

## **4\. Layer Types**

Supported types:

* image  
* region  
* text  
* icon  
* fx (alpha video)  
* character\_part

Each type has predefined capabilities.

---

## **5\. Semantic Tags**

Semantics:

* Are human-readable  
* Are AI-generated  
* Enable scene matching and emphasis

Examples:

* "cause"  
* "effect"  
* "misconception"  
* "truth"  
* "hub"  
* "bottleneck"

---

## **6\. Transform Constraints**

Layers declare **allowed transforms**.

If a transform is not declared, it cannot be applied.

This prevents:

* Accidental distortion  
* Inconsistent motion  
* Visual abuse

---

## **7\. Z-Ordering Rules**

* z\_index is absolute  
* Scenes may group layers but not reorder them  
* FX layers must always be topmost

---

## **8\. Validation Rules**

A Layer Graph is valid only if:

* All RGBA assets exist  
* Bounding boxes are normalized (0–1)  
* Semantics are non-empty  
* No baked motion is present

---

## **9\. Reuse & Caching**

Layer Graphs:

* Can be reused across scenes  
* Can be cached per user or brand  
* Are immutable once validated

---

## **10\. Why This Matters**

The Layer Graph:

* Makes motion explainable  
* Makes animation predictable  
* Makes AI safe to use  
* Makes scale possible

Without it, the system collapses into ad-hoc video generation.

---

\---

\#\# Closing Note

At this point, you have something \*\*rare\*\*:

\- A clear motion philosophy    
\- A safe AI boundary    
\- A production-grade architecture  

This is the kind of foundation that \*\*actual motion studios\*\* wish they had written down.

If you want next, the logical follow-ups are:  
\- \`motion\_tokens.md\`  
\- \`scene\_library\_v1.md\`  
\- \`agent\_contracts.md\`

Just tell me which one you want to lock next.

—---------------------------------------------------------  
