import os
import json
import time
import requests
import base64
import random

# Configuration
API_KEY = os.getenv("RUNPOD_API_KEY")
ENDPOINT_ID = "588osdz7w07dyc"
WORKFLOW_FILE = r"d:\Work\The Conscious Movie Factory December\comfyui-workflows\cmf_gmg_qwen.json"

def run_gmg_test():
    if not os.path.exists(WORKFLOW_FILE):
        print(f"Error: Workflow file not found at {WORKFLOW_FILE}")
        return

    with open(WORKFLOW_FILE, 'r') as f:
        workflow = json.load(f)

    # GMG Test Prompt with embedded typography
    prompt_text = "Big bold 3D text 'TRANSFORM' made of glowing golden particles, floating in a cosmic void with subtle nebula colors, ethereal glow, professional typography, centered composition, vertical, 9:16, cinematic lighting"
    
    # Find and update the positive prompt node
    # The Qwen workflow uses a different node structure - need to find CLIPTextEncode for positive
    prompt_updated = False
    for node_id, node in workflow.items():
        if isinstance(node, dict) and node.get("class_type") == "CLIPTextEncode":
            title = node.get("_meta", {}).get("title", "")
            if "Positive" in title or "positive" in title.lower():
                if "widgets_values" in node:
                    node["widgets_values"] = [prompt_text]
                    prompt_updated = True
                    print(f"Updated positive prompt in node {node_id}")
                elif "inputs" in node and "text" in node["inputs"]:
                    node["inputs"]["text"] = prompt_text
                    prompt_updated = True
                    print(f"Updated positive prompt in node {node_id}")
    
    if not prompt_updated:
        print("Warning: Could not find positive prompt node to update")
        # Try to find any text encode node
        for node_id, node in workflow.items():
            if isinstance(node, dict) and node.get("class_type") == "CLIPTextEncode":
                if "widgets_values" in node and len(node["widgets_values"]) > 0:
                    node["widgets_values"][0] = prompt_text
                    print(f"Updated prompt in node {node_id}")
                    break

    # Randomize seed if KSampler exists
    for node_id, node in workflow.items():
        if isinstance(node, dict) and node.get("class_type") == "KSampler":
            if "widgets_values" in node:
                node["widgets_values"][0] = random.randint(1, 9999999999)
                print(f"Randomized seed in node {node_id}")

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
    
    print(f"Sending GMG workflow (Qwen-Image-2512) to RunPod...")
    print(f"Prompt: {prompt_text[:80]}...")
    
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

    # Poll status - Qwen takes longer, give it 10 minutes
    status_url = f"https://api.runpod.ai/v2/{ENDPOINT_ID}/status/{job_id}"
    start_time = time.time()
    max_wait = 900  # 15 minutes for Qwen cold starts
    
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
                    for i, img in enumerate(output['images']):
                        img_data = base64.b64decode(img['image'])
                        filename = f"outputs/test_gmg_{job_id}.png"
                        os.makedirs('outputs', exist_ok=True)
                        with open(filename, 'wb') as f:
                            f.write(img_data)
                        print(f"Saved image to: {filename}")
                else:
                    print("No images found in output.")
                    print(json.dumps(output, indent=2)[:500])
                break
                
            elif status == 'FAILED':
                print("Job Failed!")
                print(f"Error: {r_data.get('error')}")
                break
            
            time.sleep(5)
        except Exception as e:
            print(f"Error polling status: {e}")
            break
    else:
        print(f"Timeout after {max_wait}s - job may still be running")
        print(f"Job ID: {job_id}")

if __name__ == "__main__":
    run_gmg_test()
