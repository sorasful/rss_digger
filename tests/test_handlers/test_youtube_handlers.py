import pytest

from rss_digger.exceptions import MissingConfigError
from rss_digger.handlers.youtube import YoutubeChannelHandler


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "url, expected_url",
    [
        (
            "https://www.youtube.com/c/AurelieVache/videos",
            "https://www.youtube.com/feeds/videos.xml?channel_id=UCrRk0kOP58lBMl9B8ZS8Vlg",
        ),
        (
            "https://www.youtube.com/c/devaslife",
            "https://www.youtube.com/feeds/videos.xml?channel_id=UC7yZ6keOGsvERMp2HaEbbXQ",
        ),
        (
            "https://www.youtube.com/c/SebastiaanMath%C3%B4t",
            "https://www.youtube.com/feeds/videos.xml?channel_id=UC6HfeAa0vWeSWS6IcNAjZ2A",
        ),
    ],
)
async def test_youtube_channel_handler(url: str, expected_url: str):
    youtube_channel_handler = YoutubeChannelHandler()

    result = await youtube_channel_handler.extract_feeds_links(url)
    assert result == [expected_url]


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "url, expected_url",
    [
        (
            "https://www.youtube.com/@MrBeast",
            "https://www.youtube.com/feeds/videos.xml?channel_id=UCX6OQ3DkcsbYNE6H8uQQuVA",
        ),
    ],
)
async def test_youtube_new_channel_handler(url: str, expected_url: str):
    youtube_channel_handler = YoutubeChannelHandler()

    result = await youtube_channel_handler.extract_feeds_links(url)
    assert result == [expected_url]


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "url, expected_url",
    [
        (
            "https://www.youtube.com/channel/UCs_AZuYXi6NA9tkdbhjItHQ",
            "https://www.youtube.com/feeds/videos.xml?channel_id=UCs_AZuYXi6NA9tkdbhjItHQ",
        ),
        (
            "https://www.youtube.com/channel/UCuV2zgn7-EuODeU37QNYBSw",
            "https://www.youtube.com/feeds/videos.xml?channel_id=UCuV2zgn7-EuODeU37QNYBSw",
        ),
    ],
)
async def test_youtube_channel_initial_name_handler(url: str, expected_url: str):
    youtube_channel_handler = YoutubeChannelHandler()

    result = await youtube_channel_handler.extract_feeds_links(url)
    assert result == [expected_url]


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "url, expected_url",
    [
        (
            "https://www.youtube.com/user/legrandjd",
            "https://www.youtube.com/feeds/videos.xml?channel_id=UCzjd9v6DMprAAvOBB4sxBPA",
        ),
    ],
)
async def test_youtube_user_handler_missing_youtube_api(
    url: str, expected_url: str, monkeypatch
):
    monkeypatch.setattr("rss_digger.handlers.youtube.YOUTUBE_API_KEY", None)

    youtube_channel_handler = YoutubeChannelHandler()
    with pytest.raises(MissingConfigError):
        await youtube_channel_handler.extract_feeds_links(url)


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "url, expected_url",
    [
        (
            "https://www.youtube.com/user/legrandjd",
            "https://www.youtube.com/feeds/videos.xml?channel_id=UCzjd9v6DMprAAvOBB4sxBPA",
        ),
    ],
)
async def test_youtube_user_handler_valid(url: str, expected_url: str):
    youtube_channel_handler = YoutubeChannelHandler()

    result = await youtube_channel_handler.extract_feeds_links(url)
    assert result == [expected_url]
