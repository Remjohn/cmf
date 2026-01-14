
import re
import sys
import os

def clean_srt(input_path, output_path):
    with open(input_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    clean_lines = []
    for line in lines:
        stripped = line.strip()
        if not stripped:
            continue
        if stripped.isdigit():
            continue
        if '-->' in stripped:
            continue
        clean_lines.append(stripped)

    with open(output_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(clean_lines))

if __name__ == '__main__':
    if len(sys.argv) < 3:
        print("Usage: python clean_srt.py <input_srt> <output_md>")
        sys.exit(1)
    
    clean_srt(sys.argv[1], sys.argv[2])
