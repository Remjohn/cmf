### **tools/xml\_generator.py**

Source: Extracted from execute\_cuts.py logic

Purpose: A standalone tool to generate the DaVinci Resolve XML without performing the physical video cuts. This is useful for the Cutter agent when it just needs to build the timeline metadata.

Python

\#\!/usr/bin/env python3  
"""  
Generate DaVinci Resolve compatible XML from a cut script.  
Usage: python xml\_generator.py cut\_script.json output.xml  
"""

import json  
import sys  
import os  
from xml.etree.ElementTree import Element, SubElement, tostring  
from xml.dom import minidom

def timecode\_to\_seconds(tc):  
    """Convert HH:MM:SS.mmm to seconds"""  
    parts \= tc.split(':')  
    h, m, s \= int(parts\[0\]), int(parts\[1\]), float(parts\[2\])  
    return h \* 3600 \+ m \* 60 \+ s

def generate\_xml(cuts\_data, output\_path):  
    """Generate DaVinci Resolve compatible XML"""  
      
    \# Create XML structure  
    xmeml \= Element('xmeml', version="5")  
    sequence \= SubElement(xmeml, 'sequence')

    \# Basic info  
    SubElement(sequence, 'name').text \= "AI\_Cut\_Timeline"

    \# Rate info  
    rate \= SubElement(sequence, 'rate')  
    SubElement(rate, 'timebase').text \= str(cuts\_data.get('fps', 30))  
    SubElement(rate, 'ntsc').text \= 'FALSE'

    \# Media  
    media \= SubElement(sequence, 'media')  
    video \= SubElement(media, 'video')  
    track \= SubElement(video, 'track')

    \# Add clips  
    fps \= cuts\_data.get('fps', 30)  
    current\_frame \= 0

    for i, cut in enumerate(cuts\_data\['cuts'\]):  
        clip \= SubElement(track, 'clipitem', id\=f"clip-{i+1}")  
        SubElement(clip, 'name').text \= f"Clip\_{i+1:03d}"

        \# Convert timecodes to frames  
        start\_sec \= timecode\_to\_seconds(cut\['start'\])  
        end\_sec \= timecode\_to\_seconds(cut\['end'\])  
        duration\_frames \= int((end\_sec \- start\_sec) \* fps)

        SubElement(clip, 'start').text \= str(current\_frame)  
        SubElement(clip, 'end').text \= str(current\_frame \+ duration\_frames)  
        SubElement(clip, 'in').text \= str(int(start\_sec \* fps))  
        SubElement(clip, 'out').text \= str(int(end\_sec \* fps))

        \# File reference  
        file\_elem \= SubElement(clip, 'file', id\=f"file-{i+1}")  
        SubElement(file\_elem, 'name').text \= os.path.basename(cuts\_data\['video\_file'\])  
        SubElement(file\_elem, 'pathurl').text \= f"file://localhost{os.path.abspath(cuts\_data\['video\_file'\])}"

        \# Duration  
        SubElement(file\_elem, 'duration').text \= str(duration\_frames)

        \# Rate  
        file\_rate \= SubElement(file\_elem, 'rate')  
        SubElement(file\_rate, 'timebase').text \= str(fps)  
        SubElement(file\_rate, 'ntsc').text \= 'FALSE'

        current\_frame \+= duration\_frames

    \# Format and save  
    xml\_str \= minidom.parseString(tostring(xmeml)).toprettyxml(indent="  ")  
    with open(output\_path, 'w') as f:  
        f.write(xml\_str)

    print(f"✓ XML generated: {output\_path}")

def main():  
    if len(sys.argv) \< 3:  
        print("Usage: python xml\_generator.py \<cut\_script.json\> \<output.xml\>")  
        sys.exit(1)

    script\_path \= sys.argv\[1\]  
    output\_path \= sys.argv\[2\]

    \# Parse cut script  
    print(f"\\n📋 Reading cut script: {script\_path}")  
    with open(script\_path, 'r') as f:  
        cuts\_data \= json.load(f)

    generate\_xml(cuts\_data, output\_path)

if \_\_name\_\_ \== "\_\_main\_\_":  
    main()

