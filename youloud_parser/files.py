from pathlib import Path
import re
import zipfile
from requests_html import HTMLResponse
import sys

from youloud_parser.classes import Album
from youloud_parser.parser_io import print_save_album_message


def make_download_path(album_obj: Album):
    if sys.platform == 'win32':
        album_title = clean_string_for_windows(f'{album_obj.artist} - {album_obj.title}')
    else:
        album_title = f'{album_obj.artist} - {album_obj.title}'
    return Path().home() / 'Downloads' / {album_title}


def make_album_zip(album_path: Path, album_response: HTMLResponse) -> None:
    download_zip_path = album_path.with_suffix('.zip')
    with open(download_zip_path, 'wb') as album_zip:
        album_zip.write(album_response.content)


def unpack_album_zip(album_path: Path) -> None:
    with zipfile.ZipFile(f'{album_path}.zip') as album_zip:
        album_zip.extractall(path=album_path)
    album_path.with_suffix('.zip').unlink()


def save_album(album_obj: Album, album_response: HTMLResponse) -> None:
    download_path = make_download_path()
    make_album_zip(album_obj=album_obj, album_response=album_response)
    unpack_album_zip(album_path=download_path)
    print_save_album_message(album_path=download_path) 
    

def clean_string_for_windows(path: str) -> str:
    path = re.sub(r'[\\/:*?"<>|]', ' ', path)
    path = path.strip()
    path = re.sub(r'\s+', ' ', path)
    return path