import requests
import json
import sys

def verify_cricapi(api_key):
    url = f"https://api.cricapi.com/v1/matches?apikey={api_key}&offset=0"
    try:
        print(f"Pinging CricAPI with key: {api_key}...")
        response = requests.get(url, timeout=10)
        status = response.status_code
        print(f"HTTP Status: {status}")
        
        data = response.json()
        print(f"API Response Info: {data.get('info', 'No Info Field')}")
        print(f"API Response Status: {data.get('status', 'No Status Field')}")
        
        matches = data.get('data', [])
        print(f"Matches Found: {len(matches)}")
        
        if len(matches) > 0:
            print("\nSample Match Data:")
            print(json.dumps(matches[0], indent=2))
            
    except Exception as e:
        print(f"Verification Failed: {e}")

if __name__ == '__main__':
    verify_cricapi("a6177fed-ecff-44e0-8e3a-2c1af4efad0c")
