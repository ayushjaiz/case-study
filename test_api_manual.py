import requests
import json

# Test the API endpoints
BASE_URL = "http://localhost:5000"

def test_score_endpoint():
    """Test the /score endpoint"""
    print("Testing /score endpoint...")
    
    test_product = {
        "product_name": "Test Bottle",
        "materials": ["aluminum", "plastic"],
        "weight_grams": 300,
        "transport": "air", 
        "packaging": "recyclable",
        "gwp": 5.0,
        "cost": 10.0,
        "circularity": 80.0
    }
    
    try:
        response = requests.post(f"{BASE_URL}/score", json=test_product)
        print(f"Status Code: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
        return response.status_code == 200
    except Exception as e:
        print(f"Error: {e}")
        return False

def test_history_endpoint():
    """Test the /history endpoint"""
    print("\nTesting /history endpoint...")
    
    try:
        response = requests.get(f"{BASE_URL}/history")
        print(f"Status Code: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
        return response.status_code == 200
    except Exception as e:
        print(f"Error: {e}")
        return False

def test_summary_endpoint():
    """Test the /score-summary endpoint"""
    print("\nTesting /score-summary endpoint...")
    
    try:
        response = requests.get(f"{BASE_URL}/score-summary")
        print(f"Status Code: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
        return response.status_code == 200
    except Exception as e:
        print(f"Error: {e}")
        return False

if __name__ == "__main__":
    print("API Test Script")
    print("="*50)
    print("Make sure the Flask app is running on localhost:5000")
    print("Run: python app.py")
    print("="*50)
    
    # Test all endpoints
    score_ok = test_score_endpoint()
    history_ok = test_history_endpoint() 
    summary_ok = test_summary_endpoint()
    
    print("\n" + "="*50)
    print("Test Results:")
    print(f"Score endpoint: {'✓' if score_ok else '✗'}")
    print(f"History endpoint: {'✓' if history_ok else '✗'}")
    print(f"Summary endpoint: {'✓' if summary_ok else '✗'}")