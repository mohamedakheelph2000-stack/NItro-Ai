#!/usr/bin/env python3
"""
Test script to verify Ollama llama3 integration with Nitro AI backend
"""
import requests
import json

def test_ollama_direct():
    """Test Ollama API directly"""
    print("=== TESTING OLLAMA API DIRECTLY ===\n")
    
    try:
        # Test Ollama version
        version_response = requests.get("http://localhost:11434/api/version")
        if version_response.status_code == 200:
            print(f"✅ Ollama Version: {version_response.json()['version']}")
        
        # Test llama3 model
        print("\n🤖 Testing llama3 model...")
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": "llama3",
                "prompt": "Say 'Hello from llama3' in 5 words.",
                "stream": False
            },
            timeout=30
        )
        
        if response.status_code == 200:
            ai_response = response.json()['response']
            print(f"✅ llama3 Response: {ai_response}")
        else:
            print(f"❌ Error: HTTP {response.status_code}")
            
    except Exception as e:
        print(f"❌ Ollama Error: {e}")
        print("\nMake sure Ollama is running: ollama serve")

def test_backend():
    """Test Nitro AI backend /chat endpoint"""
    print("\n\n=== TESTING NITRO AI BACKEND ===\n")
    
    try:
        # Test health endpoint
        health = requests.get("http://localhost:8000/health")
        if health.status_code == 200:
            print("✅ Backend Health: OK")
        
        # Test /chat endpoint
        print("\n🤖 Testing /chat endpoint with llama3...")
        chat_response = requests.post(
            "http://localhost:8000/chat",
            json={"message": "What is 2+2? Answer in one word."},
            timeout=60
        )
        
        if chat_response.status_code == 200:
            data = chat_response.json()
            print(f"✅ Status: {chat_response.status_code}")
            print(f"✅ Model: {data['ai_model']}")
            print(f"✅ Source: {data['ai_source']}")
            print(f"✅ Response: {data['response'][:100]}...")
            
            if data['ai_model'] == 'llama3':
                print("\n🎉 SUCCESS! Backend is using llama3 model!")
            else:
                print(f"\n⚠️ Warning: Expected llama3, got {data['ai_model']}")
        else:
            print(f"❌ Error: HTTP {chat_response.status_code}")
            
    except Exception as e:
        print(f"❌ Backend Error: {e}")
        print("\nMake sure backend is running:")
        print("cd c:\\Nitro AI\\backend")
        print("python -m uvicorn main:app --host 0.0.0.0 --port 8000 --reload")

if __name__ == "__main__":
    test_ollama_direct()
    test_backend()
    print("\n" + "="*60)
    print("Configuration:")
    print("  Ollama API: http://localhost:11434")
    print("  Backend API: http://localhost:8000")
    print("  Model: llama3 (4.7GB)")
    print("  Error Handling: ✅ Enabled")
    print("="*60)
