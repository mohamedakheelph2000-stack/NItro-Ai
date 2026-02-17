"""
Web Search AI Module - Perplexity-style Search with AI Summarization
Optimized for low-compute laptops
"""

from typing import Optional, Dict, List
from datetime import datetime
import logging
import re

logger = logging.getLogger(__name__)

# Try importing web scraping libraries
try:
    import aiohttp
    AIOHTTP_AVAILABLE = True
except ImportError:
    AIOHTTP_AVAILABLE = False
    logger.info("⚠️  aiohttp not available. Install with: pip install aiohttp")

try:
    from bs4 import BeautifulSoup
    BS4_AVAILABLE = True
except ImportError:
    BS4_AVAILABLE = False
    logger.info("⚠️  BeautifulSoup not available. Install with: pip install beautifulsoup4")


class WebSearchAI:
    """
    AI-powered web search with summarization.
    
    BEGINNER-FRIENDLY:
    - FREE web scraping (no API keys needed)
    - Works with your local AI model (phi3/llama2)
    - Summarizes search results automatically
    - Shows citations and sources
    
    FEATURES:
    - 🔍 Search the web (DuckDuckGo HTML)
    - 📄 Extract clean text from web pages
    - 🤖 AI summarization of results
    - 📚 Citation tracking
    - 🌐 Multi-source aggregation
    """
    
    def __init__(
        self,
        chat_ai=None,
        max_results: int = 5,
        timeout: int = 10
    ):
        """
        Initialize Web Search AI.
        
        Args:
            chat_ai: ChatAI instance for summarization
            max_results: Number of search results to process
            timeout: Request timeout in seconds
        """
        self.chat_ai = chat_ai
        self.max_results = max_results
        self.timeout = timeout
        
        logger.info(f"WebSearchAI initialized: max_results={max_results}")
    
    async def search(
        self,
        query: str,
        summarize: bool = True
    ) -> Dict:
        """
        Search the web and optionally summarize results.
        
        Args:
            query: Search query
            summarize: Use AI to summarize results
        
        Returns:
            Dictionary with search results and summary
            
        Example:
            >>> search_ai = WebSearchAI(chat_ai=my_chat_ai)
            >>> result = await search_ai.search("What is quantum computing?")
            >>> print(result['summary'])
            >>> for source in result['sources']:
            ...     print(f"- {source['title']}: {source['url']}")
        """
        if not AIOHTTP_AVAILABLE or not BS4_AVAILABLE:
            return self._placeholder_response(query)
        
        try:
            logger.info(f"Searching web for: {query}")
            
            # Perform search
            search_results = await self._search_duckduckgo(query)
            
            if not search_results:
                return {
                    "status": "no_results",
                    "query": query,
                    "message": "No search results found"
                }
            
            # Extract content from top results
            contents = await self._extract_contents(search_results[:self.max_results])
            
            # Prepare response
            response = {
                "status": "success",
                "query": query,
                "sources": search_results[:self.max_results],
                "raw_content": contents,
                "timestamp": datetime.now().isoformat()
            }
            
            # Optionally summarize with AI
            if summarize and self.chat_ai and contents:
                summary = await self._summarize_results(query, contents, search_results)
                response["summary"] = summary
                response["ai_generated"] = True
            else:
                response["summary"] = "Summary not generated (AI not configured)"
                response["ai_generated"] = False
            
            logger.info(f"✅ Search completed: {len(search_results)} results")
            
            return response
            
        except Exception as e:
            logger.error(f"Search error: {e}")
            return {
                "status": "error",
                "error": str(e),
                "query": query
            }
    
    async def _search_duckduckgo(self, query: str) -> List[Dict]:
        """
        Search using DuckDuckGo HTML (no API key needed).
        
        Args:
            query: Search query
            
        Returns:
            List of search results with title, url, snippet
        """
        try:
            # DuckDuckGo HTML search
            url = "https://html.duckduckgo.com/html/"
            params = {"q": query}
            
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    url,
                    data=params,
                    timeout=aiohttp.ClientTimeout(total=self.timeout)
                ) as response:
                    html = await response.text()
            
            # Parse results
            soup = BeautifulSoup(html, 'html.parser')
            results = []
            
            # Extract search results
            for result in soup.find_all('div', class_='result'):
                try:
                    title_elem = result.find('a', class_='result__a')
                    snippet_elem = result.find('a', class_='result__snippet')
                    
                    if title_elem:
                        title = title_elem.get_text(strip=True)
                        url = title_elem.get('href', '')
                        snippet = snippet_elem.get_text(strip=True) if snippet_elem else ""
                        
                        results.append({
                            "title": title,
                            "url": url,
                            "snippet": snippet
                        })
                except:
                    continue
            
            return results
            
        except Exception as e:
            logger.error(f"DuckDuckGo search error: {e}")
            return []
    
    async def _extract_contents(self, search_results: List[Dict]) -> List[Dict]:
        """
        Extract clean text content from search result URLs.
        
        Args:
            search_results: List of search results
            
        Returns:
            List of extracted contents
        """
        contents = []
        
        for result in search_results:
            try:
                url = result['url']
                
                # Skip invalid URLs
                if not url or not url.startswith('http'):
                    continue
                
                logger.info(f"Extracting content from: {url[:50]}...")
                
                async with aiohttp.ClientSession() as session:
                    async with session.get(
                        url,
                        timeout=aiohttp.ClientTimeout(total=self.timeout),
                        headers={'User-Agent': 'Mozilla/5.0'}
                    ) as response:
                        if response.status == 200:
                            html = await response.text()
                            
                            # Parse HTML
                            soup = BeautifulSoup(html, 'html.parser')
                            
                            # Remove script and style elements
                            for script in soup(["script", "style", "nav", "footer", "header"]):
                                script.decompose()
                            
                            # Get text
                            text = soup.get_text(separator='\n', strip=True)
                            
                            # Clean text
                            lines = [line.strip() for line in text.split('\n') if line.strip()]
                            clean_text = '\n'.join(lines[:50])  # First 50 lines
                            
                            contents.append({
                                "url": url,
                                "title": result['title'],
                                "content": clean_text[:2000]  # Max 2000 chars per source
                            })
                
            except Exception as e:
                logger.warning(f"Failed to extract from {url}: {e}")
                continue
        
        return contents
    
    async def _summarize_results(
        self,
        query: str,
        contents: List[Dict],
        sources: List[Dict]
    ) -> str:
        """
        Use AI to summarize search results.
        
        Args:
            query: Original search query
            contents: Extracted content from web pages
            sources: Search result metadata
            
        Returns:
            AI-generated summary
        """
        try:
            # Build context from web pages
            context = f"Question: {query}\n\n"
            context += "Information from web sources:\n\n"
            
            for i, content in enumerate(contents, 1):
                context += f"[{i}] {content['title']}\n"
                context += f"{content['content'][:500]}...\n\n"
            
            # Generate summary with AI
            prompt = f"""{context}

Based on the above information from multiple web sources, provide a clear and comprehensive answer to the question: "{query}"

Include:
1. A direct answer to the question
2. Key facts and details
3. Reference the sources using [1], [2], etc.

Answer:"""
            
            if self.chat_ai:
                summary = await self.chat_ai.generate_response(
                    message=prompt,
                    system_prompt="You are a helpful research assistant. Summarize web search results accurately and cite sources using [1], [2], etc."
                )
                return summary
            else:
                return "AI summarization not available (no chat_ai configured)"
                
        except Exception as e:
            logger.error(f"Summarization error: {e}")
            return f"Error generating summary: {str(e)}"
    
    def _placeholder_response(self, query: str) -> Dict:
        """Return placeholder when libraries not available."""
        return {
            "status": "placeholder",
            "query": query,
            "message": "Web search not available",
            "instructions": {
                "install": "pip install aiohttp beautifulsoup4",
                "description": "Enables web scraping and search",
                "free": "No API keys required, completely free"
            }
        }


def create_web_search_ai(
    chat_ai=None,
    max_results: int = 5
) -> WebSearchAI:
    """
    Factory function for web search AI.
    
    Args:
        chat_ai: ChatAI instance for summarization
        max_results: Number of results to process
        
    Returns:
        WebSearchAI instance
    """
    return WebSearchAI(
        chat_ai=chat_ai,
        max_results=max_results
    )
