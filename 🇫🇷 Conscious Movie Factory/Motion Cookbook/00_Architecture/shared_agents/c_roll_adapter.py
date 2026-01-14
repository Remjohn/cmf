
import os
import json
import time
import requests
import base64
from typing import Dict, List, Optional, Union
from pathlib import Path

# --- Configuration ---

# Hardcoded fallback from run_batch_generation.py to ensure it works "out of the box"
RUNPOD_API_KEY_FALLBACK = os.getenv("RUNPOD_API_KEY")
ENDPOINT_ID = "5o28xoxum6y488" # Deployed Jan 8, 2026
BASE_URL = f"https://api.runpod.ai/v2/{ENDPOINT_ID}"

# Paths to workflows (relative to workspace root usually, but we need absolute or robust finding)
# We will assume this file is in Motion Cookbook/00_Architecture/shared_agents
# Workflows are in D:/Work/The Conscious Movie Factory December/...
WORKSPACE_ROOT = r"D:\Work\The Conscious Movie Factory December"
WORKFLOW_Z_IMAGE = os.path.join(WORKSPACE_ROOT, "cmf-comfyui-serverless", "test_z_image.json")
WORKFLOW_WAN = os.path.join(WORKSPACE_ROOT, "CMF labo", "Wan 2.2 i2v Strong dynamics_api.json")

# --- RunPod Client ---

class RunPodClient:
    def __init__(self):
        self.api_key = os.getenv("RUNPOD_API_KEY", RUNPOD_API_KEY_FALLBACK)
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

    def load_workflow(self, path):
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
            if "input" in data and "workflow" in data["input"]:
                return data["input"]["workflow"]
            return data

    def run_job(self, workflow, images=None):
        payload = {"input": {"workflow": workflow}}
        if images:
            payload["input"]["images"] = images
            
        print(f"    Submitting Job to RunPod...")
        try:
            resp = requests.post(f"{BASE_URL}/run", headers=self.headers, json=payload, timeout=30)
            resp.raise_for_status()
            result = resp.json()
            job_id = result["id"]
        except Exception as e:
            print(f"    Error submitting job: {e}")
            return None

        # Poll
        start_time = time.time()
        while True:
            if time.time() - start_time > 600: # 10 min
                print("    Timeout waiting for job")
                return None
                
            time.sleep(5)
            try:
                status_resp = requests.get(f"{BASE_URL}/status/{job_id}", headers=self.headers, timeout=30)
                status = status_resp.json()
                state = status.get("status", "UNKNOWN")
                
                if state == "COMPLETED":
                    print(f"    DEBUG: Full RunPod Response: {json.dumps(status)}")
                    return status.get("output", {})
                elif state == "FAILED":
                    print(f"    Job failed: {status.get('error')}")
                    print(f"    DEBUG: Full RunPod Response: {json.dumps(status)}")
                    return None
            except Exception as e:
                print(f"    Error polling status: {e}")
                time.sleep(5)

    def save_images(self, output, prefix, save_dir):
        if not output or "images" not in output: return None
        saved_paths = []
        for idx, img in enumerate(output["images"]):
            image_data = img.get("data")
            if image_data:
                img_bytes = base64.b64decode(image_data)
                filename = f"{prefix}_{idx}.png"
                filepath = os.path.join(save_dir, filename)
                with open(filepath, "wb") as f:
                    f.write(img_bytes)
                saved_paths.append(filepath)
        return saved_paths[0] if saved_paths else None

    def save_video(self, output, prefix, save_dir):
        if not output: return None
        
        # VHS outputs videos under 'gifs' key, also check 'videos' and 'images'
        video_items = []
        for key in ["gifs", "videos", "images"]:
            if key in output:
                print(f"    DEBUG: Found '{key}' key with {len(output[key])} items")
                video_items.extend(output[key])
        
        if not video_items:
            print(f"    No video outputs found. Keys in output: {output.keys() if output else 'N/A'}")
            return None
        
        print(f"    DEBUG: Processing {len(video_items)} video items")
        for i, item in enumerate(video_items[:2]):  # Show first 2 items
            print(f"    DEBUG: Item {i} keys: {item.keys() if isinstance(item, dict) else type(item)}")
            if isinstance(item, dict):
                print(f"    DEBUG: Item {i} filename: {item.get('filename')}, has_data: {'data' in item}")
            
        saved_paths = []
        for idx, item in enumerate(video_items):
            image_data = item.get("data")
            filename_orig = item.get("filename", "")
            ext = os.path.splitext(filename_orig)[1] or ".mp4"
            
            if image_data:
                img_bytes = base64.b64decode(image_data)
                filename = f"{prefix}{ext}"
                filepath = os.path.join(save_dir, filename)
                with open(filepath, "wb") as f:
                    f.write(img_bytes)
                saved_paths.append(filepath)
                print(f"    Saved video: {filepath} ({len(img_bytes)} bytes)")
            else:
                print(f"    DEBUG: Item {idx} has no 'data' field")
        return saved_paths[0] if saved_paths else None

# --- Model Wrappers ---

class ZImageTurbo:
    def __init__(self):
        self.client = RunPodClient()
        self.workflow_template = self.client.load_workflow(WORKFLOW_Z_IMAGE)

    def generate(self, prompt: str, width: int = 1080, height: int = 1920, 
                 negative_prompt: str = "", seed: int = None, output_path: str = None) -> str:
        print(f"Generating image with Z-Image Turbo (RunPod): '{prompt[:50]}...'")
        
        # Modify Workflow
        wf = json.loads(json.dumps(self.workflow_template)) # Deep copy
        
        # Node 45: Text Prompt
        wf["45"]["inputs"]["text"] = prompt
        
        # Node 41: Dimensions (Z-Image uses 768x1344 by default in template, we try to override if supported, or stick to template)
        # Template has 768x1344. Z-Image Turbo supports 1080x1920? 
        # Let's set it to user request, closest multiple of 16 usually good.
        wf["41"]["inputs"]["width"] = width
        wf["41"]["inputs"]["height"] = height
        
        # Node 44: Seed
        if seed: wf["44"]["inputs"]["seed"] = seed
        
        # Node 9: Filename Prefix
        prefix = Path(output_path).stem if output_path else "z_image_out"
        wf["9"]["inputs"]["filename_prefix"] = prefix

        output = self.client.run_job(wf)
        
        # Save output
        save_dir = os.path.dirname(output_path) if output_path else os.getcwd()
        result_path = self.client.save_images(output, prefix, save_dir)
        
        # Rename if exact output_path was requested and filename differs (RunPod adds _0001 counter usually)
        if result_path and output_path and result_path != output_path:
            # Simple rename or copy logic if needed, but save_images uses prefix_0.png
            # If output_path is 'foo/bar.png', result is 'foo/bar_0.png'.
            # We rename 'foo/bar_0.png' to 'foo/bar.png'
            try:
                if os.path.exists(output_path): os.remove(output_path)
                os.rename(result_path, output_path)
                return output_path
            except Exception as e:
                print(f"Warning renaming file: {e}")
                return result_path
        return result_path or output_path

    def _create_placeholder(self, path, w, h, text):
        # Fallback for mock if needed, but we try real gen
        pass

class Wan2_2:
    def __init__(self):
        self.client = RunPodClient()
        self.workflow_template = self.client.load_workflow(WORKFLOW_WAN)

    def animate(self, image_path: str, prompt: str, duration: float = 5.0, 
                motion_strength: float = 0.5, fps: int = 24, output_path: str = None) -> str:
        print(f"Animating {Path(image_path).name} with Wan 2.2 (RunPod)...")
        
        if not os.path.exists(image_path):
            print(f"Error: Input image {image_path} does not exist.")
            return None

        # Read Input Image for Upload
        with open(image_path, "rb") as f:
            img_b64 = base64.b64encode(f.read()).decode('utf-8')
        
        upload_filename = f"source_{Path(image_path).name}"
        upload_payload = [{"name": upload_filename, "image": img_b64}]

        # Modify Workflow
        wf = json.loads(json.dumps(self.workflow_template))
        
        # Node 29: Prompt
        wf["29"]["inputs"]["text"] = prompt
        
        # Node 34: Load Image
        wf["34"]["inputs"]["image"] = upload_filename
        
        # Node 19: Filename Prefix (VHS) - with save_output fix
        prefix = Path(output_path).stem if output_path else "wan_video_out"
        if "19" in wf:
             wf["19"]["inputs"]["filename_prefix"] = prefix
             wf["19"]["inputs"]["save_output"] = True  # Critical fix!
        
        output = self.client.run_job(wf, images=upload_payload)
        
        save_dir = os.path.dirname(output_path) if output_path else os.getcwd()
        result_path = self.client.save_video(output, prefix, save_dir)
        
        if result_path and output_path and result_path != output_path:
             try:
                if os.path.exists(output_path): os.remove(output_path)
                os.rename(result_path, output_path)
                return output_path
             except Exception as e:
                return result_path
        return result_path or output_path

class QwenImageEdit:
    def __init__(self):
        self.client = RunPodClient()
        # No workflow template for Qwen yet, keeping as Simulation/Placeholder
    
    def edit(self, image_path: str, instruction: str, output_path: str = None) -> str:
        print(f"Editing {Path(image_path).name} (Simulated): '{instruction}'")
        # Just copy input to output for now or CREATE Placeholder
        if output_path:
             with open(output_path, 'w') as f: f.write("SIMULATED EDIT")
        return output_path

# --- Factory Wrappers ---

z_image_turbo = ZImageTurbo()
wan_2_2 = Wan2_2()
qwen_image_edit = QwenImageEdit()
