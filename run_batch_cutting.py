import os
import json
import re
import subprocess
from pathlib import Path
import glob

# Configuration
WORKSPACE_ROOT = r"d:\Work\The Conscious Movie Factory December"
INPUTS_DIR = os.path.join(WORKSPACE_ROOT, "🇫🇷 Conscious Movie Factory", "inputs", "Coach Adele")

def parse_timecode(tc):
    """Convert MM:SS or HH:MM:SS to seconds."""
    if not tc: return 0.0
    tc = tc.replace('[', '').replace(']', '')
    parts = tc.split(':')
    try:
        if len(parts) == 2:
            return int(parts[0]) * 60 + float(parts[1])
        elif len(parts) == 3:
            return int(parts[0]) * 3600 + int(parts[1]) * 60 + float(parts[2])
    except ValueError:
        pass
    return 0.0

def parse_transcript(transcript_path):
    """
    Parses transcript markdown into list of dicts:
    {'start': float, 'text': "content...", 'end': float (next line start)}
    """
    segments = []
    with open(transcript_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    # Regex for \[MM:SS\]
    tc_pattern = re.compile(r'\\\[(\d+:\d+)\\\]') 
    # Note: The file uses \[MM:SS\] escaped brackets based on previous view
    # Let's verify the pattern from the file view: "\[0:09\] Super."
    
    for i, line in enumerate(lines):
        match = tc_pattern.search(line)
        if match:
            tc_str = match.group(1)
            start_sec = parse_timecode(tc_str)
            text_content = line[match.end():].strip()
            
            # Look ahead for next timecode to define 'end' (duration)
            end_sec = start_sec + 5.0 # Default 5s duration if end not found
            
            # Find next valid timecode
            for j in range(i + 1, len(lines)):
                next_match = tc_pattern.search(lines[j])
                if next_match:
                    end_sec = parse_timecode(next_match.group(1))
                    break
            
            segments.append({
                'start': start_sec,
                'end': end_sec,
                'text': text_content,
                'full_line': line
            })
            
    return segments

def normalize_text(text):
    """Remove unwanted chars for matching."""
    return re.sub(r'[^\w\s]', '', text.lower()).replace('\n', ' ').strip()

def find_quote_times(quote_text, transcript_segments):
    """
    Finds start and end time of a quote in the transcript.
    Matches sequences of words.
    """
    norm_quote = normalize_text(quote_text)
    if not norm_quote: return None, None
    
    # We scramble through segments to find the starting segment
    # This is a naive heuristic: find the segment that contains the start of the quote
    # Detailed match needed because quote might span multiple segments
    
    start_time = None
    end_time = None
    
    # Try to find the first chunk of the quote
    quote_words = norm_quote.split()
    if not quote_words: return None, None
    
    # Sliding window or start-of-string search
    # Let's search for the first 5 words
    search_phrase = " ".join(quote_words[:5])
    if len(quote_words) < 5: search_phrase = " ".join(quote_words)
    
    matched_start_idx = -1
    
    for idx, seg in enumerate(transcript_segments):
        norm_seg = normalize_text(seg['text'])
        if search_phrase in norm_seg:
            start_time = seg['start']
            matched_start_idx = idx
            break
            
    if start_time is None:
        print(f"      ⚠️ Couln't find start: '{search_phrase}...'")
        return None, None
        
    # Now find the end
    # We look from the start segment onwards for the last words
    search_end_phrase = " ".join(quote_words[-5:])
    if len(quote_words) < 5: search_end_phrase = " ".join(quote_words)
    
    current_acc_text = ""
    for i in range(matched_start_idx, len(transcript_segments)):
        seg = transcript_segments[i]
        norm_seg = normalize_text(seg['text'])
        
        # Check if the END matches here
        if search_end_phrase in norm_seg:
             end_time = seg['end']
             break
        
        # Safety: don't look too far (e.g. 2 minutes)
        if seg['start'] - start_time > 120:
            break
            
    if end_time is None:
        # Fallback: assume 10 seconds or single segment
        end_time = transcript_segments[matched_start_idx]['end']
        print(f"      ⚠️ Couldn't find end: '...{search_end_phrase}'. Using segment end.")

    return start_time, end_time

def cut_clip(source_video, start, end, output_path):
    """Cuts video using ffmpeg with afade."""
    duration = end - start
    if duration < 0.5: duration = 0.5 # Min duration
    
    # Filters: Fade in/out audio (5ms) to prevent clicks
    # video is untouched (stream copy not possible if we want accurate cuts, so we re-encode fast)
    
    cmd = [
        "ffmpeg", "-y", "-hide_banner", "-loglevel", "error",
        "-ss", str(start),
        "-i", source_video,
        "-t", str(duration),
        "-c:v", "libx264", "-preset", "fast", "-crf", "22",
        "-af", "afade=t=in:st=0:d=0.01,afade=t=out:st={}:d=0.01".format(duration-0.01),
        "-c:a", "aac", "-b:a", "192k",
        output_path
    ]
    
    subprocess.run(cmd, check=False)
    # Check if file exists to confirm
    return os.path.exists(output_path)

def main():
    print("✂️ Starting Batch Cutter Agent")
    
    projects = [d for d in Path(INPUTS_DIR).iterdir() if d.is_dir()]
    
    for proj in projects:
        proj_name = proj.name
        print(f"\n📂 Project: {proj_name}")
        
        # 1. Find Source Video
        videos = list(proj.glob("*fullVideo*.mp4"))
        if not videos:
            print("    ❌ No '*fullVideo*.mp4' found inside project.")
            continue
        source_video = str(videos[0])
        print(f"    📽️ Source: {source_video}")
        
        # 2. Find Transcript
        transcripts = list(proj.glob("*TRANSCRIPT*.md"))
        if not transcripts:
             print("    ❌ No Transcript found.")
             continue
        transcript = parse_transcript(transcripts[0])
        print(f"    📝 Transcript parsed ({len(transcript)} segments)")
        
        # 3. Find Premise/Script Analysis
        analysis_files = list(proj.glob("*premise_analysis.json"))
        if not analysis_files:
            print("    ❌ No premise_analysis.json found.")
            continue
            
        with open(analysis_files[0], 'r', encoding='utf-8') as f:
            data = json.load(f)
            
        # Extract Scene Recommendations
        if "composed_script_recommendation" not in data:
            print("    ⚠️ No composed_script_recommendation in JSON.")
            continue
            
        scenes = data["composed_script_recommendation"].get("witness_arc_composition", {})
        
        # 4. Process Cuts
        output_dir = os.path.join(proj, "04_assets", "a_roll")
        os.makedirs(output_dir, exist_ok=True)
        print(f"    📂 Output: {output_dir}")
        
        for scene_key, scene_data in scenes.items():
            # scene_key = "W1_HOOK", etc.
            quote_text = scene_data.get("quote")
            if not quote_text: continue
            
            # Find times
            start, end = find_quote_times(quote_text, transcript)
            
            if start is not None and end is not None:
                # Add tiny padding?
                # User asked for "not too mechanic"
                # Let's add 0.1s padding if possible, but we risk cross talk.
                # Safe bet: start - 0.1, end + 0.1?
                # Let's stick to strict timestamp + audio fade first. 
                # The text matching is usually "loose" enough to capturing the breath.
                
                duration = end - start
                filename = f"{proj_name}_{scene_key}_aroll.mp4"
                save_path = os.path.join(output_dir, filename)
                
                print(f"    Cutting {scene_key} ({start:.2f}s -> {end:.2f}s) ...")
                success = cut_clip(source_video, start, end, save_path)
                if success:
                    print(f"      ✅ Saved: {filename}")
                else:
                    print(f"      ❌ Ffmpeg failed for {scene_key}")
            else:
                print(f"      ⚠️ Manual check needed for {scene_key}: '{quote_text[:30]}...'")

if __name__ == "__main__":
    main()
