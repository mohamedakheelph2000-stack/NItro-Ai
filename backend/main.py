"""
main.py - Enhanced Nitro AI Backend Server
Professional AI assistant platform with memory, history, and security

AI Integration:
- Uses Ollama for 100% free, private, local AI
- No cloud APIs, no paid services, fully offline capable
- Data never leaves your device
"""
from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, StreamingResponse
from fastapi.staticfiles import StaticFiles
from datetime import datetime
from typing import List, Optional, Dict, Any
import time
import json
import sys
import asyncio
from pathlib import Path

# Add parent directory to path so we can import models
sys.path.insert(0, str(Path(__file__).parent.parent))

# Import our custom modules with compatibility for both local and package mode
try:
    # Try relative imports first (for package mode: python -m backend.main)
    from .ai_router import get_ai_response
    from .config import settings
    from .schemas import (
        ChatMessage, ChatResponse, ErrorResponse, HealthCheckResponse,
        SessionCreate, SessionResponse, HistoryResponse,
        LanguageDetectRequest, LanguageDetectResponse, LanguagePreferenceRequest,
        LanguagePreferenceResponse, SupportedLanguagesResponse,
        VideoGenerateRequest, VideoGenerateResponse, VideoStatusResponse
    )
    from .logger import logger
    from .memory_manager import memory_manager
    from .language_detector import LanguageDetector
    from .automation_agents import agent_manager
except ImportError:
    # Fallback to absolute imports (for local dev: cd backend && python -m uvicorn main:app)
    from ai_router import get_ai_response
    from config import settings
    from schemas import (
        ChatMessage, ChatResponse, ErrorResponse, HealthCheckResponse,
        SessionCreate, SessionResponse, HistoryResponse,
        LanguageDetectRequest, LanguageDetectResponse, LanguagePreferenceRequest,
        LanguagePreferenceResponse, SupportedLanguagesResponse,
        VideoGenerateRequest, VideoGenerateResponse, VideoStatusResponse
    )
    from logger import logger
    from memory_manager import memory_manager
    from language_detector import LanguageDetector
    from automation_agents import agent_manager

# These always work from parent directory (models/ is a sibling to backend/)
from models.ai_modules.video_gen import VideoGenerator
from models.ai_modules.chat_ai import create_chat_ai
from models.ai_modules.image_gen_enhanced import create_image_generator
from models.ai_modules.voice_enhanced import create_voice_assistant
from models.ai_modules.web_search_enhanced import create_web_search_ai

# Initialize services
language_detector = LanguageDetector()
video_generator = VideoGenerator()

# Initialize Chat AI with Ollama (phi3 model from .env)
# This connects to your local Ollama server for FREE AI chat!
chat_ai = create_chat_ai(
    model_type=settings.AI_MODEL if hasattr(settings, 'AI_MODEL') else "ollama",
    config={
        "model": settings.OLLAMA_MODEL if hasattr(settings, 'OLLAMA_MODEL') else "phi3",
        "base_url": settings.OLLAMA_BASE_URL if hasattr(settings, 'OLLAMA_BASE_URL') else "http://localhost:11434",
        "temperature": settings.AI_TEMPERATURE if hasattr(settings, 'AI_TEMPERATURE') else 0.7,
        "max_tokens": settings.AI_MAX_TOKENS if hasattr(settings, 'AI_MAX_TOKENS') else 500
    }
)

# Initialize Image Generator (placeholder by default, enable in settings)
image_generator = create_image_generator(
    model_type="placeholder",  # Change to "stable-diffusion" when ready
    device="cpu",
    low_memory=True
)

# Initialize Voice Assistant (placeholder by default)
voice_assistant = create_voice_assistant(
    stt_engine="google",
    tts_engine="gtts",
    language="en"
)

# Initialize Web Search AI (with chat_ai for summarization)
web_search_ai = create_web_search_ai(
    chat_ai=chat_ai,
    max_results=5
)

# Create FastAPI application
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.VERSION,
    description="A professional AI assistant platform - Nitro AI"
)

# === MIDDLEWARE ===

# CORS Configuration
# Localhost-only for local deployment
_cors_origins = settings._build_origins()
print(f"[CORS] Allowed origins: {_cors_origins}")

app.add_middleware(
    CORSMiddleware,
    allow_origins=_cors_origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS", "PATCH"],
    allow_headers=[
        "Content-Type",
        "Authorization",
        "Accept",
        "Origin",
        "X-Requested-With",
        "Access-Control-Request-Method",
        "Access-Control-Request-Headers",
    ],
    expose_headers=["X-Process-Time", "X-Request-ID"],
    max_age=3600,  # Cache preflight for 1 hour
)

# Request timing middleware
@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    """
    Middleware to track request processing time.
    Useful for monitoring performance.
    """
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(round(process_time, 3))
    return response

# Global exception handler
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """
    Global exception handler to catch any unhandled errors.
    Returns a consistent error response format.
    """
    logger.error(f"Unhandled exception: {exc}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={
            "error": "Internal server error",
            "detail": str(exc) if settings.DEBUG_MODE else "An unexpected error occurred",
            "timestamp": datetime.now().isoformat()
        }
    )

# === STARTUP & SHUTDOWN EVENTS ===

@app.on_event("startup")
async def startup_event():
    """Initialize services on startup."""
    logger.info(f"🚀 {settings.APP_NAME} v{settings.VERSION} is starting...")
    logger.info(f"📝 Debug mode: {settings.DEBUG_MODE}")
    logger.info(f"🌐 Server will run on {settings.HOST}:{settings.PORT}")
    logger.info(f"💾 Memory system initialized")

@app.on_event("shutdown")
async def shutdown_event():
    """Cleanup on shutdown."""
    logger.info(f"👋 {settings.APP_NAME} is shutting down...")

# === ENDPOINTS ===

@app.get("/")
async def root():
    """
    Root endpoint - Welcome message and API info.
    """
    logger.info("Root endpoint accessed")
    return {
        "message": f"Welcome to {settings.APP_NAME}!",
        "status": "running",
        "version": settings.VERSION,
        "docs": "/docs",
        "health": "/health",
        "features": [
            "Chat with AI assistant",
            "Conversation memory",
            "Chat history",
            "Multi-session support"
        ]
    }

@app.get("/health", response_model=HealthCheckResponse)
async def health_check():
    """
    Health check endpoint.
    Returns server status and memory statistics.
    """
    logger.debug("Health check requested")
    
    # Get memory statistics
    memory_stats = memory_manager.get_statistics()
    
    return HealthCheckResponse(
        status="healthy",
        timestamp=datetime.now().isoformat(),
        version=settings.VERSION,
        memory_stats=memory_stats
    )

@app.post("/chat", response_model=ChatResponse)
async def chat(chat_message: ChatMessage, request: Request):
    """
    Main chat endpoint - Receives messages and returns AI responses.
    
    Now includes:
    - Session management
    - Conversation memory storage
    - Better error handling
    - Request sanitization
    """
    try:
        # Log incoming message
        logger.info(f"Chat request from {chat_message.user_id}: {chat_message.message[:50]}...")
        
        # Sanitize input (basic security)
        user_text = chat_message.message.strip()
        
        # Validate message
        if not user_text:
            raise HTTPException(status_code=400, detail="Message cannot be empty")
        
        if len(user_text) > settings.MAX_MESSAGE_LENGTH:
            logger.warning(f"Message too long: {len(user_text)} characters")
            raise HTTPException(
                status_code=400,
                detail=f"Message too long. Maximum {settings.MAX_MESSAGE_LENGTH} characters allowed."
            )
        
        # Get or create session
        session_id = chat_message.session_id
        if not session_id:
            # Create new session if none provided
            session_id = memory_manager.create_session(user_id=chat_message.user_id)
            logger.info(f"Created new session: {session_id}")
        
        # === AI RESPONSE GENERATION ===
        # Local AI System (Ollama - 100% Free):
        # 
        # Uses Ollama for completely free, private AI responses.
        # No cloud APIs, no tracking, no costs - runs entirely locally.
        # 
        # Supported models (install with: ollama pull <model>):
        # - llama3.2:1b (1.3GB) - Ultra fast, excellent for chat
        # - phi3 (2.3GB) - Microsoft's efficient model
        # - mistral (4.1GB) - Very capable, balanced
        # - llama3:8b (4.7GB) - Meta's latest, highest quality
        
        ai_model_used = "unknown"
        ai_source = "unknown"
        
        try:
            # Call hybrid AI router
            ai_result = get_ai_response(user_text)
            
            # Extract response and metadata
            if isinstance(ai_result, dict):
                ai_response = ai_result.get("response", "")
                ai_model_used = ai_result.get("model", "unknown")
                ai_source = ai_result.get("source", "unknown")
            else:
                # Handle legacy string response
                ai_response = str(ai_result)
                ai_model_used = "legacy"
                ai_source = "legacy"
            
            # Log success with model info
            logger.info(f"✅ AI response generated | Model: {ai_model_used} | Source: {ai_source}")
            
        except Exception as ai_error:
            # Ollama not available - provide helpful setup instructions
            logger.error(f"❌ Ollama unavailable: {ai_error}")
            
            # Determine specific error type for better user guidance
            error_msg = str(ai_error).lower()
            if "connection" in error_msg or "not running" in error_msg:
                ai_response = (
                    "🚨 **Ollama is not running**\n\n"
                    "Please start Ollama to use Nitro AI:\n\n"
                    "**Quick Fix:**\n"
                    "1. Open a terminal/command prompt\n"
                    "2. Run: `ollama serve`\n"
                    "3. Refresh and try again\n\n"
                    "**First time setup?**\n"
                    "1. Install Ollama: https://ollama.com/download\n"
                    "2. Pull a model: `ollama pull llama3`\n"
                    "3. Start server: `ollama serve`\n\n"
                    "Need help? Check the README.md file."
                )
            elif "timeout" in error_msg:
                ai_response = (
                    "⏱️ **Request Timeout**\n\n"
                    "The AI model took too long to respond. This can happen when:\n\n"
                    "- The model is loading for the first time\n"
                    "- Your computer is busy with other tasks\n"
                    "- The model is too large for your system\n\n"
                    "**Try:**\n"
                    "- Wait a moment and try again\n"
                    "- Use a smaller model like `llama3.2:1b`\n"
                    "- Close other applications to free up resources"
                )
            else:
                ai_response = (
                    "🤖 **Ollama Connection Error**\n\n"
                    "Quick Setup (100% FREE):\n"
                    "1. Install: https://ollama.com/download\n"
                    "2. Pull model: `ollama pull llama3`\n"
                    "3. Start server: `ollama serve`\n\n"
                    f"**Technical details:** {str(ai_error)}"
                )
            
            ai_model_used = "none"
            ai_source = "error"
            
            # Still allow the request to succeed with error message
            # This prevents breaking the frontend
        
        # Store conversation in memory
        memory_manager.add_message(
            session_id=session_id,
            message=user_text,
            sender="user",
            response=ai_response
        )
        
        logger.info(f"💾 Conversation saved | Session: {session_id} | Model: {ai_model_used}")
        
        # Return clean JSON response with model tracking
        return ChatResponse(
            response=ai_response,
            timestamp=datetime.now().isoformat(),
            status="success",
            user_id=chat_message.user_id,
            session_id=session_id,
            ai_model=ai_model_used,  # Which model responded (phi3, llama3.2:1b, mistral, etc.)
            ai_source=ai_source  # Where it came from (ollama_local, error)
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error in chat endpoint: {e}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail="An error occurred while processing your message."
        )

@app.post("/session/create", response_model=SessionResponse)
async def create_session(session_create: SessionCreate):
    """
    Create a new conversation session.
    
    Returns:
        Session ID for tracking conversation
    """
    try:
        session_id = memory_manager.create_session(user_id=session_create.user_id)
        logger.info(f"Created session: {session_id} for user: {session_create.user_id}")
        
        return SessionResponse(
            session_id=session_id,
            user_id=session_create.user_id,
            created_at=datetime.now().isoformat(),
            message="Session created successfully"
        )
    except Exception as e:
        logger.error(f"Error creating session: {e}")
        raise HTTPException(status_code=500, detail="Failed to create session")

@app.get("/history/{session_id}", response_model=HistoryResponse)
async def get_session_history(session_id: str):
    """
    Retrieve conversation history for a specific session.
    
    Args:
        session_id: The session identifier
    
    Returns:
        Complete conversation history
    """
    try:
        history = memory_manager.get_session_history(session_id)
        
        if not history:
            raise HTTPException(status_code=404, detail="Session not found")
        
        logger.info(f"Retrieved history for session: {session_id}")
        
        return HistoryResponse(
            session_id=history["session_id"],
            user_id=history["user_id"],
            created_at=history["created_at"],
            last_updated=history["last_updated"],
            messages=history["messages"],
            message_count=history["message_count"]
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error retrieving history: {e}")
        raise HTTPException(status_code=500, detail="Failed to retrieve history")

@app.get("/sessions/recent")
async def get_recent_sessions(limit: int = 10, user_id: Optional[str] = None):
    """
    Get recent conversation sessions.
    
    Args:
        limit: Maximum number of sessions to return (default: 10)
        user_id: Filter by user ID (optional)
    
    Returns:
        List of recent sessions
    """
    try:
        sessions = memory_manager.get_recent_sessions(limit=limit, user_id=user_id)
        logger.info(f"Retrieved {len(sessions)} recent sessions")
        
        return {
            "sessions": sessions,
            "count": len(sessions),
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        logger.error(f"Error retrieving recent sessions: {e}")
        raise HTTPException(status_code=500, detail="Failed to retrieve sessions")

@app.delete("/session/{session_id}")
async def delete_session(session_id: str):
    """
    Delete a conversation session.
    
    Args:
        session_id: Session to delete
    
    Returns:
        Deletion status
    """
    try:
        success = memory_manager.delete_session(session_id)
        
        if not success:
            raise HTTPException(status_code=404, detail="Session not found")
        
        logger.info(f"Deleted session: {session_id}")
        
        return {
            "message": "Session deleted successfully",
            "session_id": session_id,
            "timestamp": datetime.now().isoformat()
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error deleting session: {e}")
        raise HTTPException(status_code=500, detail="Failed to delete session")

@app.get("/stats")
async def get_statistics():
    """
    Get platform statistics.
    
    Returns:
        Memory and usage statistics
    """
    try:
        stats = memory_manager.get_statistics()
        logger.info("Statistics retrieved")
        
        return {
            "statistics": stats,
            "server_version": settings.VERSION,
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        logger.error(f"Error retrieving statistics: {e}")
        raise HTTPException(status_code=500, detail="Failed to retrieve statistics")


# ============================================================================
# LANGUAGE DETECTION & TRANSLATION ENDPOINTS
# ============================================================================

@app.post("/language/detect", response_model=LanguageDetectResponse)
async def detect_language(request: LanguageDetectRequest):
    """
    Detect language from text.
    
    LIGHTWEIGHT - No AI required!
    Uses pattern matching to identify language.
    
    Args:
        request: Text to analyze
        
    Returns:
        Detected language code, name, and confidence
        
    Example:
        POST /language/detect
        {"text": "Hola, ¿cómo estás?"}
        
        Response:
        {
            "detected_language": "es",
            "language_name": "Spanish",
            "confidence": 0.85,
            "supported": true
        }
    """
    try:
        lang_code, confidence = language_detector.detect_language(request.text)
        lang_name = language_detector.get_language_name(lang_code)
        is_supported = language_detector.is_supported(lang_code)
        
        logger.info(f"Detected language: {lang_name} ({lang_code}) with confidence {confidence:.2f}")
        
        return LanguageDetectResponse(
            detected_language=lang_code,
            language_name=lang_name,
            confidence=confidence,
            supported=is_supported
        )
    except Exception as e:
        logger.error(f"Language detection error: {e}")
        raise HTTPException(status_code=500, detail="Failed to detect language")


@app.get("/language/supported", response_model=SupportedLanguagesResponse)
async def get_supported_languages():
    """
    Get list of all supported languages.
    
    Returns:
        Dictionary of language codes and names
        
    Example Response:
        {
            "languages": {
                "en": "English",
                "es": "Spanish",
                "fr": "French",
                ...
            },
            "total": 10
        }
    """
    try:
        languages = language_detector.get_supported_languages()
        return SupportedLanguagesResponse(
            languages=languages,
            total=len(languages)
        )
    except Exception as e:
        logger.error(f"Error getting languages: {e}")
        raise HTTPException(status_code=500, detail="Failed to retrieve languages")


@app.post("/language/preference", response_model=LanguagePreferenceResponse)
async def set_language_preference(request: LanguagePreferenceRequest):
    """
    Set user's preferred language.
    
    FUTURE: Store in database
    Currently just validates and returns confirmation
    
    Args:
        request: User ID and language preference
        
    Returns:
        Confirmation with language details
    """
    try:
        # Validate language is supported
        if not language_detector.is_supported(request.language):
            raise HTTPException(
                status_code=400,
                detail=f"Language '{request.language}' is not supported"
            )
        
        lang_name = language_detector.get_language_name(request.language)
        
        # FUTURE: Save to database
        # db.user_preferences.update(user_id=request.user_id, language=request.language)
        
        logger.info(f"Language preference set for {request.user_id}: {lang_name}")
        
        return LanguagePreferenceResponse(
            user_id=request.user_id,
            language=request.language,
            language_name=lang_name,
            auto_detect=request.auto_detect,
            message=f"Language preference set to {lang_name}"
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error setting language preference: {e}")
        raise HTTPException(status_code=500, detail="Failed to set language preference")


# ============================================================================
# VIDEO GENERATION ENDPOINTS
# ============================================================================

@app.post("/video/generate", response_model=VideoGenerateResponse)
async def generate_video(request: VideoGenerateRequest):
    """
    Generate video from text description (PLACEHOLDER).
    
    ⚠️ NOT YET IMPLEMENTED - Returns placeholder response
    
    FUTURE: Integrate with RunwayML, Stable Diffusion, or Sora
    
    Args:
        request: Video generation parameters
        
    Returns:
        Video ID and generation status
        
    Example:
        POST /video/generate
        {
            "prompt": "A serene sunset over the ocean",
            "duration": 4,
            "style": "cinematic",
            "resolution": "1280x720"
        }
        
    SETUP FOR REAL IMPLEMENTATION:
    1. Add VIDEO_MODEL=runway to .env
    2. Add RUNWAY_API_KEY=your-key to .env
    3. Uncomment code in models/ai_modules/video_gen.py
    4. Restart server
    """
    try:
        # Generate video (currently returns placeholder)
        result = video_generator.generate_video(
            prompt=request.prompt,
            duration=request.duration,
            style=request.style,
            resolution=request.resolution,
            fps=request.fps,
            seed=request.seed
        )
        
        logger.info(f"Video generation requested: {request.prompt[:50]}...")
        
        return VideoGenerateResponse(**result)
    except Exception as e:
        logger.error(f"Video generation error: {e}")
        raise HTTPException(status_code=500, detail="Failed to generate video")


@app.get("/video/status/{video_id}", response_model=VideoStatusResponse)
async def get_video_status(video_id: str):
    """
    Check video generation status (PLACEHOLDER).
    
    Args:
        video_id: Video generation ID
        
    Returns:
        Current status and progress
        
    FUTURE: Poll this during long video generations
    """
    try:
        status = video_generator.get_generation_status(video_id)
        return VideoStatusResponse(**status)
    except Exception as e:
        logger.error(f"Error getting video status: {e}")
        raise HTTPException(status_code=500, detail="Failed to get video status")


@app.get("/video/models")
async def get_video_models():
    """
    Get list of supported video generation models.
    
    Returns information about available models and their capabilities.
    """
    try:
        models = video_generator.get_supported_models()
        return {
            "models": models,
            "current_model": settings.VIDEO_MODEL,
            "enabled": settings.ENABLE_VIDEO_GEN
        }
    except Exception as e:
        logger.error(f"Error getting video models: {e}")
        raise HTTPException(status_code=500, detail="Failed to get video models")


# === STREAMING CHAT ENDPOINT ===

@app.post("/chat/stream")
async def chat_stream(chat_message: ChatMessage):
    """
    Streaming chat endpoint - Returns AI responses word-by-word (like ChatGPT!).
    
    Features:
    - Real-time streaming responses
    - Works with Ollama, OpenAI, etc.
    - Session management
    - Server-Sent Events (SSE) format
    
    Example Usage (JavaScript):
        const eventSource = new EventSource('/chat/stream');
        eventSource.onmessage = (event) => {
            const chunk = event.data;
            console.log(chunk);  // Display word-by-word
        };
    """
    try:
        # Validate message
        user_text = chat_message.message.strip()
        if not user_text:
            raise HTTPException(status_code=400, detail="Message cannot be empty")
        
        # Get or create session
        session_id = chat_message.session_id
        if not session_id:
            session_id = memory_manager.create_session(user_id=chat_message.user_id)
            logger.info(f"Created new session for streaming: {session_id}")
        
        # Generator function for streaming
        async def generate_stream():
            """Generate Server-Sent Events stream."""
            try:
                full_response = ""
                
                # Stream AI response
                async for chunk in chat_ai.stream_response(
                    message=user_text,
                    system_prompt="You are Nitro AI, a helpful and friendly assistant."
                ):
                    full_response += chunk
                    
                    # Send chunk as Server-Sent Event
                    yield f"data: {json.dumps({'chunk': chunk, 'done': False})}\n\n"
                
                # Store conversation in memory
                memory_manager.add_message(
                    session_id=session_id,
                    message=user_text,
                    sender="user",
                    response=full_response
                )
                
                # Send completion signal
                yield f"data: {json.dumps({'chunk': '', 'done': True, 'session_id': session_id})}\n\n"
                
            except Exception as e:
                logger.error(f"Streaming error: {e}")
                error_msg = f"Error: {str(e)}"
                yield f"data: {json.dumps({'chunk': error_msg, 'done': True, 'error': True})}\n\n"
        
        # Return streaming response
        return StreamingResponse(
            generate_stream(),
            media_type="text/event-stream",
            headers={
                "Cache-Control": "no-cache",
                "Connection": "keep-alive",
                "X-Accel-Buffering": "no"  # Disable nginx buffering
            }
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error in streaming chat: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Streaming error occurred")


# ============================================================================
# IMAGE GENERATION ENDPOINTS
# ============================================================================

@app.post("/image/generate")
async def generate_image(
    prompt: str,
    negative_prompt: Optional[str] = None,
    size: str = "512x512",
    quality: str = "standard"
):
    """
    Generate image from text prompt using Stable Diffusion.
    
    Args:
        prompt: Text description of desired image
        negative_prompt: What to avoid in image
        size: Image size ("512x512", "768x768", "1024x1024")
        quality: "standard" or "hd"
    
    Returns:
        Generated image data (base64) and file path
        
    Example Request:
        POST /image/generate
        {
            "prompt": "a futuristic city at sunset",
            "negative_prompt": "blurry, low quality",
            "size": "512x512"
        }
    """
    try:
        logger.info(f"Image generation requested: {prompt[:50]}...")
        
        result = await image_generator.generate_image(
            prompt=prompt,
            negative_prompt=negative_prompt,
            size=size,
            quality=quality
        )
        
        return result
        
    except Exception as e:
        logger.error(f"Image generation error: {e}")
        raise HTTPException(status_code=500, detail=f"Image generation failed: {str(e)}")


@app.get("/image/gallery")
async def get_image_gallery(limit: int = 20):
    """
    Get list of recently generated images.
    
    Args:
        limit: Maximum number of images to return
        
    Returns:
        List of image metadata
    """
    try:
        images = image_generator.list_gallery(limit=limit)
        
        return {
            "status": "success",
            "images": images,
            "total": len(images)
        }
        
    except Exception as e:
        logger.error(f"Gallery error: {e}")
        raise HTTPException(status_code=500, detail="Failed to load gallery")


# ============================================================================
# VOICE ASSISTANT ENDPOINTS
# ============================================================================

@app.post("/voice/speech-to-text")
async def speech_to_text(
    audio_file: Optional[str] = None,
    use_microphone: bool = False
):
    """
    Convert speech to text.
    
    Args:
        audio_file: Path to audio file (WAV, FLAC, MP3)
        use_microphone: Use microphone input instead of file
        
    Returns:
        Transcribed text
        
    Example:
        POST /voice/speech-to-text
        {"use_microphone": true}
    """
    try:
        logger.info("Speech-to-text requested")
        
        result = await voice_assistant.speech_to_text(
            audio_file=audio_file,
            use_microphone=use_microphone
        )
        
        return result
        
    except Exception as e:
        logger.error(f"STT error: {e}")
        raise HTTPException(status_code=500, detail=f"Speech-to-text failed: {str(e)}")


@app.post("/voice/text-to-speech")
async def text_to_speech(
    text: str,
    save_file: Optional[str] = None,
    language: str = "en"
):
    """
    Convert text to speech.
    
    Args:
        text: Text to convert to speech
        save_file: Optional path to save audio file
        language: Language code ("en", "es", "fr", etc.)
        
    Returns:
        Audio file path
        
    Example:
        POST /voice/text-to-speech
        {
            "text": "Hello, I am Nitro AI",
            "language": "en"
        }
    """
    try:
        logger.info(f"Text-to-speech requested: {text[:50]}...")
        
        # Update language if different
        if language != voice_assistant.language:
            voice_assistant.language = language
        
        result = await voice_assistant.text_to_speech(
            text=text,
            save_file=save_file
        )
        
        return result
        
    except Exception as e:
        logger.error(f"TTS error: {e}")
        raise HTTPException(status_code=500, detail=f"Text-to-speech failed: {str(e)}")


# ============================================================================
# WEB SEARCH ENDPOINTS
# ============================================================================

@app.post("/search")
async def web_search(
    query: str,
    summarize: bool = True
):
    """
    Search the web and get AI-summarized results (Perplexity-style).
    
    Args:
        query: Search query
        summarize: Use AI to summarize results
        
    Returns:
        Search results with AI summary and citations
        
    Example:
        POST /search
        {
            "query": "What is quantum computing?",
            "summarize": true
        }
    """
    try:
        logger.info(f"Web search requested: {query}")
        
        result = await web_search_ai.search(
            query=query,
            summarize=summarize
        )
        
        return result
        
    except Exception as e:
        logger.error(f"Search error: {e}")
        raise HTTPException(status_code=500, detail=f"Web search failed: {str(e)}")


# === DEVELOPMENT ENDPOINT ===
# Only available in debug mode
if settings.DEBUG_MODE:
    @app.post("/debug/clear-memory")
    async def clear_all_memory():
        """
        [DEBUG ONLY] Clear all conversation memory.
        WARNING: This deletes all stored conversations!
        """
        try:
            memory_manager.clear_all_sessions()
            logger.warning("All memory cleared via debug endpoint!")
            return {
                "message": "All conversation memory cleared",
                "timestamp": datetime.now().isoformat()
            }
        except Exception as e:
            logger.error(f"Error clearing memory: {e}")
            raise HTTPException(status_code=500, detail="Failed to clear memory")


# ============================================================================
# AUTOMATION AGENT ENDPOINTS (NEW)
# ============================================================================

@app.post("/agent/execute")
async def execute_agent_task(task: Dict[str, Any]):
    """
    Execute automation agent task.
    
    Supports:
    - Code analysis and assistance
    - File operations
    - Task scheduling
    
    Example Request:
        POST /agent/execute
        {
            "type": "code_analyze",
            "code": "def hello():\\n    print('world')",
            "language": "python"
        }
    """
    try:
        logger.info(f"Agent task requested: {task.get('type')}")
        
        result = await agent_manager.execute_task(task)
        
        return {
            "status": "success" if result.get("success") else "error",
            "result": result,
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Agent execution error: {e}")
        raise HTTPException(status_code=500, detail=f"Agent task failed: {str(e)}")


@app.get("/agent/list")
async def list_agents():
    """
    List all available automation agents and their capabilities.
    
    Returns:
        List of agents with descriptions and status
    """
    try:
        agents = agent_manager.get_agent_info()
        
        return {
            "status": "success",
            "agents": agents,
            "total": len(agents)
        }
        
    except Exception as e:
        logger.error(f"Error listing agents: {e}")
        raise HTTPException(status_code=500, detail="Failed to list agents")


@app.post("/agent/code-review")
async def code_review(code: str, language: str = "python"):
    """
    Quick code review endpoint.
    
    Args:
        code: Source code to review
        language: Programming language
    
    Returns:
        Code review with suggestions and issues
    """
    try:
        task = {
            "type": "code_review",
            "agent": "code_assistant",
            "code": code,
            "language": language
        }
        
        result = await agent_manager.execute_task(task)
        
        return result
        
    except Exception as e:
        logger.error(f"Code review error: {e}")
        raise HTTPException(status_code=500, detail="Code review failed")


@app.post("/agent/file-analyze")
async def analyze_file(file_path: str):
    """
    Analyze file content and metadata.
    
    Args:
        file_path: Path to file to analyze
    
    Returns:
        File analysis results
    """
    try:
        task = {
            "type": "file_analyze",
            "agent": "file_analyzer",
            "path": file_path
        }
        
        result = await agent_manager.execute_task(task)
        
        return result
        
    except Exception as e:
        logger.error(f"File analysis error: {e}")
        raise HTTPException(status_code=500, detail="File analysis failed")


# ============================================================================
# PERFORMANCE MONITORING ENDPOINT (NEW)
# ============================================================================

@app.get("/metrics")
async def get_metrics():
    """
    Get performance metrics and system status.
    
    Returns:
        System metrics including:
        - Active sessions
        - Memory usage
        - Response times
        - API call counts
    """
    try:
        import psutil
        import os
        
        # Get process info
        process = psutil.Process(os.getpid())
        
        # Get memory stats
        memory_stats = memory_manager.get_statistics()
        
        metrics = {
            "status": "healthy",
            "timestamp": datetime.now().isoformat(),
            "system": {
                "cpu_percent": process.cpu_percent(),
                "memory_mb": process.memory_info().rss / 1024 / 1024,
                "threads": process.num_threads()
            },
            "application": {
                "active_sessions": memory_stats.get("total_sessions", 0),
                "total_messages": memory_stats.get("total_messages", 0),
                "uptime_seconds": int(time.time() - process.create_time())
            },
            "agents": {
                "available": len(agent_manager.agents),
                "enabled": sum(1 for a in agent_manager.agents.values() if a.enabled)
            }
        }
        
        return metrics
        
    except ImportError:
        # psutil not available
        return {
            "status": "limited",
            "message": "Install psutil for detailed metrics: pip install psutil",
            "basic_stats": memory_manager.get_statistics()
        }
    except Exception as e:
        logger.error(f"Metrics error: {e}")
        raise HTTPException(status_code=500, detail="Failed to get metrics")


# === STATIC FILE SERVING (Frontend) ===
# Mount frontend files to serve the web interface
try:
    from pathlib import Path
    frontend_path = Path(__file__).parent.parent / "frontend"
    if frontend_path.exists():
        app.mount("/", StaticFiles(directory=str(frontend_path), html=True), name="frontend")
        logger.info(f"✅ Frontend mounted at {frontend_path}")
    else:
        logger.warning(f"⚠️ Frontend directory not found at {frontend_path}")
except Exception as e:
    logger.warning(f"⚠️ Could not mount frontend: {e}")

# === SERVER ENTRY POINT ===
if __name__ == "__main__":
    import uvicorn
    logger.info("Starting server directly from main.py")
    uvicorn.run(
        app,
        host=settings.HOST,
        port=settings.PORT,
        log_level=settings.LOG_LEVEL.lower()
    )
