# **troubleshooting.md**

\*\*Purpose:\*\* Common issues and solutions    
\*\*Status:\*\* Living document v1.0

\---

\#\# Installation & Setup Issues

\#\#\# Issue: \`motion-canvas: command not found\`

\*\*Symptom:\*\*  
\`\`\`bash  
$ npm run render  
motion-canvas: command not found  
\`\`\`

\*\*Cause:\*\* Motion Canvas not installed

\*\*Solution:\*\*  
\`\`\`bash  
cd motion-canvas  
npm install  
npm install \-g @motion-canvas/cli  \# Optional global install  
\`\`\`

\---

\#\#\# Issue: Python dependencies fail to install

\*\*Symptom:\*\*  
\`\`\`bash  
ERROR: Could not find a version that satisfies requirement X  
\`\`\`

\*\*Solution:\*\*  
\`\`\`bash  
\# Use Python 3.10+  
python \--version  \# Check version

\# Create virtual environment  
python \-m venv venv  
source venv/bin/activate  \# or \`venv\\Scripts\\activate\` on Windows

\# Install dependencies  
pip install \--upgrade pip  
pip install \-r requirements.txt  
\`\`\`

\---

\#\#\# Issue: FFmpeg not found

\*\*Symptom:\*\*  
\`\`\`bash  
RuntimeError: FFmpeg not found in system PATH  
\`\`\`

\*\*Solution:\*\*

\*\*macOS:\*\*  
\`\`\`bash  
brew install ffmpeg  
\`\`\`

\*\*Ubuntu/Debian:\*\*  
\`\`\`bash  
sudo apt update  
sudo apt install ffmpeg  
\`\`\`

\*\*Windows:\*\*  
Download from https://ffmpeg.org and add to PATH

\*\*Verify:\*\*  
\`\`\`bash  
ffmpeg \-version  
\`\`\`

\---

\#\# Agent Pipeline Issues

\#\#\# Issue: "Agent validation failed"

\*\*Symptom:\*\*  
\`\`\`json  
{  
  "error": "Schema validation failed",  
  "agent\_id": "ContextAnalyzer"  
}  
\`\`\`

\*\*Cause:\*\* Agent output doesn't match expected schema

\*\*Solution:\*\*  
\`\`\`bash  
\# Validate agent output manually  
python cli.py validate agent-output \\  
  \--agent ContextAnalyzer \\  
  \--file data/temp/analyzed.json

\# Check logs  
tail \-f logs/motion-cookbook.log  
\`\`\`

\*\*Fix:\*\* Update agent to match schema in \`schemas/agent\_io/\`

\---

\#\#\# Issue: "No suitable scene found"

\*\*Symptom:\*\*  
\`\`\`json  
{  
  "selected\_scenes": \[\]  
}  
\`\`\`

\*\*Cause:\*\* Context doesn't match any scene criteria

\*\*Solution:\*\*  
\`\`\`bash  
\# Be more explicit in context  
cat \<\< EOF \> data/input/explicit.json  
{  
  "script": "I'm at a 7",  
  "intent": "social\_proof",  
  "suggested\_scenes": \["RATING\_METER\_1\_TO\_10"\]  
}  
EOF

\# Or force scenes  
python cli.py generate \\  
  \--context data/input/example.json \\  
  \--force-scenes RATING\_METER\_1\_TO\_10  
\`\`\`

\---

\#\#\# Issue: Agent timeout

\*\*Symptom:\*\*  
\`\`\`  
subprocess.TimeoutExpired: Command timed out after 60 seconds  
\`\`\`

\*\*Cause:\*\* Agent taking too long (usually image generation or layer extraction)

\*\*Solution:\*\*  
\`\`\`bash  
\# Increase timeout  
python cli.py generate \\  
  \--context data/input/example.json \\  
  \--agent-timeout 120

\# Or skip slow agents  
python cli.py generate \\  
  \--context data/input/example.json \\  
  \--skip-layer-extraction  
\`\`\`

\---

\#\# Layer Extraction Issues

\#\#\# Issue: "Layer extraction failed"

\*\*Symptom:\*\*  
\`\`\`json  
{  
  "error": "LAYER\_EXTRACTION\_FAILED",  
  "agent\_id": "LayerExtractor"  
}  
\`\`\`

\*\*Cause:\*\* Image too complex or API failure

\*\*Solution 1:\*\* Use simpler images  
\`\`\`bash  
\# Provide pre-segmented layers manually  
mkdir \-p data/layer\_graphs/manual\_001  
\# Place layers: layer\_001.png, layer\_002.png, etc.

python cli.py generate \\  
  \--context data/input/example.json \\  
  \--manual-layers data/layer\_graphs/manual\_001/  
\`\`\`

\*\*Solution 2:\*\* Try different extraction method  
\`\`\`bash  
\# In context.json  
{  
  "script": "...",  
  "layer\_extraction\_method": "sam3"  // or "qwen" or "manual"  
}  
\`\`\`

\---

\#\#\# Issue: "Low confidence semantic labels"

\*\*Symptom:\*\*  
\`\`\`json  
{  
  "warning": "Semantic labeling confidence below threshold",  
  "confidence": 0.42  
}  
\`\`\`

\*\*Cause:\*\* AI can't reliably label image regions

\*\*Solution:\*\*  
\`\`\`bash  
\# Provide semantic hints in context  
{  
  "script": "...",  
  "assets": \["data/assets/body\_diagram.png"\],  
  "semantic\_hints": {  
    "body\_diagram.png": {  
      "regions": \["gut", "brain", "heart"\]  
    }  
  }  
}  
\`\`\`

\---

\#\# Rendering Issues

\#\#\# Issue: Motion Canvas render timeout

\*\*Symptom:\*\*  
\`\`\`  
RuntimeError: Render failed \- timeout after 90s  
\`\`\`

\*\*Cause:\*\* Complex scene taking too long

\*\*Solution:\*\*  
\`\`\`bash  
\# Increase render timeout  
python cli.py render \\  
  \--scene BODY\_MAP\_FOCUS \\  
  \--config data/configs/body\_001.json \\  
  \--render-timeout 180

\# Or generate preview  
python cli.py render \\  
  \--scene BODY\_MAP\_FOCUS \\  
  \--config data/configs/body\_001.json \\  
  \--preview  \# Lower resolution, faster  
\`\`\`

\---

\#\#\# Issue: "Scene configuration invalid"

\*\*Symptom:\*\*  
\`\`\`  
Error: required parameter 'rating\_value' missing  
\`\`\`

\*\*Cause:\*\* Scene config doesn't have all required parameters

\*\*Solution:\*\*  
\`\`\`bash  
\# Validate config before rendering  
python cli.py validate scene-config \\  
  \--file data/configs/rating\_001.json

\# Check scene requirements  
python cli.py scenes info \--scene RATING\_METER\_1\_TO\_10  
\`\`\`

\---

\#\#\# Issue: Rendered video is blank/black

\*\*Cause:\*\* Asset paths incorrect or brand kit missing

\*\*Debug:\*\*  
\`\`\`bash  
\# Check Motion Canvas logs  
cat motion-canvas/.motion-canvas/output.log

\# Verify assets exist  
ls data/layer\_graphs/{graph\_id}/\*.png

\# Check environment variables  
echo $SCENE\_CONFIG\_PATH  
echo $DATA\_DIR  
\`\`\`

\*\*Solution:\*\*  
\`\`\`bash  
\# Use absolute paths in config  
{  
  "parameters": {  
    "asset\_path": "/full/path/to/asset.png"  
  }  
}

\# Or ensure relative paths resolve correctly  
\`\`\`

\---

\#\#\# Issue: "Brand kit not found"

\*\*Symptom:\*\*  
\`\`\`  
Error: Brand kit 'my\_brand' does not exist  
\`\`\`

\*\*Solution:\*\*  
\`\`\`bash  
\# List available brand kits  
ls config/brand\_kits/

\# Create missing brand kit  
python cli.py brand create \\  
  \--name my\_brand \\  
  \--output config/brand\_kits/my\_brand.json

\# Or use default  
python cli.py generate \\  
  \--context data/input/example.json \\  
  \--brand config/brand\_kits/default\_brand.json  
\`\`\`

\---

\#\# Performance Issues

\#\#\# Issue: Pipeline very slow

\*\*Symptoms:\*\*  
\- Takes \>5 minutes for single scene  
\- High CPU usage  
\- Memory exhaustion

\*\*Solutions:\*\*

\*\*1. Enable parallel processing:\*\*  
\`\`\`bash  
python cli.py generate \\  
  \--context data/input/example.json \\  
  \--parallel 4  
\`\`\`

\*\*2. Use caching:\*\*  
\`\`\`bash  
\# Layer graphs are cached by default  
\# Check cache hit rate  
python cli.py cache stats  
\`\`\`

\*\*3. Skip expensive operations:\*\*  
\`\`\`bash  
python cli.py generate \\  
  \--context data/input/example.json \\  
  \--skip-layer-extraction \\  \# If not needed  
  \--skip-speech-analysis     \# If not needed  
\`\`\`

\*\*4. Lower resolution for testing:\*\*  
\`\`\`bash  
python cli.py render \\  
  \--scene BODY\_MAP\_FOCUS \\  
  \--config data/configs/body\_001.json \\  
  \--preview  \# 540p instead of 1080p  
\`\`\`

\---

\#\#\# Issue: Out of memory

\*\*Symptom:\*\*  
\`\`\`  
MemoryError: Unable to allocate array  
\`\`\`

\*\*Solutions:\*\*

\*\*1. Render scenes sequentially:\*\*  
\`\`\`bash  
python cli.py generate \\  
  \--context data/input/example.json \\  
  \--parallel 1  \# No parallelism  
\`\`\`

\*\*2. Clear cache between renders:\*\*  
\`\`\`bash  
python cli.py cache clear \--type temp  
\`\`\`

\*\*3. Reduce image sizes:\*\*  
\`\`\`bash  
\# Pre-process images to max 2048px  
convert large\_image.png \-resize 2048x2048\\\> resized.png  
\`\`\`

\---

\#\# File & Permission Issues

\#\#\# Issue: "Permission denied"

\*\*Symptom:\*\*  
\`\`\`bash  
PermissionError: \[Errno 13\] Permission denied: 'data/rendered/scene.mp4'  
\`\`\`

\*\*Solution:\*\*  
\`\`\`bash  
\# Check permissions  
ls \-la data/rendered/

\# Fix permissions  
chmod \-R u+rwX data/

\# Check if file is in use  
lsof data/rendered/scene.mp4  \# macOS/Linux  
\`\`\`

\---

\#\#\# Issue: "Directory not found"

\*\*Symptom:\*\*  
\`\`\`  
FileNotFoundError: \[Errno 2\] No such file or directory: 'data/layer\_graphs'  
\`\`\`

\*\*Solution:\*\*  
\`\`\`bash  
\# Initialize project structure  
./scripts/init.sh

\# Or manually create directories  
mkdir \-p data/{input,assets,layer\_graphs,configs,rendered,temp,cache}  
\`\`\`

\---

\#\# Configuration Issues

\#\#\# Issue: Environment variables not working

\*\*Symptom:\*\*  
Settings not being recognized

\*\*Solution:\*\*  
\`\`\`bash  
\# Create .env file  
cp .env.example .env

\# Edit .env  
MOTION\_COOKBOOK\_HOME=/path/to/project  
MOTION\_COOKBOOK\_WORKERS=4

\# Load environment  
export $(cat .env | xargs)

\# Or pass explicitly  
MOTION\_COOKBOOK\_WORKERS=8 python cli.py generate ...  
\`\`\`

\---

\#\#\# Issue: "Config file invalid"

\*\*Symptom:\*\*  
\`\`\`  
json.decoder.JSONDecodeError: Expecting property name  
\`\`\`

\*\*Solution:\*\*  
\`\`\`bash  
\# Validate JSON syntax  
python \-m json.tool data/input/example.json

\# Use schema validator  
python cli.py validate context \--file data/input/example.json  
\`\`\`

\---

\#\# Debugging Strategies

\#\#\# Enable Debug Mode

\`\`\`bash  
python cli.py generate \\  
  \--context data/input/example.json \\  
  \--debug \\  
  \--verbose  
\`\`\`

This shows:  
\- Agent inputs/outputs  
\- Timing information  
\- Validation results  
\- Render logs

\---

\#\#\# Save Intermediate Files

\`\`\`bash  
\# Keep temp files for inspection  
python cli.py generate \\  
  \--context data/input/example.json \\  
  \--keep-temp  
\`\`\`

\---

\#\#\# Test Individual Agents

\`\`\`bash  
\# Test single agent  
echo '{"script": "test"}' | python agents/context\_analyzer.py

\# Or use CLI  
python cli.py agents step \\  
  \--agent ContextAnalyzer \\  
  \--input data/input/example.json \\  
  \--output data/temp/test.json  
\`\`\`

\---

\#\#\# Verify Setup

\`\`\`bash  
\# Run full system test  
python cli.py test all

\# Or check specific components  
python cli.py test install  \# Dependencies  
python cli.py test agents   \# All agents  
python cli.py test scenes   \# Scene rendering  
\`\`\`

\---

\#\# Getting Help

\#\#\# Check Logs

\`\`\`bash  
\# Main log  
tail \-f logs/motion-cookbook.log

\# Agent logs  
ls logs/agents/

\# Motion Canvas logs  
cat motion-canvas/.motion-canvas/output.log  
\`\`\`

\---

\#\#\# Generate Debug Report

\`\`\`bash  
python cli.py debug-report \\  
  \--output debug\_report.json  
\`\`\`

This includes:  
\- System info  
\- Installed versions  
\- Recent errors  
\- Configuration

\---

\#\#\# Common Error Codes

| Code | Meaning | Action |  
|------|---------|--------|  
| 1 | General error | Check logs |  
| 2 | Invalid input | Validate JSON |  
| 3 | Validation failed | Check schemas |  
| 4 | Render failed | Check Motion Canvas |  
| 5 | Agent failed | Check agent logs |  
| 10 | Timeout | Increase timeout |

\---

\#\# Still Stuck?

1\. \*\*Check logs:\*\* \`logs/motion-cookbook.log\`  
2\. \*\*Validate inputs:\*\* \`python cli.py validate ...\`  
3\. \*\*Test components:\*\* \`python cli.py test ...\`  
4\. \*\*Enable debug:\*\* \`--debug \--verbose\`  
5\. \*\*Check examples:\*\* \`examples/\` directory

\---

\*\*Most issues are configuration or environment-related, not code bugs.\*\*  
