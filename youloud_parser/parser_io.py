from pathlib import Path

import inquirer
from loguru import logger
from rich.console import Console
from rich.panel import Panel

from youloud_parser.classes import Album
from youloud_parser.exceptions import NoAlbumsError

console = Console()


def print_start_message() -> None:
    console.print(Panel.fit(f"[#4be38f]{'Youloud Parser':-^40}"))


def print_info_message() -> None:
    console.print("[i #777777]🛈  Чтобы выйти из программы, нажмите Enter.\n")


def get_album_query() -> str:
    return console.input("[#4be38f]Введите запрос[/] [i #777777](исполнитель или название альбома): [/]")


def print_no_albums_message() -> None:
    console.print(
        "[#f5bc42]Альбомов по запросу не найдено. Попробуйте немного изменить предыдущий запрос или ввести новый.[/]"
    )


def print_program_stop_message() -> None:
    console.print("[#a0dddd]Работа программы завершена.")


def print_error_message(error: Exception) -> None:
    console.print(f"[#ff4a44]Возникла ошибка: {error}.[/]")


async def choose_albums_to_download(albums: list[Album]) -> list[Album]:
    if not albums:
        raise NoAlbumsError
    else:
        albums_checkbox = [
            inquirer.Checkbox(
                "albums",
                message="Выберите альбом(ы), которые хотите скачать",
                choices=albums,
                carousel=True,
            )
        ]
        try:
            needed_albums: dict = inquirer.prompt(albums_checkbox)
            return needed_albums.get("albums")
        except (AttributeError, IndexError):
            print_no_albums_message()
            logger.info("Выбор альбомов прерван пользователем.")
            return []


def print_album_code_message(response_json: dict) -> None:
    if not response_json["status"]:
        if response_json["code"] == -2:
            timeleft = response_json["timeleft"]
            if "1 часов" in timeleft:
                timeleft = timeleft.replace("часов", "час")
            limit_info_text = "Достигнут лимит скачивания альбомов. До обнуления лимита осталось:"
            console.print(f"[#ff7f44]{limit_info_text}[/] [b green]{timeleft}.[/]")
            logger.info(f"{limit_info_text} {timeleft}.")
        else:
            console.print(f'[#ff4a44]Возникла ошибка при скачивании. Код ошибки: {response_json["code"]}.[/]')
            logger.error(f"Ошибка скачивания с Youloud. Ответ сервера: {response_json}.")


def print_message_after_download(album: Album) -> None:
    console.print(f'[#4be38f]Альбом [i]"{album.artist} - {album.title}"[/] скачан успешно.[/]')
    logger.success(f'Альбом "{album.artist} - {album.title}" скачан успешно.')


def print_save_album_message(album_path: Path) -> None:
    console.print(f"[white]Путь до папки с альбомом:[/] [i #a0c2c2]{album_path}.[/]")
    logger.info(f"Путь до папки с альбомом: {album_path}.")


def print_albums_not_found_message() -> None:
    console.print("[#f5bc42]Альбомов по запросу не найдено.[/]")


def make_album_data_status_text(album: Album) -> str:
    return f'[#a0dddd]Получаю данные об альбоме [i]"{album.artist} - {album.title}"...[/][/]'


def make_download_status_text(album: Album) -> str:
    logger.info(f'Начало скачивания альбома "{album.artist} - {album.title}".')
    return f'[#a0dddd]Скачиваю альбом [i]"{album.artist} - {album.title}"...[/][/]'
