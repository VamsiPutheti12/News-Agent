"""Configuration management for AI News Agent."""

import os
from dataclasses import dataclass
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


@dataclass
class Config:
    """Application configuration."""
    
    # AI Provider settings
    ai_provider: str = os.getenv("AI_PROVIDER", "gemini")
    gemini_api_key: str = os.getenv("GEMINI_API_KEY", "")
    openai_api_key: str = os.getenv("OPENAI_API_KEY", "")
    
    # Agent settings
    top_n_articles: int = int(os.getenv("TOP_N_ARTICLES", "5"))
    
    # Request settings
    request_timeout: int = 30
    max_retries: int = 3
    
    def validate(self) -> bool:
        """Validate configuration."""
        if self.ai_provider == "gemini" and not self.gemini_api_key:
            raise ValueError("GEMINI_API_KEY is required when using Gemini provider")
        if self.ai_provider == "openai" and not self.openai_api_key:
            raise ValueError("OPENAI_API_KEY is required when using OpenAI provider")
        return True


# Global config instance
config = Config()
