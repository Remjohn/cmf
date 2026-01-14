# **agent\_pipeline\_execution.md**

\*\*Purpose:\*\* Concrete agent orchestration and data flow    
\*\*Status:\*\* Canonical v1.0

\---

\#\# 1\. Pipeline Overview

The agent pipeline transforms user input into render-ready scene configurations through a series of deterministic transformations.

\*\*Core Principle:\*\* Each agent reads JSON, processes, writes JSON. No shared state.

\---

\#\# 2\. Standard Pipeline Flow

\`\`\`  
Input: context.json  
   ↓  
\[1. ContextAnalyzer\]  
   → analyzed.json (topic, intent, concepts)  
   ↓  
\[2. ScenePlanner\]  
   → plan.json (selected scenes, priorities)  
   ↓  
\[3. AssetValidator\]  
   → validated.json (available/missing assets)  
   ↓  
\[4. ImageGenerator\] (optional)  
   → generated.json (new asset paths)  
   ↓  
\[5. LayerExtractor\]  
   → layers.json (layer graphs per asset)  
   ↓  
\[6. SemanticLabeler\]  
   → labeled.json (semantic tags added)  
   ↓  
\[7. SpeechAnalyzer\] (optional)  
   → speech.json (temporal anchors)  
   ↓  
\[8. ParameterFiller\]  
   → configs.json (scene configurations)  
   ↓  
\[9. Validator\]  
   → validated\_configs.json  
   ↓  
\[10. Renderer\] (Motion Canvas)  
   → scene\_001.mp4, scene\_002.mp4, ...  
\`\`\`

\---

\#\# 3\. Sequential Execution (Shell-Style)

\`\`\`bash  
\#\!/bin/bash  
\# Pipeline executor (simple version)

INPUT\_CONTEXT="data/input/example.json"  
TEMP\_DIR="data/temp/pipeline\_$(date \+%s)"  
OUTPUT\_DIR="data/rendered"

mkdir \-p "$TEMP\_DIR"

\# Step 1: Analyze context  
cat "$INPUT\_CONTEXT" | \\  
  python agents/context\_analyzer.py \> "$TEMP\_DIR/analyzed.json"

\# Step 2: Plan scenes  
cat "$TEMP\_DIR/analyzed.json" | \\  
  python agents/scene\_planner.py \> "$TEMP\_DIR/plan.json"

\# Step 3: Validate assets  
cat "$TEMP\_DIR/plan.json" | \\  
  python agents/asset\_validator.py \> "$TEMP\_DIR/validated.json"

\# Step 4: Extract layers (for each asset)  
cat "$TEMP\_DIR/validated.json" | \\  
  python agents/layer\_extractor.py \> "$TEMP\_DIR/layers.json"

\# Step 5: Semantic labeling  
cat "$TEMP\_DIR/layers.json" | \\  
  python agents/semantic\_labeler.py \> "$TEMP\_DIR/labeled.json"

\# Step 6: Fill scene parameters  
cat "$TEMP\_DIR/labeled.json" | \\  
  python agents/parameter\_filler.py \> "$TEMP\_DIR/configs.json"

\# Step 7: Validate configurations  
cat "$TEMP\_DIR/configs.json" | \\  
  python agents/validator.py \> "$TEMP\_DIR/validated\_configs.json"

\# Step 8: Render scenes  
python orchestrator/render\_scenes.py \\  
  \--configs "$TEMP\_DIR/validated\_configs.json" \\  
  \--output "$OUTPUT\_DIR"

echo "✅ Pipeline complete. Scenes in $OUTPUT\_DIR"  
\`\`\`

\---

\#\# 4\. Python Orchestrator (Production)

\`\`\`python  
\# orchestrator/pipeline.py

import json  
import subprocess  
from pathlib import Path  
from typing import Dict, List, Optional  
import logging

logger \= logging.getLogger(\_\_name\_\_)

class Pipeline:  
    """Agent pipeline orchestrator"""  
      
    AGENTS \= \[  
        "context\_analyzer",  
        "scene\_planner",  
        "asset\_validator",  
        "layer\_extractor",  
        "semantic\_labeler",  
        "parameter\_filler",  
        "validator"  
    \]  
      
    def \_\_init\_\_(self, temp\_dir: Path):  
        self.temp\_dir \= temp\_dir  
        self.temp\_dir.mkdir(parents=True, exist\_ok=True)  
          
    def run(self, context\_path: Path, output\_dir: Path) \-\> Dict:  
        """Run full pipeline"""  
        logger.info(f"Starting pipeline for {context\_path}")  
          
        \# Load initial context  
        with open(context\_path) as f:  
            current\_data \= json.load(f)  
          
        \# Execute agents sequentially  
        for agent\_name in self.AGENTS:  
            logger.info(f"Running {agent\_name}...")  
              
            try:  
                current\_data \= self.\_run\_agent(agent\_name, current\_data)  
                self.\_save\_checkpoint(agent\_name, current\_data)  
            except Exception as e:  
                logger.error(f"Agent {agent\_name} failed: {e}")  
                return self.\_handle\_failure(agent\_name, e)  
          
        \# Render scenes  
        logger.info("Rendering scenes...")  
        rendered\_scenes \= self.\_render\_scenes(current\_data, output\_dir)  
          
        return {  
            "status": "success",  
            "scenes": rendered\_scenes,  
            "pipeline\_data": current\_data  
        }  
      
    def \_run\_agent(self, agent\_name: str, input\_data: Dict) \-\> Dict:  
        """Execute single agent via subprocess"""  
        agent\_path \= f"agents/{agent\_name}.py"  
          
        \# Run agent as subprocess  
        process \= subprocess.Popen(  
            \["python", agent\_path\],  
            stdin=subprocess.PIPE,  
            stdout=subprocess.PIPE,  
            stderr=subprocess.PIPE,  
            text=True  
        )  
          
        \# Send input, get output  
        stdout, stderr \= process.communicate(  
            input=json.dumps(input\_data),  
            timeout=60  
        )  
          
        if process.returncode \!= 0:  
            raise RuntimeError(f"Agent failed: {stderr}")  
          
        \# Parse output  
        return json.loads(stdout)  
      
    def \_save\_checkpoint(self, agent\_name: str, data: Dict):  
        """Save intermediate result"""  
        checkpoint\_path \= self.temp\_dir / f"{agent\_name}\_output.json"  
        with open(checkpoint\_path, 'w') as f:  
            json.dump(data, f, indent=2)  
      
    def \_render\_scenes(self, pipeline\_data: Dict, output\_dir: Path) \-\> List\[Dict\]:  
        """Render all scene configurations"""  
        from orchestrator.renderer import render\_scene  
          
        scene\_configs \= pipeline\_data.get("scene\_configs", \[\])  
        rendered \= \[\]  
          
        for config in scene\_configs:  
            try:  
                output\_path \= render\_scene(config, output\_dir)  
                rendered.append({  
                    "scene\_id": config\["scene\_id"\],  
                    "path": str(output\_path),  
                    "status": "success"  
                })  
            except Exception as e:  
                logger.error(f"Render failed for {config\['scene\_id'\]}: {e}")  
                rendered.append({  
                    "scene\_id": config\["scene\_id"\],  
                    "status": "failed",  
                    "error": str(e)  
                })  
          
        return rendered  
      
    def \_handle\_failure(self, agent\_name: str, error: Exception) \-\> Dict:  
        """Handle agent failure"""  
        logger.error(f"Pipeline failed at {agent\_name}")  
        return {  
            "status": "failed",  
            "failed\_agent": agent\_name,  
            "error": str(error)  
        }

def run\_pipeline(context\_path: str, output\_dir: str):  
    """CLI entry point"""  
    import tempfile  
      
    with tempfile.TemporaryDirectory() as temp\_dir:  
        pipeline \= Pipeline(Path(temp\_dir))  
        result \= pipeline.run(Path(context\_path), Path(output\_dir))  
          
        if result\["status"\] \== "success":  
            print(f"✅ Generated {len(result\['scenes'\])} scenes")  
        else:  
            print(f"❌ Pipeline failed: {result\['error'\]}")  
            exit(1)  
\`\`\`

\---

\#\# 5\. Agent Runner (Subprocess Management)

\`\`\`python  
\# orchestrator/agent\_runner.py

import subprocess  
import json  
from typing import Dict, Optional  
from pathlib import Path

class AgentRunner:  
    """Execute agents with error handling and retries"""  
      
    def \_\_init\_\_(self, max\_retries: int \= 3, timeout: int \= 60):  
        self.max\_retries \= max\_retries  
        self.timeout \= timeout  
      
    def run(self, agent\_name: str, input\_data: Dict) \-\> Dict:  
        """Run agent with retries"""  
        for attempt in range(self.max\_retries):  
            try:  
                return self.\_execute(agent\_name, input\_data)  
            except subprocess.TimeoutExpired:  
                if attempt \== self.max\_retries \- 1:  
                    raise  
                print(f"Retry {attempt \+ 1}/{self.max\_retries}...")  
          
        raise RuntimeError(f"Agent {agent\_name} failed after {self.max\_retries} attempts")  
      
    def \_execute(self, agent\_name: str, input\_data: Dict) \-\> Dict:  
        """Execute single attempt"""  
        agent\_script \= Path("agents") / f"{agent\_name}.py"  
          
        if not agent\_script.exists():  
            raise FileNotFoundError(f"Agent not found: {agent\_script}")  
          
        \# Execute  
        process \= subprocess.Popen(  
            \["python", str(agent\_script)\],  
            stdin=subprocess.PIPE,  
            stdout=subprocess.PIPE,  
            stderr=subprocess.PIPE,  
            text=True  
        )  
          
        \# Communicate with timeout  
        stdout, stderr \= process.communicate(  
            input=json.dumps(input\_data),  
            timeout=self.timeout  
        )  
          
        \# Check success  
        if process.returncode \!= 0:  
            error\_data \= json.loads(stderr) if stderr else {"error": "Unknown"}  
            raise RuntimeError(f"Agent error: {error\_data}")  
          
        \# Parse output  
        try:  
            output \= json.loads(stdout)  
            return output  
        except json.JSONDecodeError as e:  
            raise RuntimeError(f"Invalid JSON output from {agent\_name}: {e}")  
\`\`\`

\---

\#\# 6\. Parallel Execution (Optional)

\`\`\`python  
\# orchestrator/parallel\_pipeline.py

from concurrent.futures import ProcessPoolExecutor, as\_completed  
from typing import List, Dict

class ParallelPipeline(Pipeline):  
    """Pipeline with parallel layer extraction"""  
      
    def run(self, context\_path: Path, output\_dir: Path) \-\> Dict:  
        \# Run sequential agents first  
        current\_data \= self.\_run\_sequential\_phase(context\_path)  
          
        \# Parallel layer extraction  
        current\_data \= self.\_run\_parallel\_layer\_extraction(current\_data)  
          
        \# Continue sequential  
        current\_data \= self.\_run\_final\_phase(current\_data)  
          
        \# Render (can also be parallel)  
        rendered \= self.\_render\_scenes\_parallel(current\_data, output\_dir)  
          
        return {"status": "success", "scenes": rendered}  
      
    def \_run\_parallel\_layer\_extraction(self, data: Dict) \-\> Dict:  
        """Extract layers from multiple images in parallel"""  
        assets \= data.get("assets", \[\])  
          
        with ProcessPoolExecutor(max\_workers=4) as executor:  
            futures \= {  
                executor.submit(self.\_extract\_layers, asset): asset  
                for asset in assets  
            }  
              
            layer\_graphs \= \[\]  
            for future in as\_completed(futures):  
                asset \= futures\[future\]  
                try:  
                    layer\_graph \= future.result()  
                    layer\_graphs.append(layer\_graph)  
                except Exception as e:  
                    logger.error(f"Layer extraction failed for {asset}: {e}")  
          
        data\["layer\_graphs"\] \= layer\_graphs  
        return data  
\`\`\`

\---

\#\# 7\. Data Flow Examples

\#\#\# Example 1: Simple Rating Scene

\*\*Input (context.json):\*\*  
\`\`\`json  
{  
  "script": "I'd say I'm at a 7 right now",  
  "rating": 7  
}  
\`\`\`

\*\*After ContextAnalyzer:\*\*  
\`\`\`json  
{  
  "agent\_id": "ContextAnalyzer",  
  "output": {  
    "topic": "self\_assessment",  
    "intent": "social\_proof",  
    "rating\_detected": 7,  
    "confidence": 0.95  
  }  
}  
\`\`\`

\*\*After ScenePlanner:\*\*  
\`\`\`json  
{  
  "agent\_id": "ScenePlanner",  
  "output": {  
    "selected\_scenes": \[  
      {  
        "scene\_id": "RATING\_METER\_1\_TO\_10",  
        "priority": 1,  
        "confidence": 0.98  
      }  
    \]  
  }  
}  
\`\`\`

\*\*After ParameterFiller:\*\*  
\`\`\`json  
{  
  "agent\_id": "ParameterFiller",  
  "output": {  
    "scene\_configs": \[  
      {  
        "scene\_id": "RATING\_METER\_1\_TO\_10",  
        "version": "1.0",  
        "parameters": {  
          "rating\_value": 7,  
          "min\_value": 0,  
          "max\_value": 10,  
          "label\_text": "Current Level"  
        }  
      }  
    \]  
  }  
}  
\`\`\`

\---

\#\#\# Example 2: Body Map Scene with Layer Extraction

\*\*Input (context.json):\*\*  
\`\`\`json  
{  
  "script": "Your gut is your second brain",  
  "assets": \["data/assets/body\_diagram.png"\]  
}  
\`\`\`

\*\*After LayerExtractor:\*\*  
\`\`\`json  
{  
  "layer\_graphs": \[  
    {  
      "graph\_id": "body\_001",  
      "layers": \[  
        {"layer\_id": "body\_base", "src": "..."},  
        {"layer\_id": "gut\_region", "src": "..."}  
      \]  
    }  
  \]  
}  
\`\`\`

\*\*After SemanticLabeler:\*\*  
\`\`\`json  
{  
  "layer\_graphs": \[  
    {  
      "graph\_id": "body\_001",  
      "layers": \[  
        {  
          "layer\_id": "gut\_region",  
          "semantics": \["gut", "intuition", "nervous\_system"\]  
        }  
      \]  
    }  
  \]  
}  
\`\`\`

\*\*After ParameterFiller:\*\*  
\`\`\`json  
{  
  "scene\_configs": \[  
    {  
      "scene\_id": "BODY\_MAP\_FOCUS",  
      "layer\_graph\_id": "body\_001",  
      "parameters": {  
        "headline\_text": "Your intuition lives here",  
        "focus\_layer\_id": "gut\_region"  
      }  
    }  
  \]  
}  
\`\`\`

\---

\#\# 8\. Error Handling Strategies

\#\#\# Strategy 1: Fail Fast  
\`\`\`python  
def run\_fail\_fast(self, context\_path: Path):  
    """Stop immediately on any error"""  
    for agent in self.AGENTS:  
        result \= self.\_run\_agent(agent, current\_data)  
        if result.get("error"):  
            raise RuntimeError(f"Agent {agent} failed")  
        current\_data \= result  
\`\`\`

\#\#\# Strategy 2: Continue with Fallbacks  
\`\`\`python  
def run\_with\_fallbacks(self, context\_path: Path):  
    """Continue with degraded functionality"""  
    for agent in self.AGENTS:  
        try:  
            result \= self.\_run\_agent(agent, current\_data)  
            current\_data \= result  
        except Exception as e:  
            logger.warning(f"Agent {agent} failed, using fallback")  
            current\_data \= self.\_get\_fallback(agent, current\_data)  
\`\`\`

\#\#\# Strategy 3: Partial Success  
\`\`\`python  
def run\_partial(self, context\_path: Path):  
    """Generate what's possible, skip failures"""  
    successful\_configs \= \[\]  
    for scene\_config in all\_configs:  
        try:  
            rendered \= self.\_render\_scene(scene\_config)  
            successful\_configs.append(rendered)  
        except Exception:  
            logger.warning(f"Skipping scene {scene\_config\['scene\_id'\]}")  
    return successful\_configs  
\`\`\`

\---

\#\# 9\. Debugging & Inspection

\#\#\# Save All Intermediate Outputs  
\`\`\`python  
def run\_debug(self, context\_path: Path, debug\_dir: Path):  
    """Save every intermediate step"""  
    debug\_dir.mkdir(exist\_ok=True)  
      
    for i, agent in enumerate(self.AGENTS):  
        input\_path \= debug\_dir / f"{i:02d}\_{agent}\_input.json"  
        output\_path \= debug\_dir / f"{i:02d}\_{agent}\_output.json"  
          
        \# Save input  
        with open(input\_path, 'w') as f:  
            json.dump(current\_data, f, indent=2)  
          
        \# Run agent  
        current\_data \= self.\_run\_agent(agent, current\_data)  
          
        \# Save output  
        with open(output\_path, 'w') as f:  
            json.dump(current\_data, f, indent=2)  
\`\`\`

\---

\#\# 10\. CLI Integration

\`\`\`python  
\# cli.py (generate command)

@cli.command()  
@click.option('--context', required=True, type=click.Path(exists=True))  
@click.option('--output', required=True, type=click.Path())  
@click.option('--debug', is\_flag=True)  
@click.option('--parallel/--sequential', default=False)  
def generate(context, output, debug, parallel):  
    """Generate scenes from context"""  
      
    \# Choose pipeline  
    if parallel:  
        from orchestrator.parallel\_pipeline import ParallelPipeline as PipelineClass  
    else:  
        from orchestrator.pipeline import Pipeline as PipelineClass  
      
    \# Setup  
    temp\_dir \= Path("data/temp") / f"pipeline\_{int(time.time())}"  
    pipeline \= PipelineClass(temp\_dir)  
      
    \# Run  
    try:  
        result \= pipeline.run(Path(context), Path(output))  
          
        if debug:  
            print(json.dumps(result, indent=2))  
        else:  
            print(f"✅ Generated {len(result\['scenes'\])} scenes")  
            for scene in result\['scenes'\]:  
                print(f"  \- {scene\['scene\_id'\]}: {scene\['path'\]}")  
      
    except Exception as e:  
        print(f"❌ Pipeline failed: {e}", file=sys.stderr)  
        exit(1)  
\`\`\`

\---

\#\# 11\. Performance Monitoring

\`\`\`python  
\# orchestrator/metrics.py

import time  
from contextlib import contextmanager

class PipelineMetrics:  
    def \_\_init\_\_(self):  
        self.timings \= {}  
        self.errors \= \[\]  
      
    @contextmanager  
    def measure(self, agent\_name: str):  
        """Measure agent execution time"""  
        start \= time.time()  
        try:  
            yield  
        except Exception as e:  
            self.errors.append({  
                "agent": agent\_name,  
                "error": str(e)  
            })  
            raise  
        finally:  
            duration \= time.time() \- start  
            self.timings\[agent\_name\] \= duration  
      
    def report(self) \-\> Dict:  
        """Generate metrics report"""  
        return {  
            "total\_time": sum(self.timings.values()),  
            "agent\_timings": self.timings,  
            "errors": self.errors  
        }  
\`\`\`

\---

\*\*The pipeline is now concrete, debuggable, and production-ready.\*\*  
