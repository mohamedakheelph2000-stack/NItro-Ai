"""
gemini_client.py - Google Gemini API Client
Cloud-based AI fallback when Ollama unavailable

Configuration:
- Set GEMINI_API_KEY in .env file
- Get free API key: https://makersuite.google.com/app/apikey
"""
import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

# Configure Gemini API
api_key = os.getenv("GEMINI_API_KEY")
if api_key:
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel("gemini-pro")
else:
    model = None


def gemini_response(prompt):
    """
    Query Google Gemini API for AI response.
    
    Args:
        prompt: User message/question
    
    Returns:
        AI response string or error message
    """
    if not model or not api_key:
        return "Gemini error: GEMINI_API_KEY not configured in .env"
    
    try:
        # Generate response with timeout and safety settings
        response = model.generate_content(
            prompt,
            generation_config={
                "temperature": 0.7,
                "top_p": 0.9,
                "top_k": 40,
                "max_output_tokens": 500,  # Limit for faster response
            }
        )
        
        if response and response.text:
            return response.text.strip()
        else:
            return "Gemini error: Empty response received"
    
    except Exception as e:
        error_msg = str(e)
        # Check for common errors
        if "API_KEY" in error_msg.upper():
            return "Gemini error: Invalid API key. Check GEMINI_API_KEY in .env"
        elif "QUOTA" in error_msg.upper():
            return "Gemini error: API quota exceeded. Try again later or use Ollama."
        else:
            return f"Gemini error: {error_msg}"
