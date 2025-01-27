import pytest

from rss_digger.handlers.reddit import RedditHandler


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "url, expected_url",
    [
        (
            "https://www.reddit.com/r/python",
            "https://www.reddit.com/r/python.rss",
        ),
        (
            "https://www.reddit.com/r/programming/.rss",
            "https://www.reddit.com/r/programming/.rss",
        ),
        (
            "https://www.reddit.com/user/spez",
            "https://www.reddit.com/user/spez.rss",
        ),
        (
            "https://www.reddit.com/r/python/comments/123abc",
            "https://www.reddit.com/r/python/comments/123abc.rss",
        ),
        (
            "https://www.reddit.com/user/testuser/posts",
            "https://www.reddit.com/user/testuser/posts.rss",
        ),
        (
            "https://www.reddit.com/r/machinelearning",
            "https://www.reddit.com/r/machinelearning.rss",
        ),
        (
            "https://www.reddit.com/user/testuser/comments",
            "https://www.reddit.com/user/testuser/comments.rss",
        ),
    ],
)
async def test_reddit_handler_valid_urls(url: str, expected_url: str):
    reddit_handler = RedditHandler()

    result = await reddit_handler.extract_feeds_links(url)
    assert result == [expected_url]


@pytest.mark.asyncio
async def test_reddit_handler_invalid_url():
    reddit_handler = RedditHandler()

    result = await reddit_handler.extract_feeds_links(
        "https://youtube.com/channel/yolo"
    )
    assert result == []
