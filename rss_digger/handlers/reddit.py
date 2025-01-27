import re
from dataclasses import dataclass
from furl import furl


@dataclass
class RedditHandler:

    @classmethod
    async def extract_feeds_links(cls, url: str | furl) -> list[str]:
        # TODO: check if it's a valid reddit url
        furl_url = furl(url)

        if not re.search(r"(www\.)?reddit\.com", furl_url.netloc):
            return []

        path_segments = furl_url.path.segments

        if not path_segments[-1].endswith(".rss"):
            result = f"{furl_url.url}.rss"
            return [result]

        return [furl_url.url]
