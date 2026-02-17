"""
Voice Assistant Module - Speech-to-Text & Text-to-Speech
Optimized for low-compute laptops
"""

from typing import Optional, Dict
from datetime import datetime
import os
import logging

logger = logging.getLogger(__name__)

# Try importing voice libraries
try:
    import speech_recognition as sr
    SR_AVAILABLE = True
except ImportError:
    SR_AVAILABLE = False
    logger.info("⚠️  speech_recognition not available. Install with: pip install SpeechRecognition")

try:
    from gtts import gTTS
    GTTS_AVAILABLE = True
except ImportError:
    GTTS_AVAILABLE = False
    logger.info("⚠️  gTTS not available. Install with: pip install gTTS")

try:
    import pyttsx3
    PYTTSX3_AVAILABLE = True
except ImportError:
    PYTTSX3_AVAILABLE = False
    logger.info("⚠️  pyttsx3 not available. Install with: pip install pyttsx3")


class VoiceAssistant:
    """
    Voice assistant interface with STT and TTS.
    
    BEGINNER-FRIENDLY:
    - FREE speech-to-text using Google Web Speech API
    - FREE text-to-speech using gTTS or pyttsx3
    - No API keys required for basic features
    - Works offline with pyttsx3
    
    FEATURES:
    - 🎤 Speech-to-Text (microphone input)
    - 🔊 Text-to-Speech (audio output)
    - 🌐 Multi-language support
    - 💾 Audio file transcription
    """
    
    def __init__(
        self,
        stt_engine: str = "google",
        tts_engine: str = "gtts",
        language: str = "en"
    ):
        """
        Initialize Voice Assistant.
        
        Args:
            stt_engine: "google" (online, free) or "sphinx" (offline)
            tts_engine: "gtts" (online, free) or "pyttsx3" (offline)
            language: Language code ("en", "es", "fr", etc.)
        """
        self.stt_engine = stt_engine
        self.tts_engine = tts_engine
        self.language = language
        self.recognizer = sr.Recognizer() if SR_AVAILABLE else None
        
        logger.info(f"VoiceAssistant initialized: STT={stt_engine}, TTS={tts_engine}, Lang={language}")
    
    async def speech_to_text(
        self,
        audio_file: Optional[str] = None,
        use_microphone: bool = False,
        timeout: int = 5
    ) -> Dict:
        """
        Convert speech to text.
        
        Args:
            audio_file: Path to audio file (WAV, FLAC, MP3)
            use_microphone: Use microphone input instead of file
            timeout: Recording timeout in seconds
        
        Returns:
            Dictionary with transcribed text
            
        Example:
            >>> va = VoiceAssistant()
            >>> result = await va.speech_to_text(use_microphone=True)
            >>> print(result['text'])
        """
        if not SR_AVAILABLE:
            return self._placeholder_stt_response()
        
        try:
            if use_microphone:
                # Record from microphone
                logger.info("Listening from microphone...")
                
                with sr.Microphone() as source:
                    # Adjust for ambient noise
                    self.recognizer.adjust_for_ambient_noise(source, duration=1)
                    logger.info("Recording... (speak now)")
                    
                    # Listen with timeout
                    audio = self.recognizer.listen(source, timeout=timeout)
                
                logger.info("Recording complete. Transcribing...")
                
            else:
                # Load from file
                if not audio_file or not os.path.exists(audio_file):
                    return {
                        "status": "error",
                        "error": "Audio file not found"
                    }
                
                logger.info(f"Transcribing audio file: {audio_file}")
                
                with sr.AudioFile(audio_file) as source:
                    audio = self.recognizer.record(source)
            
            # Transcribe using selected engine
            if self.stt_engine == "google":
                text = self.recognizer.recognize_google(audio, language=self.language)
            else:
                # Fallback to Google
                text = self.recognizer.recognize_google(audio, language=self.language)
            
            logger.info(f"✅ Transcribed: {text}")
            
            return {
                "status": "success",
                "text": text,
                "language": self.language,
                "engine": self.stt_engine,
                "timestamp": datetime.now().isoformat()
            }
            
        except sr.WaitTimeoutError:
            return {
                "status": "error",
                "error": "No speech detected (timeout)"
            }
        except sr.UnknownValueError:
            return {
                "status": "error",
                "error": "Speech not understood"
            }
        except sr.RequestError as e:
            return {
                "status": "error",
                "error": f"Speech recognition service error: {str(e)}"
            }
        except Exception as e:
            logger.error(f"STT error: {e}")
            return {
                "status": "error",
                "error": str(e)
            }
    
    async def text_to_speech(
        self,
        text: str,
        save_file: Optional[str] = None,
        play: bool = False
    ) -> Dict:
        """
        Convert text to speech.
        
        Args:
            text: Text to convert to speech
            save_file: Path to save audio file (MP3)
            play: Play audio immediately (requires audio device)
        
        Returns:
            Dictionary with audio file path
            
        Example:
            >>> va = VoiceAssistant()
            >>> result = await va.text_to_speech(
            ...     text="Hello, I am Nitro AI",
            ...     save_file="response.mp3"
            ... )
        """
        if not GTTS_AVAILABLE and not PYTTSX3_AVAILABLE:
            return self._placeholder_tts_response()
        
        try:
            logger.info(f"Converting text to speech: {text[:50]}...")
            
            # Generate filename if not provided
            if not save_file:
                audio_dir = os.path.join(os.path.dirname(__file__), "..", "..", "audio")
                os.makedirs(audio_dir, exist_ok=True)
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                save_file = os.path.join(audio_dir, f"tts_{timestamp}.mp3")
            
            # Use selected TTS engine
            if self.tts_engine == "gtts" and GTTS_AVAILABLE:
                # Use Google Text-to-Speech (online, natural voices)
                tts = gTTS(text=text, lang=self.language, slow=False)
                tts.save(save_file)
                
            elif PYTTSX3_AVAILABLE:
                # Use pyttsx3 (offline, robotic voices but works without internet)
                engine = pyttsx3.init()
                engine.setProperty('rate', 150)  # Speed
                engine.setProperty('volume', 0.9)  # Volume
                engine.save_to_file(text, save_file)
                engine.runAndWait()
            
            logger.info(f"✅ Audio saved to: {save_file}")
            
            # Optionally play audio
            if play:
                try:
                    import platform
                    import subprocess
                    
                    if platform.system() == "Windows":
                        os.startfile(save_file)
                    elif platform.system() == "Darwin":  # macOS
                        subprocess.call(["open", save_file])
                    else:  # Linux
                        subprocess.call(["xdg-open", save_file])
                except:
                    logger.warning("Could not auto-play audio")
            
            return {
                "status": "success",
                "file_path": save_file,
                "text": text,
                "language": self.language,
                "engine": self.tts_engine,
                "timestamp": datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"TTS error: {e}")
            return {
                "status": "error",
                "error": str(e)
            }
    
    def _placeholder_stt_response(self) -> Dict:
        """Return placeholder when STT not available."""
        return {
            "status": "placeholder",
            "message": "Speech-to-text not available",
            "instructions": {
                "install": "pip install SpeechRecognition pyaudio",
                "pyaudio_windows": "Download wheel from: https://www.lfd.uci.edu/~gohlke/pythonlibs/#pyaudio",
                "microphone": "Requires microphone access",
                "free": "Uses Google Web Speech API (free)"
            }
        }
    
    def _placeholder_tts_response(self) -> Dict:
        """Return placeholder when TTS not available."""
        return {
            "status": "placeholder",
            "message": "Text-to-speech not available",
            "instructions": {
                "install_online": "pip install gTTS (requires internet)",
                "install_offline": "pip install pyttsx3 (works offline)",
                "free": "Both options are completely free"
            }
        }


def create_voice_assistant(
    stt_engine: str = "google",
    tts_engine: str = "gtts",
    language: str = "en"
) -> VoiceAssistant:
    """
    Factory function for voice assistants.
    
    Args:
        stt_engine: Speech-to-text engine
        tts_engine: Text-to-speech engine
        language: Language code
        
    Returns:
        VoiceAssistant instance
    """
    return VoiceAssistant(
        stt_engine=stt_engine,
        tts_engine=tts_engine,
        language=language
    )
