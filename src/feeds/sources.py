"""RSS feed source definitions for tech news."""

from dataclasses import dataclass
from typing import List


@dataclass
class FeedSource:
    """Represents an RSS feed source."""
    name: str
    url: str
    category: str
    priority: int = 1


# Comprehensive tech news RSS feeds
TECH_FEEDS: List[FeedSource] = [
    # Major Tech Publications
    FeedSource(
        name="TechCrunch",
        url="https://techcrunch.com/feed/",
        category="Startups",
        priority=5
    ),
    FeedSource(
        name="The Verge",
        url="https://www.theverge.com/rss/index.xml",
        category="Tech",
        priority=5
    ),
    FeedSource(
        name="Ars Technica",
        url="https://feeds.arstechnica.com/arstechnica/index",
        category="Tech",
        priority=5
    ),
    FeedSource(
        name="Hacker News",
        url="https://hnrss.org/frontpage",
        category="Tech",
        priority=5
    ),
    FeedSource(
        name="Engadget",
        url="https://www.engadget.com/rss.xml",
        category="Gadgets",
        priority=4
    ),
    FeedSource(
        name="CNET",
        url="https://www.cnet.com/rss/news/",
        category="Tech",
        priority=5
    ),
    FeedSource(
        name="VentureBeat",
        url="https://feeds.feedburner.com/venturebeat/SZYF",
        category="AI/Startups",
        priority=4
    ),
    FeedSource(
        name="ZDNet",
        url="https://www.zdnet.com/news/rss.xml",
        category="Enterprise",
        priority=4
    ),
    FeedSource(
        name="TechRadar",
        url="https://www.techradar.com/rss",
        category="Reviews",
        priority=4
    ),
    FeedSource(
        name="The Next Web",
        url="https://thenextweb.com/feed",
        category="Tech",
        priority=4
    ),
    FeedSource(
        name="9to5Mac",
        url="https://9to5mac.com/feed/",
        category="Apple",
        priority=4
    ),
    FeedSource(
        name="Android Authority",
        url="https://www.androidauthority.com/feed/",
        category="Android",
        priority=4
    ),
    FeedSource(
        name="Tom's Hardware",
        url="https://www.tomshardware.com/feeds/all",
        category="Hardware",
        priority=4
    ),
    FeedSource(
        name="Gizmodo",
        url="https://gizmodo.com/rss",
        category="Tech",
        priority=4
    ),
    FeedSource(
        name="PCMag",
        url="https://www.pcmag.com/rss",
        category="Reviews",
        priority=3
    ),
    FeedSource(
        name="Digital Trends",
        url="https://www.digitaltrends.com/feed/",
        category="Tech",
        priority=3
    ),
    FeedSource(
        name="How-To Geek",
        url="https://www.howtogeek.com/feed/",
        category="How-To",
        priority=3
    ),
    FeedSource(
        name="SlashGear",
        url="https://www.slashgear.com/feed/",
        category="Tech",
        priority=3
    ),
    FeedSource(
        name="Mashable",
        url="https://mashable.com/feeds/rss/all",
        category="Tech",
        priority=3
    ),
]
