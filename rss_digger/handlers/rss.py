import ssl
from dataclasses import dataclass
import logging
from typing import Literal

import feedparser
import httpx
from furl import furl
from httpx import AsyncClient

from rss_digger.exceptions import InvalidFeedURLException

logger = logging.getLogger(__name__)


async def get_content_of_url(
    url: str,
    method: Literal["get", "post", "put", "post", "delete", "patch", "options"] = "get",
) -> str:
    """
    Function used to get the content of an url..
    """

    async def send_request(client: AsyncClient, url: str, method: str) -> str:
        logger.debug(f"Getting url {url}")
        try:
            r = await client.request(method, url)
            logger.debug(f"Status code : {r.status_code} ")
            logger.debug(f"Text : {r.text} ")
            return r.text
        except ssl.SSLCertVerificationError:
            logger.debug("Insecure, sending http request without secure")
            raise

        except Exception as e:
            logger.error(
                f"Could not get url {url} because of {str(e)}",
                extra=dict(exception=e),
            )
            raise InvalidFeedURLException

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:20.0) Gecko/20100101 Firefox/20.0",
    }
    try:
        async with httpx.AsyncClient(
            timeout=5,
            headers=headers,
            follow_redirects=True,
        ) as client:
            return await send_request(client, url, method)
    except ssl.SSLCertVerificationError:
        # doing the same but with verify = False, should be on client
        async with httpx.AsyncClient(
            timeout=5,
            headers=headers,
            follow_redirects=True,
            verify=False,
        ) as client:
            return await send_request(client, url, method)


@dataclass
class RSSHandler:

    @staticmethod
    def __parse_content(content: str, raise_on_invalid: bool = False) -> dict:
        parsed_content = feedparser.parse(content, resolve_relative_uris=True)
        if raise_on_invalid and hasattr(parsed_content, "bozo_exception"):
            raise InvalidFeedURLException(
                f"Could not parse content : {parsed_content.bozo_exception}",
            )
        return parsed_content

    @staticmethod
    def __find_rss_links_in_list_of_links(links: list[dict]) -> list[str]:
        """
        Function used to retrieve a list of URLS that can be potentially RSS feeds.
        Useful when you are given a website like realpython.com/ to find the realpython.com/atom.xml link.
        The dicts are of this form :
        {'rel': 'stylesheet', 'href': 'https://cdn.realpython.com/static/realpython.min.1ecfd4a9d422.css', 'type': 'text/html'}
        {'href': 'https://realpython.com/atom.xml', 'rel': 'alternate', 'title': 'Real Python', 'type': 'application/atom+xml'}
        """
        rss_links = []
        for link in links:
            link_type = link.get("type", "").lower()
            link_text = link.get("text", "").lower()
            link_href = link.get("href", "").lower()

            original_href = link["href"]
            if "rss+xml" in link_type:
                rss_links.append(original_href)

            elif "atom+xml" in link_type:
                rss_links.append(original_href)

            elif "rss" in link_text or "feed" in link_text:
                rss_links.append(original_href)

            elif "rss" in link_href or "feed" in link_href:
                rss_links.append(original_href)

        return rss_links

    @classmethod
    async def extract_feeds_links(cls, url: str | furl) -> list[str]:
        furl_url = furl(url)
        stripped_url = url.strip("/")

        potential_suffixes = {".rss", ".xml", "feed", "feeds"}

        for suffix in potential_suffixes:
            if stripped_url.endswith(suffix):
                return [furl_url.url]

        feed_content = await get_content_of_url(url)
        parsed_content = cls.__parse_content(feed_content)
        if hasattr(parsed_content, "bozo_exception"):
            potentials_links = cls.__find_rss_links_in_list_of_links(
                parsed_content["feed"]["links"]
            )
            for link in potentials_links:
                try:
                    feed_content = await get_content_of_url(link)
                    parsed_content = cls.__parse_content(
                        feed_content, raise_on_invalid=True
                    )
                    return [link]
                except InvalidFeedURLException:
                    continue
            else:
                raise InvalidFeedURLException

        return [url]
