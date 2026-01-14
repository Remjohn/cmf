"""
Test for cmf_image_edit.json workflow (Qwen Image Edit / Img2Img variant creation)
Uses the successful GMG Qwen output as input to create a first-frame variant
"""
import os
import json
import time
import requests
import base64
import random

# Configuration
API_KEY = os.getenv("RUNPOD_API_KEY")
ENDPOINT_ID = "588osdz7w07dyc"
WORKFLOW_FILE = r"d:\Work\The Conscious Movie Factory December\comfyui-workflows\cmf_image_edit.json"
INPUT_IMAGE = r"d:\Work\The Conscious Movie Factory December\outputs\test_gmg_qwen_SUCCESS.png"

def run_image_edit_test():
    if not os.path.exists(WORKFLOW_FILE):
        print(f"Error: Workflow not found at {WORKFLOW_FILE}")
        return
    
    if not os.path.exists(INPUT_IMAGE):
        print(f"Error: Input image not found at {INPUT_IMAGE}")
        return

    with open(WORKFLOW_FILE, 'r') as f:
        workflow = json.load(f)

    # Read input image and encode to base64
    with open(INPUT_IMAGE, 'rb') as f:
        img_data = base64.b64encode(f.read()).decode('utf-8')
    
    print(f"Loaded input image: {INPUT_IMAGE}")

    # Prepare images for upload
    images = [{
        "name": "gmg_last_frame.png",
        "image": img_data
    }]

    # Update workflow to use our uploaded image
    workflow["1"]["inputs"]["image"] = "gmg_last_frame.png"
    
    # Set edit prompt - create a subtle variant for first frame
    edit_prompt = "Same image with slightly brighter glow, subtle particle movement suggestion, ethereal light"
    workflow["5"]["inputs"]["text"] = edit_prompt
    print(f"Edit prompt: {edit_prompt}")

    # Randomize seed
    seed = random.randint(1, 9999999999)
    workflow["9"]["inputs"]["seed"] = seed
    print(f"Seed: {seed}")

    # Update filename prefix
    workflow["11"]["inputs"]["filename_prefix"] = "TEST_IMG_EDIT"

    url = f"https://api.runpod.ai/v2/{ENDPOINT_ID}/run"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {API_KEY}"
    }
    
    payload = {
        "input": {
            "workflow": workflow,
            "images": images
        }
    }
    
    print(f"Sending Image Edit workflow to RunPod...")
    
    try:
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()
        data = response.json()
        job_id = data.get('id')
        print(f"Job started! ID: {job_id}")
    except Exception as e:
        print(f"Failed to start job: {e}")
        if 'response' in locals():
            print(f"Response: {response.text}")
        return

    # Poll status
    status_url = f"https://api.runpod.ai/v2/{ENDPOINT_ID}/status/{job_id}"
    start_time = time.time()
    max_wait = 600  # 10 minutes - Img2Img with Z-Image Turbo is fast
    
    while time.time() - start_time < max_wait:
        try:
            r = requests.get(status_url, headers=headers)
            r_data = r.json()
            status = r_data.get('status')
            elapsed = int(time.time() - start_time)
            print(f"Status: {status} ({elapsed}s elapsed)")
            
            if status == 'COMPLETED':
                print("Job Completed Successfully!")
                output = r_data.get('output', {})
                
                if 'images' in output:
                    for i, img in enumerate(output['images']):
                        img_bytes = base64.b64decode(img['data'])
                        filename = f"outputs/test_image_edit_{job_id}.png"
                        os.makedirs('outputs', exist_ok=True)
                        with open(filename, 'wb') as f:
                            f.write(img_bytes)
                        print(f"Saved: {filename}")
                else:
                    print("No images found in output.")
                    print(json.dumps(output, indent=2)[:500])
                break
                
            elif status == 'FAILED':
                print("Job Failed!")
                print(f"Error: {r_data.get('error')}")
                break
            
            time.sleep(3)
        except Exception as e:
            print(f"Error polling status: {e}")
            break
    else:
        print(f"Timeout after {max_wait}s")

if __name__ == "__main__":
    run_image_edit_test()
