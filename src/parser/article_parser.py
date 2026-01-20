"""Article content parser and extractor."""

import asyncio
from dataclasses import dataclass, field
from typing import List, Optional
import aiohttp
from .cleaner import TextCleaner


@dataclass
class ParsedArticle:
    """Represents a fully parsed article with extracted content."""
    title: str
    url: str
    source: str
    published: str
    content: str
    summary: str = ""
    author: str = ""
    tags: List[str] = field(default_factory=list)
    image_url: str = ""
    
    def __post_init__(self):
        if self.tags is None:
            self.tags = []


class ArticleParser:
    """Parses and extracts full article content from URLs."""
    
    def __init__(self, timeout: int = 30):
        self.timeout = timeout
        self.cleaner = TextCleaner()
    
    async def parse(self, url: str, title: str = "", source: str = "", 
                    published: str = "", summary: str = "", author: str = "",
                    tags: List[str] = None) -> Optional[ParsedArticle]:
        """Parse a single article URL and extract content."""
        try:
            content = await self._fetch_and_extract(url)
            
            # Fall back to summary if content extraction fails
            if not content:
                content = summary
            
            return ParsedArticle(
                title=title,
                url=url,
                source=source,
                published=published,
                content=content,
                summary=summary,
                author=author,
                tags=tags or []
            )
        except Exception as e:
            print(f"⚠️  Error parsing article {url}: {str(e)}")
            # Return article with just summary as content
            return ParsedArticle(
                title=title,
                url=url,
                source=source,
                published=published,
                content=summary,
                summary=summary,
                author=author,
                tags=tags or []
            )
    
    async def _fetch_and_extract(self, url: str) -> str:
        """Fetch URL and extract main content."""
        try:
            # Try using newspaper3k for content extraction
            from newspaper import Article
            
            article = Article(url)
            article.download()
            article.parse()
            
            content = article.text
            if content:
                return self.cleaner.clean(content)
        except Exception:
            pass
        
        # Fallback: fetch and do basic extraction
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url, timeout=aiohttp.ClientTimeout(total=self.timeout)) as response:
                    if response.status == 200:
                        html = await response.text()
                        return self._extract_from_html(html)
        except Exception:
            pass
        
        return ""
    
    def _extract_from_html(self, html: str) -> str:
        """Extract main content from HTML using BeautifulSoup."""
        try:
            from bs4 import BeautifulSoup
            
            soup = BeautifulSoup(html, 'lxml')
            
            # Remove script and style elements
            for element in soup(['script', 'style', 'nav', 'header', 'footer', 'aside']):
                element.decompose()
            
            # Try to find article content
            content = ""
            
            # Look for common article containers
            article_selectors = [
                'article',
                '[class*="article-content"]',
                '[class*="post-content"]',
                '[class*="entry-content"]',
                'main',
                '[role="main"]'
            ]
            
            for selector in article_selectors:
                element = soup.select_one(selector)
                if element:
                    # Get text from paragraphs
                    paragraphs = element.find_all('p')
                    if paragraphs:
                        content = ' '.join(p.get_text() for p in paragraphs)
                        break
            
            # Fallback: get all paragraph text
            if not content:
                paragraphs = soup.find_all('p')
                content = ' '.join(p.get_text() for p in paragraphs[:10])  # First 10 paragraphs
            
            return self.cleaner.clean(content)
        except Exception:
            return ""
    
    async def batch_parse(self, articles: List[dict], max_concurrent: int = 5) -> List[ParsedArticle]:
        """Parse multiple articles concurrently."""
        semaphore = asyncio.Semaphore(max_concurrent)
        
        async def parse_with_limit(article_data):
            async with semaphore:
                return await self.parse(**article_data)
        
        tasks = [parse_with_limit(article) for article in articles]
        results = await asyncio.gather(*tasks)
        
        # Filter out None results
        return [r for r in results if r is not None]
