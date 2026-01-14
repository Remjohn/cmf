import os
import requests
import base64
import json
from dotenv import load_dotenv

def save_last_video():
    # Hardcoded to match test_i2v_workflow.py
    api_key = os.getenv("RUNPOD_API_KEY")
    endpoint_id = "588osdz7w07dyc"
    job_id = "5aa43f94-9634-4642-97ad-42f17711edac-e2"
    
    print(f"Fetching job {job_id} from endpoint {endpoint_id}...")
    url = f"https://api.runpod.ai/v2/{endpoint_id}/status/{job_id}"
    headers = {"Authorization": f"Bearer {api_key}"}
    
    try:
        resp_raw = requests.get(url, headers=headers)
        if resp_raw.status_code != 200:
            print(f"Error: HTTP {resp_raw.status_code}")
            print(resp_raw.text)
            return
            
        resp = resp_raw.json()
        if 'output' in resp and resp['output'] and 'videos' in resp['output'] and len(resp['output']['videos']) > 0:
            data = resp['output']['videos'][0]['data']
            os.makedirs('outputs', exist_ok=True)
            output_path = 'outputs/test_i2v_output.mp4'
            with open(output_path, 'wb') as f:
                f.write(base64.b64decode(data))
            print(f"Success! Video saved to: {output_path}")
        else:
            print("No video found in job output.")
            print(json.dumps(resp, indent=2))
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    save_last_video()
