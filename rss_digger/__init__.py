from rss_digger.handlers import (
    RSSHandler,
    YoutubeChannelHandler,
    RedditHandler,
    GenericRSSHandler,
)
from furl import furl

HANDLERS: list[GenericRSSHandler] = [
    RSSHandler,
    RedditHandler,
    YoutubeChannelHandler,
]


async def get_rss_feeds_for(url: str) -> list[str]:
    furl_url = furl(url=url)

    if not furl_url.path.isabsolute:
        raise ValueError("URL must be absolute")

    if furl_url.scheme not in {"http", "https"}:
        raise ValueError("URL scheme must be http or https")

    for handler in HANDLERS:
        feeds_links = await handler.extract_feeds_links(url=url)
        if feeds_links:
            return feeds_links

    return []
