#!/usr/bin/env python3
"""
AI News Agent - Top 5 Tech News Summarizer
============================================

An end-to-end AI agent that fetches RSS feeds from top tech sources
and delivers daily curated news summaries using Google Gemini AI.

Usage:
    python main.py                  # Run with default settings
    python main.py --help           # Show help
    python main.py --top 10         # Get top 10 articles
"""

import argparse
import asyncio
import sys
from datetime import datetime

from rich.console import Console
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.table import Table
from rich.markdown import Markdown
from rich.text import Text
from rich import box

from src.agent import NewsAgent
from src.config import config

# Initialize Rich console
console = Console()


def print_banner():
    """Print the application banner."""
    banner = """
╔═══════════════════════════════════════════════════════════════════╗
║                                                                   ║
║   🤖  AI NEWS AGENT - Your Daily Tech News Companion             ║
║                                                                   ║
║   Powered by Google Gemini AI                                     ║
╚═══════════════════════════════════════════════════════════════════╝
    """
    console.print(banner, style="bold cyan")


def print_article(index: int, article, is_last: bool = False):
    """Print a single article with formatting."""
    # Create header with source badge
    source_colors = {
        "TechCrunch": "green",
        "The Verge": "magenta",
        "Ars Technica": "orange1",
        "Wired": "red",
        "Engadget": "blue",
    }
    source_color = source_colors.get(article.source, "white")
    
    # Title line
    title_text = Text()
    title_text.append(f"📰 {index}. ", style="bold yellow")
    title_text.append(f"[{article.source}] ", style=f"bold {source_color}")
    title_text.append(article.title, style="bold white")
    
    console.print()
    console.print(title_text)
    console.print("━" * 70, style="dim")
    
    # Category and score
    info_text = Text()
    info_text.append(f"   📂 {article.category}", style="dim cyan")
    info_text.append(f"  •  ⭐ Importance: {article.importance_score:.1f}/10", style="dim yellow")
    console.print(info_text)
    
    # Summary
    console.print()
    console.print(f"   {article.summary}", style="white")
    
    # Key points
    if article.key_points:
        console.print()
        console.print("   🔑 Key Points:", style="bold green")
        for point in article.key_points[:3]:  # Max 3 points
            console.print(f"      • {point}", style="dim white")
    
    # URL
    console.print()
    console.print(f"   🔗 ", style="dim", end="")
    console.print(article.url, style="dim blue underline")
    
    if not is_last:
        console.print()


def print_summary_stats(summary):
    """Print summary statistics."""
    stats_table = Table(
        show_header=False,
        box=box.SIMPLE,
        padding=(0, 2),
    )
    stats_table.add_column("Label", style="dim")
    stats_table.add_column("Value", style="cyan")
    
    stats_table.add_row("📊 Articles Fetched", str(summary.total_fetched))
    stats_table.add_row("📝 Articles Processed", str(summary.total_parsed))
    stats_table.add_row("📰 Sources Used", ", ".join(summary.sources_used))
    
    console.print()
    console.print(Panel(
        stats_table,
        title="[bold]Pipeline Statistics[/bold]",
        border_style="dim",
        padding=(1, 2)
    ))


async def run_agent(top_n: int = 5):
    """Run the AI News Agent."""
    print_banner()
    
    # Show date
    today = datetime.now().strftime("%A, %B %d, %Y")
    console.print(f"📅 {today}", style="bold", justify="center")
    console.print()
    
    # Check for API key
    if not config.gemini_api_key:
        console.print(Panel(
            "[yellow]⚠️  GEMINI_API_KEY not found![/yellow]\n\n"
            "Please set your API key:\n"
            "1. Copy .env.example to .env\n"
            "2. Add your Gemini API key from https://makersuite.google.com/app/apikey\n\n"
            "[dim]Example:[/dim]\n"
            "GEMINI_API_KEY=your_api_key_here",
            title="[bold red]Configuration Required[/bold red]",
            border_style="red"
        ))
        return
    
    # Initialize agent
    agent = NewsAgent(top_n=top_n)
    
    # Run with progress indicator
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=console
    ) as progress:
        task = progress.add_task("Starting AI News Agent...", total=None)
        
        def update_progress(message: str):
            progress.update(task, description=message)
        
        try:
            summary = await agent.run(progress_callback=update_progress)
        except Exception as e:
            console.print(f"\n[red]❌ Error running agent: {str(e)}[/red]")
            return
    
    # Display results
    if not summary.articles:
        console.print(Panel(
            "No articles found for today. This might be due to:\n"
            "• Network issues with RSS feeds\n"
            "• No new articles published recently\n"
            "• API rate limiting\n\n"
            "Try running again later.",
            title="[yellow]No Results[/yellow]",
            border_style="yellow"
        ))
        return
    
    # Print header
    console.print()
    console.print(Panel(
        f"[bold]Top {len(summary.articles)} Tech News Stories[/bold]\n"
        f"[dim]Curated and summarized by AI[/dim]",
        style="bold cyan",
        padding=(1, 2)
    ))
    
    # Print each article
    for i, article in enumerate(summary.articles, 1):
        is_last = i == len(summary.articles)
        print_article(i, article, is_last)
    
    # Print statistics
    print_summary_stats(summary)
    
    # Footer
    console.print()
    console.print("─" * 70, style="dim")
    console.print(
        "🤖 Generated by AI News Agent | Powered by Google Gemini",
        style="dim",
        justify="center"
    )
    console.print()


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="AI News Agent - Top Tech News Summarizer",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python main.py              Run with default settings (top 5 articles)
  python main.py --top 10     Get top 10 articles
  python main.py -n 3         Get top 3 articles

Environment Variables:
  GEMINI_API_KEY    Your Google Gemini API key (required)
  TOP_N_ARTICLES    Default number of articles (optional)
        """
    )
    parser.add_argument(
        "-n", "--top",
        type=int,
        default=config.top_n_articles,
        help=f"Number of top articles to display (default: {config.top_n_articles})"
    )
    parser.add_argument(
        "--version",
        action="version",
        version="AI News Agent v1.0.0"
    )
    
    args = parser.parse_args()
    
    try:
        asyncio.run(run_agent(top_n=args.top))
    except KeyboardInterrupt:
        console.print("\n[yellow]Interrupted by user[/yellow]")
        sys.exit(0)
    except Exception as e:
        console.print(f"\n[red]Fatal error: {str(e)}[/red]")
        sys.exit(1)


if __name__ == "__main__":
    main()
