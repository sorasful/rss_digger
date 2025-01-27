# from rss_digger.handlers import RSSHandler, YoutubeChannelHandler
# from furl import furl
#
# HANDLERS = [
#     YoutubeChannelHandler,
# ]
#
# def get_handler_for(url: str | furl) -> RSSHandler:
#     if isinstance(url, str):
#         url = furl(url)
#
#     for handler in HANDLERS:
#         handler.check_is_valid(url)
#
#
# def get_rss_feeds_for(url: str, load_js: bool = False) -> list[str]:
#     """
#
#     :param url:
#     :param load_js:
#     :return:
#     """
#     furl_url = furl(url=url)
#
#     if not furl_url.path.isabsolute:
#         raise ValueError("URL must be absolute")
#
#     if furl_url.scheme not in {"http", "https"}:
#         raise ValueError("URL scheme must be http or https")
#
#     handler = get_handler_for(url=url)
#
#     feeds_links = handler.extract_feeds_links(url=url)
#
#     return feeds_links
