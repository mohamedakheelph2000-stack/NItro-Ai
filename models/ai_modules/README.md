# AI Modules - README

This folder contains placeholder modules for future AI features.

## Modules

### 1. chat_ai.py - Chat AI Integration
- **Purpose**: Generate AI responses to user messages
- **Future Integrations**:
  - OpenAI GPT (GPT-3.5, GPT-4)
  - Local models via Ollama (Llama 2, Mistral, etc.)
  - Anthropic Claude
  - Google Gemini
  
- **Usage** (when implemented):
  ```python
  from ai_modules.chat_ai import create_chat_ai
  
  ai = create_chat_ai('openai', api_key='your-key')
  response = await ai.generate_response("Hello!")
  ```

### 2. image_gen.py - Image Generation
- **Purpose**: Generate images from text descriptions
- **Future Integrations**:
  - DALL-E 3 (OpenAI)
  - Stable Diffusion (Local or API)
  - Midjourney (API)
  
- **Usage** (when implemented):
  ```python
  from ai_modules.image_gen import create_image_generator
  
  generator = create_image_generator('dalle')
  image = await generator.generate_image("A cat on Mars")
  ```

### 3. voice.py - Voice Assistant
- **Purpose**: Speech-to-text and text-to-speech
- **Future Integrations**:
  - Speech-to-Text: OpenAI Whisper, Google Speech, Azure
  - Text-to-Speech: ElevenLabs, Google TTS, Azure TTS
  
- **Usage** (when implemented):
  ```python
  from ai_modules.voice import create_voice_assistant
  
  voice = create_voice_assistant(stt_type='whisper', tts_type='elevenlabs')
  text = await voice.speech_to_text("audio.mp3")
  audio = await voice.text_to_speech("Hello world")
  ```

### 4. web_search.py - Web Search & RAG
- **Purpose**: Web search and Retrieval-Augmented Generation
- **Future Integrations**:
  - Google Search API
  - Bing Search API
  - Tavily AI
  - Vector databases (ChromaDB, Pinecone)
  
- **Usage** (when implemented):
  ```python
  from ai_modules.web_search import create_web_search
  
  search = create_web_search('google', api_key='your-key')
  results = await search.search("Latest AI news")
  summary = await search.search_and_summarize("AI trends 2026")
  ```

## Implementation Status

🔴 **Not Implemented** - All modules are currently placeholders

To implement these features:
1. Choose your preferred AI service
2. Install required packages
3. Uncomment and adapt the example code in each module
4. Add API keys to `.env` file
5. Update `main.py` to use the modules

## Lightweight Recommendations

For **low-compute laptops**, consider:

1. **Chat AI**: 
   - ✅ OpenAI API (cloud-based, no local compute)
   - ✅ Smaller local models via Ollama (Phi-2, TinyLlama)
   - ❌ Avoid large models like Llama 70B

2. **Image Generation**:
   - ✅ DALL-E API (cloud-based)
   - ❌ Avoid running Stable Diffusion locally

3. **Voice**:
   - ✅ Whisper API or small Whisper models
   - ✅ ElevenLabs API for TTS

4. **Web Search**:
   - ✅ All search APIs are cloud-based (no local compute)

## Next Steps

When you're ready to add AI features:
1. Choose one module to implement first
2. Follow the integration examples in the code
3. Test with small examples
4. Gradually expand functionality

## Security Note

**Never commit API keys to Git!**
- Store keys in `.env` file
- `.env` is already in `.gitignore`
- Use environment variables in production
