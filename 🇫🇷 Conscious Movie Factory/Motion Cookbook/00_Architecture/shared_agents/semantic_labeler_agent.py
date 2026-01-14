#!/usr/bin/env python3
"""Semantic Labeler Agent - Assign semantic tags to layers"""

import json
import sys
from pathlib import Path
from typing import Dict, List, Set
from PIL import Image
import numpy as np

class SemanticLabeler:
    """Assigns semantic labels to layers"""
    
    # Semantic taxonomy
    SEMANTIC_CATEGORIES = {
        "anatomy": ["body", "anatomy", "organ", "region", "system"],
        "body_parts": ["gut", "brain", "heart", "lungs", "liver", "spine", "nervous_system"],
        "spatial": ["background", "foreground", "center", "periphery"],
        "functional": ["hub", "node", "connection", "flow", "bottleneck"],
        "conceptual": ["cause", "effect", "problem", "solution", "before", "after"],
        "subjects": ["person", "speaker", "subject", "character"],
        "misc": ["text", "icon", "decoration", "effect"]
    }
    
    # Transform permissions based on semantics
    ALLOWED_TRANSFORMS = {
        "background": ["opacity", "blur", "scale"],
        "foreground": ["opacity", "scale", "position", "glow"],
        "body": ["opacity", "scale"],
        "region": ["opacity", "scale", "glow", "outline"],
        "person": ["opacity", "scale", "position", "glow"],
        "text": ["opacity", "scale", "position"],
        "icon": ["opacity", "scale", "position", "rotate"]
    }
    
    def __init__(self):
        pass
    
    def process(self, input_data: Dict) -> Dict:
        """Label all layer graphs"""
        layer_graphs = input_data.get("layer_graphs", [])
        context = input_data.get("context", {})
        
        labeled_graphs = []
        low_confidence = []
        
        for graph in layer_graphs:
            labeled_graph = self._label_graph(graph, context)
            labeled_graphs.append(labeled_graph)
            
            # Collect low confidence layers
            for layer in labeled_graph["layers"]:
                if layer.get("confidence", 1.0) < 0.7:
                    low_confidence.append({
                        "graph_id": graph["graph_id"],
                        "layer_id": layer["layer_id"],
                        "confidence": layer["confidence"],
                        "warning": "Low semantic labeling confidence"
                    })
        
        return {
            "agent_id": "SemanticLabeler",
            "version": "1.0",
            "output": {
                "labeled_layer_graphs": labeled_graphs,
                "low_confidence_layers": low_confidence
            }
        }
    
    def _label_graph(self, graph: Dict, context: Dict) -> Dict:
        """Label all layers in a graph"""
        layers = graph.get("layers", [])
        labeled_layers = []
        
        for layer in layers:
            labeled = self._label_layer(layer, context, graph)
            labeled_layers.append(labeled)
        
        return {
            "graph_id": graph["graph_id"],
            "layers": labeled_layers
        }
    
    def _label_layer(self, layer: Dict, context: Dict, graph: Dict) -> Dict:
        """Label a single layer"""
        layer_id = layer["layer_id"]
        layer_type = layer.get("type", "image")
        bbox = layer.get("bbox", {})
        rgba_asset = layer.get("rgba_asset")
        
        # Analyze layer properties
        spatial_features = self._analyze_spatial(bbox)
        visual_features = self._analyze_visual(rgba_asset) if rgba_asset else {}
        
        # Generate semantic labels
        semantics = self._generate_semantics(
            layer_id,
            layer_type,
            spatial_features,
            visual_features,
            context
        )
        
        # Calculate confidence
        confidence = self._calculate_confidence(
            semantics,
            spatial_features,
            visual_features
        )
        
        # Determine primary semantic
        primary = self._determine_primary(semantics, spatial_features)
        
        # Get allowed transforms
        allowed_transforms = self._get_allowed_transforms(semantics)
        
        return {
            "layer_id": layer_id,
            "semantics": semantics,
            "confidence": confidence,
            "primary_semantic": primary,
            "allowed_transforms": allowed_transforms
        }
    
    def _analyze_spatial(self, bbox: Dict) -> Dict:
        """Analyze spatial properties of layer"""
        x, y, w, h = bbox.get("x", 0), bbox.get("y", 0), bbox.get("w", 1), bbox.get("h", 1)
        
        area = w * h
        center_x = x + w / 2
        center_y = y + h / 2
        
        # Determine position
        is_centered = (0.3 < center_x < 0.7) and (0.3 < center_y < 0.7)
        is_top = y < 0.3
        is_bottom = (y + h) > 0.7
        is_full = w > 0.9 and h > 0.9
        
        return {
            "area": area,
            "center": (center_x, center_y),
            "is_centered": is_centered,
            "is_top": is_top,
            "is_bottom": is_bottom,
            "is_full": is_full,
            "aspect_ratio": w / h if h > 0 else 1.0
        }
    
    def _analyze_visual(self, asset_path: str) -> Dict:
        """Analyze visual properties of layer"""
        try:
            with Image.open(asset_path) as img:
                img_array = np.array(img)
                
                # Check if has alpha
                has_alpha = img_array.shape[2] == 4 if len(img_array.shape) == 3 else False
                
                # Calculate coverage (if alpha)
                coverage = 1.0
                if has_alpha:
                    alpha = img_array[:, :, 3]
                    coverage = np.sum(alpha > 128) / alpha.size
                
                # Simple color analysis
                if has_alpha:
                    rgb = img_array[:, :, :3]
                    mask = img_array[:, :, 3] > 128
                    masked_rgb = rgb[mask] if np.any(mask) else rgb
                else:
                    masked_rgb = img_array[:, :, :3].reshape(-1, 3)
                
                mean_color = masked_rgb.mean(axis=0) if len(masked_rgb) > 0 else [0, 0, 0]
                
                return {
                    "has_alpha": has_alpha,
                    "coverage": float(coverage),
                    "mean_color": mean_color.tolist(),
                    "is_dark": float(mean_color.mean()) < 128
                }
        except Exception:
            return {}
    
    def _generate_semantics(
        self,
        layer_id: str,
        layer_type: str,
        spatial: Dict,
        visual: Dict,
        context: Dict
    ) -> List[str]:
        """Generate semantic labels"""
        semantics = set()
        
        # Layer ID hints
        id_lower = layer_id.lower()
        for category, keywords in self.SEMANTIC_CATEGORIES.items():
            for keyword in keywords:
                if keyword in id_lower:
                    semantics.add(keyword)
        
        # Type-based
        if layer_type == "cutout":
            semantics.add("person")
            semantics.add("foreground")
        elif layer_type == "region":
            semantics.add("region")
        
        # Spatial-based
        if spatial.get("is_full"):
            semantics.add("background")
        elif spatial.get("is_centered"):
            semantics.add("center")
            semantics.add("foreground")
        
        if spatial.get("is_top"):
            semantics.add("header")
        if spatial.get("is_bottom"):
            semantics.add("footer")
        
        # Coverage-based
        coverage = visual.get("coverage", 1.0)
        if coverage > 0.8:
            semantics.add("major")
        elif coverage < 0.2:
            semantics.add("detail")
        
        # Context-based
        topic = context.get("topic", "").lower()
        key_concepts = [c.lower() for c in context.get("key_concepts", [])]
        
        # Match topic/concepts to semantics
        for concept in key_concepts:
            for category, keywords in self.SEMANTIC_CATEGORIES.items():
                if concept in keywords:
                    semantics.add(concept)
        
        # Default fallback
        if not semantics:
            if spatial.get("is_full"):
                semantics.add("background")
            else:
                semantics.add("foreground")
        
        return sorted(list(semantics))
    
    def _calculate_confidence(
        self,
        semantics: List[str],
        spatial: Dict,
        visual: Dict
    ) -> float:
        """Calculate labeling confidence"""
        confidence = 0.5  # Base
        
        # More semantics = higher confidence
        if len(semantics) >= 2:
            confidence += 0.2
        
        # Clear spatial position = higher confidence
        if spatial.get("is_full") or spatial.get("is_centered"):
            confidence += 0.15
        
        # Good visual data = higher confidence
        if visual.get("has_alpha"):
            confidence += 0.1
        
        # High coverage = higher confidence
        coverage = visual.get("coverage", 0.5)
        if coverage > 0.7:
            confidence += 0.1
        
        return min(confidence, 1.0)
    
    def _determine_primary(self, semantics: List[str], spatial: Dict) -> str:
        """Determine primary semantic label"""
        if not semantics:
            return "unknown"
        
        # Priority order
        priority = [
            "person", "subject",
            "gut", "brain", "heart",
            "hub", "node",
            "foreground", "background"
        ]
        
        for sem in priority:
            if sem in semantics:
                return sem
        
        return semantics[0]
    
    def _get_allowed_transforms(self, semantics: List[str]) -> List[str]:
        """Get allowed transforms based on semantics"""
        allowed = set()
        
        for semantic in semantics:
            transforms = self.ALLOWED_TRANSFORMS.get(semantic, [])
            allowed.update(transforms)
        
        # Default minimum
        if not allowed:
            allowed = {"opacity", "scale"}
        
        return sorted(list(allowed))

def main():
    """CLI entry point"""
    try:
        input_data = json.loads(sys.stdin.read())
        labeler = SemanticLabeler()
        output = labeler.process(input_data)
        print(json.dumps(output, indent=2))
        sys.exit(0)
    except Exception as e:
        error = {
            "error": str(e),
            "agent_id": "SemanticLabeler"
        }
        print(json.dumps(error), file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
