"""
ai_router.py - Free Local AI Router System
Uses Ollama for 100% free, private, offline AI responses.

Supported Models (get them with: ollama pull <model>):
- llama3.2:1b (1.3GB) - Ultra fast, good for chat
- phi3 (2.3GB) - Microsoft's efficient model
- mistral (4.1GB) - Very capable, balanced
- llama3 (4.7GB) - Meta's latest, excellent quality (DEFAULT)

Setup:
1. Install Ollama: https://ollama.com/download
2. Pull a model: ollama pull llama3.2:1b
3. Start server: ollama serve (auto-starts on most systems)
4. That's it! 100% free forever.
"""
import os
import requests

# Import with compatibility for both local and package mode
try:
    from .logger import logger
except ImportError:
    from logger import logger


def ollama_response(prompt, timeout=45):
    """
    Query local Ollama AI server.
    
    Args:
        prompt: User message/question
        timeout: Request timeout in seconds
    
    Returns:
        str: AI response or None if failed
    """
    try:
        ollama_url = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
        ollama_model = os.getenv("OLLAMA_MODEL", "llama3")
        
        logger.info(f"🤖 Querying Ollama ({ollama_model})...")
        
        response = requests.post(
            f"{ollama_url}/api/generate",
            json={
                "model": ollama_model,
                "prompt": prompt,
                "stream": False,
                "options": {
                    "num_predict": 800,  # Max response length
                    "temperature": 0.7,   # Creativity vs accuracy
                    "top_p": 0.9,
                    "num_ctx": 2048      # Context window
                }
            },
            timeout=timeout
        )
        
        if response.status_code == 200:
            ai_text = response.json().get("response", "").strip()
            if ai_text:
                logger.info(f"✅ Ollama ({ollama_model}) responded successfully")
                return ai_text
            logger.warning("⚠️ Ollama returned empty response")
            return None
        
        logger.warning(f"⚠️ Ollama HTTP {response.status_code}")
        return None
        
    except requests.exceptions.ConnectionError:
        logger.warning("❌ Ollama not running - start with: ollama serve")
        return None
    except requests.exceptions.Timeout:
        logger.warning("⏱️ Ollama timeout - model may be loading")
        return None
    except Exception as e:
        logger.error(f"❌ Ollama error: {type(e).__name__}: {str(e)}")
        return None


def get_ai_response(prompt):
    """
    Main AI router - uses Ollama local AI only.
    
    Args:
        prompt: User message/question
    
    Returns:
        dict: {"response": str, "model": str, "source": str}
    
    Raises:
        Exception: If Ollama is not available
    """
    ollama_model = os.getenv("OLLAMA_MODEL", "llama3")
    
    # Try Ollama
    local_response = ollama_response(prompt)
    
    if local_response:
        logger.info(f"📍 Using FREE local Ollama ({ollama_model})")
        return {
            "response": local_response,
            "model": ollama_model,
            "source": "ollama_local"
        }
    
    # Ollama unavailable - provide helpful error
    logger.error("❌ Ollama unavailable")
    raise Exception(
        "Ollama AI is not running. Please:\n\n"
        "1. Install Ollama: https://ollama.com/download\n"
        "2. Pull a model: ollama pull llama3.2:1b\n"
        "3. Start server: ollama serve\n\n"
        "Ollama is 100% free and runs locally on your device!"
    )
