import os
import re
from dataclasses import dataclass
from urllib.parse import unquote
import logging

from bs4 import BeautifulSoup
import httpx
import unidecode
from furl import furl

from rss_digger.exceptions import MissingConfigException

logger = logging.getLogger(__name__)

YOUTUBE_API_KEY = os.environ.get("YOUTUBE_API_KEY")
if not YOUTUBE_API_KEY:  # pragma: no cover
    logger.error(
        "YOUTUBE_API_KEY environment variable not set, you won't be able to fetch Youtube Channels with /user/ format"
    )


@dataclass
class YoutubeChannelHandler:

    @staticmethod
    async def __get_rss_link_for_channel(url: str) -> str:
        # for decoding channel names with ô for examples
        url = unquote(url)

        async with httpx.AsyncClient() as http_client:
            response = await http_client.get(
                url,
                follow_redirects=True,
                headers={"user-agent": ""},
            )
            if response.status_code != 200:
                logger.error(
                    f"Got an {response.status_code} status code while trying to fetch youtube",
                )
                raise ValueError(
                    f"Got an error {response.status_code} while fetching youtube channel {url}"
                )

            soup = BeautifulSoup(response.text, "html.parser")
            link = soup.find("link", {"type": "application/rss+xml"}).attrs["href"]
            return link

    @staticmethod
    async def __get_rss_link_for_user(url: str) -> str:
        furl_url = furl(url)

        username = furl_url.path.segments[1]
        username = unidecode.unidecode(username)  # remove accents
        async with httpx.AsyncClient() as http_client:
            api_url = f"https://www.googleapis.com/youtube/v3/channels?part=snippet&forUsername={username}&key={YOUTUBE_API_KEY}"
            response = await http_client.get(api_url)
            if response.status_code != 200:
                raise ValueError(
                    f"Got an error {response.status_code} while fetching youtube channel {url}"
                )
            channel_id = response.json()["items"][0]["id"]

        return f"https://www.youtube.com/feeds/videos.xml?channel_id={channel_id}"

    @classmethod
    async def extract_feeds_links(cls, url: str | furl) -> list[str]:
        furl_url = furl(url)

        if not re.search(r"(www\.)?youtube\.com", furl_url.netloc):
            return []

        if not furl_url.path.segments:
            return []

        if furl_url.path.segments[0] == "channel" and len(furl_url.path.segments) > 1:
            channel_name = furl_url.path.segments[1]
            return [
                f"https://www.youtube.com/feeds/videos.xml?channel_id={channel_name}"
            ]

        if (
            furl_url.path.segments[0] == "c" and len(furl_url.path.segments) > 1
        ) or furl_url.path.segments[0].startswith("@"):
            rss_link = await cls.__get_rss_link_for_channel(url=furl_url.url)
            return [rss_link]

        if furl_url.path.segments[0] == "user" and len(furl_url.path.segments) > 1:
            if not YOUTUBE_API_KEY:
                raise MissingConfigException(
                    "To retrieve feed from this url you need to setup your YOUTUBE_API_KEY as env variable"
                )
            rss_link = await cls.__get_rss_link_for_user(url=furl_url.url)
            return [rss_link]

        # TODO: handle direct links which redirects ?
        # "https://www.youtube.com/YouTubeCreators",

        return []
