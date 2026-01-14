# **quickstart.md**

\*\*Purpose:\*\* Get from zero to your first rendered scene in 10 minutes    
\*\*Status:\*\* Essential v1.0

\---

\#\# 1\. Prerequisites

\`\`\`bash  
\# System requirements  
\- Python 3.10+  
\- Node.js 18+  
\- FFmpeg  
\- 8GB RAM minimum

\# Install dependencies  
pip install \-r requirements.txt  
npm install  
\`\`\`

\---

\#\# 2\. Project Setup

\`\`\`bash  
\# Clone and setup  
git clone \<repo\>  
cd motion-cookbook

\# Initialize  
./scripts/init.sh  
\`\`\`

This creates:  
\`\`\`  
motion-cookbook/  
├── data/  
│   ├── assets/          \# Your images  
│   ├── layer\_graphs/    \# Generated layers  
│   └── rendered/        \# Output videos  
├── config/  
│   └── brand\_kit.json   \# Your brand settings  
└── temp/                \# Processing files  
\`\`\`

\---

\#\# 3\. Your First Scene (5 minutes)

\#\#\# Step 1: Create Context File

\`\`\`bash  
\# data/input/example\_context.json  
{  
  "script": "I'd say I'm at about a 7 right now in terms of confidence",  
  "topic": "confidence\_check\_in",  
  "target\_scene": "RATING\_METER\_1\_TO\_10"  
}  
\`\`\`

\#\#\# Step 2: Add an Asset (Optional)

\`\`\`bash  
\# If you have a speaker cutout:  
cp your\_speaker.png data/assets/speaker\_001.png  
\`\`\`

\#\#\# Step 3: Run the Pipeline

\`\`\`bash  
python cli.py generate \\  
  \--context data/input/example\_context.json \\  
  \--output data/rendered/  
\`\`\`

\#\#\# Step 4: Check Output

\`\`\`bash  
\# Scene will be at:  
\# data/rendered/rating\_meter\_001.mp4

open data/rendered/rating\_meter\_001.mp4  
\`\`\`

\---

\#\# 4\. What Just Happened?

The system:

1\. \*\*Analyzed context\*\* → Detected rating (7/10)  
2\. \*\*Selected scene\*\* → RATING\_METER\_1\_TO\_10  
3\. \*\*Extracted parameters\*\* → value=7, label="Confidence"  
4\. \*\*Rendered with Motion Canvas\*\* → Animated meter  
5\. \*\*Encoded video\*\* → Final MP4

All automatically.

\---

\#\# 5\. Customize with Brand Kit

\`\`\`bash  
\# config/brand\_kit.json  
{  
  "brand\_id": "my\_brand",  
  "colors": {  
    "primary": "\#FF6B6B",  
    "secondary": "\#4ECDC4",  
    "accent": "\#FFE66D"  
  },  
  "fonts": {  
    "headline": "Inter-Bold",  
    "body": "Inter-Regular"  
  }  
}  
\`\`\`

Then regenerate:  
\`\`\`bash  
python cli.py generate \\  
  \--context data/input/example\_context.json \\  
  \--brand config/brand\_kit.json \\  
  \--output data/rendered/  
\`\`\`

\---

\#\# 6\. Manual Scene Selection

\`\`\`bash  
\# Force a specific scene  
python cli.py render \\  
  \--scene BODY\_MAP\_FOCUS \\  
  \--config data/configs/body\_map\_example.json \\  
  \--output data/rendered/  
\`\`\`

\---

\#\# 7\. Batch Processing

\`\`\`bash  
\# Process multiple contexts  
python cli.py batch \\  
  \--input-dir data/input/ \\  
  \--output-dir data/rendered/ \\  
  \--parallel 4  
\`\`\`

\---

\#\# 8\. View Available Scenes

\`\`\`bash  
python cli.py list-scenes

\# Output:  
\# Available Scenes:  
\# \- RATING\_METER\_1\_TO\_10 (Response & Progress)  
\# \- BEFORE\_AFTER\_SELF\_SCORE (Response & Progress)  
\# \- BODY\_MAP\_FOCUS (Explainer)  
\# \- CUTOUT\_METAPHOR (Storytelling)  
\# ...  
\`\`\`

\---

\#\# 9\. Debug Mode

\`\`\`bash  
\# See what the agents are doing  
python cli.py generate \\  
  \--context data/input/example\_context.json \\  
  \--debug \\  
  \--verbose  
\`\`\`

This shows:  
\- Agent outputs  
\- Layer extraction results  
\- Scene parameter resolution  
\- Render logs

\---

\#\# 10\. Common First Issues

\#\#\# "No suitable scene found"  
\*\*Fix:\*\* Be more explicit in context  
\`\`\`json  
{  
  "script": "...",  
  "intent": "explain",  // Add this  
  "suggested\_scenes": \["BODY\_MAP\_FOCUS"\]  // Or this  
}  
\`\`\`

\#\#\# "Layer extraction failed"  
\*\*Fix:\*\* Provide cleaner source images or use manual layers  
\`\`\`bash  
python cli.py generate \\  
  \--context data/input/example\_context.json \\  
  \--skip-layer-extraction \\  
  \--manual-layers data/layers/manual/  
\`\`\`

\#\#\# "Render timeout"  
\*\*Fix:\*\* Increase timeout or use simpler scene  
\`\`\`bash  
python cli.py generate \\  
  \--context data/input/example\_context.json \\  
  \--render-timeout 120  
\`\`\`

\---

\#\# 11\. Next Steps

Once you have your first render:

1\. \*\*Explore scenes:\*\* Try different scene types  
2\. \*\*Add assets:\*\* Upload your own images  
3\. \*\*Customize brands:\*\* Create brand kits  
4\. \*\*Batch process:\*\* Generate multiple scenes  
5\. \*\*Read advanced docs:\*\* Check \`cli\_reference.md\`

\---

\#\# 12\. Getting Help

\`\`\`bash  
\# CLI help  
python cli.py \--help  
python cli.py generate \--help

\# Check logs  
tail \-f logs/motion-cookbook.log

\# Test installation  
python cli.py test  
\`\`\`

\---

\#\# 13\. Example Context Library

The system includes example contexts:

\`\`\`bash  
ls examples/contexts/  
\# rating\_example.json  
\# body\_map\_example.json  
\# before\_after\_example.json  
\# quote\_example.json  
\`\`\`

Try them:  
\`\`\`bash  
python cli.py generate \\  
  \--context examples/contexts/rating\_example.json  
\`\`\`

\---

\#\# 14\. Minimal Working Example

\*\*Absolute minimum to render a scene:\*\*

\`\`\`bash  
\# 1\. Create simple context  
echo '{  
  "script": "I feel great today",  
  "rating": 8  
}' \> test.json

\# 2\. Render  
python cli.py generate \--context test.json

\# Done. Check data/rendered/  
\`\`\`

\---

\#\# 15\. Verify Installation

\`\`\`bash  
python scripts/verify\_setup.py  
\`\`\`

This checks:  
\- ✅ Python dependencies  
\- ✅ Node.js and Motion Canvas  
\- ✅ FFmpeg  
\- ✅ File structure  
\- ✅ Example scenes render

\---

\*\*You're ready to generate scenes\!\*\*

For advanced usage, see \`cli\_reference.md\`    
For troubleshooting, see \`troubleshooting.md\`    
For extending, see \`extending\_scenes.md\`  
