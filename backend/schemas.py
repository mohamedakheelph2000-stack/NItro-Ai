# schemas.py - Data models/schemas for our API
# This file defines the structure of data we send and receive
# Keeping models in a separate file makes the code more organized

from pydantic import BaseModel, Field, validator
from datetime import datetime
from typing import Optional, List, Dict, Any
from enum import Enum

class ChatMessage(BaseModel):
    """
    Schema for incoming chat messages from users.
    
    This defines what data we expect when someone sends a message to /chat endpoint.
    """
    message: str = Field(
        ..., 
        min_length=1, 
        max_length=1000,
        description="The user's message text"
    )
    user_id: Optional[str] = Field(
        default="anonymous",
        description="Identifier for the user (optional)"
    )
    session_id: Optional[str] = Field(
        default=None,
        description="Session ID for conversation tracking (optional)"
    )
    
    @validator('message')
    def message_not_empty(cls, v):
        """
        Validator to ensure the message isn't just whitespace.
        This runs automatically when data is received.
        """
        if not v.strip():
            raise ValueError('Message cannot be empty or just whitespace')
        return v.strip()

    class Config:
        # Example data shown in API documentation
        schema_extra = {
            "example": {
                "message": "Hello Nitro AI, how are you?",
                "user_id": "user_123"
            }
        }


class ChatResponse(BaseModel):
    """
    Schema for chat responses sent back to users.
    
    This defines the structure of our reply.
    """
    session_id: Optional[str] = Field(None, description="Session ID for this conversation")
    response: str = Field(..., description="The AI's response message")
    timestamp: str = Field(..., description="When the response was generated")
    status: str = Field(..., description="Status of the request (success/error)")
    user_id: Optional[str] = Field(None, description="The user who sent the message")
    ai_model: Optional[str] = Field("unknown", description="AI model used (phi3, gemini-pro, etc.)")
    ai_source: Optional[str] = Field("unknown", description="AI source (ollama_local, gemini_cloud, fallback)")
    
    class Config:
        # Example data shown in API documentation
        schema_extra = {
            "example": {
                "response": "Hello! I'm Nitro AI, how can I help you today?",
                "timestamp": "2026-02-17T10:30:00",
                "status": "success",
                "user_id": "user_123",
                "ai_model": "phi3",
                "ai_source": "ollama_local"
            }
        }


class ErrorResponse(BaseModel):
    """
    Schema for error responses.
    
    When something goes wrong, we send a consistent error format.
    """
    error: str = Field(..., description="Error message")
    detail: Optional[str] = Field(None, description="Additional error details")
    timestamp: str = Field(..., description="When the error occurred")
    
    class Config:
        schema_extra = {
            "example": {
                "error": "Invalid message format",
                "detail": "Message cannot be empty",
                "timestamp": "2026-02-17T10:30:00"
            }
        }


class HealthCheckResponse(BaseModel):
    """
    Schema for health check responses.
    
    Used to monitor if the server is running properly.
    """
    status: str = Field(..., description="Health status (healthy/unhealthy)")
    timestamp: str = Field(..., description="Current server time")
    memory_stats: Optional[Dict[str, Any]] = Field(None, description="Memory system statistics")
    
    class Config:
        schema_extra = {
            "example": {
                "status": "healthy",
                "timestamp": "2026-02-17T10:30:00",
                "version": "1.0.0",
                "memory_stats": {
                    "total_sessions": 5,
                    "total_messages": 50
                }
            }
        }


class SessionCreate(BaseModel):
    """
    Schema for creating a new conversation session.
    """
    user_id: str = Field(default="anonymous", description="User identifier")
    
    class Config:
        schema_extra = {
            "example": {
                "user_id": "user_123"
            }
        }


class SessionResponse(BaseModel):
    """
    Schema for session creation response.
    """
    session_id: str = Field(..., description="Unique session identifier")
    user_id: str = Field(..., description="User identifier")
    created_at: str = Field(..., description="Session creation timestamp")
    message: str = Field(..., description="Status message")
    
    class Config:
        schema_extra = {
            "example": {
                "session_id": "abc-123-def",
                "user_id": "user_123",
                "created_at": "2026-02-17T10:30:00",
                "message": "Session created successfully"
            }
        }


class HistoryResponse(BaseModel):
    """
    Schema for conversation history response.
    """
    session_id: str = Field(..., description="Session identifier")
    user_id: str = Field(..., description="User identifier")
    created_at: str = Field(..., description="Session creation time")
    last_updated: str = Field(..., description="Last message time")
    messages: List[Dict[str, Any]] = Field(..., description="List of messages")
    message_count: int = Field(..., description="Total number of messages")
    
    class Config:
        schema_extra = {
            "example": {
                "session_id": "abc-123",
                "user_id": "user_123",
                "created_at": "2026-02-17T10:00:00",
                "last_updated": "2026-02-17T10:30:00",
                "messages": [
                    {
                        "timestamp": "2026-02-17T10:00:00",
                        "sender": "user",
                        "message": "Hello!",
                        "response": "Hi there!"
                    }
                ],
                "message_count": 1,
                "created_at": "2025-02-17T10:30:00",
                "version": "1.0.0"
            }
        }


# ============================================================================
# LANGUAGE DETECTION & TRANSLATION SCHEMAS
# ============================================================================

class LanguageDetectRequest(BaseModel):
    """Request for language detection."""
    text: str = Field(..., max_length=5000, description="Text to detect language")


class LanguageDetectResponse(BaseModel):
    """Response from language detection."""
    detected_language: str = Field(..., description="Detected language code (e.g., 'en', 'es')")
    language_name: str = Field(..., description="Full language name (e.g., 'English')")
    confidence: float = Field(..., ge=0.0, le=1.0, description="Confidence score 0-1")
    supported: bool = Field(..., description="Whether language is supported")


class LanguagePreferenceRequest(BaseModel):
    """Set user's language preference."""
    user_id: str = Field(..., description="User ID")
    language: str = Field(..., min_length=2, max_length=5, description="Language code")
    auto_detect: bool = Field(default=True, description="Auto-detect language from messages")


class LanguagePreferenceResponse(BaseModel):
    """Language preference confirmation."""
    user_id: str
    language: str
    language_name: str
    auto_detect: bool
    message: str


class SupportedLanguagesResponse(BaseModel):
    """List of supported languages."""
    languages: Dict[str, str] = Field(..., description="Dictionary of {code: name}")
    total: int = Field(..., description="Total number of supported languages")


# ============================================================================
# VIDEO GENERATION SCHEMAS
# ============================================================================

class VideoStyle(str, Enum):
    """Video generation styles."""
    REALISTIC = "realistic"
    ANIME = "anime"
    CARTOON = "cartoon"
    CINEMATIC = "cinematic"
    ABSTRACT = "abstract"
    DOCUMENTARY = "documentary"


class VideoResolution(str, Enum):
    """Video resolutions."""
    SD = "512x512"
    HD = "1280x720"
    FULL_HD = "1920x1080"
    ULTRA_HD = "3840x2160"


class VideoGenerateRequest(BaseModel):
    """Request to generate video."""
    prompt: str = Field(..., min_length=3, max_length=1000, description="Text description of video")
    duration: int = Field(default=4, ge=2, le=16, description="Video duration in seconds")
    style: VideoStyle = Field(default=VideoStyle.REALISTIC, description="Visual style")
    resolution: VideoResolution = Field(default=VideoResolution.HD, description="Output resolution")
    fps: int = Field(default=24, ge=12, le=60, description="Frames per second")
    seed: Optional[int] = Field(default=None, description="Random seed for reproducibility")
    
    class Config:
        schema_extra = {
            "example": {
                "prompt": "A serene sunset over the ocean with gentle waves",
                "duration": 4,
                "style": "cinematic",
                "resolution": "1280x720",
                "fps": 24
            }
        }


class VideoGenerateResponse(BaseModel):
    """Response from video generation."""
    video_id: str
    prompt: str
    status: str = Field(..., description="Status: 'placeholder', 'queued', 'processing', 'completed', 'failed'")
    duration: int
    style: str
    resolution: str
    fps: int
    url: Optional[str] = None
    thumbnail_url: Optional[str] = None
    size_mb: Optional[float] = None
    created_at: str
    estimated_time: int = Field(..., description="Estimated generation time in seconds")
    message: str


class VideoStatusResponse(BaseModel):
    """Video generation status."""
    video_id: str
    status: str
    progress: int = Field(..., ge=0, le=100, description="Progress percentage")
    eta_seconds: int = Field(..., description="Estimated time remaining")
    message: str
