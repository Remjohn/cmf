# **speech\_analysis\_implementation.md**

**Purpose:** Concrete implementation of speech analysis for timing anchors  
 **Status:** Canonical v1.0

---

## **1\. Overview**

Speech analysis extracts **temporal anchors** from audio/transcript to enable speech-aligned scene timing.

**Key Principle:** Speech analysis provides **timing only**, never semantic interpretation.

---

## **2\. Technology Stack**

### **Primary Library: Librosa \+ PyAnnote**

**Why this stack:**

* ✅ Librosa: Robust audio processing  
* ✅ PyAnnote: State-of-art VAD  
* ✅ Both: Open source, no API costs  
* ✅ Can run locally or serverless

**Alternatives considered:**

* ❌ Whisper: Too heavy, we don't need transcription  
* ❌ Cloud APIs: Cost \+ latency  
* ❌ WebRTC VAD: Less accurate

---

## **3\. Installation**

\# Core dependencies  
pip install librosa\>=0.10.0  
pip install pyannote.audio\>=3.0.0  
pip install scipy\>=1.11.0  
pip install numpy\>=1.24.0

\# Optional: for advanced features  
pip install webrtcvad\>=2.0.10

---

## **4\. SpeechAnalyzer Agent Implementation**

### **File: agents/speech\_analyzer.py**

\#\!/usr/bin/env python3  
"""Speech Analyzer Agent \- Extract temporal anchors from audio"""

import json  
import sys  
import librosa  
import numpy as np  
from pathlib import Path  
from typing import Dict, Optional, List  
from pyannote.audio import Pipeline

class SpeechAnalyzer:  
    """Extracts speech timing anchors from audio clips"""  
      
    def \_\_init\_\_(self):  
        \# Load VAD pipeline (voice activity detection)  
        self.vad \= Pipeline.from\_pretrained(  
            "pyannote/voice-activity-detection"  
        )  
          
        \# Configure VAD parameters  
        self.vad\_params \= {  
            "min\_duration\_on": 0.2,   \# Min speech segment: 200ms  
            "min\_duration\_off": 0.1   \# Min silence: 100ms  
        }  
      
    def process(self, input\_data: Dict) \-\> Dict:  
        """Process audio and extract anchors"""  
        audio\_path \= input\_data.get("audio")  
        transcript \= input\_data.get("transcript")  
        scene\_duration\_frames \= input\_data.get("scene\_duration\_frames", 150\)  
        fps \= input\_data.get("fps", 30\)  
          
        if not audio\_path:  
            return self.\_fallback\_response()  
          
        \# Load audio  
        try:  
            y, sr \= librosa.load(audio\_path, sr=16000)  
        except Exception as e:  
            return self.\_error\_response(f"Audio load failed: {e}")  
          
        \# Run VAD  
        vad\_result \= self.vad(audio\_path, \*\*self.vad\_params)  
          
        \# Extract speech segments  
        speech\_segments \= self.\_extract\_segments(vad\_result)  
          
        if len(speech\_segments) \== 0:  
            return self.\_fallback\_response("No speech detected")  
          
        \# Detect pauses  
        pauses \= self.\_detect\_pauses(speech\_segments)  
          
        \# Detect peaks (energy/emphasis)  
        peaks \= self.\_detect\_peaks(y, sr, speech\_segments)  
          
        \# Calculate anchors  
        anchors \= self.\_calculate\_anchors(  
            speech\_segments,   
            pauses,   
            peaks,   
            scene\_duration\_frames,   
            fps  
        )  
          
        \# Calculate confidence  
        confidence \= self.\_calculate\_confidence(  
            speech\_segments,   
            pauses,   
            peaks  
        )  
          
        return {  
            "agent\_id": "SpeechAnalyzer",  
            "version": "1.0",  
            "output": {  
                "anchors": anchors,  
                "confidence": confidence,  
                "speech\_segments": speech\_segments,  
                "detected\_pauses": pauses,  
                "energy\_peaks": peaks  
            }  
        }  
      
    def \_extract\_segments(self, vad\_result) \-\> List\[Dict\]:  
        """Convert VAD output to segment list"""  
        segments \= \[\]  
        for segment in vad\_result.get\_timeline():  
            segments.append({  
                "start": segment.start,  
                "end": segment.end,  
                "duration": segment.duration  
            })  
        return segments  
      
    def \_detect\_pauses(self, segments: List\[Dict\]) \-\> List\[float\]:  
        """Find pauses between speech segments"""  
        pauses \= \[\]  
        for i in range(len(segments) \- 1):  
            gap \= segments\[i+1\]\["start"\] \- segments\[i\]\["end"\]  
            if gap \> 0.2:  \# \>200ms silence  
                pauses.append(segments\[i\]\["end"\] \+ gap/2)  
        return pauses  
      
    def \_detect\_peaks(  
        self,   
        y: np.ndarray,   
        sr: int,   
        segments: List\[Dict\]  
    ) \-\> List\[float\]:  
        """Find energy peaks (emphasis points)"""  
        \# Calculate RMS energy  
        rms \= librosa.feature.rms(y=y, hop\_length=512)\[0\]  
        times \= librosa.frames\_to\_time(  
            np.arange(len(rms)),   
            sr=sr,   
            hop\_length=512  
        )  
          
        peaks \= \[\]  
        for segment in segments:  
            \# Find peak within segment  
            mask \= (times \>= segment\["start"\]) & (times \<= segment\["end"\])  
            segment\_rms \= rms\[mask\]  
            segment\_times \= times\[mask\]  
              
            if len(segment\_rms) \> 0:  
                peak\_idx \= np.argmax(segment\_rms)  
                peaks.append(float(segment\_times\[peak\_idx\]))  
          
        return peaks  
      
    def \_calculate\_anchors(  
        self,  
        segments: List\[Dict\],  
        pauses: List\[float\],  
        peaks: List\[float\],  
        duration\_frames: int,  
        fps: int  
    ) \-\> Dict\[str, int\]:  
        """Calculate frame-based anchors"""  
        if len(segments) \== 0:  
            return {}  
          
        \# Convert to frames  
        max\_time \= duration\_frames / fps  
          
        \# Response start \= first speech onset  
        response\_start \= self.\_time\_to\_frame(  
            segments\[0\]\["start"\],   
            fps,   
            duration\_frames  
        )  
          
        \# Response end \= last speech offset  
        response\_end \= self.\_time\_to\_frame(  
            segments\[-1\]\["end"\],   
            fps,   
            duration\_frames  
        )  
          
        \# Response peak \= highest energy peak  
        if peaks:  
            peak\_time \= max(peaks, key=lambda t: t)  
            response\_peak \= self.\_time\_to\_frame(  
                peak\_time,   
                fps,   
                duration\_frames  
            )  
        else:  
            \# Fallback: midpoint  
            response\_peak \= (response\_start \+ response\_end) // 2  
          
        \# Optional: pause anchor  
        pause\_mid \= None  
        if pauses:  
            pause\_time \= pauses\[0\]  \# First significant pause  
            pause\_mid \= self.\_time\_to\_frame(  
                pause\_time,   
                fps,   
                duration\_frames  
            )  
          
        anchors \= {  
            "response\_start": int(response\_start),  
            "response\_peak": int(response\_peak),  
            "response\_end": int(response\_end)  
        }  
          
        if pause\_mid:  
            anchors\["pause\_mid"\] \= int(pause\_mid)  
          
        \# Validate monotonicity  
        if not (anchors\["response\_start"\] \< anchors\["response\_peak"\] \< anchors\["response\_end"\]):  
            \# Fallback to absolute timing  
            return {}  
          
        return anchors  
      
    def \_time\_to\_frame(self, time\_sec: float, fps: int, max\_frames: int) \-\> int:  
        """Convert time to frame number"""  
        frame \= int(time\_sec \* fps)  
        return max(0, min(frame, max\_frames \- 1))  
      
    def \_calculate\_confidence(  
        self,   
        segments: List\[Dict\],   
        pauses: List\[float\],   
        peaks: List\[float\]  
    ) \-\> float:  
        """Calculate confidence score (0-1)"""  
        confidence \= 0.5  \# Base  
          
        \# More segments \= higher confidence  
        if len(segments) \>= 1:  
            confidence \+= 0.1  
        if len(segments) \>= 2:  
            confidence \+= 0.1  
          
        \# Clear pauses \= higher confidence  
        if len(pauses) \> 0:  
            confidence \+= 0.1  
          
        \# Clear peaks \= higher confidence  
        if len(peaks) \> 0:  
            confidence \+= 0.15  
          
        \# Consistent segment lengths \= higher confidence  
        if len(segments) \> 1:  
            durations \= \[s\["duration"\] for s in segments\]  
            cv \= np.std(durations) / np.mean(durations)  
            if cv \< 0.5:  \# Low coefficient of variation  
                confidence \+= 0.1  
          
        return min(confidence, 1.0)  
      
    def \_fallback\_response(self, reason: str \= "No audio") \-\> Dict:  
        """Return fallback when analysis fails"""  
        return {  
            "agent\_id": "SpeechAnalyzer",  
            "version": "1.0",  
            "output": {  
                "anchors": {},  
                "confidence": 0.0,  
                "fallback\_reason": reason,  
                "recommendation": "Use absolute timing"  
            }  
        }  
      
    def \_error\_response(self, error: str) \-\> Dict:  
        """Return error response"""  
        return {  
            "error": error,  
            "agent\_id": "SpeechAnalyzer"  
        }

def main():  
    """CLI entry point"""  
    try:  
        input\_data \= json.loads(sys.stdin.read())  
        analyzer \= SpeechAnalyzer()  
        output \= analyzer.process(input\_data)  
        print(json.dumps(output, indent=2))  
        sys.exit(0)  
    except Exception as e:  
        error \= {  
            "error": str(e),  
            "agent\_id": "SpeechAnalyzer"  
        }  
        print(json.dumps(error), file=sys.stderr)  
        sys.exit(1)

if \_\_name\_\_ \== "\_\_main\_\_":  
    main()

---

## **5\. Usage Examples**

### **Example 1: Simple Response**

**Input:**

cat \<\< EOF | python agents/speech\_analyzer.py  
{  
  "audio": "data/audio/response\_001.wav",  
  "scene\_duration\_frames": 150,  
  "fps": 30  
}  
EOF

**Output:**

{  
  "agent\_id": "SpeechAnalyzer",  
  "version": "1.0",  
  "output": {  
    "anchors": {  
      "response\_start": 42,  
      "response\_peak": 78,  
      "response\_end": 118  
    },  
    "confidence": 0.87,  
    "speech\_segments": \[  
      {"start": 1.4, "end": 3.93, "duration": 2.53}  
    \],  
    "detected\_pauses": \[\],  
    "energy\_peaks": \[2.6\]  
  }  
}

---

### **Example 2: Multi-Segment Response with Pause**

**Input:**

cat \<\< EOF | python agents/speech\_analyzer.py  
{  
  "audio": "data/audio/interview\_002.wav",  
  "transcript": "Well... I'd say I'm at about a 7 right now",  
  "scene\_duration\_frames": 180,  
  "fps": 30  
}  
EOF

**Output:**

{  
  "output": {  
    "anchors": {  
      "response\_start": 38,  
      "response\_peak": 95,  
      "response\_end": 142,  
      "pause\_mid": 65  
    },  
    "confidence": 0.92,  
    "speech\_segments": \[  
      {"start": 1.27, "end": 1.82, "duration": 0.55},  
      {"start": 2.45, "end": 4.73, "duration": 2.28}  
    \],  
    "detected\_pauses": \[2.13\],  
    "energy\_peaks": \[1.5, 3.17\]  
  }  
}

---

## **6\. Integration with Scene Rendering**

### **Modified Scene Config**

{  
  "scene\_id": "RATING\_METER\_1\_TO\_10",  
  "timing": {  
    "mode": "speech\_aligned",  
    "anchors": {  
      "response\_start": 42,  
      "response\_peak": 78,  
      "response\_end": 118  
    },  
    "anchor\_confidence": 0.87  
  },  
  "fallback\_timing": {  
    "mode": "absolute",  
    "duration\_frames": 150  
  }  
}

### **Motion Canvas Integration**

// motion-canvas/src/scenes/rating\_meter.tsx

export default makeScene2D(function\* (view) {  
  const config \= loadSceneConfig();  
  const timing \= config.timing;  
    
  let startFrame, endFrame;  
    
  if (timing.mode \=== "speech\_aligned" && timing.anchor\_confidence \> 0.7) {  
    // Use speech anchors  
    startFrame \= timing.anchors.response\_start;  
    endFrame \= timing.anchors.response\_end;  
  } else {  
    // Fallback to absolute  
    startFrame \= 30;  
    endFrame \= 120;  
  }  
    
  // Animate meter from startFrame to endFrame  
  yield\* all(  
    meter().width(0, 0).to(targetWidth, endFrame \- startFrame, easeOutCubic),  
    // ...  
  );  
});

---

## **7\. Confidence Thresholds**

| Confidence | Interpretation | Action |
| ----- | ----- | ----- |
| 0.85 \- 1.0 | High | Use anchors |
| 0.70 \- 0.85 | Medium | Use anchors with caution |
| 0.50 \- 0.70 | Low | Consider fallback |
| \< 0.50 | Very Low | Use absolute timing |

**Default Threshold:** 0.70

---

## **8\. Advanced Features (Optional)**

### **Prosody Analysis**

def \_detect\_prosody(self, y, sr, segments):  
    """Detect pitch contours for emotional emphasis"""  
    pitches, magnitudes \= librosa.piptrack(y=y, sr=sr)  
      
    \# Extract pitch per segment  
    segment\_prosody \= \[\]  
    for segment in segments:  
        \# ... analyze pitch variation  
        pass  
      
    return segment\_prosody

### **Transcript Alignment (If Available)**

def \_align\_transcript(self, transcript, segments):  
    """Align words to segments (basic)"""  
    words \= transcript.split()  
    words\_per\_segment \= len(words) // len(segments)  
      
    \# Simple heuristic alignment  
    alignments \= \[\]  
    for i, segment in enumerate(segments):  
        start\_word \= i \* words\_per\_segment  
        end\_word \= min((i \+ 1\) \* words\_per\_segment, len(words))  
        alignments.append({  
            "segment": segment,  
            "words": words\[start\_word:end\_word\]  
        })  
      
    return alignments

---

## **9\. Testing**

### **Unit Tests**

\# tests/agents/test\_speech\_analyzer.py

def test\_basic\_speech\_detection():  
    """Test basic anchor extraction"""  
    analyzer \= SpeechAnalyzer()  
      
    input\_data \= {  
        "audio": "tests/fixtures/simple\_response.wav",  
        "scene\_duration\_frames": 150,  
        "fps": 30  
    }  
      
    output \= analyzer.process(input\_data)  
    anchors \= output\["output"\]\["anchors"\]  
      
    assert "response\_start" in anchors  
    assert "response\_end" in anchors  
    assert anchors\["response\_start"\] \< anchors\["response\_end"\]  
    assert output\["output"\]\["confidence"\] \> 0.5

def test\_no\_speech\_fallback():  
    """Test fallback when no speech detected"""  
    analyzer \= SpeechAnalyzer()  
      
    input\_data \= {  
        "audio": "tests/fixtures/silence.wav",  
        "scene\_duration\_frames": 150,  
        "fps": 30  
    }  
      
    output \= analyzer.process(input\_data)  
      
    assert output\["output"\]\["anchors"\] \== {}  
    assert output\["output"\]\["confidence"\] \== 0.0  
    assert "fallback\_reason" in output\["output"\]

---

## **10\. Performance Optimization**

### **Caching**

@functools.lru\_cache(maxsize=100)  
def \_cached\_vad(audio\_path):  
    """Cache VAD results"""  
    return vad(audio\_path)

### **Preprocessing**

def \_preprocess\_audio(audio\_path):  
    """Normalize audio before analysis"""  
    y, sr \= librosa.load(audio\_path, sr=16000)  
      
    \# Normalize volume  
    y \= librosa.util.normalize(y)  
      
    \# Trim silence  
    y, \_ \= librosa.effects.trim(y, top\_db=20)  
      
    return y, sr

---

## **11\. Fallback Strategy**

def determine\_timing(speech\_output, scene\_config):  
    """Decide whether to use speech anchors or absolute timing"""  
      
    confidence \= speech\_output.get("confidence", 0\)  
    anchors \= speech\_output.get("anchors", {})  
      
    if confidence \>= 0.70 and anchors:  
        \# Use speech-aligned  
        return {  
            "mode": "speech\_aligned",  
            "anchors": anchors,  
            "confidence": confidence  
        }  
    else:  
        \# Fallback to absolute  
        return {  
            "mode": "absolute",  
            "duration\_frames": scene\_config\["duration\_frames"\],  
            "reason": f"Low confidence ({confidence})"  
        }

---

**Speech analysis enables human-paced graphics without sacrificing determinism.**

