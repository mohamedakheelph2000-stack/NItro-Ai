"""
ai_router.py - Hybrid AI Router System
Intelligently routes AI requests with local-first strategy

Flow:
1. Try Ollama (local, FREE, private, fast on laptop)
2. Fallback to Gemini API (cloud, requires API key)
3. Return error if both fail

Performance optimized for low-compute laptops.
"""
import requests

# Import with compatibility for both local and package mode
try:
    from .gemini_client import gemini_response
    from .logger import logger
except ImportError:
    from gemini_client import gemini_response
    from logger import logger


def ollama_response(prompt, timeout=30):
    """
    Query local Ollama AI server (phi3 model).
    
    Args:
        prompt: User message/question
        timeout: Request timeout in seconds (optimized for laptops)
    
    Returns:
        AI response string or None if failed
    """
    try:
        logger.info("🔄 Attempting Ollama local AI (phi3)...")
        
        # Optimized settings for low-compute laptops
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": "phi3",  # 3.8GB model, laptop-friendly
                "prompt": prompt,
                "stream": False,  # No streaming for simpler handling
                "options": {
                    "num_predict": 500,  # Limit tokens for faster response
                    "temperature": 0.7,  # Balanced creativity/accuracy
                    "top_p": 0.9,
                    "num_ctx": 2048  # Context window (lower = faster)
                }
            },
            timeout=timeout  # Prevent hanging on slow systems
        )

        if response.status_code == 200:
            ai_text = response.json().get("response", "").strip()
            if ai_text:
                logger.info("✅ Ollama responded successfully (LOCAL AI)")
                return ai_text
            else:
                logger.warning("⚠️ Ollama returned empty response")
                return None
        else:
            logger.warning(f"⚠️ Ollama HTTP {response.status_code}: {response.text[:100]}")
            return None

    except requests.exceptions.ConnectionError:
        logger.warning("❌ Ollama not running (connection refused)")
        return None
    except requests.exceptions.Timeout:
        logger.warning("⏱️ Ollama timeout (may need to reduce num_predict)")
        return None
    except Exception as e:
        logger.error(f"❌ Ollama error: {type(e).__name__}: {str(e)}")
        return None


def get_ai_response(prompt):
    """
    Main AI router - tries Ollama first, then Gemini.
    
    Args:
        prompt: User message/question
    
    Returns:
        dict: {"response": str, "model": str, "source": str}
    
    Raises:
        Exception: If both AI services fail
    """
    # === PHASE 1: Try Local Ollama (PREFERRED) ===
    # Benefits: FREE, private, no internet needed, fast on laptop
    local_response = ollama_response(prompt)
    
    if local_response:
        logger.info("📍 Using LOCAL Ollama AI (phi3)")
        return {
            "response": local_response,
            "model": "phi3",
            "source": "ollama_local"
        }
    
    # === PHASE 2: Fallback to Gemini (CLOUD) ===
    # Only used when Ollama unavailable
    logger.info("🌐 Falling back to Gemini API (cloud)...")
    
    try:
        gemini_text = gemini_response(prompt)
        
        # Check if Gemini returned error message
        if gemini_text and not gemini_text.startswith("Gemini error:"):
            logger.info("✅ Gemini responded successfully (CLOUD AI)")
            return {
                "response": gemini_text,
                "model": "gemini-pro",
                "source": "gemini_cloud"
            }
        else:
            logger.error(f"❌ Gemini error: {gemini_text}")
            raise Exception(f"Gemini failed: {gemini_text}")
    
    except Exception as e:
        logger.error(f"❌ Gemini exception: {str(e)}")
        raise Exception(
            "Both AI services unavailable. "
            "Please start Ollama (ollama serve) or configure Gemini API key."
        )
