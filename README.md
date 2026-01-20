# 🤖 AI News Agent

> **Your Daily Tech News Companion** - An end-to-end AI agent that fetches RSS feeds from top tech sources and delivers curated, AI-summarized news.

![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)
![Gemini AI](https://img.shields.io/badge/Powered%20by-Google%20Gemini-4285F4.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)

## ✨ Features

- **📡 Multi-Source RSS Aggregation** - Fetches from 5 top tech publications
- **🧠 AI-Powered Summarization** - Uses Google Gemini to generate concise summaries
- **🎯 Smart Ranking** - Prioritizes based on importance, recency, and diversity
- **📊 Key Points Extraction** - Highlights critical takeaways from each article
- **🎨 Beautiful CLI** - Rich terminal output with colors and formatting

## 📰 News Sources

| Source | Category |
|--------|----------|
| TechCrunch | Startups, VC, Tech Industry |
| The Verge | Tech & Culture |
| Ars Technica | Tech & Science |
| Wired | Tech & Innovation |
| Engadget | Gadgets & Reviews |

## 🚀 Quick Start

### 1. Clone & Install

```bash
cd News-Agent
pip install -r requirements.txt
```

### 2. Configure API Key

Get your free Gemini API key from [Google AI Studio](https://makersuite.google.com/app/apikey).

```bash
# Copy the example environment file
cp .env.example .env

# Edit .env and add your API key
GEMINI_API_KEY=your_api_key_here
```

### 3. Run the Agent

```bash
python main.py
```

## 📖 Usage

```bash
# Get top 5 tech news (default)
python main.py

# Get top 10 articles
python main.py --top 10

# Get top 3 articles
python main.py -n 3

# Show help
python main.py --help
```

## 📋 Sample Output

```
╔═══════════════════════════════════════════════════════════════════╗
║   🤖  AI NEWS AGENT - Your Daily Tech News Companion             ║
╚═══════════════════════════════════════════════════════════════════╝

📅 Friday, January 17, 2026

┌─────────────────────────────────────────────────────────────────┐
│              Top 5 Tech News Stories                            │
│              Curated and summarized by AI                       │
└─────────────────────────────────────────────────────────────────┘

📰 1. [TechCrunch] OpenAI Announces Revolutionary GPT-5 Model
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
   📂 AI/ML  •  ⭐ Importance: 9.5/10

   OpenAI has unveiled GPT-5, featuring significant improvements in
   reasoning, multimodal capabilities, and reduced hallucinations...

   🔑 Key Points:
      • 10x improvement in reasoning benchmarks
      • Native multimodal support for images and audio
      • Available to API users starting next month

   🔗 https://techcrunch.com/article/...

... (4 more articles)
```

## 🏗️ Architecture

```
News-Agent/
├── src/
│   ├── config.py              # Configuration management
│   ├── feeds/
│   │   ├── fetcher.py         # RSS feed fetching
│   │   └── sources.py         # Feed source definitions
│   ├── parser/
│   │   ├── article_parser.py  # Article content extraction
│   │   └── cleaner.py         # Text cleaning utilities
│   ├── ai/
│   │   ├── summarizer.py      # AI summarization logic
│   │   └── gemini_client.py   # Google Gemini API client
│   ├── ranking/
│   │   └── ranker.py          # Article ranking algorithm
│   └── agent/
│       └── news_agent.py      # Main orchestrator
├── main.py                     # CLI entry point
├── requirements.txt
└── .env.example
```

## 🔧 Configuration

| Variable | Default | Description |
|----------|---------|-------------|
| `GEMINI_API_KEY` | - | Your Google Gemini API key (required) |
| `AI_PROVIDER` | `gemini` | AI provider to use |
| `TOP_N_ARTICLES` | `5` | Default number of articles |

## 🧪 How It Works

1. **Fetch** - Concurrently retrieves RSS feeds from all sources
2. **Filter** - Keeps only articles from the last 24-48 hours
3. **Parse** - Extracts full article content from URLs
4. **Summarize** - Uses Gemini AI to generate summaries and key points
5. **Rank** - Scores articles by importance, recency, and diversity
6. **Display** - Presents top N articles in a beautiful CLI format

## 📦 Dependencies

- `feedparser` - RSS feed parsing
- `aiohttp` - Async HTTP requests
- `beautifulsoup4` - HTML parsing
- `newspaper3k` - Article extraction
- `google-generativeai` - Gemini API client
- `python-dotenv` - Environment management
- `rich` - Beautiful CLI output

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License

MIT License - See [LICENSE](LICENSE) for details.

---

<p align="center">
  Made with ❤️ by AI News Agent | Powered by Google Gemini
</p>