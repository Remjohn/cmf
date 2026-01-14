import os
import json
import time
import requests
import base64

# Configuration
API_KEY = os.getenv("RUNPOD_API_KEY")
ENDPOINT_ID = "588osdz7w07dyc"

def test_workflow(workflow_file, workflow_name):
    """Test a workflow and return the result"""
    print(f"\n{'='*60}")
    print(f"Testing: {workflow_name}")
    print(f"File: {workflow_file}")
    print(f"{'='*60}")
    
    if not os.path.exists(workflow_file):
        print(f"ERROR: File not found")
        return {"status": "FILE_NOT_FOUND"}
    
    with open(workflow_file, 'r') as f:
        workflow = json.load(f)
    
    url = f"https://api.runpod.ai/v2/{ENDPOINT_ID}/run"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {API_KEY}"
    }
    
    payload = {"input": {"workflow": workflow}}
    
    try:
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()
        data = response.json()
        job_id = data.get('id')
        print(f"Job started! ID: {job_id}")
    except Exception as e:
        print(f"Failed to start job: {e}")
        return {"status": "FAILED_TO_START", "error": str(e)}
    
    # Poll status
    status_url = f"https://api.runpod.ai/v2/{ENDPOINT_ID}/status/{job_id}"
    start_time = time.time()
    max_wait = 120  # 2 min per workflow
    
    while time.time() - start_time < max_wait:
        try:
            r = requests.get(status_url, headers=headers)
            r_data = r.json()
            status = r_data.get('status')
            elapsed = int(time.time() - start_time)
            print(f"Status: {status} ({elapsed}s)")
            
            if status == 'COMPLETED':
                print("✅ COMPLETED!")
                return {"status": "COMPLETED", "output": r_data.get('output')}
            elif status == 'FAILED':
                error = r_data.get('error', 'Unknown error')
                print(f"❌ FAILED: {error}")
                return {"status": "FAILED", "error": error}
            
            time.sleep(5)
        except Exception as e:
            print(f"Poll error: {e}")
            break
    
    return {"status": "TIMEOUT"}

def main():
    base_path = r"d:\Work\The Conscious Movie Factory December\comfyui-workflows"
    
    workflows = [
        ("cmf_video_upscale.json", "Video Upscale (FlashVSR)"),
        ("cmf_image_edit.json", "Image Edit (Img2Img)"),
    ]
    
    results = {}
    for filename, name in workflows:
        filepath = os.path.join(base_path, filename)
        results[name] = test_workflow(filepath, name)
    
    print("\n" + "="*60)
    print("SUMMARY")
    print("="*60)
    for name, result in results.items():
        status = result.get('status', 'UNKNOWN')
        error = result.get('error', '')[:80] if result.get('error') else ''
        print(f"{status:15} | {name}")
        if error:
            print(f"               | Error: {error}")

if __name__ == "__main__":
    main()
