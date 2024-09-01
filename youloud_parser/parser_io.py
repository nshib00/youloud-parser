from pathlib import Path
from rich.console import Console
import inquirer
from pyfiglet import figlet_format

from youloud_parser.classes import Album
from youloud_parser.exceptions import NoAlbumsError


console = Console()


def print_ascii_art() -> None:
    art = figlet_format('Youloud * Parser')
    console.print(f'[#4be38f]{"-" * 75}')
    console.print(f'[#4be38f]{art}')
    console.print(f'[#4be38f]{"-" * 75}')


def print_info_message() -> None:
    console.print(f'[i #777777]🛈  Чтобы выйти из программы, нажмите Enter.\n')


def get_album_query() -> str:
    return console.input('[#4be38f]Введите запрос[/] [i #777777](исполнитель и/или название альбома): [/]')


def print_no_albums_message() -> None:
    console.print(
        '[#f5bc42]Альбомов по запросу не найдено. Попробуйте немного изменить предыдущий запрос или ввести новый.[/]'
    )


def print_program_stop_message() -> None:
    console.print('[#a0dddd]Работа программы завершена.')


def print_error_message(error: Exception) -> None:
    console.print(f'[#ff4a44]Возникла ошибка: {error}.[/]')
 

async def choose_albums_to_download(albums: list[Album]) -> list[Album]:
    if not albums:
        raise NoAlbumsError
    else:
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
            print_no_albums_message()
            return []
    

def print_album_code_message(response_json: dict) -> None:
    if response_json['status'] == False:
        if response_json['code'] == -2: 
            timeleft = response_json['timeleft']
            if '1 часов' in timeleft:
                timeleft = timeleft.replace('часов', 'час')
            console.print(f'[#ff7f44]Достигнут лимит скачивания альбомов. До обнуления лимита осталось:[/] [b green]{timeleft}.[/]')
        else:
            console.print(f'[#ff4a44]Возникла ошибка при скачивании. Код ошибки: {response_json["code"]}.[/]')
            # console.print(f'[#a0dddd]Ответ сервера: {response_json}[/]')


def print_message_after_download(album: Album) -> None:
    console.print(f'[#4be38f]Альбом [i]"{album.artist} - {album.title}"[/] скачан успешно.[/]')


def print_save_album_message(album_path: Path) -> None:
    console.print(f'[white]Путь до папки с альбомом:[/] [i #a0c2c2]{album_path}.[/]')


def print_albums_not_found_message() -> None:
    console.print('[#f5bc42]Альбомов по запросу не найдено.[/]')


def make_album_data_status_text(album: Album) -> str:
    return f'[#a0dddd]Получаю данные об альбоме [i]"{album.artist} - {album.title}"...[/][/]'


def make_download_status_text(album: Album) -> str:
    return f'[#a0dddd]Скачиваю альбом [i]"{album.artist} - {album.title}"...[/][/]'




