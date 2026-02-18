"""
gemini_client.py - Google Gemini API Client
Cloud-based AI provider for production deployment on Render

Configuration:
- Set GEMINI_API_KEY as an environment variable on Render
- Get FREE API key: https://aistudio.google.com/app/apikey
- Free tier: 15 RPM, 1 million TPM (more than enough)
"""
import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

# Configure Gemini API
api_key = os.getenv("GEMINI_API_KEY")
if api_key:
    genai.configure(api_key=api_key)
else:
    pass  # Will return clear error on first call

# Model priority list - try newest/fastest first
GEMINI_MODELS = [
    "gemini-1.5-flash",   # Fast, free, generous quota
    "gemini-1.5-pro",     # Smarter, same free tier
    "gemini-pro",         # Legacy fallback
]


def gemini_response(prompt):
    """
    Query Google Gemini API for AI response.
    Tries model fallback chain automatically.

    Args:
        prompt: User message/question

    Returns:
        AI response string or error message
    """
    if not api_key:
        return "Gemini error: GEMINI_API_KEY not set. Add it to Render environment variables."

    last_error = None
    for model_name in GEMINI_MODELS:
        try:
            model = genai.GenerativeModel(model_name)
            response = model.generate_content(
                prompt,
                generation_config={
                    "temperature": 0.7,
                    "top_p": 0.9,
                    "top_k": 40,
                    "max_output_tokens": 800,
                }
            )
            if response and response.text:
                return response.text.strip()
        except Exception as e:
            last_error = str(e)
            error_upper = last_error.upper()
            if "API_KEY" in error_upper or "PERMISSION" in error_upper:
                return f"Gemini error: Invalid API key — check GEMINI_API_KEY on Render."
            if "QUOTA" in error_upper or "RESOURCE_EXHAUSTED" in error_upper:
                return f"Gemini error: Quota exceeded on {model_name}, trying next model..."
            # Other errors — try next model in chain
            continue

    return f"Gemini error: All models failed. Last error: {last_error}"
