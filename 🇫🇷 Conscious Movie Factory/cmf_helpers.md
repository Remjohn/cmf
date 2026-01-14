`cmf_helpers.sh` (The Safety Layer)

\#\!/bin/bash

\# \==============================================================================  
\# CMF SAFETY LAYER (v3.0 \- Video Production Edition)  
\# Handles Context Loading, Output Sanitization, Atomic Writes, and Execution  
\# \==============================================================================

\# 1\. SMART CONTEXT LOADER  
\# Prevents "Context Explosion" by only loading what is needed for the specific production phase.  
build\_cmf\_context() {  
    local phase="$1"  
    local pid="$2" \# Project ID (e.g., "project\_001")

    \# \--- GLOBAL CONTEXT \---  
    echo "--- SYSTEM IDENTITY \---"  
    echo "You are operating within the Conscious Movie Factory (CMF) v3.0."  
    echo \-e "\\n"  
      
    echo "--- CONFIGURATION \---"  
    cat \~/cmf/config.yaml  
    echo \-e "\\n"

    \# \--- PHASE-SPECIFIC CONTEXT \---  
    case "$phase" in  
        "hunter")  
            \# Context: Raw Data \+ Scoring Logic (The Premise Hunter)  
            echo "--- TRIBE SOUL \---"  
            cat $(yq '.paths.ccf\_tribe\_soul' \~/cmf/config.yaml)  
            echo "--- SCORING RUBRIC \---"  
            cat \~/cmf/intelligence/frameworks/viral\_trinity\_scoring.yaml  
            echo "--- RAW TRANSCRIPT \---"  
            \# Looks for transcript matching project ID  
            cat \~/cmf/inputs/transcripts/"$pid".txt 2\>/dev/null || echo "ERROR: Transcript not found."  
            ;;  
              
        "composer")  
            \# Context: The Winning Idea (The Script Composer)  
            echo "--- PREMISE ANALYSIS \---"  
            cat \~/cmf/output/"$pid"/01\_narrative/premise\_analysis.json  
            ;;  
              
        "architect")  
            \# Context: The Script \+ Production Constraints (The Blueprint Architect)  
            echo "--- FINAL SCRIPT \---"  
            cat \~/cmf/output/"$pid"/01\_narrative/final\_script.json  
            echo "--- SCENE LIBRARY \---"  
            cat \~/cmf/intelligence/frameworks/scene\_builder\_library.yaml  
            echo "--- SONIC ARCS \---"  
            cat \~/cmf/intelligence/frameworks/sonic\_story\_arcs.yaml  
            ;;

        "sonic")  
            \# Context: Blueprint \+ Cultural Data (Sonic Sommelier & Scribe)  
            echo "--- PRODUCTION BLUEPRINT \---"  
            cat \~/cmf/output/"$pid"/01\_narrative/production\_blueprint.json  
            echo "--- TRIBE SOUL \---"  
            cat $(yq '.paths.ccf\_tribe\_soul' \~/cmf/config.yaml)  
            echo "--- SONIC ARCS \---"  
            cat \~/cmf/intelligence/frameworks/sonic\_story\_arcs.yaml  
            ;;

        "visual")  
            \# Context: Blueprint \+ Visual Recipes \+ Avatar (Virtual Director)  
            echo "--- PRODUCTION BLUEPRINT \---"  
            cat \~/cmf/output/"$pid"/01\_narrative/production\_blueprint.json  
            echo "--- VISUAL RECIPES \---"  
            cat \~/cmf/intelligence/frameworks/visual\_hooks\_recipes.yaml  
            echo "--- BRAND AVATAR \---"  
            cat \~/cmf/output/"$pid"/03\_storyboard/brand\_avatar.json 2\>/dev/null || echo "{}"  
            ;;

        "cutter")  
            \# Context: Timestamps \+ Video Specs (The Cutter)  
            \# CRITICAL: This agent needs MINIMAL context to avoid hallucinating timestamps.  
            echo "--- FINAL SCRIPT \---"  
            cat \~/cmf/output/"$pid"/01\_narrative/final\_script.json  
            echo "--- RAW VIDEO METADATA \---"  
            \# In a real pipeline, this would pull from ffprobe. For now, we echo the path.  
            echo "Source File: $(yq '.paths.raw\_video\_source' \~/cmf/config.yaml)"  
            ;;  
              
        "assembly")  
            \# Context: Asset Manifests (Post-Super)  
            echo "--- PRODUCTION BLUEPRINT \---"  
            cat \~/cmf/output/"$pid"/01\_narrative/production\_blueprint.json  
            echo "--- ASSET DIRECTORY STRUCTURE \---"  
            ls \-R \~/cmf/output/"$pid"/04\_assets/  
            ;;

        \*)  
            echo "Unknown phase context: $phase" \>&2  
            return 1  
            ;;  
    esac  
}

\# 2\. ATOMIC JSON SAVER  
\# Prevents corrupted files and handles Markdown backticks common in LLM output  
save\_json\_safe() {  
    local raw\_input="$1"  
    local target\_path="$2"  
      
    \# Extract JSON content between \`\`\`json and \`\`\` blocks if they exist  
    local clean\_json=$(echo "$raw\_input" | sed \-n '/^\`\`\`json/,/^\`\`\`/p' | sed '1d;$d')  
      
    if \[ \-z "$clean\_json" \]; then  
        \# Fallback: Try to find start/end brackets if no markdown blocks  
        clean\_json=$(echo "$raw\_input" | sed \-n '/^{/,/^}/p')  
    fi

    \# VALIDATION: Check if valid JSON using python one-liner  
    echo "$clean\_json" | python3 \-c "import sys, json; json.load(sys.stdin)" 2\>/dev/null  
      
    if \[ $? \-eq 0 \]; then  
        \# Atomic Write strategy to prevent data corruption  
        mkdir \-p "$(dirname "$target\_path")"  
        echo "$clean\_json" \> "${target\_path}.tmp"  
        mv "${target\_path}.tmp" "$target\_path"  
        echo "✅ SUCCESS: Saved valid JSON to $target\_path"  
    else  
        echo "❌ ERROR: Agent generated invalid JSON. Raw content saved to error.log"  
        echo "$raw\_input" \> \~/cmf/logs/error\_$(date \+%s).log  
        return 1  
    fi  
}

\# 3\. AGENT EXECUTOR  
\# The main wrapper function  
run\_cmf\_agent() {  
    local agent\_file="$1"  
    local context\_phase="$2"  
    local project\_id="$3"  
    local output\_file="$4"  
      
    echo "🤖 Activating Agent: $agent\_file for Project: $project\_id..."  
      
    \# Build Context  
    local context=$(build\_cmf\_context "$context\_phase" "$project\_id")  
      
    if \[ \-z "$context" \]; then  
        echo "❌ Context build failed."  
        return 1  
    fi

    \# Execute Gemini (using CLI tool)  
    \# Note: Assumes 'gemini' command is configured in PATH  
    local result=$(gemini \-m gemini-3-pro-preview \\  
        \--system "$(cat "$agent\_file")" \\  
        \--context "$context" \\  
        "EXECUTE PROTOCOL based on the provided context. Return ONLY the JSON output.")  
              
    \# Save Safely  
    save\_json\_safe "$result" "$output\_file"  
}

\# \==============================================================================  
\# COMMAND SHORTCUTS (ALIASES)  
\# \==============================================================================

\# Initialize Project  
alias cmf-init='\~/cmf/tools/init\_project.sh' \# Requires creation of init script

\# Phase 1: Narrative  
alias cmf-premise='run\_cmf\_agent "\~/cmf/agents/extraction/premise\_hunter.md" "hunter"'  
alias cmf-compose='run\_cmf\_agent "\~/cmf/agents/extraction/script\_composer.md" "composer"'  
alias cmf-blueprint='run\_cmf\_agent "\~/cmf/agents/\_master/blueprint\_architect.md" "architect"'

\# Phase 2: Sonic  
alias cmf-sonic='run\_cmf\_agent "\~/cmf/agents/sonic/sommelier.md" "sonic"'

\# Phase 3: Visual  
alias cmf-visual='run\_cmf\_agent "\~/cmf/agents/visual/virtual\_director.md" "visual"'

\# Phase 4: Procurement (The Hands)  
alias cmf-cut='run\_cmf\_agent "\~/cmf/agents/procurement/cutter.md" "cutter"'  
\# Note: cmf-hunt requires the specialized Python vision script, not just LLM generation.

\# Phase 5: Assembly  
alias cmf-assemble='run\_cmf\_agent "\~/cmf/agents/\_master/post\_super.md" "assembly"'

echo "🎬 CMF Safety Layer Active. Ready for production."  
