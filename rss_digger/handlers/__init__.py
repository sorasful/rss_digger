from typing import Protocol
from furl import furl

from .youtube import YoutubeChannelHandler as YoutubeChannelHandler
from .reddit import RedditHandler as RedditHandler
from .rss import RSSHandler as RSSHandler


class GenericRSSHandler(Protocol):
    """
    Represents a handler for a given website.
    """

    @classmethod
    async def extract_feeds_links(cls, url: str | furl) -> list[str]: ...
