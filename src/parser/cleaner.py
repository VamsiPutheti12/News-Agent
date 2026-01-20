"""Text cleaning utilities."""

import re
from typing import Optional


class TextCleaner:
    """Utility class for cleaning and normalizing text content."""
    
    @staticmethod
    def remove_html(text: str) -> str:
        """Remove HTML tags from text."""
        if not text:
            return ""
        # Remove HTML tags
        clean = re.sub(r'<[^>]+>', '', text)
        # Decode HTML entities
        clean = TextCleaner._decode_entities(clean)
        return clean
    
    @staticmethod
    def _decode_entities(text: str) -> str:
        """Decode common HTML entities."""
        entities = {
            '&nbsp;': ' ',
            '&amp;': '&',
            '&lt;': '<',
            '&gt;': '>',
            '&quot;': '"',
            '&#39;': "'",
            '&apos;': "'",
            '&mdash;': '—',
            '&ndash;': '–',
            '&hellip;': '...',
        }
        for entity, char in entities.items():
            text = text.replace(entity, char)
        return text
    
    @staticmethod
    def normalize_whitespace(text: str) -> str:
        """Normalize whitespace in text."""
        if not text:
            return ""
        # Replace multiple whitespace with single space
        text = re.sub(r'\s+', ' ', text)
        # Strip leading/trailing whitespace
        return text.strip()
    
    @staticmethod
    def remove_urls(text: str) -> str:
        """Remove URLs from text."""
        if not text:
            return ""
        return re.sub(r'https?://\S+', '', text)
    
    @staticmethod
    def clean(text: str) -> str:
        """Apply all cleaning operations."""
        if not text:
            return ""
        text = TextCleaner.remove_html(text)
        text = TextCleaner.normalize_whitespace(text)
        return text
    
    @staticmethod
    def truncate(text: str, max_length: int = 500, suffix: str = "...") -> str:
        """Truncate text to specified length."""
        if not text or len(text) <= max_length:
            return text
        return text[:max_length - len(suffix)].rsplit(' ', 1)[0] + suffix
