# **motion\_canvas\_integration.md**

\*\*Purpose:\*\* How Motion Canvas actually renders scenes    
\*\*Status:\*\* Canonical v1.0

\---

\#\# 1\. Integration Overview

Motion Canvas is the \*\*only rendering engine\*\* in the system. It consumes scene configurations and produces video frames.

\*\*Key Principle:\*\* Motion Canvas never makes decisions—it executes instructions.

\---

\#\# 2\. Motion Canvas Project Structure

\`\`\`  
motion-canvas/  
├── src/  
│   ├── project.ts              \# Project configuration  
│   ├── scenes/                 \# Scene implementations  
│   │   ├── rating\_meter.tsx  
│   │   ├── body\_map\_focus.tsx  
│   │   └── ...  
│   ├── components/             \# Reusable components  
│   │   ├── meters/  
│   │   │   ├── HorizontalMeter.tsx  
│   │   │   └── CircularDial.tsx  
│   │   ├── text/  
│   │   │   └── KineticText.tsx  
│   │   └── layers/  
│   │       └── ImageLayer.tsx  
│   ├── tokens/                 \# Motion token implementations  
│   │   ├── entrance.ts  
│   │   ├── emphasis.ts  
│   │   └── camera.ts  
│   └── utils/  
│       ├── config\_loader.ts    \# Load scene configs  
│       └── brand\_kit.ts        \# Apply brand styling  
├── package.json  
└── tsconfig.json  
\`\`\`

\---

\#\# 3\. Scene Configuration Loading

\#\#\# How Configs Reach Motion Canvas

\`\`\`typescript  
// utils/config\_loader.ts

import { readFileSync } from 'fs';  
import { join } from 'path';

interface SceneConfig {  
  scene\_id: string;  
  version: string;  
  parameters: Record\<string, any\>;  
  layer\_graph\_id?: string;  
  brand\_kit\_id?: string;  
}

let CURRENT\_CONFIG: SceneConfig | null \= null;

export function loadSceneConfig(): SceneConfig {  
  if (CURRENT\_CONFIG) return CURRENT\_CONFIG;  
    
  // Motion Canvas passes config path via environment  
  const configPath \= process.env.SCENE\_CONFIG\_PATH;  
  if (\!configPath) {  
    throw new Error('SCENE\_CONFIG\_PATH not set');  
  }  
    
  const configData \= readFileSync(configPath, 'utf-8');  
  CURRENT\_CONFIG \= JSON.parse(configData);  
    
  return CURRENT\_CONFIG;  
}

export function getParameter\<T\>(key: string, defaultValue?: T): T {  
  const config \= loadSceneConfig();  
  return config.parameters\[key\] ?? defaultValue;  
}  
\`\`\`

\#\#\# Layer Graph Loading

\`\`\`typescript  
// utils/layer\_loader.ts

import { readFileSync } from 'fs';  
import { join } from 'path';

interface LayerGraph {  
  graph\_id: string;  
  layers: Array\<{  
    layer\_id: string;  
    rgba\_asset: string;  
    bbox: { x: number; y: number; w: number; h: number };  
    semantics: string\[\];  
  }\>;  
}

export function loadLayerGraph(): LayerGraph | null {  
  const config \= loadSceneConfig();  
  if (\!config.layer\_graph\_id) return null;  
    
  const graphPath \= join(  
    process.env.DATA\_DIR || '../data',  
    'layer\_graphs',  
    config.layer\_graph\_id,  
    'graph.json'  
  );  
    
  const graphData \= readFileSync(graphPath, 'utf-8');  
  return JSON.parse(graphData);  
}

export function getLayerAssetPath(layerId: string): string {  
  const graph \= loadLayerGraph();  
  const layer \= graph?.layers.find(l \=\> l.layer\_id \=== layerId);  
    
  if (\!layer) {  
    throw new Error(\`Layer not found: ${layerId}\`);  
  }  
    
  return layer.rgba\_asset;  
}  
\`\`\`

\---

\#\# 4\. Example Scene Implementation

\#\#\# Rating Meter Scene (Complete)

\`\`\`typescript  
// scenes/rating\_meter.tsx

import { makeScene2D } from '@motion-canvas/2d';  
import { Rect, Txt, Layout } from '@motion-canvas/2d/lib/components';  
import { createRef } from '@motion-canvas/core';  
import { easeOutCubic } from '@motion-canvas/core/lib/tweening';  
import { loadSceneConfig, getParameter } from '../utils/config\_loader';  
import { applyBrandColors } from '../utils/brand\_kit';

export default makeScene2D(function\* (view) {  
  // Load configuration  
  const config \= loadSceneConfig();  
  const brand \= applyBrandColors(config.brand\_kit\_id);  
    
  // Extract parameters  
  const ratingValue \= getParameter\<number\>('rating\_value', 7);  
  const minValue \= getParameter\<number\>('min\_value', 0);  
  const maxValue \= getParameter\<number\>('max\_value', 10);  
  const labelText \= getParameter\<string\>('label\_text', 'Rating');  
  const orientation \= getParameter\<string\>('orientation', 'horizontal');  
    
  // Create refs  
  const meterContainer \= createRef\<Rect\>();  
  const fillBar \= createRef\<Rect\>();  
  const valueLabel \= createRef\<Txt\>();  
    
  // Calculate dimensions  
  const containerWidth \= 800;  
  const containerHeight \= 60;  
  const fillRatio \= (ratingValue \- minValue) / (maxValue \- minValue);  
  const targetWidth \= containerWidth \* fillRatio;  
    
  // Build scene  
  view.add(  
    \<Layout  
      direction="column"  
      gap={24}  
      alignItems="center"  
      y={0}  
    \>  
      {/\* Label \*/}  
      \<Txt  
        text={labelText}  
        fontSize={28}  
        fill={brand.text}  
        fontFamily="Inter-Medium"  
      /\>  
        
      {/\* Meter \*/}  
      \<Rect  
        ref={meterContainer}  
        width={containerWidth}  
        height={containerHeight}  
        fill={brand.background}  
        radius={8}  
      \>  
        \<Rect  
          ref={fillBar}  
          width={0}  
          height={containerHeight}  
          fill={brand.primary}  
          radius={8}  
        /\>  
      \</Rect\>  
        
      {/\* Value \*/}  
      \<Txt  
        ref={valueLabel}  
        text={ratingValue.toString()}  
        fontSize={64}  
        fill={brand.primary}  
        fontFamily="SpaceGrotesk-Bold"  
        opacity={0}  
      /\>  
    \</Layout\>  
  );  
    
  // Animation sequence  
  yield\* fillBar().width(0, 0).to(targetWidth, 30, easeOutCubic);  
  yield\* valueLabel().opacity(0, 0).to(1, 18, easeOutCubic);  
});  
\`\`\`

\---

\#\# 5\. Reusable Component Example

\`\`\`typescript  
// components/meters/HorizontalMeter.tsx

import { Rect, Txt, Layout } from '@motion-canvas/2d/lib/components';  
import { createRef, Reference } from '@motion-canvas/core';  
import { easeOutCubic } from '@motion-canvas/core/lib/tweening';

export interface HorizontalMeterProps {  
  width: number;  
  height: number;  
  minValue: number;  
  maxValue: number;  
  fillColor: string;  
  backgroundColor: string;  
}

export class HorizontalMeter extends Layout {  
  private fillBar: Reference\<Rect\> \= createRef\<Rect\>();  
    
  constructor(props: HorizontalMeterProps) {  
    super({  
      direction: 'row',  
    });  
      
    this.add(  
      \<Rect  
        width={props.width}  
        height={props.height}  
        fill={props.backgroundColor}  
        radius={8}  
      \>  
        \<Rect  
          ref={this.fillBar}  
          width={0}  
          height={props.height}  
          fill={props.fillColor}  
          radius={8}  
        /\>  
      \</Rect\>  
    );  
  }  
    
  \*animateTo(targetValue: number, duration: number) {  
    const props \= this.props as HorizontalMeterProps;  
    const fillRatio \= (targetValue \- props.minValue) / (props.maxValue \- props.minValue);  
    const targetWidth \= props.width \* fillRatio;  
      
    yield\* this.fillBar().width(0, 0).to(targetWidth, duration, easeOutCubic);  
  }  
}  
\`\`\`

\---

\#\# 6\. Motion Token Implementation

\`\`\`typescript  
// tokens/entrance.ts

import { Reference } from '@motion-canvas/core';  
import { Node } from '@motion-canvas/2d/lib/components';  
import { easeOutCubic } from '@motion-canvas/core/lib/tweening';

export function\* fadeIn(node: Reference\<Node\>, duration: number \= 18\) {  
  yield\* node().opacity(0, 0).to(1, duration, easeOutCubic);  
}

export function\* fadeInUp(  
  node: Reference\<Node\>,   
  duration: number \= 18,  
  distance: number \= 24  
) {  
  const startY \= node().position.y() \+ distance;  
    
  yield\* all(  
    node().opacity(0, 0).to(1, duration, easeOutCubic),  
    node().position.y(startY, 0).to(node().position.y(), duration, easeOutCubic)  
  );  
}

export function\* slideInLeft(  
  node: Reference\<Node\>,  
  duration: number \= 24  
) {  
  const startX \= \-200; // Off-screen left  
  const endX \= node().position.x();  
    
  yield\* node().position.x(startX, 0).to(endX, duration, easeOutCubic);  
}  
\`\`\`

\---

\#\# 7\. Brand Kit Application

\`\`\`typescript  
// utils/brand\_kit.ts

import { readFileSync } from 'fs';  
import { join } from 'path';

interface BrandColors {  
  primary: string;  
  secondary: string;  
  accent: string;  
  text: string;  
  background: string;  
}

interface BrandKit {  
  brand\_id: string;  
  colors: BrandColors;  
  fonts: {  
    headline: string;  
    body: string;  
    number: string;  
  };  
}

let BRAND\_CACHE: Record\<string, BrandKit\> \= {};

export function loadBrandKit(brandId: string): BrandKit {  
  if (BRAND\_CACHE\[brandId\]) {  
    return BRAND\_CACHE\[brandId\];  
  }  
    
  const brandPath \= join(  
    process.env.CONFIG\_DIR || '../config',  
    'brand\_kits',  
    \`${brandId}.json\`  
  );  
    
  const brandData \= readFileSync(brandPath, 'utf-8');  
  const brand \= JSON.parse(brandData);  
    
  BRAND\_CACHE\[brandId\] \= brand;  
  return brand;  
}

export function applyBrandColors(brandId?: string): BrandColors {  
  const brand \= loadBrandKit(brandId || 'default\_brand');  
  return brand.colors;  
}  
\`\`\`

\---

\#\# 8\. Rendering Execution

\#\#\# Python Wrapper for Motion Canvas

\`\`\`python  
\# orchestrator/renderer.py

import subprocess  
import json  
from pathlib import Path  
from typing import Dict

class MotionCanvasRenderer:  
    """Wrapper for Motion Canvas rendering"""  
      
    def \_\_init\_\_(self, motion\_canvas\_dir: Path):  
        self.mc\_dir \= motion\_canvas\_dir  
      
    def render\_scene(  
        self,   
        scene\_config: Dict,  
        output\_path: Path  
    ) \-\> Path:  
        """Render a single scene"""  
          
        \# Write config to temp file  
        config\_path \= Path("data/temp") / f"config\_{scene\_config\['scene\_id'\]}.json"  
        with open(config\_path, 'w') as f:  
            json.dump(scene\_config, f)  
          
        \# Determine which scene file to use  
        scene\_id \= scene\_config\['scene\_id'\]  
        scene\_file \= self.\_map\_scene\_id\_to\_file(scene\_id)  
          
        \# Build Motion Canvas command  
        cmd \= \[  
            "npm", "run", "render",  
            "--",  
            "--scene", scene\_file,  
            "--output", str(output\_path)  
        \]  
          
        \# Set environment variables  
        env \= {  
            "SCENE\_CONFIG\_PATH": str(config\_path),  
            "DATA\_DIR": "data",  
            "CONFIG\_DIR": "config"  
        }  
          
        \# Execute  
        result \= subprocess.run(  
            cmd,  
            cwd=self.mc\_dir,  
            env={\*\*subprocess.os.environ, \*\*env},  
            capture\_output=True,  
            text=True,  
            timeout=120  
        )  
          
        if result.returncode \!= 0:  
            raise RuntimeError(f"Render failed: {result.stderr}")  
          
        return output\_path  
      
    def \_map\_scene\_id\_to\_file(self, scene\_id: str) \-\> str:  
        """Map scene ID to TypeScript file"""  
        scene\_map \= {  
            "RATING\_METER\_1\_TO\_10": "rating\_meter",  
            "BODY\_MAP\_FOCUS": "body\_map\_focus",  
            "BEFORE\_AFTER\_SELF\_SCORE": "before\_after",  
            \# ... more mappings  
        }  
          
        scene\_file \= scene\_map.get(scene\_id)  
        if not scene\_file:  
            raise ValueError(f"Unknown scene: {scene\_id}")  
          
        return scene\_file  
\`\`\`

\---

\#\# 9\. Complete Render Flow

\`\`\`  
1\. Python orchestrator creates scene config JSON  
   └─ data/configs/rating\_meter\_001.json

2\. Python calls Motion Canvas renderer  
   └─ subprocess.run(\["npm", "run", "render"\])  
   └─ Sets SCENE\_CONFIG\_PATH environment variable

3\. Motion Canvas project starts  
   └─ src/project.ts loads scenes

4\. Scene TypeScript file executes  
   └─ loadSceneConfig() reads JSON  
   └─ Creates Motion Canvas components  
   └─ Executes animation generators

5\. Motion Canvas renders frames  
   └─ Outputs to temp directory

6\. FFmpeg encodes video  
   └─ Final MP4 at data/rendered/rating\_meter\_001.mp4  
\`\`\`

\---

\#\# 10\. Project Configuration

\`\`\`typescript  
// motion-canvas/src/project.ts

import { makeProject } from '@motion-canvas/core';

// Import all scene modules  
import ratingMeter from './scenes/rating\_meter';  
import bodyMapFocus from './scenes/body\_map\_focus';  
import beforeAfter from './scenes/before\_after';  
// ... more scenes

export default makeProject({  
  scenes: \[  
    ratingMeter,  
    bodyMapFocus,  
    beforeAfter,  
    // ... more scenes  
  \],  
});  
\`\`\`

\---

\#\# 11\. CLI Integration

\`\`\`bash  
\# From Python orchestrator  
cd motion-canvas

\# Render specific scene  
SCENE\_CONFIG\_PATH=../data/configs/rating\_001.json \\  
  npm run render \-- \\  
  \--scene rating\_meter \\  
  \--output ../data/rendered/rating\_meter\_001.mp4  
\`\`\`

\---

\#\# 12\. Performance Considerations

\#\#\# Frame Caching  
Motion Canvas automatically caches unchanged frames.

\#\#\# Parallel Rendering  
\`\`\`python  
\# Render multiple scenes in parallel  
from concurrent.futures import ProcessPoolExecutor

def render\_all\_scenes(configs: List\[Dict\], output\_dir: Path):  
    with ProcessPoolExecutor(max\_workers=4) as executor:  
        futures \= \[  
            executor.submit(renderer.render\_scene, config, output\_dir)  
            for config in configs  
        \]  
        return \[f.result() for f in futures\]  
\`\`\`

\---

\#\# 13\. Error Handling

\`\`\`typescript  
// scenes/rating\_meter.tsx

export default makeScene2D(function\* (view) {  
  try {  
    const config \= loadSceneConfig();  
      
    // Validate required parameters  
    if (config.parameters.rating\_value \=== undefined) {  
      throw new Error('rating\_value parameter required');  
    }  
      
    // ... rest of scene  
      
  } catch (error) {  
    console.error('Scene error:', error);  
      
    // Render error state  
    view.add(  
      \<Txt  
        text="Scene Error"  
        fontSize={48}  
        fill="\#FF0000"  
      /\>  
    );  
  }  
});  
\`\`\`

\---

\#\# 14\. Testing Scenes

\`\`\`typescript  
// tests/scene\_test.ts

import { test } from '@playwright/test';  
import { loadSceneConfig } from '../src/utils/config\_loader';

test('rating meter renders correctly', async () \=\> {  
  // Set test config  
  process.env.SCENE\_CONFIG\_PATH \= 'tests/fixtures/rating\_config.json';  
    
  // Render scene  
  const scene \= await import('../src/scenes/rating\_meter');  
    
  // Assertions  
  const config \= loadSceneConfig();  
  expect(config.parameters.rating\_value).toBe(7);  
});  
\`\`\`

\---

\#\# 15\. Motion Canvas Limitations

\#\#\# Known Constraints  
\- \*\*No audio handling\*\* \- Audio managed externally  
\- \*\*No video input\*\* \- Only images and generated graphics  
\- \*\*CPU rendering\*\* \- GPU acceleration limited  
\- \*\*Memory usage\*\* \- High-res scenes consume significant RAM

\#\#\# Workarounds  
\- \*\*Audio:\*\* Composite separately with FFmpeg  
\- \*\*Video input:\*\* Convert to image sequences first  
\- \*\*Performance:\*\* Use lower preview resolution during development  
\- \*\*Memory:\*\* Render in batches, clear cache between scenes

\---

\*\*Motion Canvas integration is now fully specified and executable.\*\*  
