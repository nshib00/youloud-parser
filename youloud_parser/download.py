import json
from requests_html import AsyncHTMLSession

from album import Album
from parser import get_album_data_to_download
from consts import SITE_URL, ALBUMS_REQUEST_HEADERS
from parser_io import print_download_message, print_message_after_download


async def download_album(album: Album) -> None:
    album_id, page_id = await get_album_data_to_download(album)
    print_download_message(album)
    session = AsyncHTMLSession()
    album_response = await session.post(
        url=SITE_URL + '/download.php',
        data={'albumid': album_id, 'page': page_id},
        headers=ALBUMS_REQUEST_HEADERS,
    )
    album_response_json = json.loads(album_response.json())
    print_message_after_download(
        album=album, 
        response_json=album_response_json,
    )
    # TODO: реализовать счетчик скачанных альбомов для отслеживания лимита по скачанных альбомов
    # с таймером в 2 часа (лимит сайта - 3 альбома). Хранение - в файле json. При успешном запросе альбома
    # c сайта уменьшать значение счетчика на 1. Если с момента скачивания альбома (первого из всех альбомов,
    # если их несколько) прошло 2 часа и ли более, восстанавливать счетчик до значения по умолчанию (3). 


async def download_albums(albums: list[Album]) -> None:
    for album_to_download in albums:
        await download_album(album_to_download)
    

