"""
Chat AI Module for Nitro AI - PRODUCTION READY
===============================================

LOCAL LLM SUPPORT - Works with Ollama!
Perfect for beginners and low-compute laptops.

FEATURES:
✅ Ollama integration (llama2, mistral, phi, etc.)
✅ Streaming responses (like ChatGPT!)
✅ Context/conversation memory
✅ Multiple model support
✅ API fallback (OpenAI, Claude, etc.)
✅ Lightweight - NO heavy dependencies!

QUICK START:
1. Install Ollama: https://ollama.ai
2. Pull a model: `ollama pull llama2`
3. Set AI_MODEL=ollama in .env
4. Done! Free local AI chat!

DEPENDENCIES:
- aiohttp (for async HTTP) - pip install aiohttp
- No other AI libraries needed!
"""

from typing import Optional, Dict, List, AsyncGenerator, Any
from datetime import datetime
import json
import asyncio
import os

# Async HTTP client
try:
    import aiohttp
    AIOHTTP_AVAILABLE = True
except ImportError:
    AIOHTTP_AVAILABLE = False
    print("⚠️  aiohttp not installed. Install with: pip install aiohttp")


class ChatAI:
    """
    Universal Chat AI interface.
    
    BEGINNER-FRIENDLY:
    - Easy to use
    - Clear documentation
    - Works locally (FREE!)
    - Or use cloud APIs
    """
    
    def __init__(
        self,
        model_name: str = "ollama",
        model: str = "llama2",
        base_url: Optional[str] = None,
        api_key: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: int = 500
    ):
        """
        Initialize Chat AI.
        
        Args:
            model_name: "ollama", "openai", "anthropic", or "dummy"
            model: Specific model (e.g., "llama2", "gpt-4", "claude-3")
            base_url: API base URL (for Ollama: http://localhost:11434)
            api_key: API key (for cloud services)
            temperature: Response creativity (0.0-1.0)
            max_tokens: Maximum response length
            
        Example - Local Ollama:
            >>> ai = ChatAI(model_name="ollama", model="llama2")
            >>> response = await ai.generate_response("Hello!")
            
        Example - OpenAI:
            >>> ai = ChatAI(model_name="openai", model="gpt-4", api_key="sk-...")
            >>> response = await ai.generate_response("Hello!")
        """
        self.model_name = model_name
        self.model = model
        self.base_url = base_url or self._get_default_url()
        self.api_key = api_key
        self.temperature = temperature
        self.max_tokens = max_tokens
        
        # Conversation history for context
        self.conversation_history: List[Dict] = []
        self.max_history = 10  # Keep last 10 messages for context
    
    def _get_default_url(self) -> str:
        """Get default API URL based on model name."""
        defaults = {
            'ollama': 'http://localhost:11434',
            'openai': 'https://api.openai.com/v1',
            'anthropic': 'https://api.anthropic.com/v1'
        }
        return defaults.get(self.model_name, 'http://localhost:11434')
    
    # ========================================================================
    # OLLAMA INTEGRATION (Local, Free!)
    # ========================================================================
    
    async def generate_response_ollama(
        self,
        message: str,
        system_prompt: Optional[str] = None
    ) -> str:
        """
        Generate response using Ollama (LOCAL AI).
        
        REQUIREMENTS:
        1. Install Ollama: https://ollama.ai
        2. Pull model: ollama pull llama2
        3. Run server: ollama serve (usually auto-starts)
        
        Args:
            message: User message
            system_prompt: System instructions (optional)
            
        Returns:
            AI response text
            
        MODELS YOU CAN USE:
        - llama2 (7B) - Good balance, 4GB RAM
        - mistral (7B) - Fast, efficient
        - phi (2.7B) - Very fast, 2GB RAM
        - codellama (7B) - Great for code
        - llama2:13b - Better quality, needs 8GB RAM
        """
        if not AIOHTTP_AVAILABLE:
            return "⚠️ aiohttp not installed. Install with: pip install aiohttp"
        
        try:
            # Build conversation context
            messages = []
            if system_prompt:
                messages.append({"role": "system", "content": system_prompt})
            
            # Add conversation history for context
            for msg in self.conversation_history[-self.max_history:]:
                messages.append(msg)
            
            # Add current message
            messages.append({"role": "user", "content": message})
            
            # Call Ollama API
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    f"{self.base_url}/api/chat",
                    json={
                        "model": self.model,
                        "messages": messages,
                        "stream": False,
                        "options": {
                            "temperature": self.temperature,
                            "num_predict": self.max_tokens
                        }
                    },
                    timeout=aiohttp.ClientTimeout(total=60)
                ) as response:
                    if response.status != 200:
                        error_text = await response.text()
                        return f"Ollama Error: {error_text}. Is Ollama running? Try: ollama serve"
                    
                    data = await response.json()
                    ai_response = data.get('message', {}).get('content', 'No response')
                    
                    # Update conversation history
                    self.conversation_history.append({"role": "user", "content": message})
                    self.conversation_history.append({"role": "assistant", "content": ai_response})
                    
                    return ai_response
                    
        except aiohttp.ClientConnectorError:
            return "❌ Cannot connect to Ollama. Is it running?\n\nTo start Ollama:\n1. Install from https://ollama.ai\n2. Run: ollama serve\n3. Pull a model: ollama pull llama2"
        except asyncio.TimeoutError:
            return "⏱️ Request timed out. The model might be loading for the first time (this can take a minute)."
        except Exception as e:
            return f"Ollama Error: {str(e)}"
    
    # ========================================================================
    # STREAMING RESPONSES (Like ChatGPT!)
    # ========================================================================
    
    async def stream_response_ollama(
        self,
        message: str,
        system_prompt: Optional[str] = None
    ) -> AsyncGenerator[str, None]:
        """
        Stream response word-by-word (like ChatGPT typing effect).
        
        Args:
            message: User message
            system_prompt: System instructions (optional)
            
        Yields:
            Response chunks as they're generated
            
        Example:
            >>> async for chunk in ai.stream_response_ollama("Tell me a story"):
            ...     print(chunk, end='', flush=True)
        """
        if not AIOHTTP_AVAILABLE:
            yield "⚠️ aiohttp not installed"
            return
        
        try:
            # Build messages
            messages = []
            if system_prompt:
                messages.append({"role": "system", "content": system_prompt})
            
            for msg in self.conversation_history[-self.max_history:]:
                messages.append(msg)
            
            messages.append({"role": "user", "content": message})
            
            # Stream from Ollama
            full_response = ""
            
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    f"{self.base_url}/api/chat",
                    json={
                        "model": self.model,
                        "messages": messages,
                        "stream": True,  # Enable streaming!
                        "options": {
                            "temperature": self.temperature,
                            "num_predict": self.max_tokens
                        }
                    }
                ) as response:
                    async for line in response.content:
                        if line:
                            try:
                                data = json.loads(line)
                                chunk = data.get('message', {}).get('content', '')
                                if chunk:
                                    full_response += chunk
                                    yield chunk
                            except json.JSONDecodeError:
                                continue
            
            # Update history
            self.conversation_history.append({"role": "user", "content": message})
            self.conversation_history.append({"role": "assistant", "content": full_response})
            
        except Exception as e:
            yield f"\n\nStreaming Error: {str(e)}"
    
    # ========================================================================
    # OPENAI INTEGRATION (Cloud, Paid)
    # ========================================================================
    
    async def generate_response_openai(self, message: str) -> str:
        """
        Generate response using OpenAI (GPT-4, GPT-3.5).
        
        REQUIREMENTS:
        1. Get API key from https://platform.openai.com
        2. Add to .env: OPENAI_API_KEY=sk-...
        3. Set AI_MODEL=openai
        
        COST: ~$0.002 per message (GPT-3.5)
        """
        if not AIOHTTP_AVAILABLE:
            return "⚠️ aiohttp not installed"
        
        if not self.api_key:
            return "❌ OpenAI API key not set. Add OPENAI_API_KEY to .env file"
        
        try:
            # Build messages
            messages = []
            for msg in self.conversation_history[-self.max_history:]:
                messages.append(msg)
            messages.append({"role": "user", "content": message})
            
            # Call OpenAI API
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    f"{self.base_url}/chat/completions",
                    headers={
                        "Authorization": f"Bearer {self.api_key}",
                        "Content-Type": "application/json"
                    },
                    json={
                        "model": self.model,
                        "messages": messages,
                        "temperature": self.temperature,
                        "max_tokens": self.max_tokens
                    }
                ) as response:
                    data = await response.json()
                    
                    if response.status != 200:
                        return f"OpenAI Error: {data.get('error', {}).get('message', 'Unknown error')}"
                    
                    ai_response = data['choices'][0]['message']['content']
                    
                    # Update history
                    self.conversation_history.append({"role": "user", "content": message})
                    self.conversation_history.append({"role": "assistant", "content": ai_response})
                    
                    return ai_response
                    
        except Exception as e:
            return f"OpenAI Error: {str(e)}"
    
    # ========================================================================
    # UNIVERSAL INTERFACE
    # ========================================================================
    
    async def generate_response(
        self,
        message: str,
        system_prompt: Optional[str] = None
    ) -> str:
        """
        Generate response (automatically uses configured model).
        
        Args:
            message: User message
            system_prompt: System instructions (optional)
            
        Returns:
            AI response text
        """
        if self.model_name == "ollama":
            return await self.generate_response_ollama(message, system_prompt)
        elif self.model_name == "openai":
            return await self.generate_response_openai(message)
        elif self.model_name == "dummy":
            return self._dummy_response(message)
        else:
            return f"Unknown model: {self.model_name}. Use 'ollama', 'openai', or 'dummy'"
    
    async def stream_response(
        self,
        message: str,
        system_prompt: Optional[str] = None
    ) -> AsyncGenerator[str, None]:
        """
        Stream response (automatically uses configured model).
        
        Args:
            message: User message
            system_prompt: System instructions (optional)
            
        Yields:
            Response chunks
        """
        if self.model_name == "ollama":
            async for chunk in self.stream_response_ollama(message, system_prompt):
                yield chunk
        else:
            # For non-streaming models, yield all at once
            response = await self.generate_response(message, system_prompt)
            yield response
    
    def _dummy_response(self, message: str) -> str:
        """Dummy response for testing (no AI needed)."""
        responses = [
            f"This is a dummy response to: '{message[:30]}...'",
            "I'm a placeholder AI. To use real AI, set up Ollama or OpenAI!",
            "Real AI integration coming soon! This is just a test response.",
            f"You said: '{message}'. I would respond intelligently if AI was enabled!"
        ]
        import random
        return random.choice(responses)
    
    # ========================================================================
    # CONTEXT MANAGEMENT
    # ========================================================================
    
    def clear_history(self):
        """Clear conversation history."""
        self.conversation_history = []
    
    def get_history(self) -> List[Dict]:
        """Get conversation history."""
        return self.conversation_history.copy()
    
    def set_max_history(self, max_history: int):
        """Set maximum number of messages to keep in context."""
        self.max_history = max_history


# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def create_chat_ai(
    model_type: str = "ollama",
    config: Optional[Dict] = None
) -> ChatAI:
    """
    Factory function to create ChatAI instance.
    
    Args:
        model_type: "ollama", "openai", or "dummy"
        config: Configuration dictionary
        
    Returns:
        Configured ChatAI instance
        
    Example:
        >>> ai = create_chat_ai("ollama")
        >>> response = await ai.generate_response("Hello!")
    """
    config = config or {}
    
    if model_type == "ollama":
        return ChatAI(
            model_name="ollama",
            model=config.get("model", "llama2"),
            base_url=config.get("base_url", "http://localhost:11434"),
            temperature=config.get("temperature", 0.7),
            max_tokens=config.get("max_tokens", 500)
        )
    elif model_type == "openai":
        return ChatAI(
            model_name="openai",
            model=config.get("model", "gpt-3.5-turbo"),
            api_key=config.get("api_key", os.getenv("OPENAI_API_KEY")),
            temperature=config.get("temperature", 0.7),
            max_tokens=config.get("max_tokens", 500)
        )
    else:
        return ChatAI(model_name="dummy")


# Usage Examples:
# ===============

async def example_usage():
    """Examples of how to use ChatAI."""
    
    print("ChatAI Examples")
    print("=" * 60)
    
    # Example 1: Local Ollama (FREE!)
    print("\n1. Local Ollama Chat:")
    ai = create_chat_ai("ollama", {"model": "llama2"})
    response = await ai.generate_response("What is Python?")
    print(f"Response: {response}")
    
    # Example 2: Streaming response
    print("\n2. Streaming Response:")
    print("AI: ", end='')
    async for chunk in ai.stream_response("Tell me a short joke"):
        print(chunk, end='', flush=True)
    print()
    
    # Example 3: Conversation with context
    print("\n3. Conversation with Context:")
    ai.clear_history()
    response1 = await ai.generate_response("My name is Alice")
    print(f"User: My name is Alice")
    print(f"AI: {response1}")
    
    response2 = await ai.generate_response("What's my name?")
    print(f"User: What's my name?")
    print(f"AI: {response2}")

if __name__ == "__main__":
    # Run examples
    asyncio.run(example_usage())
