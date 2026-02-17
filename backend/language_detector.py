"""
Language Detection Module for Nitro AI
======================================

This module provides lightweight language detection for user messages.
Currently uses simple pattern matching - ready for future AI integration.

FUTURE INTEGRATION:
- Use langdetect library for better accuracy
- Use OpenAI/Anthropic for context-aware translation
- Add support for 100+ languages
- Implement automatic translation

For now: Detects English, Spanish, French, German, Chinese, Japanese, Arabic
Uses simple character patterns (no heavy dependencies)
"""

import re
from typing import Dict, Optional, Tuple
from datetime import datetime


class LanguageDetector:
    """
    Lightweight language detector using character patterns.
    
    NO HEAVY AI DEPENDENCIES - Just pattern matching!
    Perfect for low-compute laptops.
    
    Supported languages:
    - English (en)
    - Spanish (es)
    - French (fr)
    - German (de)
    - Chinese (zh)
    - Japanese (ja)
    - Arabic (ar)
    - Portuguese (pt)
    - Russian (ru)
    - Italian (it)
    """
    
    # Language patterns (character sets and common words)
    PATTERNS = {
        'zh': r'[\u4e00-\u9fff]+',  # Chinese characters
        'ja': r'[\u3040-\u309f\u30a0-\u30ff]+',  # Japanese hiragana/katakana
        'ar': r'[\u0600-\u06ff]+',  # Arabic script
        'ru': r'[\u0400-\u04ff]+',  # Cyrillic script
    }
    
    # Common words for pattern matching (simple detection)
    COMMON_WORDS = {
        'en': ['the', 'is', 'are', 'and', 'or', 'you', 'what', 'how', 'when', 'where'],
        'es': ['el', 'la', 'los', 'las', 'que', 'como', 'cuando', 'donde', 'por', 'para'],
        'fr': ['le', 'la', 'les', 'un', 'une', 'est', 'sont', 'que', 'comme', 'pour'],
        'de': ['der', 'die', 'das', 'ist', 'sind', 'und', 'oder', 'wie', 'was', 'wo'],
        'pt': ['o', 'a', 'os', 'as', 'que', 'como', 'quando', 'onde', 'por', 'para'],
        'it': ['il', 'la', 'i', 'le', 'che', 'come', 'quando', 'dove', 'per', 'sono'],
    }
    
    # Supported languages with names
    SUPPORTED_LANGUAGES = {
        'en': 'English',
        'es': 'Spanish',
        'fr': 'French',
        'de': 'German',
        'zh': 'Chinese',
        'ja': 'Japanese',
        'ar': 'Arabic',
        'pt': 'Portuguese',
        'ru': 'Russian',
        'it': 'Italian',
    }
    
    def __init__(self):
        """Initialize the language detector."""
        self.detection_history = []
    
    def detect_language(self, text: str) -> Tuple[str, float]:
        """
        Detect language from text.
        
        Args:
            text: Input text to analyze
            
        Returns:
            Tuple of (language_code, confidence_score)
            Example: ('en', 0.95) or ('es', 0.80)
        
        FUTURE: Replace with proper AI-based detection
        - Use langdetect library
        - Use OpenAI for context-aware detection
        - Support mixed-language content
        """
        if not text or len(text.strip()) < 3:
            return ('en', 0.5)  # Default to English for short text
        
        text_lower = text.lower()
        scores = {}
        
        # Check character-based patterns (Chinese, Japanese, Arabic, Russian)
        for lang_code, pattern in self.PATTERNS.items():
            matches = re.findall(pattern, text)
            if matches:
                # Calculate ratio of special characters
                special_chars = ''.join(matches)
                ratio = len(special_chars) / len(text)
                scores[lang_code] = ratio
        
        # If character pattern found with high confidence, return it
        if scores:
            best_lang = max(scores, key=scores.get)
            if scores[best_lang] > 0.3:  # 30% threshold
                return (best_lang, min(scores[best_lang], 1.0))
        
        # Check word-based patterns (European languages)
        for lang_code, common_words in self.COMMON_WORDS.items():
            word_count = sum(1 for word in common_words if word in text_lower)
            if word_count > 0:
                # Score based on word matches
                scores[lang_code] = word_count / len(common_words)
        
        # Return best match or default to English
        if scores:
            best_lang = max(scores, key=scores.get)
            confidence = min(scores[best_lang], 1.0)
            
            # Log detection for history
            self._log_detection(text, best_lang, confidence)
            
            return (best_lang, confidence)
        
        # Default to English with low confidence
        return ('en', 0.3)
    
    def get_language_name(self, lang_code: str) -> str:
        """
        Get full language name from code.
        
        Args:
            lang_code: Two-letter language code (e.g., 'en', 'es')
            
        Returns:
            Full language name (e.g., 'English', 'Spanish')
        """
        return self.SUPPORTED_LANGUAGES.get(lang_code, 'Unknown')
    
    def is_supported(self, lang_code: str) -> bool:
        """
        Check if language is supported.
        
        Args:
            lang_code: Two-letter language code
            
        Returns:
            True if supported, False otherwise
        """
        return lang_code in self.SUPPORTED_LANGUAGES
    
    def get_supported_languages(self) -> Dict[str, str]:
        """
        Get all supported languages.
        
        Returns:
            Dictionary of {code: name} pairs
            Example: {'en': 'English', 'es': 'Spanish', ...}
        """
        return self.SUPPORTED_LANGUAGES.copy()
    
    def _log_detection(self, text: str, lang_code: str, confidence: float):
        """
        Log language detection for analytics.
        
        FUTURE: Use for improving detection accuracy
        - Store in database
        - Track user corrections
        - Train custom models
        """
        self.detection_history.append({
            'timestamp': datetime.now().isoformat(),
            'text_length': len(text),
            'detected_language': lang_code,
            'confidence': confidence,
        })
        
        # Keep only last 100 detections (memory management)
        if len(self.detection_history) > 100:
            self.detection_history = self.detection_history[-100:]
    
    def get_detection_stats(self) -> Dict:
        """
        Get statistics about detected languages.
        
        Returns:
            Dictionary with language usage stats
            
        FUTURE: Use for analytics dashboard
        """
        if not self.detection_history:
            return {}
        
        stats = {}
        for detection in self.detection_history:
            lang = detection['detected_language']
            stats[lang] = stats.get(lang, 0) + 1
        
        return {
            'total_detections': len(self.detection_history),
            'language_counts': stats,
            'most_common': max(stats, key=stats.get) if stats else 'en',
        }


# FUTURE: Translation Support
# ============================
# When you want to add translation, use these placeholders:

class TranslationService:
    """
    PLACEHOLDER for future translation service.
    
    INTEGRATION OPTIONS:
    1. Google Translate API (paid, very accurate)
    2. LibreTranslate (free, open-source, self-hosted)
    3. OpenAI GPT-4 (context-aware translation)
    4. DeepL API (best quality, paid)
    
    SETUP STEPS (when ready):
    1. Choose translation service
    2. Add API key to .env
    3. Uncomment code below
    4. Update frontend to show translations
    """
    
    def __init__(self, api_key: Optional[str] = None):
        """Initialize translation service (placeholder)."""
        self.api_key = api_key
        self.enabled = False  # Set to True when implemented
    
    def translate(self, text: str, source_lang: str, target_lang: str) -> str:
        """
        Translate text between languages (placeholder).
        
        Args:
            text: Text to translate
            source_lang: Source language code
            target_lang: Target language code
            
        Returns:
            Translated text
            
        FUTURE IMPLEMENTATION:
        # Using OpenAI:
        # response = openai.ChatCompletion.create(
        #     model="gpt-4",
        #     messages=[{
        #         "role": "user",
        #         "content": f"Translate from {source_lang} to {target_lang}: {text}"
        #     }]
        # )
        # return response.choices[0].message.content
        
        # Using Google Translate:
        # from google.cloud import translate_v2
        # client = translate_v2.Client()
        # result = client.translate(text, target_language=target_lang)
        # return result['translatedText']
        """
        return f"[Translation placeholder: {text}]"
    
    def detect_and_translate(self, text: str, target_lang: str) -> Dict:
        """
        Auto-detect language and translate (placeholder).
        
        FUTURE: Combine detection + translation in one step
        """
        return {
            'original_text': text,
            'detected_language': 'en',
            'translated_text': text,
            'target_language': target_lang,
        }


# Usage Examples (for developers):
# =================================

if __name__ == "__main__":
    # Example 1: Basic language detection
    detector = LanguageDetector()
    
    test_texts = [
        "Hello, how are you?",
        "Hola, ¿cómo estás?",
        "Bonjour, comment allez-vous?",
        "你好，你好吗？",
        "こんにちは、元気ですか？",
    ]
    
    print("Language Detection Examples:")
    print("-" * 50)
    for text in test_texts:
        lang_code, confidence = detector.detect_language(text)
        lang_name = detector.get_language_name(lang_code)
        print(f"Text: {text}")
        print(f"Detected: {lang_name} ({lang_code}) - Confidence: {confidence:.2f}")
        print()
    
    # Example 2: Get supported languages
    print("\nSupported Languages:")
    print("-" * 50)
    for code, name in detector.get_supported_languages().items():
        print(f"{code}: {name}")
    
    # Example 3: Detection statistics
    print("\nDetection Statistics:")
    print("-" * 50)
    stats = detector.get_detection_stats()
    print(stats)
