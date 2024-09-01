import re

from requests_html import AsyncHTMLSession

from youloud_parser.classes import Album
from youloud_parser.consts import ALBUMS_REQUEST_HEADERS, SITE_URL
from youloud_parser.parser_io import get_album_query

data_for_albums = {
    "do": "search",
    "subaction": "search",
    "catlist[]": "album",
}


async def get_albums_response():
    data_for_albums["story"] = get_album_query()
    if not data_for_albums["story"]:
        raise KeyboardInterrupt
    session = AsyncHTMLSession()
    albums_response = await session.post(
        SITE_URL + "/search",
        data=data_for_albums,
        headers=ALBUMS_REQUEST_HEADERS,
    )
    return albums_response


def parse_download_script_str(script_str: str) -> tuple[str, str]:
    album_id = re.search(r"prepareFrame\(\d{1,8},", script_str).group(0)[13:-1]
    page_id = re.search(r"[^' ]\S+==", script_str).group(0)
    return album_id, page_id


async def get_album_data_to_download(album: Album) -> tuple[str, str]:
    session = AsyncHTMLSession()
    page_response = await session.get(
        url=album.link,
        headers=ALBUMS_REQUEST_HEADERS,
    )

    download_btn_selector = "a.fbtn.falbum.fx-row.fx-middle.fdl"
    download_button = page_response.html.find(download_btn_selector, first=True)
    download_script = download_button.attrs.get("onclick")

    album_id, page_id = parse_download_script_str(download_script)
    return album_id, page_id


async def parse_albums() -> list[Album]:
    albums_response = await get_albums_response()
    albums_html = albums_response.html.find("a.album-item")
    albums_data = []
    for album in albums_html:
        albums_data.append(
            Album(
                artist=album.find("div.album-artist", first=True).text,
                title=album.find("div.album-title", first=True).text.rstrip().replace("\n", " "),
                link=SITE_URL + album.attrs.get("href"),
            )
        )
    return albums_data
