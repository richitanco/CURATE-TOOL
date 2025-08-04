"""
Custom tools for CrewAI agents
"""
import json
import requests
from typing import Dict, List, Callable
import google.generativeai as genai
from bs4 import BeautifulSoup

from config.settings import SERPER_API_KEY, GOOGLE_API_KEY, MAX_SEARCH_RESULTS, SEARCH_LANGUAGE, GEMINI_MODEL

# Configure Gemini
genai.configure(api_key=GOOGLE_API_KEY)


def search_web(query: str) -> str:
    """
    Search the web using Serper API
    
    Args:
        query: Search query string
        
    Returns:
        JSON string with search results
    """
    try:
        url = "https://google.serper.dev/search"
        
        headers = {
            'X-API-KEY': SERPER_API_KEY,
            'Content-Type': 'application/json'
        }
        
        payload = {
            "q": query,
            "gl": SEARCH_LANGUAGE,
            "hl": SEARCH_LANGUAGE,
            "num": MAX_SEARCH_RESULTS
        }
        
        response = requests.post(url, headers=headers, json=payload, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            results = []
            
            # Extract organic results
            for item in data.get('organic', [])[:5]:
                results.append({
                    'title': item.get('title'),
                    'snippet': item.get('snippet'),
                    'link': item.get('link')
                })
            
            return json.dumps(results, indent=2, ensure_ascii=False)
        else:
            return f"Error: HTTP {response.status_code}"
            
    except Exception as e:
        return f"Search error: {str(e)}"


def analyze_with_gemini(prompt: str, context: str = "") -> str:
    """
    Perform deep analysis using Gemini AI
    
    Args:
        prompt: Analysis prompt
        context: Additional context
        
    Returns:
        Analysis result as string
    """
    try:
        model = genai.GenerativeModel(GEMINI_MODEL)
        
        full_prompt = f"""
        You are an expert educational content analyst.
        
        Context: {context if context else 'General educational content'}
        
        Task: {prompt}
        
        Provide a detailed, structured analysis.
        """
        
        response = model.generate_content(full_prompt)
        return response.text
        
    except Exception as e:
        return f"Analysis error: {str(e)}"


def scrape_webpage(url: str) -> str:
    """
    Extract content from a webpage
    
    Args:
        url: URL to scrape
        
    Returns:
        Extracted content as string
    """
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        
        response = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(response.content, 'lxml')
        
        # Remove scripts and styles
        for element in soup(['script', 'style']):
            element.decompose()
        
        # Extract text
        text = soup.get_text()
        lines = (line.strip() for line in text.splitlines())
        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
        text = ' '.join(chunk for chunk in chunks if chunk)
        
        # Limit length
        max_length = 2000
        if len(text) > max_length:
            text = text[:max_length] + "..."
        
        return text
        
    except Exception as e:
        return f"Scraping error: {str(e)}"


def evaluate_content_quality(content: str) -> str:
    """
    Evaluate the quality of educational content
    
    Args:
        content: Content to evaluate
        
    Returns:
        Quality report as string
    """
    # Calculate metrics
    word_count = len(content.split())
    paragraph_count = len(content.split('\n\n'))
    has_structure = any(marker in content for marker in ['#', '##', '1.', '•', '-'])
    has_examples = any(word in content.lower() for word in ['ejemplo', 'example', 'caso'])
    has_sources = 'http' in content or 'www' in content
    
    # Calculate score
    score = 0
    if word_count > 300: score += 20
    if paragraph_count > 3: score += 15
    if has_structure: score += 20
    if has_examples: score += 20
    if has_sources: score += 25
    
    # Generate report
    report = f"""
📊 Content Quality Evaluation
Score: {score}/100

📈 Metrics:
- Words: {word_count}
- Paragraphs: {paragraph_count}
- Structured: {'Yes' if has_structure else 'No'}
- Examples: {'Yes' if has_examples else 'No'}
- Sources: {'Yes' if has_sources else 'No'}
"""
    
    return report


# Intentar usar las herramientas nativas de CrewAI
try:
    from crewai_tools import BaseTool
    
    # Crear clases personalizadas que hereden de BaseTool
    class WebSearchTool(BaseTool):
        name: str = "web_search"
        description: str = "Search for information on the web"
        
        def _run(self, query: str) -> str:
            return search_web(query)
    
    class GeminiAnalysisTool(BaseTool):
        name: str = "gemini_analysis"
        description: str = "Perform deep analysis using Gemini AI"
        
        def _run(self, prompt: str, context: str = "") -> str:
            return analyze_with_gemini(prompt, context)
    
    class WebScrapeTool(BaseTool):
        name: str = "webpage_scraper"
        description: str = "Extract content from webpages"
        
        def _run(self, url: str) -> str:
            return scrape_webpage(url)
    
    class QualityTool(BaseTool):
        name: str = "quality_evaluator"
        description: str = "Evaluate content quality"
        
        def _run(self, content: str) -> str:
            return evaluate_content_quality(content)
    
    # Crear instancias de las herramientas
    search_tool = WebSearchTool()
    gemini_tool = GeminiAnalysisTool()
    scrape_tool = WebScrapeTool()
    quality_tool = QualityTool()
    
    print("✅ Using crewai_tools.BaseTool")

except ImportError:
    try:
        from crewai.tools import BaseTool
        
        # Crear clases personalizadas que hereden de BaseTool
        class WebSearchTool(BaseTool):
            name: str = "web_search"
            description: str = "Search for information on the web"
            
            def _run(self, query: str) -> str:
                return search_web(query)
        
        class GeminiAnalysisTool(BaseTool):
            name: str = "gemini_analysis"
            description: str = "Perform deep analysis using Gemini AI"
            
            def _run(self, prompt: str, context: str = "") -> str:
                return analyze_with_gemini(prompt, context)
        
        class WebScrapeTool(BaseTool):
            name: str = "webpage_scraper"
            description: str = "Extract content from webpages"
            
            def _run(self, url: str) -> str:
                return scrape_webpage(url)
        
        class QualityTool(BaseTool):
            name: str = "quality_evaluator"
            description: str = "Evaluate content quality"
            
            def _run(self, content: str) -> str:
                return evaluate_content_quality(content)
        
        # Crear instancias de las herramientas
        search_tool = WebSearchTool()
        gemini_tool = GeminiAnalysisTool()
        scrape_tool = WebScrapeTool()
        quality_tool = QualityTool()
        
        print("✅ Using crewai.tools.BaseTool")
        
    except ImportError:
        # Fallback usando funciones directas como herramientas
        print("⚠️ Using function-based tools as fallback")
        
        # Crear objetos simples que simulen herramientas
        class FunctionTool:
            def __init__(self, name, description, func):
                self.name = name
                self.description = description
                self.func = func
                self._run = func
                
            def run(self, *args, **kwargs):
                return self.func(*args, **kwargs)
        
        search_tool = FunctionTool(
            name="web_search",
            description="Search for information on the web",
            func=search_web
        )
        
        gemini_tool = FunctionTool(
            name="gemini_analysis", 
            description="Perform deep analysis using Gemini AI",
            func=analyze_with_gemini
        )
        
        scrape_tool = FunctionTool(
            name="webpage_scraper",
            description="Extract content from webpages",
            func=scrape_webpage
        )
        
        quality_tool = FunctionTool(
            name="quality_evaluator",
            description="Evaluate content quality",
            func=evaluate_content_quality
        )