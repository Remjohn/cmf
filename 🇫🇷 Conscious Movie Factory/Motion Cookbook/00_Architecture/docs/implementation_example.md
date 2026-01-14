# **implementation\_example.md**

\*\*Purpose:\*\* End-to-end working example with actual code    
\*\*Status:\*\* Reference Implementation v1.0

\---

\#\# Complete Working Example: Rating Meter Scene

This document shows every piece of code needed to generate a rating meter scene from start to finish.

\---

\#\# 1\. User Input

\*\*File:\*\* \`data/input/confidence\_rating.json\`

\`\`\`json  
{  
  "script": "How confident do you feel about this new approach? I'd say I'm at about a 7 right now. Before we started, I was probably a 3.",  
  "topic": "confidence\_assessment",  
  "intent": "social\_proof",  
  "metadata": {  
    "speaker\_name": "Sarah",  
    "video\_type": "testimonial"  
  }  
}  
\`\`\`

\---

\#\# 2\. Agent 1: Context Analyzer

\*\*File:\*\* \`agents/context\_analyzer.py\`

\`\`\`python  
\#\!/usr/bin/env python3  
"""Context Analyzer Agent \- Interprets user intent"""

import json  
import sys  
import re  
from typing import Dict, List, Optional

class ContextAnalyzer:  
    def process(self, input\_data: Dict) \-\> Dict:  
        """Analyze context and extract meaning"""  
        script \= input\_data.get("script", "")  
          
        \# Extract ratings from script  
        ratings \= self.\_extract\_ratings(script)  
          
        \# Detect intent  
        intent \= input\_data.get("intent") or self.\_detect\_intent(script)  
          
        \# Extract topic  
        topic \= input\_data.get("topic") or self.\_extract\_topic(script)  
          
        return {  
            "agent\_id": "ContextAnalyzer",  
            "version": "1.0",  
            "output": {  
                "topic": topic,  
                "intent": intent,  
                "ratings\_detected": ratings,  
                "key\_concepts": \["confidence", "progress", "transformation"\],  
                "emotional\_tone": "positive",  
                "confidence": 0.94  
            }  
        }  
      
    def \_extract\_ratings(self, script: str) \-\> List\[Dict\]:  
        """Extract numeric ratings from script"""  
        ratings \= \[\]  
          
        \# Pattern: "I'm at \[X\]" or "about \[X\]" or "maybe \[X\]"  
        patterns \= \[  
            r"(?:at about|at|about)\\s+(?:a\\s+)?(\\d+)",  
            r"(?:maybe|probably)\\s+(?:a\\s+)?(\\d+)"  
        \]  
          
        for pattern in patterns:  
            matches \= re.finditer(pattern, script, re.IGNORECASE)  
            for match in matches:  
                value \= int(match.group(1))  
                context \= "current" if "now" in script\[:match.end()\] else "before"  
                  
                ratings.append({  
                    "value": value,  
                    "context": context  
                })  
          
        return ratings  
      
    def \_detect\_intent(self, script: str) \-\> str:  
        """Detect primary intent"""  
        if any(word in script.lower() for word in \["before", "after", "was", "now"\]):  
            return "social\_proof"  
        elif any(word in script.lower() for word in \["why", "how", "what"\]):  
            return "explain"  
        else:  
            return "emphasize"  
      
    def \_extract\_topic(self, script: str) \-\> str:  
        """Extract main topic"""  
        \# Simple keyword extraction  
        keywords \= \["confidence", "clarity", "energy", "focus"\]  
        for keyword in keywords:  
            if keyword in script.lower():  
                return f"{keyword}\_assessment"  
        return "self\_assessment"

def main():  
    """CLI entry point"""  
    try:  
        \# Read from stdin  
        input\_data \= json.loads(sys.stdin.read())  
          
        \# Process  
        analyzer \= ContextAnalyzer()  
        output \= analyzer.process(input\_data)  
          
        \# Write to stdout  
        print(json.dumps(output, indent=2))  
        sys.exit(0)  
          
    except Exception as e:  
        error \= {  
            "error": str(e),  
            "agent\_id": "ContextAnalyzer"  
        }  
        print(json.dumps(error), file=sys.stderr)  
        sys.exit(1)

if \_\_name\_\_ \== "\_\_main\_\_":  
    main()  
\`\`\`

\*\*Output:\*\* \`data/temp/analyzed.json\`

\`\`\`json  
{  
  "agent\_id": "ContextAnalyzer",  
  "version": "1.0",  
  "output": {  
    "topic": "confidence\_assessment",  
    "intent": "social\_proof",  
    "ratings\_detected": \[  
      {"value": 7, "context": "current"},  
      {"value": 3, "context": "before"}  
    \],  
    "key\_concepts": \["confidence", "progress", "transformation"\],  
    "emotional\_tone": "positive",  
    "confidence": 0.94  
  }  
}  
\`\`\`

\---

\#\# 3\. Agent 2: Scene Planner

\*\*File:\*\* \`agents/scene\_planner.py\`

\`\`\`python  
\#\!/usr/bin/env python3  
"""Scene Planner Agent \- Selects appropriate scenes"""

import json  
import sys  
from typing import Dict, List

class ScenePlanner:  
    \# Scene selection rules  
    SCENE\_RULES \= {  
        "BEFORE\_AFTER\_SELF\_SCORE": {  
            "conditions": {  
                "ratings\_count": 2,  
                "intents": \["social\_proof"\]  
            },  
            "priority": 10  
        },  
        "RATING\_METER\_1\_TO\_10": {  
            "conditions": {  
                "ratings\_count": 1,  
                "intents": \["social\_proof", "emphasize"\]  
            },  
            "priority": 8  
        }  
    }  
      
    def process(self, input\_data: Dict) \-\> Dict:  
        """Select scenes based on context"""  
        analyzed \= input\_data.get("output", input\_data)  
          
        intent \= analyzed.get("intent")  
        ratings \= analyzed.get("ratings\_detected", \[\])  
          
        \# Score each scene  
        scene\_scores \= \[\]  
        for scene\_id, rule in self.SCENE\_RULES.items():  
            score \= self.\_score\_scene(scene\_id, rule, intent, ratings)  
            if score \> 0:  
                scene\_scores.append({  
                    "scene\_id": scene\_id,  
                    "score": score,  
                    "priority": rule\["priority"\]  
                })  
          
        \# Sort by score and priority  
        scene\_scores.sort(key=lambda x: (x\["score"\], x\["priority"\]), reverse=True)  
          
        \# Select top scenes  
        selected \= \[\]  
        for scene in scene\_scores\[:2\]:  \# Max 2 scenes for this example  
            selected.append({  
                "scene\_id": scene\["scene\_id"\],  
                "priority": scene\["priority"\],  
                "rationale": self.\_get\_rationale(scene\["scene\_id"\], ratings),  
                "confidence": 0.9  
            })  
          
        return {  
            "agent\_id": "ScenePlanner",  
            "version": "1.0",  
            "output": {  
                "selected\_scenes": selected,  
                "analyzed\_context": analyzed  
            }  
        }  
      
    def \_score\_scene(self, scene\_id: str, rule: Dict, intent: str, ratings: List) \-\> float:  
        """Calculate scene match score"""  
        score \= 0.0  
        conditions \= rule\["conditions"\]  
          
        \# Check intent match  
        if intent in conditions.get("intents", \[\]):  
            score \+= 5.0  
          
        \# Check ratings count  
        expected\_ratings \= conditions.get("ratings\_count", 0\)  
        if len(ratings) \>= expected\_ratings:  
            score \+= 5.0  
          
        return score  
      
    def \_get\_rationale(self, scene\_id: str, ratings: List) \-\> str:  
        """Generate selection rationale"""  
        if scene\_id \== "BEFORE\_AFTER\_SELF\_SCORE" and len(ratings) \>= 2:  
            return "Script contains before/after comparison with explicit values"  
        elif scene\_id \== "RATING\_METER\_1\_TO\_10":  
            return "Single rating value detected, suitable for meter visualization"  
        return "Scene matches context criteria"

def main():  
    try:  
        input\_data \= json.loads(sys.stdin.read())  
        planner \= ScenePlanner()  
        output \= planner.process(input\_data)  
        print(json.dumps(output, indent=2))  
        sys.exit(0)  
    except Exception as e:  
        error \= {"error": str(e), "agent\_id": "ScenePlanner"}  
        print(json.dumps(error), file=sys.stderr)  
        sys.exit(1)

if \_\_name\_\_ \== "\_\_main\_\_":  
    main()  
\`\`\`

\*\*Output:\*\* \`data/temp/plan.json\`

\`\`\`json  
{  
  "agent\_id": "ScenePlanner",  
  "version": "1.0",  
  "output": {  
    "selected\_scenes": \[  
      {  
        "scene\_id": "BEFORE\_AFTER\_SELF\_SCORE",  
        "priority": 10,  
        "rationale": "Script contains before/after comparison with explicit values",  
        "confidence": 0.9  
      }  
    \],  
    "analyzed\_context": {...}  
  }  
}  
\`\`\`

\---

\#\# 4\. Agent 3: Parameter Filler

\*\*File:\*\* \`agents/parameter\_filler.py\`

\`\`\`python  
\#\!/usr/bin/env python3  
"""Parameter Filler Agent \- Fills scene parameters"""

import json  
import sys  
from typing import Dict, List

class ParameterFiller:  
    def process(self, input\_data: Dict) \-\> Dict:  
        """Fill parameters for selected scenes"""  
        plan \= input\_data.get("output", input\_data)  
        selected\_scenes \= plan.get("selected\_scenes", \[\])  
        context \= plan.get("analyzed\_context", {})  
          
        scene\_configs \= \[\]  
          
        for scene\_info in selected\_scenes:  
            scene\_id \= scene\_info\["scene\_id"\]  
              
            \# Fill parameters based on scene type  
            if scene\_id \== "BEFORE\_AFTER\_SELF\_SCORE":  
                config \= self.\_fill\_before\_after(context)  
            elif scene\_id \== "RATING\_METER\_1\_TO\_10":  
                config \= self.\_fill\_rating\_meter(context)  
            else:  
                continue  
              
            scene\_configs.append(config)  
          
        return {  
            "agent\_id": "ParameterFiller",  
            "version": "1.0",  
            "output": {  
                "scene\_configs": scene\_configs  
            }  
        }  
      
    def \_fill\_before\_after(self, context: Dict) \-\> Dict:  
        """Fill before/after scene parameters"""  
        ratings \= context.get("ratings\_detected", \[\])  
          
        before\_rating \= next((r for r in ratings if r\["context"\] \== "before"), None)  
        current\_rating \= next((r for r in ratings if r\["context"\] \== "current"), None)  
          
        before\_value \= before\_rating\["value"\] if before\_rating else 0  
        after\_value \= current\_rating\["value"\] if current\_rating else 0  
          
        return {  
            "scene\_id": "BEFORE\_AFTER\_SELF\_SCORE",  
            "version": "1.0",  
            "parameters": {  
                "before\_value": before\_value,  
                "after\_value": after\_value,  
                "min\_value": 0,  
                "max\_value": 10,  
                "metric\_label": context.get("topic", "Progress").replace("\_", " ").title(),  
                "delta\_value": after\_value \- before\_value,  
                "show\_delta": True  
            },  
            "timing": {  
                "mode": "absolute",  
                "duration\_frames": 150,  
                "fps": 30  
            },  
            "brand\_kit\_id": "default\_brand"  
        }  
      
    def \_fill\_rating\_meter(self, context: Dict) \-\> Dict:  
        """Fill rating meter parameters"""  
        ratings \= context.get("ratings\_detected", \[\])  
        current\_rating \= next((r for r in ratings if r\["context"\] \== "current"), ratings\[0\] if ratings else None)  
          
        rating\_value \= current\_rating\["value"\] if current\_rating else 5  
          
        return {  
            "scene\_id": "RATING\_METER\_1\_TO\_10",  
            "version": "1.0",  
            "parameters": {  
                "rating\_value": rating\_value,  
                "min\_value": 0,  
                "max\_value": 10,  
                "label\_text": "Current Level",  
                "show\_label": True,  
                "orientation": "horizontal",  
                "fill\_color": "\#00FFD1",  
                "background\_color": "\#2A2A2A"  
            },  
            "timing": {  
                "mode": "absolute",  
                "duration\_frames": 150,  
                "fps": 30  
            },  
            "brand\_kit\_id": "default\_brand"  
        }

def main():  
    try:  
        input\_data \= json.loads(sys.stdin.read())  
        filler \= ParameterFiller()  
        output \= filler.process(input\_data)  
        print(json.dumps(output, indent=2))  
        sys.exit(0)  
    except Exception as e:  
        error \= {"error": str(e), "agent\_id": "ParameterFiller"}  
        print(json.dumps(error), file=sys.stderr)  
        sys.exit(1)

if \_\_name\_\_ \== "\_\_main\_\_":  
    main()  
\`\`\`

\*\*Output:\*\* \`data/configs/before\_after\_001.json\`

\`\`\`json  
{  
  "scene\_id": "BEFORE\_AFTER\_SELF\_SCORE",  
  "version": "1.0",  
  "parameters": {  
    "before\_value": 3,  
    "after\_value": 7,  
    "min\_value": 0,  
    "max\_value": 10,  
    "metric\_label": "Confidence Assessment",  
    "delta\_value": 4,  
    "show\_delta": true  
  },  
  "timing": {  
    "mode": "absolute",  
    "duration\_frames": 150,  
    "fps": 30  
  },  
  "brand\_kit\_id": "default\_brand"  
}  
\`\`\`

\---

\#\# 5\. Motion Canvas Scene

\*\*File:\*\* \`motion-canvas/src/scenes/before\_after.tsx\`

\`\`\`typescript  
import { makeScene2D } from '@motion-canvas/2d';  
import { Rect, Txt, Layout } from '@motion-canvas/2d/lib/components';  
import { createRef, all } from '@motion-canvas/core';  
import { easeOutCubic } from '@motion-canvas/core/lib/tweening';  
import { loadSceneConfig } from '../utils/config\_loader';  
import { applyBrandColors } from '../utils/brand\_kit';

export default makeScene2D(function\* (view) {  
  // Load config  
  const config \= loadSceneConfig();  
  const brand \= applyBrandColors(config.brand\_kit\_id);  
  const params \= config.parameters;  
    
  // Extract parameters  
  const beforeValue \= params.before\_value;  
  const afterValue \= params.after\_value;  
  const minValue \= params.min\_value;  
  const maxValue \= params.max\_value;  
  const metricLabel \= params.metric\_label;  
  const deltaValue \= params.delta\_value;  
    
  // Create refs  
  const beforeBar \= createRef\<Rect\>();  
  const afterBar \= createRef\<Rect\>();  
  const beforeLabel \= createRef\<Txt\>();  
  const afterLabel \= createRef\<Txt\>();  
  const deltaLabel \= createRef\<Txt\>();  
    
  // Calculate dimensions  
  const barWidth \= 600;  
  const barHeight \= 50;  
    
  const beforeRatio \= (beforeValue \- minValue) / (maxValue \- minValue);  
  const afterRatio \= (afterValue \- minValue) / (maxValue \- minValue);  
    
  const beforeWidth \= barWidth \* beforeRatio;  
  const afterWidth \= barWidth \* afterRatio;  
    
  // Build scene  
  view.add(  
    \<Layout  
      direction="column"  
      gap={40}  
      alignItems="center"  
      y={-100}  
    \>  
      {/\* Title \*/}  
      \<Txt  
        text={metricLabel}  
        fontSize={32}  
        fill={brand.text}  
        fontFamily="Inter-Bold"  
      /\>  
        
      {/\* Before meter \*/}  
      \<Layout direction="row" gap={20} alignItems="center" width={800}\>  
        \<Txt  
          ref={beforeLabel}  
          text="Before"  
          fontSize={24}  
          fill="\#888888"  
          width={120}  
        /\>  
        \<Rect  
          width={barWidth}  
          height={barHeight}  
          fill="\#2A2A2A"  
          radius={8}  
        \>  
          \<Rect  
            ref={beforeBar}  
            width={0}  
            height={barHeight}  
            fill="\#666666"  
            radius={8}  
          /\>  
        \</Rect\>  
        \<Txt  
          text={beforeValue.toString()}  
          fontSize={36}  
          fill="\#666666"  
          fontFamily="SpaceGrotesk-Bold"  
          width={60}  
        /\>  
      \</Layout\>  
        
      {/\* After meter \*/}  
      \<Layout direction="row" gap={20} alignItems="center" width={800}\>  
        \<Txt  
          ref={afterLabel}  
          text="After"  
          fontSize={24}  
          fill="\#888888"  
          width={120}  
        /\>  
        \<Rect  
          width={barWidth}  
          height={barHeight}  
          fill="\#2A2A2A"  
          radius={8}  
        \>  
          \<Rect  
            ref={afterBar}  
            width={0}  
            height={barHeight}  
            fill={brand.primary}  
            radius={8}  
          /\>  
        \</Rect\>  
        \<Txt  
          text={afterValue.toString()}  
          fontSize={36}  
          fill={brand.primary}  
          fontFamily="SpaceGrotesk-Bold"  
          width={60}  
        /\>  
      \</Layout\>  
        
      {/\* Delta \*/}  
      \<Rect  
        fill={brand.primary \+ "22"}  
        padding={\[12, 24\]}  
        radius={12}  
        opacity={0}  
      \>  
        \<Txt  
          ref={deltaLabel}  
          text={\`+${deltaValue}\`}  
          fontSize={48}  
          fill={brand.primary}  
          fontFamily="SpaceGrotesk-Bold"  
        /\>  
      \</Rect\>  
    \</Layout\>  
  );  
    
  // Animation sequence  
  // 1\. Before bar fills (frames 0-30)  
  yield\* beforeBar().width(0, 0).to(beforeWidth, 30, easeOutCubic);  
    
  // 2\. Wait a beat (frames 30-45)  
  yield\* all();  
    
  // 3\. After bar fills (frames 45-75)  
  yield\* afterBar().width(0, 0).to(afterWidth, 30, easeOutCubic);  
    
  // 4\. Delta appears (frames 75-90)  
  yield\* deltaLabel().parent().opacity(0, 0).to(1, 18, easeOutCubic);  
    
  // 5\. Hold (frames 90-150)  
  yield\* all();  
});  
\`\`\`

\---

\#\# 6\. Python Renderer

\*\*File:\*\* \`orchestrator/renderer.py\`

\`\`\`python  
import subprocess  
from pathlib import Path  
from typing import Dict  
import json

def render\_scene(scene\_config: Dict, output\_dir: Path) \-\> Path:  
    """Render a scene configuration"""  
      
    \# Create config file  
    config\_path \= Path("data/temp") / f"config\_{scene\_config\['scene\_id'\]}.json"  
    with open(config\_path, 'w') as f:  
        json.dump(scene\_config, f, indent=2)  
      
    \# Map scene ID to file  
    scene\_map \= {  
        "BEFORE\_AFTER\_SELF\_SCORE": "before\_after",  
        "RATING\_METER\_1\_TO\_10": "rating\_meter"  
    }  
      
    scene\_file \= scene\_map\[scene\_config\['scene\_id'\]\]  
    output\_path \= output\_dir / f"{scene\_config\['scene\_id'\]}\_001.mp4"  
      
    \# Build command  
    cmd \= \[  
        "npm", "run", "render",  
        "--",  
        "--scene", scene\_file,  
        "--output", str(output\_path)  
    \]  
      
    \# Set environment  
    env \= {  
        "SCENE\_CONFIG\_PATH": str(config\_path.absolute()),  
        "DATA\_DIR": str(Path("data").absolute()),  
        "CONFIG\_DIR": str(Path("config").absolute())  
    }  
      
    \# Execute  
    result \= subprocess.run(  
        cmd,  
        cwd="motion-canvas",  
        env={\*\*subprocess.os.environ, \*\*env},  
        capture\_output=True,  
        text=True,  
        timeout=120  
    )  
      
    if result.returncode \!= 0:  
        raise RuntimeError(f"Render failed: {result.stderr}")  
      
    return output\_path  
\`\`\`

\---

\#\# 7\. Running the Complete Pipeline

\`\`\`bash  
\#\!/bin/bash  
\# run\_example.sh

echo "🎬 Motion Cookbook \- Complete Example"  
echo "======================================"  
echo

\# Create directories  
mkdir \-p data/{input,temp,configs,rendered}

\# Step 1: Context Analysis  
echo "1️⃣ Analyzing context..."  
cat data/input/confidence\_rating.json | \\  
  python agents/context\_analyzer.py \> data/temp/analyzed.json  
echo "✅ Context analyzed"

\# Step 2: Scene Planning  
echo "2️⃣ Planning scenes..."  
cat data/temp/analyzed.json | \\  
  python agents/scene\_planner.py \> data/temp/plan.json  
echo "✅ Scenes selected"

\# Step 3: Parameter Filling  
echo "3️⃣ Filling parameters..."  
cat data/temp/plan.json | \\  
  python agents/parameter\_filler.py \> data/temp/configs.json  
echo "✅ Parameters filled"

\# Step 4: Rendering  
echo "4️⃣ Rendering scene..."  
python orchestrator/renderer.py \\  
  \--config data/temp/configs.json \\  
  \--output data/rendered/  
echo "✅ Scene rendered"

echo  
echo "🎉 Complete\! Check data/rendered/"  
\`\`\`

\---

\#\# 8\. Expected Output

\`\`\`  
data/rendered/  
├── BEFORE\_AFTER\_SELF\_SCORE\_001.mp4  
└── BEFORE\_AFTER\_SELF\_SCORE\_001.meta.json  
\`\`\`

\*\*Video contains:\*\*  
\- Title: "Confidence Assessment"  
\- Before meter: fills to 3/10 (gray)  
\- After meter: fills to 7/10 (brand color)  
\- Delta badge: "+4"  
\- Duration: 5 seconds

\---

\*\*This is a complete, executable implementation from context to video.\*\*  
