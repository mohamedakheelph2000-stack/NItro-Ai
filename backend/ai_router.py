"""
ai_router.py - Hybrid AI Router System
Routes AI requests based on environment:
- Production (Render/cloud): Gemini API directly (Ollama not available on cloud)
- Development (localhost): Ollama first, Gemini fallback

Get free Gemini API key: https://aistudio.google.com/app/apikey
Add GEMINI_API_KEY to Render environment variables to enable chat.
"""
import os
import requests

# Import with compatibility for both local and package mode
try:
    from .gemini_client import gemini_response
    from .logger import logger
except ImportError:
    from gemini_client import gemini_response
    from logger import logger


def _is_cloud_environment():
    """
    Detect if running in cloud (Render, Heroku, Railway, etc.).
    On cloud: skip Ollama entirely — it's never available there.
    """
    # Render sets RENDER=true automatically
    if os.getenv("RENDER"):
        return True
    # Other common cloud signals
    if os.getenv("DYNO") or os.getenv("RAILWAY_ENVIRONMENT") or os.getenv("FLY_APP_NAME"):
        return True
    # If Ollama URL is explicitly set to a remote host, it's cloud
    ollama_url = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
    if "localhost" not in ollama_url and "127.0.0.1" not in ollama_url:
        return True
    return False


def ollama_response(prompt, timeout=30):
    """
    Query local Ollama AI server (phi3 model).
    Only called in development — never in cloud deployments.
    """
    try:
        logger.info("Attempting Ollama local AI (phi3)...")
        ollama_url = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
        ollama_model = os.getenv("OLLAMA_MODEL", "phi3")
        response = requests.post(
            f"{ollama_url}/api/generate",
            json={
                "model": ollama_model,
                "prompt": prompt,
                "stream": False,
                "options": {
                    "num_predict": 500,
                    "temperature": 0.7,
                    "top_p": 0.9,
                    "num_ctx": 2048
                }
            },
            timeout=timeout
        )
        if response.status_code == 200:
            ai_text = response.json().get("response", "").strip()
            if ai_text:
                logger.info("Ollama responded successfully (LOCAL AI)")
                return ai_text
            logger.warning("Ollama returned empty response")
            return None
        logger.warning(f"Ollama HTTP {response.status_code}")
        return None
    except requests.exceptions.ConnectionError:
        logger.warning("Ollama not running (connection refused)")
        return None
    except requests.exceptions.Timeout:
        logger.warning("Ollama timeout")
        return None
    except Exception as e:
        logger.error(f"Ollama error: {type(e).__name__}: {str(e)}")
        return None


def get_ai_response(prompt):
    """
    Main AI router.
    Cloud: Gemini only (Ollama unavailable on Render).
    Local: Ollama first, Gemini fallback.

    Returns:
        dict: {"response": str, "model": str, "source": str}
    """
    is_cloud = _is_cloud_environment()

    # === PRODUCTION / CLOUD — use Gemini directly ===
    if is_cloud:
        logger.info("Cloud environment detected — using Gemini API")
        try:
            gemini_text = gemini_response(prompt)
            if gemini_text and not gemini_text.startswith("Gemini error:"):
                return {"response": gemini_text, "model": "gemini-1.5-flash", "source": "gemini_cloud"}
            logger.error(f"Gemini error: {gemini_text}")
            raise Exception(gemini_text)
        except Exception as e:
            raise Exception(str(e))

    # === DEVELOPMENT — Ollama first, Gemini fallback ===
    logger.info("Development environment — trying Ollama first...")
    local_response = ollama_response(prompt)
    if local_response:
        return {"response": local_response, "model": "phi3", "source": "ollama_local"}

    logger.info("Ollama unavailable — falling back to Gemini API...")
    try:
        gemini_text = gemini_response(prompt)
        if gemini_text and not gemini_text.startswith("Gemini error:"):
            return {"response": gemini_text, "model": "gemini-1.5-flash", "source": "gemini_cloud"}
        raise Exception(f"Gemini failed: {gemini_text}")
    except Exception as e:
        raise Exception(
            "Both AI services unavailable. "
            "Start Ollama (ollama serve) or add GEMINI_API_KEY to .env"
        )



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
