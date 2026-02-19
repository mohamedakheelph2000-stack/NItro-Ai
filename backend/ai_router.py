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


def ollama_response(prompt, timeout=60, max_retries=2):
    """
    Query local Ollama AI server with system prompt and retry logic.
    
    Args:
        prompt: User message/question
        timeout: Request timeout in seconds (default: 60)
        max_retries: Number of retries on connection error (default: 2)
    
    Returns:
        str: AI response or None if failed
    """
    ollama_url = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
    ollama_model = os.getenv("OLLAMA_MODEL", "llama3")
    
    # System prompt for Nitro AI
    system_prompt = (
        "You are Nitro AI, a personal AI assistant created by Mohamed Akheel. "
        "You run locally using Ollama. "
        "You help with coding, AI, productivity and general questions. "
        "Never invent company information about Nitro AI."
    )
    
    # Retry loop for robustness
    for attempt in range(max_retries + 1):
        try:
            if attempt > 0:
                logger.info(f"🔄 Retry attempt {attempt}/{max_retries}...")
            else:
                logger.info(f"🤖 Querying Ollama ({ollama_model})...")
            
            response = requests.post(
                f"{ollama_url}/api/chat",
                json={
                    "model": ollama_model,
                    "messages": [
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": prompt}
                    ],
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
                response_data = response.json()
                # Extract AI response from chat API format
                ai_text = response_data.get("message", {}).get("content", "").strip()
                if ai_text:
                    logger.info(f"✅ Ollama ({ollama_model}) responded successfully")
                    return ai_text
                logger.warning("⚠️ Ollama returned empty response")
                # Don't retry on empty response, return None
                return None
            
            logger.warning(f"⚠️ Ollama HTTP {response.status_code}")
            # Don't retry on HTTP errors, return None
            return None
            
        except requests.exceptions.ConnectionError as e:
            if attempt < max_retries:
                logger.warning(f"⚠️ Connection failed, retrying... ({attempt + 1}/{max_retries})")
                continue
            logger.error("❌ Ollama not running. Please start it with: ollama serve")
            return None
            
        except requests.exceptions.Timeout as e:
            if attempt < max_retries:
                logger.warning(f"⏱️ Request timeout, retrying... ({attempt + 1}/{max_retries})")
                continue
            logger.error(f"❌ Ollama timeout after {timeout}s. Model may be loading or too slow.")
            return None
            
        except Exception as e:
            logger.error(f"❌ Ollama error: {type(e).__name__}: {str(e)}")
            return None
    
    # Should never reach here, but return None as fallback
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
