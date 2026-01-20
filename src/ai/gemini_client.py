"""Google Gemini API client for AI summarization."""

import warnings
from typing import Optional

# Suppress the deprecation warning
warnings.filterwarnings("ignore", category=FutureWarning, module="google.generativeai")

import google.generativeai as genai


class GeminiClient:
    """Client for Google Gemini API."""
    
    def __init__(self, api_key: str, model: str = "gemini-1.5-flash"):
        """Initialize Gemini client with API key."""
        self.api_key = api_key
        self.model_name = model
        
        # Configure the API
        genai.configure(api_key=api_key)
        
        # Create model instance
        self.model = genai.GenerativeModel(
            model_name=model,
            generation_config={
                "temperature": 0.7,
                "top_p": 0.95,
                "top_k": 40,
                "max_output_tokens": 1024,
            }
        )
    
    async def generate(self, prompt: str) -> Optional[str]:
        """Generate text using Gemini API."""
        try:
            response = await self.model.generate_content_async(prompt)
            
            if response and response.text:
                return response.text.strip()
            return None
        except Exception as e:
            print(f"⚠️  Gemini API error: {str(e)}")
            return None
    
    def generate_sync(self, prompt: str) -> Optional[str]:
        """Generate text synchronously."""
        try:
            response = self.model.generate_content(prompt)
            
            if response and response.text:
                return response.text.strip()
            return None
        except Exception as e:
            print(f"⚠️  Gemini API error: {str(e)}")
            return None

