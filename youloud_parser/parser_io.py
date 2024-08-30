from pathlib import Path
from rich.console import Console
import inquirer

from classes import Album


console = Console()


def get_album_query() -> str:
    return console.input('[#4be38f]Введите запрос[/] [i #777777](исполнитель и/или название альбома): [/]')
 

async def choose_albums_to_download(albums: list[Album]) -> list[Album]:
    albums_checkbox = [
            inquirer.Checkbox(
            'albums',
            message='Выберите альбом(ы), которые хотите скачать',
            choices=albums,
            carousel=True,
        )
    ]
    try:
        needed_albums: dict = inquirer.prompt(albums_checkbox)
        return needed_albums.get('albums')
    except (AttributeError, IndexError):
        console.print('[#f5bc42]Альбомов по запросу не найдено. Попробуйте немного изменить предыдущий запрос или ввести новый.[/]')
        return []
    

def print_album_data_message(album: Album) -> None:
    console.print(f'[#a0dddd]Получаю данные об альбоме [i]"{album.artist} - {album.title}"...[/][/]')
    

def print_download_message() -> None:
    console.print('[#a0dddd]Скачиваю альбом...[/]')


def print_album_code_message(response_json: dict) -> None:
    if response_json['status'] == True:
        print_download_message()
    else:
        if response_json['code'] == -2: 
            timeleft = response_json['timeleft']
            if '1 часов' in timeleft:
                timeleft = timeleft.replace('часов', 'час')
            console.print(f'[orangered]Достигнут лимит скачивания альбомов. До обнуления лимита осталось:[/] [b green]{timeleft}.[/]')
        else:
            console.print(f'[firebrick]Возникла ошибка. Код ошибки: {response_json["code"]}.[/]')
            console.print(f'[maroon]Ответ сервера: {response_json}[/]')


def print_message_after_download(album: Album) -> None:
    console.print(f'[#4be38f]Альбом [i]"{album.artist} - {album.title}"[/] скачан успешно.[/]')


def print_save_album_message(album_path: Path) -> None:
    console.print(f'[white]Путь до папки с альбомом:[/] [i #a0c2c2]{album_path}.[/]')


def print_albums_not_found_message() -> None:
    console.print('[#f5bc42]Альбомов по запросу не найдено.[/]')


