"""AI module for summarization and analysis."""

from .summarizer import AISummarizer, ArticleSummary
from .gemini_client import GeminiClient

__all__ = ["AISummarizer", "ArticleSummary", "GeminiClient"]
