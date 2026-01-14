#!/usr/bin/env python3
"""Layer Extractor Agent - Decompose images into RGBA layers"""

import json
import sys
import time
import hashlib
from pathlib import Path
from typing import Dict, List, Tuple
import numpy as np
from PIL import Image

class LayerExtractor:
    """Extracts layers from images"""
    
    def __init__(self):
        self.output_dir = Path("data/layer_graphs")
        self.output_dir.mkdir(parents=True, exist_ok=True)
    
    def process(self, input_data: Dict) -> Dict:
        """Process layer extraction requests"""
        assets = input_data.get("assets", [])
        output_dir = Path(input_data.get("output_dir", self.output_dir))
        
        layer_graphs = []
        failed_extractions = []
        
        for asset_config in assets:
            try:
                graph = self._extract_layers(asset_config, output_dir)
                layer_graphs.append(graph)
            except Exception as e:
                failed_extractions.append({
                    "asset_id": asset_config.get("asset_id", "unknown"),
                    "error": str(e),
                    "fallback_strategy": self._determine_fallback(e)
                })
        
        return {
            "agent_id": "LayerExtractor",
            "version": "1.0",
            "output": {
                "layer_graphs": layer_graphs,
                "failed_extractions": failed_extractions
            }
        }
    
    def _extract_layers(self, asset_config: Dict, output_dir: Path) -> Dict:
        """Extract layers from single image"""
        asset_id = asset_config.get("asset_id")
        asset_path = Path(asset_config.get("path"))
        method = asset_config.get("method", "qwen_layered")
        
        # Generate unique graph ID
        graph_id = self._generate_graph_id(asset_path)
        graph_dir = output_dir / graph_id
        graph_dir.mkdir(parents=True, exist_ok=True)
        
        start_time = time.time()
        
        # Load image
        with Image.open(asset_path) as img:
            # Convert to RGBA if needed
            if img.mode != 'RGBA':
                img = img.convert('RGBA')
            
            img_array = np.array(img)
            width, height = img.size
        
        # Extract layers based on method
        if method == "manual":
            layers = self._extract_manual(asset_path, graph_dir)
        elif method == "sam3":
            layers = self._extract_sam3(img_array, graph_dir)
        else:  # qwen_layered (default)
            layers = self._extract_qwen(img_array, graph_dir)
        
        processing_time = int((time.time() - start_time) * 1000)
        
        # Save graph metadata
        graph = {
            "graph_id": graph_id,
            "source_asset": str(asset_path),
            "extraction_method": method,
            "extraction_confidence": self._calculate_confidence(layers),
            "canvas": {
                "width": width,
                "height": height,
                "aspect_ratio": f"{width}:{height}"
            },
            "layers": layers,
            "processing_time_ms": processing_time
        }
        
        # Save graph.json
        with open(graph_dir / "graph.json", 'w') as f:
            json.dump(graph, f, indent=2)
        
        return graph
    
    def _extract_qwen(self, img_array: np.ndarray, output_dir: Path) -> List[Dict]:
        """Extract layers using Qwen-style decomposition (simplified)"""
        # This is a simplified placeholder
        # In production, call actual Qwen Image Layered API
        
        height, width = img_array.shape[:2]
        layers = []
        
        # Create base layer (full image)
        base_path = output_dir / "base.png"
        Image.fromarray(img_array).save(base_path)
        
        layers.append({
            "layer_id": "base",
            "type": "image",
            "rgba_asset": str(base_path),
            "z_index": 0,
            "bbox": {"x": 0, "y": 0, "w": 1, "h": 1},
            "extraction_confidence": 1.0
        })
        
        # Simple center region extraction (demo)
        center_region = self._extract_center_region(img_array)
        if center_region is not None:
            region_path = output_dir / "center_region.png"
            Image.fromarray(center_region).save(region_path)
            
            # Calculate bbox
            bbox = self._calculate_bbox(center_region, width, height)
            
            layers.append({
                "layer_id": "center_region",
                "type": "region",
                "rgba_asset": str(region_path),
                "z_index": 1,
                "bbox": bbox,
                "extraction_confidence": 0.85
            })
        
        return layers
    
    def _extract_sam3(self, img_array: np.ndarray, output_dir: Path) -> List[Dict]:
        """Extract layers using SAM3 (placeholder)"""
        # Placeholder for SAM3 integration
        # Would require actual SAM3 model loading and inference
        return self._extract_qwen(img_array, output_dir)
    
    def _extract_manual(self, asset_path: Path, output_dir: Path) -> List[Dict]:
        """Use manually provided layers"""
        # Look for manual layers directory
        manual_dir = asset_path.parent / f"{asset_path.stem}_layers"
        
        if not manual_dir.exists():
            raise FileNotFoundError(f"Manual layers not found at {manual_dir}")
        
        layers = []
        layer_files = sorted(manual_dir.glob("*.png"))
        
        for i, layer_file in enumerate(layer_files):
            # Copy to output directory
            output_path = output_dir / layer_file.name
            
            with Image.open(layer_file) as img:
                img.save(output_path)
                width, height = img.size
            
            # Load to calculate bbox
            img_array = np.array(Image.open(layer_file))
            bbox = self._calculate_bbox(img_array, width, height)
            
            layers.append({
                "layer_id": layer_file.stem,
                "type": "image",
                "rgba_asset": str(output_path),
                "z_index": i,
                "bbox": bbox,
                "extraction_confidence": 1.0
            })
        
        return layers
    
    def _extract_center_region(self, img_array: np.ndarray) -> np.ndarray:
        """Extract center region (simple demo implementation)"""
        height, width = img_array.shape[:2]
        
        # Create mask for center 50%
        mask = np.zeros((height, width), dtype=np.uint8)
        center_y, center_x = height // 2, width // 2
        radius_y, radius_x = height // 4, width // 4
        
        y_min, y_max = center_y - radius_y, center_y + radius_y
        x_min, x_max = center_x - radius_x, center_x + radius_x
        
        mask[y_min:y_max, x_min:x_max] = 255
        
        # Apply mask
        result = img_array.copy()
        result[:, :, 3] = np.minimum(result[:, :, 3], mask)
        
        # Return if any non-transparent pixels
        if np.any(result[:, :, 3] > 0):
            return result
        return None
    
    def _calculate_bbox(
        self, 
        layer_array: np.ndarray, 
        canvas_width: int, 
        canvas_height: int
    ) -> Dict:
        """Calculate normalized bounding box"""
        # Find non-transparent pixels
        alpha = layer_array[:, :, 3] if layer_array.shape[2] == 4 else np.ones(layer_array.shape[:2]) * 255
        y_coords, x_coords = np.where(alpha > 0)
        
        if len(x_coords) == 0:
            return {"x": 0, "y": 0, "w": 1, "h": 1}
        
        x_min, x_max = x_coords.min(), x_coords.max()
        y_min, y_max = y_coords.min(), y_coords.max()
        
        # Normalize to 0-1
        return {
            "x": round(x_min / canvas_width, 3),
            "y": round(y_min / canvas_height, 3),
            "w": round((x_max - x_min) / canvas_width, 3),
            "h": round((y_max - y_min) / canvas_height, 3)
        }
    
    def _calculate_confidence(self, layers: List[Dict]) -> float:
        """Calculate overall extraction confidence"""
        if not layers:
            return 0.0
        
        confidences = [l.get("extraction_confidence", 0) for l in layers]
        return sum(confidences) / len(confidences)
    
    def _generate_graph_id(self, asset_path: Path) -> str:
        """Generate unique graph ID"""
        content = f"{asset_path.stem}_{time.time()}".encode()
        return hashlib.sha256(content).hexdigest()[:16]
    
    def _determine_fallback(self, error: Exception) -> str:
        """Determine fallback strategy"""
        error_str = str(error).lower()
        
        if "timeout" in error_str:
            return "retry"
        elif "not found" in error_str:
            return "skip"
        else:
            return "use_whole_image"

def main():
    """CLI entry point"""
    try:
        input_data = json.loads(sys.stdin.read())
        extractor = LayerExtractor()
        output = extractor.process(input_data)
        print(json.dumps(output, indent=2))
        sys.exit(0)
    except Exception as e:
        error = {
            "error": str(e),
            "agent_id": "LayerExtractor"
        }
        print(json.dumps(error), file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
