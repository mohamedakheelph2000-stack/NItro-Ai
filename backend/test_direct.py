"""Quick test of ai_router without FastAPI"""
import sys
sys.path.insert(0, '.')

from ai_router import get_ai_response

print("Testing ai_router.py directly...")
result = get_ai_response("Say 'Hello' in 3 words")

print("✅ SUCCESS!")
print(f"Model: {result['model']}")
print(f"Source: {result['source']}")
print(f"Response: {result['response']}")
