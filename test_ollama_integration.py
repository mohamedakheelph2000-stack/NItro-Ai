# Test Ollama Integration with Nitro AI
# This script tests if phi3 model is connected and working

import requests
import json
import sys

print("🧪 Testing Nitro AI + Ollama (phi3) Integration")
print("=" * 60)

# Test 1: Backend Health Check
print("\n📋 Test 1: Backend Health Check...")
try:
    response = requests.get("http://localhost:8000/health")
    if response.status_code == 200:
        print("✅ Backend is running!")
        print(f"   Response: {response.json()}")
    else:
        print(f"❌ Backend returned status {response.status_code}")
        sys.exit(1)
except Exception as e:
    print(f"❌ Cannot connect to backend: {e}")
    print("   Make sure backend is running: python -m uvicorn main:app --reload")
    sys.exit(1)

# Test 2: Ollama Server Check
print("\n📋 Test 2: Ollama Server Check...")
try:
    response = requests.get("http://localhost:11434/api/tags")
    if response.status_code == 200:
        models = response.json().get('models', [])
        model_names = [m['name'] for m in models]
        print(f"✅ Ollama is running!")
        print(f"   Available models: {model_names}")
        
        if any('phi3' in name for name in model_names):
            print("   ✅ phi3 model found!")
        else:
            print("   ⚠️  phi3 not found. Run: ollama pull phi3")
    else:
        print(f"❌ Ollama returned status {response.status_code}")
except Exception as e:
    print(f"❌ Cannot connect to Ollama: {e}")
    print("   Make sure Ollama is running: ollama serve")
    print("   Or it may auto-start in background")

# Test 3: Simple Chat (Non-AI, should work even without Ollama)
print("\n📋 Test 3: Basic Chat Endpoint...")
try:
    payload = {
        "message": "Hello!",
        "user_id": "test_user"
    }
    response = requests.post(
        "http://localhost:8000/chat",
        json=payload,
        headers={"Content-Type": "application/json"}
    )
    
    if response.status_code == 200:
        result = response.json()
        print("✅ Chat endpoint working!")
        print(f"   Response: {result.get('response', 'No response')[:100]}...")
    else:
        print(f"❌ Chat returned status {response.status_code}")
        print(f"   Error: {response.text}")
except Exception as e:
    print(f"❌ Chat test failed: {e}")

# Test 4: AI Chat (Requires Ollama + phi3)
print("\n📋 Test 4: Real AI Chat with phi3...")
print("   (This will take 10-30 seconds on first run as phi3 loads)")
try:
    payload = {
        "message": "What is 2+2? Answer in one short sentence.",
        "user_id": "test_user"
    }
    
    print("   Sending request to Ollama...")
    response = requests.post(
        "http://localhost:8000/chat",
        json=payload,
        headers={"Content-Type": "application/json"},
        timeout=60  # 60 second timeout
    )
    
    if response.status_code == 200:
        result = response.json()
        ai_response = result.get('response', '')
        print("✅ AI Chat working!")
        print(f"   Question: {payload['message']}")
        print(f"   AI Answer: {ai_response}")
        
        # Check if it's a real AI response (not dummy)
        if "phi3" in ai_response.lower() or "4" in ai_response:
            print("   ✅ Real AI response detected!")
        else:
            print("   ℹ️  Response received (may be fallback if Ollama not ready)")
    else:
        print(f"❌ AI Chat returned status {response.status_code}")
        print(f"   Error: {response.text}")
except requests.Timeout:
    print("⏱️  Request timed out (Ollama might be loading phi3 for first time)")
    print("   Try again in a moment - model should be loaded now")
except Exception as e:
    print(f"❌ AI Chat test failed: {e}")

# Summary
print("\n" + "=" * 60)
print("🎯 Test Summary:")
print("   - Backend running on http://localhost:8000")
print("   - Interactive docs: http://localhost:8000/docs")
print("   - Open frontend/index.html to test in browser!")
print("\n   If all tests passed: Your Nitro AI is ready! 🚀")
print("=" * 60)
