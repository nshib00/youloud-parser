import json
from requests_html import AsyncHTMLSession, HTMLResponse
from pathlib import Path
import zipfile
from rich.status import Status

from classes import Album
from parser import get_album_data_to_download
from consts import SITE_URL, ALBUMS_REQUEST_HEADERS
from parser_io import (
    print_album_code_message, print_message_after_download, print_save_album_message, console,
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
    

def unpack_album_zip(album_path: Path) -> None:
    with zipfile.ZipFile(f'{album_path}.zip') as album_zip:
        album_zip.extractall(path=album_path)


def save_album(album_obj: Album, album_response: HTMLResponse) -> None:
    download_path = Path().home() / 'Downloads' / f'{album_obj.artist} - {album_obj.title}'
    download_zip_path = download_path.with_suffix('.zip')
    with open(download_zip_path, 'wb') as album_zip:
        album_zip.write(album_response.content)
    unpack_album_zip(album_path=download_path)
    download_zip_path.unlink()
    print_save_album_message(album_path=download_path)


async def download_album(album: Album, status: Status) -> None:
    album_data_text = make_album_data_status_text(album)
    status.update(album_data_text)

    album_code = await get_album_code(album)
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
    

