# config.py - Enhanced configuration settings for Nitro AI Backend
# This file stores all settings in one place, making them easy to change

import os
from dotenv import load_dotenv
from pathlib import Path

# Load environment variables from .env file (if it exists)
# This allows us to store secrets safely without hardcoding them
load_dotenv()

class Settings:
    """
    Settings class that holds all configuration values.
    Think of this as a control panel for your backend.
    """
    
    # === SERVER SETTINGS ===
    APP_NAME: str = "Nitro AI Backend"
    VERSION: str = "5.0.0"  # Production v5.0 with automation agents
    HOST: str = "0.0.0.0"  # Listen on all network interfaces
    PORT: int = int(os.getenv("PORT", "8000"))  # Dynamic port for cloud platforms
    
    # === CORS SETTINGS ===
    # Which websites can talk to our backend
    # Supports both wildcard for development and specific origins for production
    _allowed_origins = os.getenv("ALLOWED_ORIGINS", "*")
    ALLOWED_ORIGINS: list = _allowed_origins.split(",") if "," in _allowed_origins else [_allowed_origins]
    
    # === API KEYS & SECRETS ===
    # Never hardcode secrets! Always use environment variables.
    API_KEY: str = os.getenv("NITRO_API_KEY", "")
    
    # AI Service API Keys (for future use)
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")
    ANTHROPIC_API_KEY: str = os.getenv("ANTHROPIC_API_KEY", "")
    GOOGLE_API_KEY: str = os.getenv("GOOGLE_API_KEY", "")
    
    # === DATABASE SETTINGS ===
    # For future database integration
    DATABASE_URL: str = os.getenv("DATABASE_URL", "")
    
    # === LOGGING SETTINGS ===
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")  # INFO, DEBUG, WARNING, ERROR
    
    # === CHAT SETTINGS ===
    MAX_MESSAGE_LENGTH: int = 1000  # Maximum characters in a user message
    DEFAULT_USER_ID: str = "anonymous"
    MAX_CONVERSATION_HISTORY: int = 50  # Max messages to keep in context
    
    # === AI MODEL SETTINGS ===
    # Default AI model configuration
    AI_MODEL: str = os.getenv("AI_MODEL", "ollama")  # ollama, openai, dummy, etc.
    DEFAULT_AI_MODEL: str = os.getenv("AI_MODEL", "ollama")  # Backward compatibility
    AI_TEMPERATURE: float = 0.7  # Creativity level (0.0 - 1.0)
    AI_MAX_TOKENS: int = 500  # Maximum response length
    
    # Local model settings (Ollama) - FREE and PRIVATE!
    OLLAMA_BASE_URL: str = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
    OLLAMA_MODEL: str = os.getenv("OLLAMA_MODEL", "llama2")  # llama2, mistral, phi, etc.
    
    # === MEMORY SETTINGS ===
    MEMORY_DIR: str = "../memory"  # Directory for conversation storage
    MAX_SESSIONS_PER_USER: int = 100  # Maximum sessions to keep per user
    AUTO_DELETE_OLD_SESSIONS: bool = False  # Auto-delete sessions older than X days
    SESSION_RETENTION_DAYS: int = 30  # Days to keep old sessions
    
    # === FEATURE FLAGS ===
    # Enable/disable features
    ENABLE_WEB_SEARCH: bool = os.getenv("ENABLE_WEB_SEARCH", "False").lower() == "true"
    ENABLE_IMAGE_GEN: bool = os.getenv("ENABLE_IMAGE_GEN", "False").lower() == "true"
    ENABLE_VOICE: bool = os.getenv("ENABLE_VOICE", "False").lower() == "true"
    ENABLE_RAG: bool = os.getenv("ENABLE_RAG", "False").lower() == "true"
    ENABLE_VIDEO_GEN: bool = os.getenv("ENABLE_VIDEO_GEN", "False").lower() == "true"
    ENABLE_TRANSLATION: bool = os.getenv("ENABLE_TRANSLATION", "False").lower() == "true"
    ENABLE_AUTO_LANGUAGE_DETECT: bool = os.getenv("ENABLE_AUTO_LANGUAGE_DETECT", "True").lower() == "true"
    
    # === LANGUAGE & TRANSLATION SETTINGS ===
    DEFAULT_LANGUAGE: str = os.getenv("DEFAULT_LANGUAGE", "en")  # Default to English
    SUPPORTED_LANGUAGES: list = ["en", "es", "fr", "de", "zh", "ja", "ar", "pt", "ru", "it"]
    AUTO_DETECT_LANGUAGE: bool = True
    TRANSLATION_SERVICE: str = os.getenv("TRANSLATION_SERVICE", "none")  # Options: 'openai', 'google', 'deepl', 'none'
    GOOGLE_TRANSLATE_API_KEY: str = os.getenv("GOOGLE_TRANSLATE_API_KEY", "")
    DEEPL_API_KEY: str = os.getenv("DEEPL_API_KEY", "")
    
    # === VIDEO GENERATION SETTINGS ===
    VIDEO_MODEL: str = os.getenv("VIDEO_MODEL", "none")  # Options: 'runway', 'stable-diffusion', 'sora', 'none'
    RUNWAY_API_KEY: str = os.getenv("RUNWAY_API_KEY", "")
    VIDEO_OUTPUT_DIR: str = "../videos"
    MAX_VIDEO_DURATION: int = 16  # Maximum video length in seconds
    DEFAULT_VIDEO_RESOLUTION: str = "1280x720"  # HD by default
    VIDEO_GENERATION_TIMEOUT: int = 600  # 10 minutes timeout
    
    # === DEVELOPMENT MODE ===
    DEBUG_MODE: bool = os.getenv("DEBUG_MODE", "False").lower() == "true"  # Default to production mode
    
    # === RATE LIMITING ===
    # Prevent abuse
    RATE_LIMIT_ENABLED: bool = True
    MAX_REQUESTS_PER_MINUTE: int = 60
    MAX_REQUESTS_PER_HOUR: int = 1000
    
    # === SECURITY SETTINGS ===
    # JWT secret for future authentication
    SECRET_KEY: str = os.getenv("SECRET_KEY", "change-this-in-production-use-random-string")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # === FILE UPLOAD SETTINGS ===
    # For future file upload features
    MAX_UPLOAD_SIZE_MB: int = 10
    ALLOWED_FILE_TYPES: list = [".txt", ".pdf", ".docx", ".jpg", ".png"]
    UPLOAD_DIR: str = "../uploads"
    
    # === PATHS ===
    # Absolute paths for different directories
    BASE_DIR: Path = Path(__file__).parent.parent
    MODELS_DIR: Path = BASE_DIR / "models"
    MEMORY_DIR_PATH: Path = BASE_DIR / "memory"
    LOGS_DIR: Path = BASE_DIR / "logs"
    
    @classmethod
    def create_directories(cls):
        """Create necessary directories if they don't exist."""
        directories = [
            cls.MEMORY_DIR_PATH,
            cls.LOGS_DIR,
            cls.MODELS_DIR
        ]
        
        for directory in directories:
            directory.mkdir(parents=True, exist_ok=True)
    
    @classmethod
    def validate_config(cls) -> bool:
        """
        Validate configuration settings.
        Returns True if configuration is valid.
        """
        issues = []
        
        # Check if AI model requires API key
        if cls.DEFAULT_AI_MODEL == "openai" and not cls.OPENAI_API_KEY:
            issues.append("OpenAI model selected but OPENAI_API_KEY not set")
        
        # Check memory directory
        if not cls.MEMORY_DIR:
            issues.append("MEMORY_DIR not configured")
        
        # Log issues
        if issues:
            print("⚠️  Configuration issues found:")
            for issue in issues:
                print(f"  - {issue}")
            return False
        
        print("✓ Configuration validated successfully")
        return True

# Create a single instance of settings to use throughout the app
settings = Settings()

# Create necessary directories on import
settings.create_directories()

