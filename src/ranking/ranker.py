"""Article ranking and selection logic."""

from collections import defaultdict
from datetime import datetime
from typing import List
from ..ai.summarizer import ArticleSummary


class ArticleRanker:
    """Ranks and selects top articles based on multiple factors."""
    
    def __init__(self, 
                 recency_weight: float = 0.2,
                 importance_weight: float = 0.6,
                 diversity_weight: float = 0.2):
        """Initialize ranker with scoring weights."""
        self.recency_weight = recency_weight
        self.importance_weight = importance_weight
        self.diversity_weight = diversity_weight
    
    def calculate_recency_score(self, published: str) -> float:
        """Calculate recency score (higher for more recent articles)."""
        try:
            # Try parsing the date string
            if isinstance(published, datetime):
                pub_date = published
            else:
                # Try common formats
                for fmt in ["%Y-%m-%d %H:%M:%S", "%Y-%m-%dT%H:%M:%S", "%Y-%m-%d"]:
                    try:
                        pub_date = datetime.strptime(str(published)[:19], fmt)
                        break
                    except ValueError:
                        continue
                else:
                    return 5.0  # Default score if parsing fails
            
            # Calculate hours ago
            hours_ago = (datetime.now() - pub_date).total_seconds() / 3600
            
            # Score: 10 for very recent, decreasing over 24 hours
            if hours_ago <= 1:
                return 10.0
            elif hours_ago <= 6:
                return 9.0
            elif hours_ago <= 12:
                return 7.0
            elif hours_ago <= 24:
                return 5.0
            else:
                return max(1.0, 5.0 - (hours_ago - 24) / 24)
        except Exception:
            return 5.0
    
    def calculate_diversity_penalty(self, 
                                   article: ArticleSummary, 
                                   selected: List[ArticleSummary]) -> float:
        """Calculate penalty for similar sources/categories already selected."""
        penalty = 0.0
        
        for sel in selected:
            # Penalize same source
            if article.source == sel.source:
                penalty += 2.0
            
            # Penalize same category
            if article.category == sel.category:
                penalty += 1.0
        
        return penalty
    
    def calculate_final_score(self,
                             article: ArticleSummary,
                             selected: List[ArticleSummary] = None) -> float:
        """Calculate final ranking score for an article."""
        selected = selected or []
        
        # Base importance score (1-10)
        importance = article.importance_score
        
        # Recency score (1-10)
        recency = self.calculate_recency_score(article.published)
        
        # Diversity penalty (reduces score)
        diversity_penalty = self.calculate_diversity_penalty(article, selected)
        
        # Weighted final score
        final_score = (
            self.importance_weight * importance +
            self.recency_weight * recency -
            self.diversity_weight * diversity_penalty
        )
        
        return max(0.0, final_score)
    
    def rank(self, summaries: List[ArticleSummary]) -> List[ArticleSummary]:
        """Rank all articles by final score."""
        # Calculate initial scores
        scored = [(s, self.calculate_final_score(s)) for s in summaries]
        
        # Sort by score descending
        scored.sort(key=lambda x: x[1], reverse=True)
        
        return [s for s, _ in scored]
    
    def get_top_n(self, summaries: List[ArticleSummary], n: int = 5) -> List[ArticleSummary]:
        """Select top N articles with diversity consideration."""
        if len(summaries) <= n:
            return summaries
        
        selected = []
        remaining = list(summaries)
        
        while len(selected) < n and remaining:
            # Recalculate scores considering already selected articles
            best_score = -1
            best_idx = 0
            
            for i, article in enumerate(remaining):
                score = self.calculate_final_score(article, selected)
                if score > best_score:
                    best_score = score
                    best_idx = i
            
            # Add best article to selected
            selected.append(remaining.pop(best_idx))
        
        return selected
    
    def ensure_source_diversity(self, 
                               summaries: List[ArticleSummary], 
                               n: int = 5,
                               max_per_source: int = 2) -> List[ArticleSummary]:
        """Ensure no single source dominates the selection."""
        source_counts = defaultdict(int)
        selected = []
        
        # Sort by importance first
        sorted_summaries = sorted(summaries, key=lambda s: s.importance_score, reverse=True)
        
        for article in sorted_summaries:
            if len(selected) >= n:
                break
            
            # Check source limit
            if source_counts[article.source] < max_per_source:
                selected.append(article)
                source_counts[article.source] += 1
        
        return selected
