### **`config.yaml` (The Session Truth)**

This is the master configuration file. It stores the paths to your intelligence assets, defines which models to use, and sets the thresholds for the automated procurement engine (like the Authenticity Score

\# \============================================================================  
\# CMF MASTER CONFIGURATION (v3.0 \- Raw-to-Edit Edition)  
\# \============================================================================  
\# This file serves as the "Session Truth" for all agents.  
\# It defines file paths, model selection, and production thresholds.  
\# \============================================================================

\# 1\. CLIENT IDENTITY (Inherited from CCF)  
\# These fields should be updated per project or linked to CCF output  
client:  
  name: "Sarah Chen"                   
  industry: "Real Estate"  
  voice\_baseline: "TTT-03"         \# From CCF Soul  
  brand\_colors: \["\#1A1A1A", "\#C0A15E"\] \# Primary/Accent

\# 2\. FILE PATHS (The Nervous System)  
\# Absolute or relative paths to critical system assets  
paths:  
  root: "\~/cmf"  
    
  \# Inputs (Raw Material)  
  ccf\_client\_soul: "\~/ccf/output/setup/03\_client\_soul.json"  
  ccf\_tribe\_soul: "\~/ccf/output/setup/04\_tribe\_soul.json"  
  raw\_video\_source: "\~/cmf/inputs/raw\_video/source\_master.mp4" \# Default source file  
  transcripts\_dir: "\~/cmf/inputs/transcripts/"  
    
  \# Tools (The Mechanical Room)  
  tools\_dir: "\~/cmf/tools"  
  cutter\_script: "\~/cmf/tools/execute\_cuts.py"  
  xml\_script: "\~/cmf/tools/xml\_generator.py"  
    
  \# Intelligence Assets (The Brain)  
  viral\_scoring: "\~/cmf/intelligence/frameworks/viral\_trinity\_scoring.yaml"  
  sonic\_arcs: "\~/cmf/intelligence/frameworks/sonic\_story\_arcs.yaml"  
  scene\_library: "\~/cmf/intelligence/frameworks/scene\_builder\_library.yaml"  
  visual\_recipes: "\~/cmf/intelligence/frameworks/visual\_hooks\_recipes.yaml"  
  master\_effects: "\~/cmf/intelligence/frameworks/master\_effects.yaml"

\# 3\. AI MODELS (The Engines)  
models:  
  reasoning: "gemini-3-pro-preview" \# For Premise Hunter & Architect (Logic)  
  creative: "gemini-3-pro-preview"  \# For Script Composer (Voice/Flow)  
  vision: "gemini-pro-vision"       \# For Asset Filtering & Authenticity Checks  
  generation: "midjourney-v6"       \# For A-Roll Prompts (Reference only)

\# 4\. PROCUREMENT & CUTTING SETTINGS  
procurement:  
  d\_roll\_threshold: 8.0            \# Minimum Authenticity Score (0-10) to download a clip  
  max\_search\_results: 20           \# Number of images to scan per scene request  
  enable\_vision\_filter: true       \# Use Gemini Vision to score thumbnails

cutting:  
  ffmpeg\_path: "/usr/bin/ffmpeg"   \# Path to FFmpeg binary  
  audio\_sample\_rate: "48000"       \# Standard for video editing  
  video\_codec: "libx264"           \# Standard H.264  
  output\_format: "mp4"

\# 5\. FEATURE FLAGS  
features:  
  force\_verbatim\_mode: true        \# STRICTLY forbids AI from inventing script text  
  enable\_auto\_cut: true            \# Enables the FFmpeg slicing module  
  enable\_voice\_cloning: true       \# Enables Ad-Libber to request voice clones  
  generate\_xml\_timeline: true      \# Auto-generate .xml for DaVinci Resolve

\# 6\. API KEYS (Environment Variable References)  
api\_keys:  
  \# Keys should be set in your .env file, referenced here  
  gemini\_api\_key: "${GEMINI\_API\_KEY}"  
  pexels\_api\_key: "${PEXELS\_API\_KEY}" \# Optional: For stock hunting  
