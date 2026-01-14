#!/usr/bin/env python3
"""Asset Validator Agent - Validate asset availability and quality"""

import json
import sys
from pathlib import Path
from typing import Dict, List, Tuple
from PIL import Image

class AssetValidator:
    """Validates assets before processing"""
    
    SUPPORTED_FORMATS = {
        'image': ['.png', '.jpg', '.jpeg', '.webp'],
        'video': ['.mp4', '.mov', '.webm']
    }
    
    MIN_DIMENSIONS = 1080  # Minimum pixels (shortest side)
    MAX_FILE_SIZE_MB = 50
    
    def __init__(self):
        pass
    
    def process(self, input_data: Dict) -> Dict:
        """Validate all assets"""
        plan = input_data.get("plan", {})
        assets_config = input_data.get("assets", {})
        
        user_provided = assets_config.get("user_provided", [])
        required_by_scenes = assets_config.get("required_by_scenes", [])
        
        # Validate available assets
        available_assets = []
        for asset_path in user_provided:
            result = self._validate_asset(asset_path)
            if result:
                available_assets.append(result)
        
        # Check for missing assets
        missing_assets = self._find_missing_assets(
            available_assets, 
            required_by_scenes
        )
        
        # Generate warnings
        warnings = self._generate_warnings(available_assets)
        
        # Determine overall status
        status = self._determine_status(available_assets, missing_assets)
        
        return {
            "agent_id": "AssetValidator",
            "version": "1.0",
            "output": {
                "validation_status": status,
                "available_assets": available_assets,
                "missing_assets": missing_assets,
                "warnings": warnings
            }
        }
    
    def _validate_asset(self, asset_path: str) -> Dict:
        """Validate single asset"""
        path = Path(asset_path)
        
        # Check existence
        if not path.exists():
            return None
        
        # Check readability
        if not path.is_file():
            return None
        
        # Get basic info
        file_size_mb = path.stat().st_size / (1024 * 1024)
        suffix = path.suffix.lower()
        
        # Determine type
        asset_type = None
        for type_name, extensions in self.SUPPORTED_FORMATS.items():
            if suffix in extensions:
                asset_type = type_name
                break
        
        if not asset_type:
            return None
        
        # Get dimensions and quality
        dimensions = None
        quality_score = 1.0
        
        if asset_type == 'image':
            dimensions, quality_score = self._validate_image(path)
        elif asset_type == 'video':
            dimensions = self._get_video_dimensions(path)
        
        if not dimensions:
            return None
        
        return {
            "asset_id": path.stem,
            "path": str(path),
            "type": f"{asset_type}/{suffix[1:]}",
            "dimensions": dimensions,
            "file_size_mb": round(file_size_mb, 2),
            "quality_score": quality_score
        }
    
    def _validate_image(self, path: Path) -> Tuple[Dict, float]:
        """Validate image and calculate quality score"""
        try:
            with Image.open(path) as img:
                width, height = img.size
                
                # Check if corrupted
                img.verify()
                
                # Calculate quality score
                min_dim = min(width, height)
                quality_score = min(1.0, min_dim / 2048.0)
                
                # Check minimum dimensions
                if min_dim < self.MIN_DIMENSIONS:
                    quality_score *= 0.7  # Penalty
                
                return {
                    "width": width,
                    "height": height
                }, quality_score
                
        except Exception:
            return None, 0.0
    
    def _get_video_dimensions(self, path: Path) -> Dict:
        """Get video dimensions using ffprobe"""
        import subprocess
        
        try:
            cmd = [
                'ffprobe',
                '-v', 'error',
                '-select_streams', 'v:0',
                '-show_entries', 'stream=width,height',
                '-of', 'json',
                str(path)
            ]
            
            result = subprocess.run(
                cmd, 
                capture_output=True, 
                text=True, 
                timeout=10
            )
            
            if result.returncode == 0:
                data = json.loads(result.stdout)
                stream = data.get('streams', [{}])[0]
                return {
                    "width": stream.get('width', 0),
                    "height": stream.get('height', 0)
                }
        except Exception:
            pass
        
        return None
    
    def _find_missing_assets(
        self, 
        available: List[Dict], 
        required: List[Dict]
    ) -> List[str]:
        """Identify missing assets"""
        available_ids = {asset['asset_id'] for asset in available}
        missing = []
        
        for scene_req in required:
            for required_asset in scene_req.get('requires', []):
                if required_asset not in available_ids:
                    missing.append(required_asset)
        
        return list(set(missing))  # Deduplicate
    
    def _generate_warnings(self, assets: List[Dict]) -> List[Dict]:
        """Generate warnings for assets"""
        warnings = []
        
        for asset in assets:
            dims = asset['dimensions']
            min_dim = min(dims['width'], dims['height'])
            
            # Resolution warnings
            if min_dim < self.MIN_DIMENSIONS:
                warnings.append({
                    "asset_id": asset['asset_id'],
                    "warning": f"Low resolution ({min_dim}px < {self.MIN_DIMENSIONS}px)",
                    "recommendation": "Image may appear pixelated"
                })
            elif min_dim > 4096:
                warnings.append({
                    "asset_id": asset['asset_id'],
                    "warning": f"Very high resolution ({min_dim}px > 4096px)",
                    "recommendation": "Will be downscaled, consider pre-processing"
                })
            
            # File size warnings
            if asset['file_size_mb'] > self.MAX_FILE_SIZE_MB:
                warnings.append({
                    "asset_id": asset['asset_id'],
                    "warning": f"Large file ({asset['file_size_mb']:.1f}MB)",
                    "recommendation": "Consider compressing"
                })
            
            # Quality warnings
            if asset['quality_score'] < 0.7:
                warnings.append({
                    "asset_id": asset['asset_id'],
                    "warning": "Low quality score",
                    "recommendation": "Image may not be suitable for high-quality output"
                })
        
        return warnings
    
    def _determine_status(
        self, 
        available: List[Dict], 
        missing: List[str]
    ) -> str:
        """Determine overall validation status"""
        if len(missing) == 0:
            return "pass"
        elif len(available) > 0:
            return "partial"
        else:
            return "fail"

def main():
    """CLI entry point"""
    try:
        input_data = json.loads(sys.stdin.read())
        validator = AssetValidator()
        output = validator.process(input_data)
        print(json.dumps(output, indent=2))
        sys.exit(0)
    except Exception as e:
        error = {
            "error": str(e),
            "agent_id": "AssetValidator"
        }
        print(json.dumps(error), file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
