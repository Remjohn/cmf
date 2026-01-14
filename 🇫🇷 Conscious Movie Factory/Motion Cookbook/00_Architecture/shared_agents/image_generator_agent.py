#!/usr/bin/env python3
"""Image Generator Agent - Generate missing images using AI models"""

import json
import sys
import time
import hashlib
import requests
from pathlib import Path
from typing import Dict, List, Optional

class ImageGenerator:
    """Generates images using various AI models"""
    
    # Model configurations
    MODELS = {
        "qwen_image_2512": {
            "endpoint": "https://api.qwen.ai/v1/images/generations",
            "max_size": 2048,
            "strength": "high_quality"
        },
        "nanobanana_pro": {
            "endpoint": "https://api.nanobanana.com/v1/generate",
            "max_size": 2048,
            "strength": "technical"
        },
        "zimage_turbo": {
            "endpoint": "https://api.zimage.ai/v1/turbo",
            "max_size": 1024,
            "strength": "fast"
        }
    }
    
    def __init__(self, api_keys: Optional[Dict[str, str]] = None):
        """Initialize with API keys from environment or config"""
        import os
        self.api_keys = api_keys or {
            "qwen": os.getenv("QWEN_API_KEY"),
            "nanobanana": os.getenv("NANOBANANA_API_KEY"),
            "zimage": os.getenv("ZIMAGE_API_KEY")
        }
        
        self.output_dir = Path("data/generated")
        self.output_dir.mkdir(parents=True, exist_ok=True)
    
    def process(self, input_data: Dict) -> Dict:
        """Process image generation requests"""
        prompts = input_data.get("prompts", [])
        context = input_data.get("context", {})
        
        if not prompts:
            return self._empty_response()
        
        generated_images = []
        failed_generations = []
        
        for prompt_config in prompts:
            try:
                result = self._generate_image(prompt_config, context)
                generated_images.append(result)
            except Exception as e:
                failed_generations.append({
                    "asset_id": prompt_config.get("asset_id", "unknown"),
                    "error": str(e),
                    "retry_recommended": self._should_retry(e)
                })
        
        return {
            "agent_id": "ImageGenerator",
            "version": "1.0",
            "output": {
                "generated_images": generated_images,
                "failed_generations": failed_generations
            }
        }
    
    def _generate_image(self, prompt_config: Dict, context: Dict) -> Dict:
        """Generate a single image"""
        asset_id = prompt_config.get("asset_id", self._generate_id())
        prompt = prompt_config.get("prompt")
        model = prompt_config.get("model", "qwen_image_2512")
        style = prompt_config.get("style", "clean, professional")
        aspect_ratio = prompt_config.get("aspect_ratio", "9:16")
        
        # Enhance prompt with context
        enhanced_prompt = self._enhance_prompt(prompt, style, context)
        
        start_time = time.time()
        
        # Call AI model (simulated - replace with actual API calls)
        image_data = self._call_model(model, enhanced_prompt, aspect_ratio)
        
        # Save image
        image_path = self._save_image(asset_id, image_data)
        
        generation_time_ms = int((time.time() - start_time) * 1000)
        
        return {
            "asset_id": asset_id,
            "path": str(image_path),
            "model_used": model,
            "prompt_used": enhanced_prompt,
            "dimensions": self._get_dimensions(aspect_ratio),
            "generation_time_ms": generation_time_ms,
            "success": True
        }
    
    def _enhance_prompt(self, prompt: str, style: str, context: Dict) -> str:
        """Enhance prompt with style and context"""
        topic = context.get("topic", "")
        
        enhanced = f"{prompt}, {style}"
        
        if topic:
            enhanced += f", related to {topic}"
        
        # Add quality modifiers
        enhanced += ", high quality, professional, clean composition"
        
        return enhanced
    
    def _call_model(self, model: str, prompt: str, aspect_ratio: str) -> bytes:
        """Call AI model API (simplified - add real implementation)"""
        
        # For demo/testing, return placeholder
        # In production, implement actual API calls:
        """
        model_config = self.MODELS.get(model)
        
        response = requests.post(
            model_config["endpoint"],
            headers={"Authorization": f"Bearer {self.api_keys.get(model)}"},
            json={
                "prompt": prompt,
                "size": self._aspect_to_size(aspect_ratio),
                "quality": model_config["strength"]
            },
            timeout=60
        )
        
        response.raise_for_status()
        return response.content
        """
        
        # Placeholder: Create empty image
        from PIL import Image
        import io
        
        width, height = self._get_dimensions(aspect_ratio).values()
        img = Image.new('RGB', (width, height), color=(50, 50, 50))
        
        buf = io.BytesIO()
        img.save(buf, format='PNG')
        return buf.getvalue()
    
    def _save_image(self, asset_id: str, image_data: bytes) -> Path:
        """Save generated image to disk"""
        filename = f"{asset_id}.png"
        filepath = self.output_dir / filename
        
        with open(filepath, 'wb') as f:
            f.write(image_data)
        
        return filepath
    
    def _get_dimensions(self, aspect_ratio: str) -> Dict[str, int]:
        """Get dimensions for aspect ratio"""
        ratios = {
            "9:16": {"width": 1080, "height": 1920},
            "1:1": {"width": 1080, "height": 1080},
            "16:9": {"width": 1920, "height": 1080}
        }
        return ratios.get(aspect_ratio, ratios["9:16"])
    
    def _aspect_to_size(self, aspect_ratio: str) -> str:
        """Convert aspect ratio to model size string"""
        dims = self._get_dimensions(aspect_ratio)
        return f"{dims['width']}x{dims['height']}"
    
    def _generate_id(self) -> str:
        """Generate unique asset ID"""
        timestamp = str(time.time()).encode()
        return hashlib.sha256(timestamp).hexdigest()[:12]
    
    def _should_retry(self, error: Exception) -> bool:
        """Determine if error is retryable"""
        retryable = ["timeout", "rate limit", "503", "502"]
        error_str = str(error).lower()
        return any(msg in error_str for msg in retryable)
    
    def _empty_response(self) -> Dict:
        """Return empty response when no work needed"""
        return {
            "agent_id": "ImageGenerator",
            "version": "1.0",
            "output": {
                "generated_images": [],
                "failed_generations": []
            }
        }

def main():
    """CLI entry point"""
    try:
        input_data = json.loads(sys.stdin.read())
        generator = ImageGenerator()
        output = generator.process(input_data)
        print(json.dumps(output, indent=2))
        sys.exit(0)
    except Exception as e:
        error = {
            "error": str(e),
            "agent_id": "ImageGenerator"
        }
        print(json.dumps(error), file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
