import os
import json
import time
import requests
import base64

# Configuration
API_KEY = os.getenv("RUNPOD_API_KEY")
ENDPOINT_ID = "588osdz7w07dyc"
WORKFLOW_FILE = r"d:\Work\The Conscious Movie Factory December\comfyui-workflows\cmf_i2v_distilled.json"

# A simple 1x1 red pixel PNG for testing (minimal image)
TEST_IMAGE_B64 = "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mP8z8DwHwAFBQIAX8jx0gAAAABJRU5ErkJggg=="

def run_i2v_test():
    if not os.path.exists(WORKFLOW_FILE):
        print(f"Error: Workflow file not found at {WORKFLOW_FILE}")
        return

    with open(WORKFLOW_FILE, 'r') as f:
        workflow = json.load(f)

    # Modify the workflow to use our test image
    # Node 34 is LoadImage - we'll upload an image first
    
    url = f"https://api.runpod.ai/v2/{ENDPOINT_ID}/run"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {API_KEY}"
    }
    
    # For I2V test, we need to provide an input image
    # The workflow expects an image file, so we'll include it as base64
    payload = {
        "input": {
            "workflow": workflow,
            "images": [
                {
                    "name": "test_hero.png",
                    "image": f"data:image/png;base64,{TEST_IMAGE_B64}"
                }
            ]
        }
    }
    
    # Update the workflow to use our uploaded image
    if "34" in workflow:
        workflow["34"]["inputs"]["image"] = "test_hero.png"

    print(f"Sending I2V workflow to RunPod Endpoint {ENDPOINT_ID}...")
    print("Note: I2V takes longer than T2I (model loading + video generation)")
    
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

    # Poll status with longer timeout check
    status_url = f"https://api.runpod.ai/v2/{ENDPOINT_ID}/status/{job_id}"
    start_time = time.time()
    max_wait = 600  # 10 minutes max
    
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
                print("Output Data:")
                print(json.dumps(output, indent=2)[:2000])  # Truncate large base64
                break
            elif status == 'FAILED':
                print("Job Failed!")
                print(f"Error: {r_data.get('error')}")
                break
            
            time.sleep(5)  # Longer polling interval for I2V
        except Exception as e:
            print(f"Error polling status: {e}")
            break
    else:
        print(f"Timeout after {max_wait}s")

if __name__ == "__main__":
    run_i2v_test()
