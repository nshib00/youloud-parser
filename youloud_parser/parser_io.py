from pathlib import Path
from rich.console import Console
import inquirer

from classes import Album


console = Console()


def get_album_query() -> str:
    return input('Введите запрос (исполнитель и/или название альбома): ')


async def choose_albums_to_download(albums: list[Album]) -> list[Album]:
    console.print('Выберите альбом(ы), которые необходимо скачать:')
    console.print(
        '[#ff7800]* ВНИМАНИЕ: за раз можно скачать не более 3 альбомов (ограничение сайта).\n\n[/]'
    )
    albums_checkbox = [
            inquirer.Checkbox(
            'albums',
            message='Выберите альбомы',
            choices=albums,
            carousel=True,
        )
    ]
    try:
        needed_albums: dict = inquirer.prompt(albums_checkbox)
        return needed_albums.get('albums')
    except IndexError:
        return []
    

def print_album_data_message(album: Album) -> None:
    print(f'Получаю данные об альбоме "{album.artist} - {album.title}"...')
    

def print_download_message(album: Album) -> None:
    print(f'Скачиваю альбом "{album.artist} - {album.title}"...')


def print_album_code_message(album: Album, response_json: dict) -> None:
    if response_json['status'] == True:
        print_download_message(album)
    else:
        if response_json['code'] == -2: 
            timeleft = response_json['timeleft']
            if '1 часов' in timeleft:
                timeleft = timeleft.replace('часов', 'час')
            print(f'Достигнут лимит скачивания альбомов. До обнуления лимита осталось: {timeleft}.')
        else:
            print(f'Возникла ошибка. Код ошибки: {response_json["code"]}.')
            print('Ответ сервера: ', response_json)


def print_message_after_download(album: Album) -> None:
    print(f'Альбом "{album.artist} - {album.title}" скачан успешно.')


def print_save_album_message(album_path: Path) -> None:
    print(f'Путь до папки с альбомом: {album_path}.')


