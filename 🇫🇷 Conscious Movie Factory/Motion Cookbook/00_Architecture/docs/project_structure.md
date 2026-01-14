# **project\_structure.md**

\*\*Purpose:\*\* Complete project file organization    
\*\*Status:\*\* Canonical v1.0

\---

\#\# Directory Tree

\`\`\`  
motion-cookbook/  
├── cli.py                          \# Main CLI entry point  
├── requirements.txt                \# Python dependencies  
├── package.json                    \# Node/Motion Canvas dependencies  
├── README.md                       \# Project overview  
├── .gitignore  
├── .env.example                    \# Environment variables template  
│  
├── agents/                         \# AI Agent implementations  
│   ├── \_\_init\_\_.py  
│   ├── base\_agent.py               \# Abstract base class  
│   ├── context\_analyzer.py         \# Interprets user intent  
│   ├── scene\_planner.py            \# Selects appropriate scenes  
│   ├── image\_generator.py          \# Generates missing images (optional)  
│   ├── layer\_extractor.py          \# Decomposes images into layers  
│   ├── semantic\_labeler.py         \# Assigns semantic tags  
│   ├── speech\_analyzer.py          \# Extracts speech anchors  
│   ├── parameter\_filler.py         \# Fills scene parameters  
│   └── validator.py                \# Validates outputs  
│  
├── orchestrator/                   \# Pipeline coordination  
│   ├── \_\_init\_\_.py  
│   ├── pipeline.py                 \# Main orchestration logic  
│   ├── agent\_runner.py             \# Executes individual agents  
│   └── error\_handler.py            \# Handles failures/retries  
│  
├── motion-canvas/                  \# Motion Canvas project  
│   ├── src/  
│   │   ├── scenes/                 \# Scene implementations  
│   │   │   ├── rating\_meter.tsx  
│   │   │   ├── body\_map\_focus.tsx  
│   │   │   ├── before\_after.tsx  
│   │   │   └── ...  
│   │   ├── components/             \# Reusable components  
│   │   │   ├── meters/  
│   │   │   ├── text/  
│   │   │   └── layers/  
│   │   ├── tokens/                 \# Motion tokens  
│   │   │   ├── entrance.ts  
│   │   │   ├── emphasis.ts  
│   │   │   └── camera.ts  
│   │   └── utils/  
│   │       ├── scene\_loader.ts     \# Load scene configs  
│   │       └── brand\_kit.ts        \# Apply brand kits  
│   ├── package.json  
│   └── tsconfig.json  
│  
├── schemas/                        \# JSON schemas  
│   ├── context.schema.json  
│   ├── layer\_graph.schema.json  
│   ├── scene\_config.schema.json  
│   ├── brand\_kit.schema.json  
│   └── agent\_io/  
│       ├── context\_analyzer.schema.json  
│       ├── layer\_extractor.schema.json  
│       └── ...  
│  
├── scenes/                         \# Scene definitions  
│   ├── definitions/                \# Scene metadata  
│   │   ├── rating\_meter\_1\_to\_10.json  
│   │   ├── body\_map\_focus.json  
│   │   ├── before\_after\_self\_score.json  
│   │   └── ...  
│   └── library.json                \# Scene catalog  
│  
├── config/                         \# System configuration  
│   ├── default.yaml                \# Default settings  
│   ├── brand\_kits/                 \# Brand kit storage  
│   │   ├── default\_brand.json  
│   │   └── health\_coach\_alpha.json  
│   └── motion\_tokens.json          \# Token registry  
│  
├── data/                           \# Working data (gitignored)  
│   ├── input/                      \# User contexts  
│   ├── assets/                     \# User-provided images  
│   ├── layer\_graphs/               \# Generated layer graphs  
│   │   └── {graph\_id}/  
│   │       ├── graph.json  
│   │       ├── layer\_001.png  
│   │       └── ...  
│   ├── configs/                    \# Scene configurations  
│   ├── rendered/                   \# Output videos  
│   ├── temp/                       \# Intermediate files  
│   │   └── agent\_outputs/  
│   └── cache/                      \# Cached assets  
│       ├── layer\_graphs/  
│       └── renders/  
│  
├── examples/                       \# Example files  
│   ├── contexts/                   \# Example context files  
│   │   ├── rating\_example.json  
│   │   ├── body\_map\_example.json  
│   │   └── before\_after\_example.json  
│   ├── assets/                     \# Example assets  
│   └── outputs/                    \# Expected outputs  
│  
├── tests/                          \# Test suite  
│   ├── unit/  
│   │   ├── test\_agents.py  
│   │   ├── test\_validation.py  
│   │   └── ...  
│   ├── integration/  
│   │   ├── test\_pipeline.py  
│   │   └── test\_rendering.py  
│   ├── fixtures/                   \# Test data  
│   │   ├── contexts/  
│   │   ├── layer\_graphs/  
│   │   └── golden\_masters/         \# Expected render outputs  
│   └── conftest.py                 \# Pytest configuration  
│  
├── scripts/                        \# Utility scripts  
│   ├── init.sh                     \# Initialize project  
│   ├── verify\_setup.py             \# Verify installation  
│   ├── render\_golden\_masters.py   \# Generate test baselines  
│   └── cleanup.sh                  \# Clean temp files  
│  
├── docs/                           \# Documentation  
│   ├── quickstart.md  
│   ├── cli\_reference.md  
│   ├── file\_formats.md  
│   ├── architecture.md  
│   ├── scene\_schema.md  
│   ├── layer\_graph\_schema.md  
│   ├── motion\_tokens.md  
│   ├── agent\_contracts.md  
│   └── ...  
│  
└── logs/                           \# Log files (gitignored)  
    ├── motion-cookbook.log  
    └── agents/  
\`\`\`

\---

\#\# Key Files Explained

\#\#\# Root Level

\#\#\#\# \`cli.py\`  
Main entry point for all CLI commands. Delegates to orchestrator or agents.

\`\`\`python  
\#\!/usr/bin/env python3  
"""Motion Cookbook CLI"""  
import click  
from orchestrator.pipeline import run\_pipeline  
from agents import \*

@click.group()  
def cli():  
    """Motion Cookbook \- Scene-based explainer animation system"""  
    pass

@cli.command()  
@click.option('--context', required=True)  
@click.option('--output', required=True)  
def generate(context, output):  
    """Generate scenes from context"""  
    run\_pipeline(context, output)

\# ... more commands  
\`\`\`

\#\#\#\# \`requirements.txt\`  
\`\`\`  
click\>=8.1.0  
pydantic\>=2.0.0  
pillow\>=10.0.0  
librosa\>=0.10.0  \# For speech analysis  
opencv-python\>=4.8.0  
jsonschema\>=4.17.0  
pyyaml\>=6.0  
requests\>=2.31.0  
\`\`\`

\#\#\#\# \`package.json\` (Motion Canvas)  
\`\`\`json  
{  
  "name": "motion-cookbook-renderer",  
  "version": "1.0.0",  
  "scripts": {  
    "render": "motion-canvas render",  
    "serve": "motion-canvas serve"  
  },  
  "dependencies": {  
    "@motion-canvas/2d": "^3.15.0",  
    "@motion-canvas/core": "^3.15.0"  
  }  
}  
\`\`\`

\---

\#\#\# Agents Directory

Each agent is a standalone module:

\`\`\`python  
\# agents/base\_agent.py  
from abc import ABC, abstractmethod  
from pydantic import BaseModel  
import json  
import sys

class BaseAgent(ABC):  
    """Abstract base class for all agents"""  
      
    @abstractmethod  
    def process(self, input\_data: dict) \-\> dict:  
        """Process input and return output"""  
        pass  
      
    def run\_from\_stdin(self):  
        """Read from stdin, process, write to stdout"""  
        try:  
            input\_data \= json.loads(sys.stdin.read())  
            output \= self.process(input\_data)  
            print(json.dumps(output))  
            sys.exit(0)  
        except Exception as e:  
            error \= {  
                "error": str(e),  
                "agent\_id": self.\_\_class\_\_.\_\_name\_\_  
            }  
            print(json.dumps(error), file=sys.stderr)  
            sys.exit(1)  
\`\`\`

\`\`\`python  
\# agents/context\_analyzer.py  
from .base\_agent import BaseAgent

class ContextAnalyzer(BaseAgent):  
    def process(self, input\_data: dict) \-\> dict:  
        script \= input\_data.get("script", "")  
          
        \# Analyze script...  
        topic \= self.\_extract\_topic(script)  
        intent \= self.\_detect\_intent(script)  
          
        return {  
            "agent\_id": "ContextAnalyzer",  
            "output": {  
                "topic": topic,  
                "intent": intent,  
                "confidence": 0.9  
            }  
        }  
      
    def \_extract\_topic(self, script: str) \-\> str:  
        \# Implementation...  
        pass  
      
    def \_detect\_intent(self, script: str) \-\> str:  
        \# Implementation...  
        pass

if \_\_name\_\_ \== "\_\_main\_\_":  
    ContextAnalyzer().run\_from\_stdin()  
\`\`\`

\---

\#\#\# Motion Canvas Directory

\`\`\`typescript  
// motion-canvas/src/scenes/rating\_meter.tsx  
import { makeScene2D } from '@motion-canvas/2d';  
import { Rect, Txt } from '@motion-canvas/2d/lib/components';  
import { createRef } from '@motion-canvas/core';  
import { loadSceneConfig } from '../utils/scene\_loader';  
import { applyBrandKit } from '../utils/brand\_kit';

export default makeScene2D(function\* (view) {  
  // Load configuration  
  const config \= loadSceneConfig();  
  const brand \= applyBrandKit(config.brand\_kit\_id);  
    
  // Extract parameters  
  const { rating\_value, max\_value, label\_text } \= config.parameters;  
    
  // Create components  
  const meter \= createRef\<Rect\>();  
  const valueText \= createRef\<Txt\>();  
    
  // ... render logic  
  yield\* meter().width(0, 0).to(targetWidth, 30);  
  yield\* valueText().opacity(0, 0).to(1, 18);  
});  
\`\`\`

\---

\#\#\# Schemas Directory

All JSON schemas for validation:

\`\`\`json  
// schemas/context.schema.json  
{  
  "$schema": "http://json-schema.org/draft-07/schema\#",  
  "type": "object",  
  "required": \["script"\],  
  "properties": {  
    "script": {"type": "string"},  
    "topic": {"type": "string"},  
    "intent": {  
      "type": "string",  
      "enum": \["explain", "emphasize", "storytelling", "social\_proof"\]  
    }  
  }  
}  
\`\`\`

\---

\#\#\# Data Directory Structure

\`\`\`  
data/  
├── input/                          \# User inputs  
│   ├── example\_001.json  
│   └── example\_002.json  
│  
├── assets/                         \# User images  
│   ├── body\_diagram.png  
│   └── speaker\_headshot.png  
│  
├── layer\_graphs/                   \# AI-generated layers  
│   ├── body\_map\_gut\_001/  
│   │   ├── graph.json              \# Layer graph metadata  
│   │   ├── body\_base.png           \# Layer images  
│   │   ├── gut\_region.png  
│   │   └── brain\_region.png  
│   └── speaker\_cutout\_001/  
│       ├── graph.json  
│       └── speaker.png  
│  
├── configs/                        \# Scene configurations  
│   ├── rating\_meter\_001.json  
│   └── body\_map\_focus\_001.json  
│  
├── rendered/                       \# Final outputs  
│   ├── rating\_meter\_001.mp4  
│   ├── rating\_meter\_001.meta.json  
│   ├── body\_map\_focus\_001.mp4  
│   └── pipeline\_20260104\_123456.json  
│  
├── temp/                           \# Intermediate files  
│   └── agent\_outputs/  
│       ├── context\_analyzer\_001.json  
│       └── layer\_extractor\_001.json  
│  
└── cache/                          \# Cached data  
    ├── layer\_graphs/               \# Reusable layer graphs  
    └── renders/                    \# Cached renders  
\`\`\`

\---

\#\# Environment Setup

\#\#\# \`.env.example\`  
\`\`\`bash  
\# Motion Cookbook Environment Variables

\# Paths  
MOTION\_COOKBOOK\_HOME=/path/to/motion-cookbook  
MOTION\_COOKBOOK\_DATA=/path/to/data  
MOTION\_COOKBOOK\_CACHE=/path/to/cache

\# API Keys (optional, for cloud models)  
QWEN\_API\_KEY=your\_key\_here  
ANTHROPIC\_API\_KEY=your\_key\_here

\# Rendering  
MOTION\_COOKBOOK\_WORKERS=4  
MOTION\_COOKBOOK\_RENDER\_TIMEOUT=90

\# Debug  
MOTION\_COOKBOOK\_DEBUG=false  
MOTION\_COOKBOOK\_LOG\_LEVEL=INFO  
\`\`\`

\---

\#\# Initialization Script

\`\`\`bash  
\#\!/bin/bash  
\# scripts/init.sh

echo "Initializing Motion Cookbook..."

\# Create directory structure  
mkdir \-p data/{input,assets,layer\_graphs,configs,rendered,temp,cache}  
mkdir \-p logs  
mkdir \-p config/brand\_kits

\# Copy default configs  
cp examples/brand\_kits/default\_brand.json config/brand\_kits/

\# Install Python dependencies  
pip install \-r requirements.txt

\# Install Node dependencies  
cd motion-canvas && npm install && cd ..

\# Verify setup  
python scripts/verify\_setup.py

echo "✅ Setup complete\!"  
\`\`\`

\---

\#\# .gitignore

\`\`\`gitignore  
\# Data (never commit user data)  
data/  
\!data/.gitkeep

\# Logs  
logs/  
\*.log

\# Temp files  
temp/  
\*.tmp

\# Cache  
cache/  
.cache/

\# Python  
\_\_pycache\_\_/  
\*.pyc  
\*.pyo  
\*.egg-info/  
.venv/  
venv/

\# Node  
node\_modules/  
.motion-canvas/  
dist/

\# Environment  
.env

\# OS  
.DS\_Store  
Thumbs.db  
\`\`\`

\---

\#\# Common File Paths Reference

\`\`\`python  
\# paths.py \- Centralized path management  
from pathlib import Path  
import os

PROJECT\_ROOT \= Path(\_\_file\_\_).parent.parent  
DATA\_DIR \= Path(os.getenv("MOTION\_COOKBOOK\_DATA", PROJECT\_ROOT / "data"))

PATHS \= {  
    "input": DATA\_DIR / "input",  
    "assets": DATA\_DIR / "assets",  
    "layer\_graphs": DATA\_DIR / "layer\_graphs",  
    "configs": DATA\_DIR / "configs",  
    "rendered": DATA\_DIR / "rendered",  
    "temp": DATA\_DIR / "temp",  
    "cache": DATA\_DIR / "cache",  
    "schemas": PROJECT\_ROOT / "schemas",  
    "scenes": PROJECT\_ROOT / "scenes" / "definitions",  
    "brand\_kits": PROJECT\_ROOT / "config" / "brand\_kits",  
    "logs": PROJECT\_ROOT / "logs",  
}

def ensure\_dirs():  
    """Create all required directories"""  
    for path in PATHS.values():  
        path.mkdir(parents=True, exist\_ok=True)  
\`\`\`

\---

\#\# Quick Navigation

\`\`\`bash  
\# Common commands from project root

\# Generate scenes  
python cli.py generate \--context data/input/example.json

\# Render single scene  
python cli.py render \--scene RATING\_METER\_1\_TO\_10 \--config data/configs/rating\_001.json

\# Run tests  
pytest tests/

\# View logs  
tail \-f logs/motion-cookbook.log

\# Clean temp files  
./scripts/cleanup.sh  
\`\`\`

\---

\*\*This structure supports:\*\*  
\- ✅ Clear separation of concerns  
\- ✅ Easy agent development  
\- ✅ Scalable data management  
\- ✅ Version control friendly  
\- ✅ CI/CD integration  
\- ✅ Multi-user workflows  
