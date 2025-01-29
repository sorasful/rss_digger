import pytest

from rss_digger import RSSHandler


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "url, expected_url",
    [
        (
            "http://realpython.com/",
            "https://realpython.com/atom.xml",
        ),
        (
            "https://www.thedailystar.net/frontpage/rss.xml",
            "https://www.thedailystar.net/frontpage/rss.xml",
        ),
        (
            "https://www.bd24live.com/feed/",
            "https://www.bd24live.com/feed/",
        ),
        (
            "https://www.businessnews.com.au/rssfeed/latest.rss",
            "https://www.businessnews.com.au/rssfeed/latest.rss",
        ),
    ],
)
async def test_rss_handler_valid_urls(url: str, expected_url: str):
    reddit_handler = RSSHandler()

    result = await reddit_handler.extract_feeds_links(url)
    assert result == [expected_url]
