import os
import json
import time
import requests

# Configuration
API_KEY = os.getenv("RUNPOD_API_KEY")
ENDPOINT_ID = "588osdz7w07dyc"

# Last failed job ID from GMG test
JOB_ID = "73e5d479-90fb-4462-a00e-ce57573fd6a3-e2"

def get_job_details():
    """Fetch detailed error information from a failed job"""
    url = f"https://api.runpod.ai/v2/{ENDPOINT_ID}/status/{JOB_ID}"
    headers = {"Authorization": f"Bearer {API_KEY}"}
    
    print(f"Fetching details for job: {JOB_ID}")
    
    try:
        r = requests.get(url, headers=headers)
        data = r.json()
        print("\n=== Full Job Response ===")
        print(json.dumps(data, indent=2))
        
        if 'error' in data:
            print(f"\n=== ERROR ===\n{data['error']}")
            
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    get_job_details()
