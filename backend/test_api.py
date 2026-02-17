"""
test_api.py - Simple script to test your Nitro AI backend
Run this after starting your server to verify everything works!
"""

import requests
import json
from datetime import datetime

# Configuration
BASE_URL = "http://localhost:8000"

# Color codes for terminal output (makes it pretty!)
GREEN = '\033[92m'
RED = '\033[91m'
YELLOW = '\033[93m'
BLUE = '\033[94m'
RESET = '\033[0m'

def print_success(message):
    """Print success message in green"""
    print(f"{GREEN}✓ {message}{RESET}")

def print_error(message):
    """Print error message in red"""
    print(f"{RED}✗ {message}{RESET}")

def print_info(message):
    """Print info message in blue"""
    print(f"{BLUE}ℹ {message}{RESET}")

def print_test(message):
    """Print test header in yellow"""
    print(f"\n{YELLOW}{'='*60}")
    print(f"  {message}")
    print(f"{'='*60}{RESET}\n")

def test_root_endpoint():
    """Test GET / endpoint"""
    print_test("TEST 1: Root Endpoint (GET /)")
    
    try:
        response = requests.get(f"{BASE_URL}/")
        
        if response.status_code == 200:
            data = response.json()
            print_success("Server is running!")
            print_info(f"Response: {json.dumps(data, indent=2)}")
            return True
        else:
            print_error(f"Unexpected status code: {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print_error("Cannot connect to server. Is it running?")
        print_info("Start server with: uvicorn main:app --reload")
        return False
    except Exception as e:
        print_error(f"Error: {str(e)}")
        return False

def test_health_endpoint():
    """Test GET /health endpoint"""
    print_test("TEST 2: Health Check (GET /health)")
    
    try:
        response = requests.get(f"{BASE_URL}/health")
        
        if response.status_code == 200:
            data = response.json()
            print_success("Health check passed!")
            print_info(f"Status: {data.get('status')}")
            print_info(f"Version: {data.get('version')}")
            print_info(f"Timestamp: {data.get('timestamp')}")
            return True
        else:
            print_error(f"Health check failed: {response.status_code}")
            return False
    except Exception as e:
        print_error(f"Error: {str(e)}")
        return False

def test_chat_endpoint():
    """Test POST /chat endpoint"""
    print_test("TEST 3: Chat Endpoint (POST /chat)")
    
    # Test data
    test_message = {
        "message": "Hello Nitro AI! This is a test message.",
        "user_id": "test_user"
    }
    
    try:
        response = requests.post(
            f"{BASE_URL}/chat",
            json=test_message,
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code == 200:
            data = response.json()
            print_success("Chat endpoint working!")
            print_info(f"Your message: {test_message['message']}")
            print_info(f"AI response: {data.get('response')}")
            print_info(f"Status: {data.get('status')}")
            print_info(f"Timestamp: {data.get('timestamp')}")
            return True
        else:
            print_error(f"Chat failed: {response.status_code}")
            print_info(f"Response: {response.text}")
            return False
    except Exception as e:
        print_error(f"Error: {str(e)}")
        return False

def test_chat_validation():
    """Test that empty messages are rejected"""
    print_test("TEST 4: Input Validation (Empty Message)")
    
    # Test with empty message (should fail)
    invalid_message = {
        "message": "   ",  # Just whitespace
        "user_id": "test_user"
    }
    
    try:
        response = requests.post(
            f"{BASE_URL}/chat",
            json=invalid_message,
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code == 422:  # Validation error expected
            print_success("Validation working! Empty messages are rejected.")
            return True
        else:
            print_error(f"Validation not working properly: {response.status_code}")
            return False
    except Exception as e:
        print_error(f"Error: {str(e)}")
        return False

def test_docs_endpoint():
    """Test that API docs are accessible"""
    print_test("TEST 5: API Documentation (GET /docs)")
    
    try:
        response = requests.get(f"{BASE_URL}/docs")
        
        if response.status_code == 200:
            print_success("API documentation is accessible!")
            print_info(f"Visit: {BASE_URL}/docs in your browser")
            return True
        else:
            print_error(f"Documentation not accessible: {response.status_code}")
            return False
    except Exception as e:
        print_error(f"Error: {str(e)}")
        return False

def run_all_tests():
    """Run all tests and show summary"""
    print(f"\n{BLUE}{'*'*60}")
    print(f"  NITRO AI BACKEND - API TESTING SUITE")
    print(f"  Testing server at: {BASE_URL}")
    print(f"  Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"{'*'*60}{RESET}\n")
    
    # Run all tests
    results = []
    results.append(("Root Endpoint", test_root_endpoint()))
    results.append(("Health Check", test_health_endpoint()))
    results.append(("Chat Endpoint", test_chat_endpoint()))
    results.append(("Input Validation", test_chat_validation()))
    results.append(("API Documentation", test_docs_endpoint()))
    
    # Print summary
    print_test("TEST SUMMARY")
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        if result:
            print_success(f"{test_name}")
        else:
            print_error(f"{test_name}")
    
    print(f"\n{BLUE}{'='*60}{RESET}")
    if passed == total:
        print_success(f"ALL TESTS PASSED! ({passed}/{total})")
        print_success("Your Nitro AI backend is working perfectly! 🎉")
    else:
        print_error(f"SOME TESTS FAILED ({passed}/{total} passed)")
        print_info("Check the errors above and fix them.")
    print(f"{BLUE}{'='*60}{RESET}\n")

if __name__ == "__main__":
    print_info("Make sure your server is running before running tests!")
    print_info("Start server: uvicorn main:app --reload\n")
    
    input("Press Enter to start testing...")
    
    run_all_tests()
    
    print_info("\nFor interactive testing, visit: http://localhost:8000/docs")
