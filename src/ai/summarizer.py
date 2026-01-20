"""AI-powered article summarization and analysis."""

import asyncio
import json
import re
from dataclasses import dataclass, field
from typing import List, Optional
from ..parser.article_parser import ParsedArticle
from .gemini_client import GeminiClient


@dataclass
class ArticleSummary:
    """Summarized article with AI-generated insights."""
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


class AISummarizer:
    """AI-powered summarizer using Gemini or OpenAI."""
    
    SUMMARIZE_PROMPT = """You are a tech news analyst. Analyze the following article and provide a structured response.

**Article Title:** {title}
**Source:** {source}
**Content:** {content}

Provide your analysis in the following JSON format (no markdown, just pure JSON):
{{
    "summary": "A concise 2-3 sentence summary of the article highlighting the key news",
    "key_points": ["Key point 1", "Key point 2", "Key point 3"],
    "importance_score": 7.5,
    "category": "Category name"
}}

Guidelines for importance_score (1-10):
- 9-10: Major industry-changing news, breakthrough announcements
- 7-8: Significant tech news, important product launches
- 5-6: Noteworthy updates, interesting developments
- 3-4: Minor news, routine updates
- 1-2: Low priority, opinion pieces

Guidelines for category:
- AI/ML, Startups, Gadgets, Software, Hardware, Cybersecurity, Space/Science, Gaming, Business, Policy

Return ONLY the JSON object, no additional text."""

    RANK_PROMPT = """You are a tech news curator. Given the following list of tech news articles with their importance scores, 
re-evaluate and rank them to select the top {n} most important and diverse stories for today.

Consider:
1. Overall importance and impact
2. Diversity of topics (avoid similar stories)
3. Timeliness and relevance
4. Interest to tech enthusiasts

Articles:
{articles}

Return a JSON array of the top {n} article indices (0-based) in order of importance:
{{"top_indices": [0, 3, 5, 2, 7]}}

Return ONLY the JSON object, no additional text."""

    def __init__(self, api_key: str, provider: str = "gemini"):
        """Initialize summarizer with AI provider."""
        self.provider = provider
        
        if provider == "gemini":
            self.client = GeminiClient(api_key)
        else:
            raise ValueError(f"Unsupported provider: {provider}")
    
    async def summarize(self, article: ParsedArticle) -> ArticleSummary:
        """Summarize a single article using AI."""
        # Prepare content (truncate if too long)
        content = article.content[:3000] if article.content else article.summary[:1000]
        
        if not content:
            # Return basic summary if no content
            return ArticleSummary(
                title=article.title,
                url=article.url,
                source=article.source,
                published=str(article.published),
                summary=article.summary or "No summary available.",
                key_points=[],
                importance_score=5.0,
                category="Tech"
            )
        
        prompt = self.SUMMARIZE_PROMPT.format(
            title=article.title,
            source=article.source,
            content=content
        )
        
        try:
            response = await self.client.generate(prompt)
            
            if response:
                parsed = self._parse_summary_response(response)
                return ArticleSummary(
                    title=article.title,
                    url=article.url,
                    source=article.source,
                    published=str(article.published),
                    summary=parsed.get("summary", article.summary),
                    key_points=parsed.get("key_points", []),
                    importance_score=float(parsed.get("importance_score", 5.0)),
                    category=parsed.get("category", "Tech")
                )
        except Exception as e:
            print(f"⚠️  Error summarizing article: {str(e)}")
        
        # Fallback
        return ArticleSummary(
            title=article.title,
            url=article.url,
            source=article.source,
            published=str(article.published),
            summary=article.summary or content[:200],
            key_points=[],
            importance_score=5.0,
            category="Tech"
        )
    
    def _parse_summary_response(self, response: str) -> dict:
        """Parse AI response into structured data."""
        try:
            # Try to extract JSON from response
            # Handle potential markdown code blocks
            json_match = re.search(r'\{[^{}]*\}', response, re.DOTALL)
            if json_match:
                return json.loads(json_match.group())
            return json.loads(response)
        except json.JSONDecodeError:
            # Try to extract key-value pairs manually
            result = {
                "summary": "",
                "key_points": [],
                "importance_score": 5.0,
                "category": "Tech"
            }
            
            # Extract summary
            summary_match = re.search(r'"summary"\s*:\s*"([^"]+)"', response)
            if summary_match:
                result["summary"] = summary_match.group(1)
            
            # Extract importance score
            score_match = re.search(r'"importance_score"\s*:\s*(\d+(?:\.\d+)?)', response)
            if score_match:
                result["importance_score"] = float(score_match.group(1))
            
            return result
    
    async def batch_summarize(self, articles: List[ParsedArticle], 
                            max_concurrent: int = 3,
                            delay: float = 0.5) -> List[ArticleSummary]:
        """Summarize multiple articles with rate limiting."""
        summaries = []
        semaphore = asyncio.Semaphore(max_concurrent)
        
        async def summarize_with_limit(article: ParsedArticle) -> ArticleSummary:
            async with semaphore:
                result = await self.summarize(article)
                await asyncio.sleep(delay)  # Rate limiting
                return result
        
        tasks = [summarize_with_limit(article) for article in articles]
        summaries = await asyncio.gather(*tasks)
        
        return list(summaries)
    
    async def rank_articles(self, summaries: List[ArticleSummary], n: int = 5) -> List[int]:
        """Use AI to rank and select top N articles."""
        if len(summaries) <= n:
            return list(range(len(summaries)))
        
        # Prepare article list for ranking
        article_list = "\n".join([
            f"{i}. [{s.source}] {s.title} (Score: {s.importance_score}, Category: {s.category})"
            for i, s in enumerate(summaries)
        ])
        
        prompt = self.RANK_PROMPT.format(n=n, articles=article_list)
        
        try:
            response = await self.client.generate(prompt)
            
            if response:
                # Extract indices from response
                json_match = re.search(r'\{[^{}]*\}', response, re.DOTALL)
                if json_match:
                    data = json.loads(json_match.group())
                    indices = data.get("top_indices", [])
                    # Validate indices
                    valid_indices = [i for i in indices if 0 <= i < len(summaries)]
                    if len(valid_indices) >= n:
                        return valid_indices[:n]
        except Exception as e:
            print(f"⚠️  Error ranking articles: {str(e)}")
        
        # Fallback: sort by importance score
        sorted_indices = sorted(
            range(len(summaries)),
            key=lambda i: summaries[i].importance_score,
            reverse=True
        )
        return sorted_indices[:n]
