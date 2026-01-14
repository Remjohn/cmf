import os
import json
import time
import requests
import base64
import random

# Configuration
API_KEY = os.getenv("RUNPOD_API_KEY")
ENDPOINT_ID = "588osdz7w07dyc"
# Using Z-Image Turbo as fallback since Qwen isn't loading
WORKFLOW_FILE = r"d:\Work\The Conscious Movie Factory December\comfyui-workflows\cmf_t2i_hero.json"

def run_gmg_test():
    if not os.path.exists(WORKFLOW_FILE):
        print(f"Error: Workflow file not found at {WORKFLOW_FILE}")
        return

    with open(WORKFLOW_FILE, 'r') as f:
        workflow = json.load(f)

    # GMG Test Prompt - using Z-Image Turbo with text focus
    prompt_text = "Big bold 3D typography 'TRANSFORM' made of glowing golden particles, floating in cosmic void with nebula colors, ethereal light rays, professional design, centered composition, vertical 9:16, cinemati, 8k"
    
    # Update Positive Prompt (Node 45)
    if "45" in workflow:
        workflow["45"]["inputs"]["text"] = prompt_text
        print(f"Set prompt: {prompt_text[:80]}...")

    # Randomize Seed (Node 44)
    if "44" in workflow:
        seed = random.randint(1, 9999999999)
        workflow["44"]["inputs"]["seed"] = seed
        print(f"Set seed: {seed}")

    # Set Filename Prefix (Node 48)
    if "48" in workflow:
        workflow["48"]["inputs"]["filename_prefix"] = "TEST_GMG_Turbo"

    url = f"https://api.runpod.ai/v2/{ENDPOINT_ID}/run"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {API_KEY}"
    }
    
    payload = {
        "input": {
            "workflow": workflow
        }
    }
    
    print(f"Sending GMG workflow (Z-Image Turbo fallback) to RunPod...")
    
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
    max_wait = 300
    
    while time.time() - start_time < max_wait:
        try:
            r = requests.get(status_url, headers=headers)
            r_data = r.json()
            status = r_data.get('status')
            elapsed = int(time.time() - start_time)
            print(f"Status: {status} ({elapsed}s elapsed)")
            
            if status == 'COMPLETED':
                print("Job Completed Successfully!")
                output = r_data.get('output')
                
                if output and 'images' in output:
                    for img in output['images']:
                        img_data = base64.b64decode(img['image'])
                        filename = f"outputs/test_gmg_turbo_{job_id}.png"
                        os.makedirs('outputs', exist_ok=True)
                        with open(filename, 'wb') as f:
                            f.write(img_data)
                        print(f"Saved image to: {filename}")
                else:
                    print("No images found in output.")
                break
                
            elif status == 'FAILED':
                print("Job Failed!")
                print(f"Error: {r_data.get('error')}")
                break
            
            time.sleep(2)
        except Exception as e:
            print(f"Error polling status: {e}")
            break
    else:
        print(f"Timeout after {max_wait}s")

if __name__ == "__main__":
    run_gmg_test()
