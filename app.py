"""
News Agent - Streamlit Web App
Clean, minimal design.
"""

import streamlit as st
import asyncio
from datetime import datetime

# Page config
st.set_page_config(
    page_title="News Agent",
    page_icon="📰",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Hide sidebar completely
st.markdown("""
<style>
    [data-testid="stSidebar"] {
        display: none;
    }
    [data-testid="stSidebarNav"] {
        display: none;
    }
</style>
""", unsafe_allow_html=True)

# Import Google Font and apply clean styling
st.markdown("""
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
<style>
    /* Global font */
    * {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    }
    
    /* Main background */
    .stApp {
        background: #f8fafc;
    }
    
    .main .block-container {
        max-width: 900px;
        padding: 2rem 1rem;
    }
    
    /* Header */
    .header {
        text-align: center;
        padding: 3rem 0 2rem;
        border-bottom: 1px solid #e2e8f0;
        margin-bottom: 2rem;
    }
    
    .header h1 {
        color: #0f172a;
        font-size: 2rem;
        font-weight: 700;
        margin: 0 0 0.5rem;
        letter-spacing: -0.5px;
    }
    
    .date {
        color: #64748b;
        font-size: 0.9rem;
        margin-top: 0.5rem;
    }
    
    /* Article card */
    .article {
        background: #ffffff;
        border: 1px solid #e2e8f0;
        border-radius: 12px;
        padding: 1.5rem;
        margin-bottom: 1rem;
        transition: box-shadow 0.2s ease, border-color 0.2s ease;
    }
    
    .article:hover {
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
        border-color: #cbd5e1;
    }
    
    .article-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 0.75rem;
    }
    
    .source {
        display: inline-block;
        padding: 0.25rem 0.75rem;
        background: #f1f5f9;
        color: #475569;
        border-radius: 6px;
        font-size: 0.75rem;
        font-weight: 500;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    .category {
        color: #94a3b8;
        font-size: 0.8rem;
    }
    
    .article-title {
        color: #0f172a;
        font-size: 1.1rem;
        font-weight: 600;
        text-decoration: none;
        line-height: 1.4;
        display: block;
        margin-bottom: 0.75rem;
        transition: color 0.2s ease;
    }
    
    .article-title:hover {
        color: #3b82f6;
    }
    
    .article-summary {
        color: #64748b;
        font-size: 0.9rem;
        line-height: 1.6;
        margin: 0;
    }
    
    .article-number {
        color: #cbd5e1;
        font-size: 0.8rem;
        font-weight: 600;
        margin-right: 0.5rem;
    }
    
    /* Button */
    .stButton > button {
        background: #0f172a;
        color: #ffffff;
        border: none;
        border-radius: 8px;
        padding: 0.75rem 2rem;
        font-weight: 500;
        font-size: 0.9rem;
        transition: background 0.2s ease;
    }
    
    .stButton > button:hover {
        background: #1e293b;
    }
    
    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
</style>
""", unsafe_allow_html=True)


def render_header():
    """Render the page header."""
    today = datetime.now().strftime("%A, %B %d, %Y")
    st.markdown(f"""
    <div class="header">
        <h1>News Agent</h1>
        <p class="date">{today}</p>
    </div>
    """, unsafe_allow_html=True)


def render_article(index: int, article):
    """Render a single article card."""
    st.markdown(f"""
    <div class="article">
        <div class="article-header">
            <span class="source">{article.source}</span>
            <span class="category">{article.category}</span>
        </div>
        <a href="{article.url}" target="_blank" class="article-title">
            {article.title}
        </a>
        <p class="article-summary">{article.summary}</p>
    </div>
    """, unsafe_allow_html=True)


async def run_agent_async():
    """Run the news agent asynchronously."""
    from src.agent import NewsAgent
    agent = NewsAgent(top_n=10)
    return await agent.run()


def main():
    """Main app function."""
    render_header()
    
    # Fetch button
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        fetch_button = st.button("Fetch Latest News", use_container_width=True)
    
    if fetch_button:
        with st.spinner("Loading..."):
            try:
                summary = asyncio.run(run_agent_async())
                
                if not summary.articles:
                    st.warning("No articles found. Please try again later.")
                    return
                
                st.session_state.summary = summary
                
            except Exception as e:
                st.error(f"Error: {str(e)}")
                return
    
    # Display results
    if hasattr(st.session_state, 'summary') and st.session_state.summary:
        summary = st.session_state.summary
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        for i, article in enumerate(summary.articles, 1):
            render_article(i, article)


if __name__ == "__main__":
    main()
