# RSS Digger

RSS Digger is a Python library designed to help you discover RSS feeds from any given URL.
Whether you're working with YouTube channels, subreddits, blogs, or other platforms, RSS Digger simplifies the process
of finding and extracting RSS feed links.

With RSS Digger, you can:

- Automatically detect RSS feeds from a variety of sources.
- Handle complex URLs like YouTube channels, subreddits, and more.
- Easily integrate RSS feed discovery into your projects.

🚀 Coming soon to PyPI!

## Quickstart

```python
import asyncio

from rss_digger import get_rss_feeds_for


async def main():
  rss_url = "https://realpython.com"
  rss_links = await get_rss_feeds_for(url=rss_url)

  print(rss_links)  # ["https://realpython.com/atom.xml", ]


if __name__ == "__main__":
  asyncio.run(main())
```

## Features

- YouTube Support: Extract RSS feeds from YouTube channel URLs.
  Example: https://www.youtube.com/@ExampleChannel → https://www.youtube.com/feeds/videos.xml?channel_id=...


- Reddit Support: Find RSS feeds for subreddits.
  Example: https://www.reddit.com/r/python/ → https://www.reddit.com/r/python.rss

...
Blogs and Websites: Detect RSS feeds from blogs and news websites.

Asynchronous: Built with asyncio for efficient, non-blocking operations.

