import os
import json
import time
import requests
import sys

# Configuration
API_KEY = os.getenv("RUNPOD_API_KEY")
ENDPOINT_ID = "588osdz7w07dyc"
WORKFLOW_FILE = r"d:\Work\The Conscious Movie Factory December\comfyui-workflows\cmf_t2i_hero.json"

def run_workflow():
    if not os.path.exists(WORKFLOW_FILE):
        print(f"Error: Workflow file not found at {WORKFLOW_FILE}")
        return

    with open(WORKFLOW_FILE, 'r') as f:
        workflow = json.load(f)

    url = f"https://api.runpod.ai/v2/{ENDPOINT_ID}/run"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {API_KEY}"
    }
    
    # Payload structure for ComfyUI Serverless usually expects 'workflow' in input
    payload = {
        "input": {
            "workflow": workflow
        }
    }

    print(f"Sending workflow to RunPod Endpoint {ENDPOINT_ID}...")
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
    
    while True:
        try:
            r = requests.get(status_url, headers=headers)
            r_data = r.json()
            status = r_data.get('status')
            print(f"Status: {status}")
            
            if status == 'COMPLETED':
                print("Job Completed Successfully!")
                output = r_data.get('output')
                print("Output Data:")
                print(json.dumps(output, indent=2))
                break
            elif status == 'FAILED':
                print("Job Failed!")
                print(f"Error: {r_data.get('error')}")
                break
            
            time.sleep(2)
        except Exception as e:
            print(f"Error polling status: {e}")
            break

if __name__ == "__main__":
    run_workflow()
