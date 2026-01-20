"""RSS feed fetcher module."""

import asyncio
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from typing import List, Optional
import feedparser
import aiohttp
from .sources import FeedSource, TECH_FEEDS


@dataclass
class RawArticle:
    """Represents a raw article fetched from RSS feed."""
    title: str
    url: str
    source: str
    published: datetime
    summary: str = ""
    author: str = ""
    tags: List[str] = field(default_factory=list)
    
    def __post_init__(self):
        # Ensure tags is a list
        if self.tags is None:
            self.tags = []


class FeedFetcher:
    """Fetches and parses RSS feeds from tech news sources."""
    
    # Common browser headers to avoid encoding issues
    HEADERS = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept': 'application/rss+xml, application/xml, text/xml, */*',
        'Accept-Encoding': 'gzip, deflate',  # Avoid brotli which causes issues
        'Accept-Language': 'en-US,en;q=0.9',
    }
    
    def __init__(self, feeds: List[FeedSource] = None, timeout: int = 15):
        self.feeds = feeds or TECH_FEEDS
        self.timeout = timeout
    
    async def fetch_feed(self, session: aiohttp.ClientSession, feed: FeedSource) -> List[RawArticle]:
        """Fetch a single RSS feed and parse articles."""
        articles = []
        
        try:
            async with session.get(
                feed.url, 
                timeout=aiohttp.ClientTimeout(total=self.timeout),
                headers=self.HEADERS,
                ssl=False  # Some feeds have SSL issues
            ) as response:
                if response.status == 200:
                    content = await response.text()
                    parsed = feedparser.parse(content)
                    
                    for entry in parsed.entries:
                        article = self._parse_entry(entry, feed)
                        if article:
                            articles.append(article)
        except asyncio.TimeoutError:
            pass  # Silent timeout
        except Exception:
            pass  # Silent errors
        
        return articles
        
        return articles
    
    def _parse_entry(self, entry: dict, feed: FeedSource) -> Optional[RawArticle]:
        """Parse a single RSS entry into RawArticle."""
        try:
            # Get title
            title = entry.get("title", "").strip()
            if not title:
                return None
            
            # Get URL
            url = entry.get("link", "")
            if not url:
                return None
            
            # Parse published date
            published = self._parse_date(entry)
            if not published:
                published = datetime.now()
            
            # Get summary/description
            summary = ""
            if "summary" in entry:
                summary = entry.summary
            elif "description" in entry:
                summary = entry.description
            
            # Clean HTML from summary
            summary = self._clean_html(summary)
            
            # Get author
            author = entry.get("author", "")
            
            # Get tags/categories
            tags = []
            if "tags" in entry:
                tags = [tag.term for tag in entry.tags if hasattr(tag, "term")]
            
            return RawArticle(
                title=title,
                url=url,
                source=feed.name,
                published=published,
                summary=summary[:500] if summary else "",  # Limit summary length
                author=author,
                tags=tags
            )
        except Exception as e:
            print(f"⚠️  Error parsing entry: {str(e)}")
            return None
    
    def _parse_date(self, entry: dict) -> Optional[datetime]:
        """Parse date from RSS entry."""
        # Try different date fields
        date_fields = ["published_parsed", "updated_parsed", "created_parsed"]
        
        for field in date_fields:
            if field in entry and entry[field]:
                try:
                    from time import mktime
                    return datetime.fromtimestamp(mktime(entry[field]))
                except Exception:
                    continue
        
        return None
    
    def _clean_html(self, text: str) -> str:
        """Remove HTML tags from text."""
        import re
        # Remove HTML tags
        clean = re.sub(r'<[^>]+>', '', text)
        # Remove extra whitespace
        clean = re.sub(r'\s+', ' ', clean).strip()
        return clean
    
    async def fetch_all_feeds(self) -> List[RawArticle]:
        """Fetch all RSS feeds concurrently."""
        all_articles = []
        
        async with aiohttp.ClientSession() as session:
            tasks = [self.fetch_feed(session, feed) for feed in self.feeds]
            results = await asyncio.gather(*tasks)
            
            for articles in results:
                all_articles.extend(articles)
        
        return all_articles
    
    def filter_today_articles(self, articles: List[RawArticle], days: int = 1) -> List[RawArticle]:
        """Filter articles from the last N days."""
        cutoff = datetime.now() - timedelta(days=days)
        return [
            article for article in articles
            if article.published >= cutoff
        ]
    
    def deduplicate(self, articles: List[RawArticle]) -> List[RawArticle]:
        """Remove duplicate articles based on URL."""
        seen_urls = set()
        unique_articles = []
        
        for article in articles:
            if article.url not in seen_urls:
                seen_urls.add(article.url)
                unique_articles.append(article)
        
        return unique_articles
