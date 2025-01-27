from typing import Protocol
from furl import furl

from .youtube import YoutubeChannelHandler as YoutubeChannelHandler


class RSSHandler(Protocol):
    """
    Represents a handler for a given website.
    """

    @classmethod
    async def extract_feeds_links(cls, url: str | furl) -> list[str]: ...
