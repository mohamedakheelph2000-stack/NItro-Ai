import sys
sys.path.insert(0, r"c:\Nitro AI\backend")

from ai_router import get_ai_response

try:
    print("Testing ai_router...")
    result = get_ai_response("Say hello in 3 words")
    print(f"✅ SUCCESS!")
    print(f"Model: {result['model']}")
    print(f"Source: {result['source']}")
    print(f"Response: {result['response']}")
except Exception as e:
    print(f"❌ ERROR: {e}")
