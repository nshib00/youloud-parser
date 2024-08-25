import json
from requests_html import AsyncHTMLSession, HTMLResponse
from pathlib import Path

from classes import Album
from parser import get_album_data_to_download
from consts import SITE_URL, ALBUMS_REQUEST_HEADERS
from parser_io import print_album_code_message, print_album_data_message, print_message_after_download


async def get_album_code(album: Album) -> str | None:
    album_id, page_id = await get_album_data_to_download(album)
    print_album_data_message(album)
    session = AsyncHTMLSession()
    album_code_response = await session.post(
        url=SITE_URL + '/download.php',
        data={'albumid': album_id, 'page': page_id},
        headers=ALBUMS_REQUEST_HEADERS,
    )
    code_response_json = json.loads(album_code_response.json())
    print_album_code_message(
        album=album, 
        response_json=code_response_json,
    )
    if code_response_json['status']:
        return code_response_json['code']


def save_album(album_obj: Album, album_response: HTMLResponse) -> None:
    download_path = Path().home() / 'Downloads' / f'{album_obj.artist} - {album_obj.title}.zip'
    with open(download_path, 'wb') as file:
        file.write(album_response.content)


def unpack_album_zip(album_path: Path) -> None:
    pass


async def download_album(album: Album) -> None:
    album_code = await get_album_code(album)
    if album_code is not None:
        session = AsyncHTMLSession()
        album_response = await session.get(
            url=f'https://vk.com/doc{album_code}',
            headers=ALBUMS_REQUEST_HEADERS,
        )
        print(type(album_response))
        save_album(album_obj=album, album_response=album_response)
        print_message_after_download(album)

    # TODO: реализовать счетчик скачанных альбомов для отслеживания лимита по скачанных альбомов
    # с таймером в 2 часа (лимит сайта - 3 альбома). Хранение - в файле json. При успешном запросе альбома
    # c сайта уменьшать значение счетчика на 1. Если с момента скачивания альбома (первого из всех альбомов,
    # если их несколько) прошло 2 часа и ли более, восстанавливать счетчик до значения по умолчанию (3). 


async def download_albums(albums: list[Album]) -> None:
    for album_to_download in albums:
        await download_album(album_to_download)
    

