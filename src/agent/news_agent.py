"""Main News Agent orchestrator - No API Key Required Version."""

import asyncio
from dataclasses import dataclass, field
from datetime import datetime
from typing import List

from ..feeds import FeedFetcher, TECH_FEEDS
from ..ranking import ArticleRanker


@dataclass
class ArticleSummary:
    """Article with summary from RSS feed."""
    title: str
    url: str
    source: str
    published: str
    summary: str
    key_points: List[str] = field(default_factory=list)
    importance_score: float = 5.0
    category: str = "Tech"
    
    def __post_init__(self):
        if self.key_points is None:
            self.key_points = []


@dataclass
class DailySummary:
    """Daily news summary result."""
    date: str
    articles: List[ArticleSummary] = field(default_factory=list)
    total_fetched: int = 0
    total_parsed: int = 0
    sources_used: List[str] = field(default_factory=list)
    
    def __post_init__(self):
        if self.articles is None:
            self.articles = []
        if self.sources_used is None:
            self.sources_used = []


class NewsAgent:
    """End-to-end News Agent that fetches and displays tech news - NO API KEY REQUIRED."""
    
    def __init__(self, top_n: int = 5, **kwargs):
        """Initialize the News Agent."""
        self.top_n = top_n
        
        # Initialize components
        self.fetcher = FeedFetcher(feeds=TECH_FEEDS)
        self.ranker = ArticleRanker()
    
    def _extract_key_points(self, summary: str) -> List[str]:
        """Extract key points from summary text."""
        if not summary:
            return []
        
        # Split by sentences and take first 2-3 as key points
        sentences = summary.replace('...', '.').split('.')
        sentences = [s.strip() for s in sentences if s.strip() and len(s.strip()) > 20]
        
        return sentences[:3]
    
    def _calculate_importance(self, article) -> float:
        """Calculate importance score based on heuristics."""
        score = 5.0
        
        title_lower = article.title.lower()
        
        # Boost for important keywords
        important_keywords = ['ai', 'artificial intelligence', 'breakthrough', 'launch', 
                            'announce', 'release', 'new', 'first', 'major', 'billion',
                            'google', 'apple', 'microsoft', 'openai', 'meta', 'amazon']
        
        for keyword in important_keywords:
            if keyword in title_lower:
                score += 0.5
        
        # Cap at 10
        return min(10.0, score)
    
    def _categorize_article(self, article) -> str:
        """Categorize article based on title and content."""
        title_lower = article.title.lower()
        
        categories = {
            'AI/ML': ['ai', 'artificial intelligence', 'machine learning', 'gpt', 'llm', 'chatgpt', 'neural'],
            'Startups': ['startup', 'funding', 'venture', 'seed', 'series a', 'series b', 'valuation'],
            'Gadgets': ['phone', 'iphone', 'android', 'laptop', 'tablet', 'wearable', 'headphone'],
            'Gaming': ['game', 'gaming', 'playstation', 'xbox', 'nintendo', 'steam'],
            'Space': ['space', 'nasa', 'spacex', 'rocket', 'satellite', 'mars', 'moon'],
            'Security': ['security', 'hack', 'breach', 'privacy', 'cyber', 'ransomware'],
            'Software': ['app', 'software', 'update', 'feature', 'version'],
        }
        
        for category, keywords in categories.items():
            for keyword in keywords:
                if keyword in title_lower:
                    return category
        
        return 'Tech'
    
    async def run(self, progress_callback=None) -> DailySummary:
        """Run the news agent pipeline - NO API KEY NEEDED."""
        today = datetime.now().strftime("%B %d, %Y")
        
        # Step 1: Fetch all feeds
        if progress_callback:
            progress_callback("Fetching RSS feeds from tech sources...")
        
        raw_articles = await self.fetcher.fetch_all_feeds()
        
        if progress_callback:
            progress_callback(f"Found {len(raw_articles)} articles from all sources")
        
        # Step 2: Filter to recent articles
        today_articles = self.fetcher.filter_today_articles(raw_articles, days=7)
        today_articles = self.fetcher.deduplicate(today_articles)
        
        if progress_callback:
            progress_callback(f"Filtered to {len(today_articles)} recent articles")
        
        if not today_articles:
            return DailySummary(
                date=today,
                articles=[],
                total_fetched=len(raw_articles),
                total_parsed=0,
                sources_used=[]
            )
        
        # Step 3: Create summaries from RSS data (no AI needed!)
        if progress_callback:
            progress_callback("Processing articles...")
        
        summaries = []
        for article in today_articles[:100]:  # Process more articles
            summary = ArticleSummary(
                title=article.title,
                url=article.url,
                source=article.source,
                published=str(article.published),
                summary=article.summary or "Click to read the full article.",
                key_points=self._extract_key_points(article.summary),
                importance_score=self._calculate_importance(article),
                category=self._categorize_article(article)
            )
            summaries.append(summary)
        
        if progress_callback:
            progress_callback(f"Processed {len(summaries)} articles")
        
        # Step 4: Rank and select top N
        if progress_callback:
            progress_callback(f"Selecting top {self.top_n} articles...")
        
        # Sort by importance score
        summaries.sort(key=lambda x: x.importance_score, reverse=True)
        
        # Select top articles - max 2 per source for diversity
        top_articles = []
        source_counts = {}
        
        for article in summaries:
            if len(top_articles) >= self.top_n:
                break
            
            # Max 2 articles per source
            if source_counts.get(article.source, 0) < 2:
                top_articles.append(article)
                source_counts[article.source] = source_counts.get(article.source, 0) + 1
        
        # Get unique sources
        sources_used = list(set(a.source for a in top_articles))
        
        return DailySummary(
            date=today,
            articles=top_articles,
            total_fetched=len(raw_articles),
            total_parsed=len(summaries),
            sources_used=sources_used
        )
    
    def run_sync(self, progress_callback=None) -> DailySummary:
        """Run the agent synchronously."""
        return asyncio.run(self.run(progress_callback))
