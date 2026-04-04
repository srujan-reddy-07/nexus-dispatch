import requests
import json

def test_inference():
    # Hugging Face local URL inside the container
    url = "http://0.0.0.0:7860/health"
    
    try:
        response = requests.get(url)
        print(f"Health Check Status: {response.status_code}")
        print(f"Response: {response.json()}")
    except Exception as e:
        print(f"Inference test failed: {e}")

if __name__ == "__main__":
    print("Starting Nexus Dispatch Inference Test...")
    test_inference()
