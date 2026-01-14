#!/usr/bin/env python3
"""
CGM Pillow Compositor
Executes JSON-defined layouts using Python Pillow (PIL).
"""

import sys
import json
import os
from PIL import Image, ImageDraw, ImageFont, ImageEnhance, ImageChops
from pathlib import Path
from typing import Dict, List, Tuple

class PillowCompositor:
    def __init__(self, asset_roots: Dict[str, str]):
        self.asset_roots = {k: Path(v) for k, v in asset_roots.items()}
        self.canvas_size = (1080, 1920)
        
    def render(self, layout: Dict, output_path: str):
        """Render layout JSON to image file"""
        canvas = Image.new('RGBA', self.canvas_size, (0, 0, 0, 0))
        
        # Sort layers by z-index
        layers = sorted(layout.get("layers", []), key=lambda x: x.get("z_index", 0))
        
        for layer_spec in layers:
            layer_img = self._create_layer(layer_spec)
            if layer_img:
                if layer_spec.get("blend_mode") == "screen":
                    # Screen blend hack
                    # canvas = ImageChops.screen(canvas, layer_img) # Needs conversion
                    canvas.alpha_composite(layer_img) # Fallback
                else:
                    canvas.alpha_composite(layer_img)
        
        # Save output
        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        canvas.convert("RGB").save(output_path)
        print(f"🖼️ Rendered composition to {output_path}")

    def _create_layer(self, spec: Dict) -> Image.Image:
        l_type = spec.get("type")
        
        if l_type == "gradient":
            return self._render_gradient(spec)
        elif l_type == "image":
            return self._render_image(spec)
        elif l_type == "text":
            return self._render_text(spec)
        elif l_type == "overlay":
            return self._render_overlay(spec)
        elif l_type == "video":
            return self._render_video_stub(spec) # Just render first frame/stub
            
        return None

    def _render_gradient(self, spec: Dict) -> Image.Image:
        colors = spec.get("colors", ["#000000", "#FFFFFF"])
        base = Image.new('RGBA', self.canvas_size, colors[0])
        # Simple solid color fallback for now, real gradient logic needs numpy usually
        return base

    def _render_image(self, spec: Dict) -> Image.Image:
        source = spec.get("source")
        if not source: return None
        
        # Resolve path
        path = self._resolve_path(source)
        if not path or not path.exists():
            print(f"⚠️ Image not found: {source}")
            return self._placeholder(source)
            
        img = Image.open(path).convert('RGBA')
        
        # Scale
        scale = spec.get("scale", 1.0)
        if scale != 1.0:
            new_size = (int(img.width * scale), int(img.height * scale))
            img = img.resize(new_size, Image.Resampling.LANCZOS)
        
        # Position
        pos = spec.get("position", {"x": 0, "y": 0})
        x = self._calc_pos(pos.get("x"), img.width, self.canvas_size[0])
        y = self._calc_pos(pos.get("y"), img.height, self.canvas_size[1])
        
        layer = Image.new('RGBA', self.canvas_size, (0,0,0,0))
        layer.paste(img, (x, y), img)
        return layer

    def _render_text(self, spec: Dict) -> Image.Image:
        content = spec.get("content", "")
        size = spec.get("font_size", 40)
        color = spec.get("color", "#FFFFFF")
        
        layer = Image.new('RGBA', self.canvas_size, (0,0,0,0))
        draw = ImageDraw.Draw(layer)
        
        try:
            # Fallback font
            font = ImageFont.truetype("arial.ttf", size)
        except:
            font = ImageFont.load_default()
            
        bbox = draw.textbbox((0, 0), content, font=font)
        w, h = bbox[2], bbox[3]
        
        pos = spec.get("position", {"x": "center", "y": "center"})
        x = self._calc_pos(pos.get("x"), w, self.canvas_size[0])
        y = self._calc_pos(pos.get("y"), h, self.canvas_size[1])
        
        draw.text((x, y), content, font=font, fill=color)
        return layer

    def _render_video_stub(self, spec: Dict) -> Image.Image:
        # For video layers, we just render a placeholder in static composition
        return self._placeholder("Video Layer (Animated downstream)")

    def _placeholder(self, text) -> Image.Image:
        img = Image.new('RGBA', self.canvas_size, (50, 50, 50, 100))
        d = ImageDraw.Draw(img)
        d.text((100, 100), f"MISSING: {text}", fill="red")
        return img
        
    def _resolve_path(self, source_str: str) -> Path:
        # Basic resolution logic
        for root in self.asset_roots.values():
            p = root / source_str
            if p.exists(): return p
        return Path(source_str)

    def _calc_pos(self, val, obj_dim, canvas_dim):
        if val == "center":
            return (canvas_dim - obj_dim) // 2
        return int(val) if val is not None else 0

def main():
    if len(sys.argv) < 3:
        print("Usage: python pillow_compositor.py <layout.json> <output.png>")
        sys.exit(1)
        
    layout_path = sys.argv[1]
    output_path = sys.argv[2]
    
    with open(layout_path, 'r') as f:
        layout = json.load(f)
        
    # Configure asset roots (mock for example)
    roots = {
        "d_roll": "04_assets/d_roll",
        "brand": "01_brand_library",
        "generated": "04_assets/generative"
    }
    
    compositor = PillowCompositor(roots)
    compositor.render(layout, output_path)

if __name__ == "__main__":
    main()
