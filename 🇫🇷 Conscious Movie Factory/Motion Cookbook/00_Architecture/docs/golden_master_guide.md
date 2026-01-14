# **golden\_master\_guide.md**

**Purpose:** Guide for creating and using golden master test renders  
 **Status:** Canonical v1.0

---

## **1\. What Are Golden Masters?**

Golden Masters are **reference renders** that define the correct visual output for each scene.

They serve as:

* **Regression test baselines** \- Detect unintended changes  
* **Quality standards** \- Define expected output  
* **Documentation** \- Show what each scene looks like

**Key Principle:** If a scene changes, the golden master must be intentionally updated.

---

## **2\. Golden Master Structure**

### **File Organization**

tests/golden/  
├── RATING\_METER\_1\_TO\_10/  
│   ├── config.json              \# Test configuration  
│   ├── golden.mp4               \# Reference video  
│   ├── golden.sha256            \# Video hash  
│   ├── metadata.json            \# Scene metadata  
│   ├── frames/                  \# Key frames  
│   │   ├── frame\_000.png  
│   │   ├── frame\_030.png  
│   │   ├── frame\_090.png  
│   │   └── frame\_150.png  
│   └── README.md                \# Scene-specific notes  
│  
├── BEFORE\_AFTER\_SELF\_SCORE/  
│   └── ...  
│  
└── index.json                   \# Master index

---

## **3\. Creating a Golden Master**

### **Step 1: Prepare Test Configuration**

Create a **deterministic, minimal** test config:

// tests/golden/RATING\_METER\_1\_TO\_10/config.json  
{  
  "scene\_id": "RATING\_METER\_1\_TO\_10",  
  "version": "1.0",  
  "parameters": {  
    "rating\_value": 7,  
    "min\_value": 0,  
    "max\_value": 10,  
    "label\_text": "Test Label",  
    "show\_ticks": true,  
    "orientation": "horizontal"  
  },  
  "brand\_kit\_id": "test\_brand",  
  "timing": {  
    "mode": "absolute",  
    "duration\_frames": 150,  
    "fps": 30  
  },  
  "test\_notes": "Standard rating meter with value 7/10"  
}

**Key Requirements:**

* Use `test_brand` (fixed colors, no variations)  
* No random elements  
* No external dependencies  
* Fixed parameter values  
* Include all required parameters

---

### **Step 2: Generate Golden Master**

\# Render the golden master  
python cli.py render \\  
  \--scene RATING\_METER\_1\_TO\_10 \\  
  \--config tests/golden/RATING\_METER\_1\_TO\_10/config.json \\  
  \--output tests/golden/RATING\_METER\_1\_TO\_10/golden.mp4 \\  
  \--no-cache

\# Generate hash  
sha256sum tests/golden/RATING\_METER\_1\_TO\_10/golden.mp4 \> \\  
  tests/golden/RATING\_METER\_1\_TO\_10/golden.sha256

\# Extract key frames  
python scripts/extract\_key\_frames.py \\  
  tests/golden/RATING\_METER\_1\_TO\_10/golden.mp4 \\  
  tests/golden/RATING\_METER\_1\_TO\_10/frames/ \\  
  \--frames 0,30,90,150

---

### **Step 3: Create Metadata**

// tests/golden/RATING\_METER\_1\_TO\_10/metadata.json  
{  
  "scene\_id": "RATING\_METER\_1\_TO\_10",  
  "version": "1.0",  
  "created\_date": "2026-01-03T14:22:10Z",  
  "created\_by": "dev\_initial\_setup",  
    
  "video": {  
    "path": "golden.mp4",  
    "sha256": "a3f7b2e9c1d4...",  
    "duration\_seconds": 5.0,  
    "frame\_count": 150,  
    "resolution": "1080x1920",  
    "codec": "h264",  
    "file\_size\_mb": 2.3  
  },  
    
  "render\_environment": {  
    "motion\_canvas\_version": "3.15.0",  
    "ffmpeg\_version": "6.0",  
    "python\_version": "3.11.5",  
    "os": "Linux Ubuntu 22.04"  
  },  
    
  "validation": {  
    "schema\_version": "1.0",  
    "expected\_duration": 5.0,  
    "tolerance\_seconds": 0.1,  
    "frame\_comparison\_threshold": 0.98,  
    "pixel\_diff\_tolerance": 0.005  
  },  
    
  "key\_frames": \[  
    {  
      "frame": 0,  
      "timestamp": 0.0,  
      "description": "Initial state \- empty meter",  
      "sha256": "b4e8c3d1..."  
    },  
    {  
      "frame": 30,  
      "timestamp": 1.0,  
      "description": "Label visible",  
      "sha256": "c5f9d4e2..."  
    },  
    {  
      "frame": 90,  
      "timestamp": 3.0,  
      "description": "Meter filled to 7/10",  
      "sha256": "d6g0e5f3..."  
    },  
    {  
      "frame": 150,  
      "timestamp": 5.0,  
      "description": "Final state with number",  
      "sha256": "e7h1f6g4..."  
    }  
  \]  
}

---

## **4\. Running Regression Tests**

### **Test Types**

#### **Type 1: Hash Comparison (Fast)**

python cli.py test regression \\  
  \--scene RATING\_METER\_1\_TO\_10 \\  
  \--quick

\# Renders scene, compares SHA256  
\# Pass/Fail in \~30 seconds

**What it checks:**

* ✅ Bitwise identical output  
* ❌ Cannot detect *acceptable* visual changes

---

#### **Type 2: Frame-by-Frame Comparison (Thorough)**

python cli.py test regression \\  
  \--scene RATING\_METER\_1\_TO\_10 \\  
  \--frames

\# Extracts frames, computes SSIM  
\# Pass/Fail in \~45 seconds

**What it checks:**

* ✅ Structural similarity (SSIM \> 0.98)  
* ✅ Pixel difference (\< 0.5%)  
* ✅ Tolerates minor rendering variations

---

#### **Type 3: Visual Diff (Debug)**

python cli.py test regression \\  
  \--scene RATING\_METER\_1\_TO\_10 \\  
  \--visual-diff

\# Generates side-by-side comparison  
\# For human review

**Output:**

tests/regression/RATING\_METER\_1\_TO\_10\_diff.mp4

---

## **5\. When Tests Fail**

### **Failure Type 1: Hash Mismatch**

❌ FAILED: RATING\_METER\_1\_TO\_10  
Expected: a3f7b2e9c1d4...  
Got:      a3f7b2e9c1d5...  
Reason: Bitwise difference detected

**Investigation Steps:**

1. Run frame comparison test  
2. Generate visual diff  
3. Determine if change is:  
   * **Intentional** → Update golden master  
   * **Bug** → Fix code  
   * **Environment** → Check render setup

---

### **Failure Type 2: Frame Similarity Low**

❌ FAILED: RATING\_METER\_1\_TO\_10  
Frame 90 SSIM: 0.92 (threshold: 0.98)  
Pixel diff: 2.3% (threshold: 0.5%)

**Investigation Steps:**

1. Inspect frame\_090.png diff  
2. Check for:  
   * Font rendering changes  
   * Color shifts  
   * Position drift  
   * Timing issues

---

### **Failure Type 3: Duration Mismatch**

❌ FAILED: RATING\_METER\_1\_TO\_10  
Expected: 5.0s (150 frames)  
Got: 5.1s (153 frames)

**Cause:** Scene timing changed **Action:** Review motion token durations

---

## **6\. Updating Golden Masters**

### **When to Update**

**Update when:**

* ✅ Intentional scene improvements  
* ✅ Motion token changes (versioned)  
* ✅ Brand kit updates  
* ✅ Bug fixes affecting output

**DO NOT update for:**

* ❌ Random test failures  
* ❌ Unreviewed changes  
* ❌ "Making tests pass"

---

### **Update Process**

\# 1\. Review changes carefully  
python cli.py test regression \\  
  \--scene RATING\_METER\_1\_TO\_10 \\  
  \--visual-diff

\# 2\. If changes are correct, update  
python cli.py golden update \\  
  \--scene RATING\_METER\_1\_TO\_10 \\  
  \--reason "Improved meter fill easing"

\# This:  
\# \- Re-renders golden master  
\# \- Updates SHA256  
\# \- Extracts new key frames  
\# \- Updates metadata  
\# \- Commits to git with message

\# 3\. Document change  
git commit \-m "Update RATING\_METER golden: improved easing

\- Changed METER\_FILL\_SMOOTH from easeOutQuad to easeOutCubic  
\- Smoother visual progression  
\- Approved by design review"

---

## **7\. Batch Operations**

### **Create All Golden Masters**

\# Generate golden masters for all scenes  
python cli.py golden create-all \\  
  \--output tests/golden/ \\  
  \--parallel 4

\# Takes \~20 minutes for 16 scenes

---

### **Run All Regression Tests**

\# Quick hash check (all scenes in \~5 min)  
python cli.py test regression-all \--quick

\# Thorough frame check (all scenes in \~15 min)  
python cli.py test regression-all \--frames

---

## **8\. CI Integration**

### **GitHub Actions Example**

\# .github/workflows/regression\_tests.yml  
name: Golden Master Regression Tests

on: \[push, pull\_request\]

jobs:  
  regression:  
    runs-on: ubuntu-latest  
      
    steps:  
    \- uses: actions/checkout@v3  
      
    \- name: Setup Python  
      uses: actions/setup-python@v4  
      with:  
        python-version: '3.11'  
      
    \- name: Install dependencies  
      run: |  
        pip install \-r requirements.txt  
        npm install  
      
    \- name: Run regression tests  
      run: |  
        python cli.py test regression-all \--frames  
      
    \- name: Upload diffs on failure  
      if: failure()  
      uses: actions/upload-artifact@v3  
      with:  
        name: regression-diffs  
        path: tests/regression/\*\_diff.mp4

---

## **9\. Golden Master Best Practices**

### **DO:**

* ✅ Use fixed test data  
* ✅ Version golden masters in git  
* ✅ Document all updates  
* ✅ Run before every release  
* ✅ Keep golden masters small (test\_brand only)

### **DON'T:**

* ❌ Use random data  
* ❌ Update without review  
* ❌ Ignore failures  
* ❌ Test with production brand kits  
* ❌ Include long/complex scenes

---

## **10\. Troubleshooting**

### **Issue: "Golden master not found"**

\# Create it  
python cli.py golden create \--scene SCENE\_ID

### **Issue: "Consistent hash mismatch"**

\# Environment changed, recreate  
python cli.py golden recreate \--scene SCENE\_ID

### **Issue: "Frame extraction failed"**

\# Check ffmpeg  
ffmpeg \-version

\# Regenerate frames  
python scripts/extract\_key\_frames.py \<video\> \<output\_dir\>

### **Issue: "SSIM calculation failing"**

\# Install scikit-image  
pip install scikit-image

\# Or use pixel diff only  
python cli.py test regression \--pixel-diff-only

---

## **11\. Helper Scripts**

### **scripts/extract\_key\_frames.py**

\#\!/usr/bin/env python3  
"""Extract key frames from video for golden master tests"""

import sys  
import subprocess  
from pathlib import Path

def extract\_frames(video\_path, output\_dir, frames):  
    """Extract specific frames as PNG"""  
    output\_dir.mkdir(parents=True, exist\_ok=True)  
      
    for frame\_num in frames:  
        output\_path \= output\_dir / f"frame\_{frame\_num:03d}.png"  
          
        cmd \= \[  
            "ffmpeg", "-i", str(video\_path),  
            "-vf", f"select=eq(n\\\\,{frame\_num})",  
            "-vframes", "1",  
            "-y",  
            str(output\_path)  
        \]  
          
        subprocess.run(cmd, check=True, capture\_output=True)  
        print(f"✅ Extracted frame {frame\_num}")

if \_\_name\_\_ \== "\_\_main\_\_":  
    video\_path \= Path(sys.argv\[1\])  
    output\_dir \= Path(sys.argv\[2\])  
    frames \= \[int(f) for f in sys.argv\[3\].split(",")\]  
      
    extract\_frames(video\_path, output\_dir, frames)

---

### **scripts/compare\_frames.py**

\#\!/usr/bin/env python3  
"""Compare two frames using SSIM"""

from skimage.metrics import structural\_similarity as ssim  
from PIL import Image  
import numpy as np  
import sys

def compare\_frames(img1\_path, img2\_path):  
    """Calculate SSIM between two frames"""  
    img1 \= np.array(Image.open(img1\_path))  
    img2 \= np.array(Image.open(img2\_path))  
      
    \# Calculate SSIM  
    score \= ssim(img1, img2, multichannel=True, channel\_axis=2)  
      
    \# Calculate pixel difference  
    diff \= np.abs(img1.astype(float) \- img2.astype(float))  
    pixel\_diff \= diff.mean() / 255.0  
      
    return {  
        "ssim": score,  
        "pixel\_diff": pixel\_diff,  
        "pass": score \> 0.98 and pixel\_diff \< 0.005  
    }

if \_\_name\_\_ \== "\_\_main\_\_":  
    img1, img2 \= sys.argv\[1\], sys.argv\[2\]  
    result \= compare\_frames(img1, img2)  
      
    print(f"SSIM: {result\['ssim'\]:.4f}")  
    print(f"Pixel Diff: {result\['pixel\_diff'\]\*100:.2f}%")  
    print(f"Status: {'✅ PASS' if result\['pass'\] else '❌ FAIL'}")

---

## **12\. Reference: Test Brand Kit**

// config/brand\_kits/test\_brand.json  
{  
  "brand\_id": "test\_brand",  
  "name": "Test Brand (For Golden Masters)",  
    
  "colors": {  
    "primary": "\#00FFD1",  
    "secondary": "\#1B1B1B",  
    "accent": "\#FFD700",  
    "text": "\#FFFFFF",  
    "background": "\#000000"  
  },  
    
  "fonts": {  
    "headline": "Inter-Bold",  
    "body": "Inter-Regular",  
    "number": "SpaceGrotesk-Bold"  
  },  
    
  "motion\_preferences": {  
    "intensity": "medium",  
    "camera\_usage": "allowed",  
    "glow\_allowed": true  
  },  
    
  "note": "Fixed brand for regression testing. DO NOT MODIFY."  
}

---

**Golden masters ensure Motion Cookbook remains deterministic and trustworthy at scale.**

