import json
from loguru import logger
from requests_html import AsyncHTMLSession
from rich.status import Status

from youloud_parser.classes import Album
from youloud_parser.files import save_album
from youloud_parser.parser import get_album_data_to_download
from youloud_parser.consts import SITE_URL, ALBUMS_REQUEST_HEADERS
from youloud_parser.parser_io import (
    print_album_code_message, print_message_after_download, console,
    make_download_status_text, make_album_data_status_text
)
 

async def get_album_code(album: Album) -> str | None:
    album_id, page_id = await get_album_data_to_download(album)
    session = AsyncHTMLSession()
    album_code_response = await session.post(
        url=SITE_URL + '/download.php',
        data={'albumid': album_id, 'page': page_id},
        headers=ALBUMS_REQUEST_HEADERS,
    )
    code_response_json = json.loads(album_code_response.json())
    print_album_code_message(response_json=code_response_json)
    if code_response_json['status']:
        return code_response_json['code']
    



async def download_album(album: Album, status: Status) -> None:
    album_data_text = make_album_data_status_text(album)
    status.update(album_data_text)

    album_code = await get_album_code(album)
    logger.success('Альбом "{album.artist} - {album.title}" найден на сайте.')
    download_status_text = make_download_status_text(album)
    status.update(download_status_text)

    if album_code is not None:
        session = AsyncHTMLSession()
        album_response = await session.get(
            url=f'https://vk.com/doc{album_code}',
            headers=ALBUMS_REQUEST_HEADERS,
        )
        print_message_after_download(album)
        save_album(album_obj=album, album_response=album_response)


async def download_albums(albums: list[Album]) -> None:
    with console.status(status='Начинаю скачивание альбомов.', spinner='aesthetic', spinner_style='#a0dddd') as status:
        for album_to_download in albums:
            await download_album(album_to_download, status=status)
    

