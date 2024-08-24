from rich.console import Console
import inquirer

from album import Album


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
    

def print_download_message(album: Album) -> None:
    print(f'Скачиваю альбом: "{album.artist} - {album.title}"...')


def print_message_after_download(album: Album, response_json: dict) -> None:
    if response_json['status'] == True:
        print(f'Альбом "{album.artist} - {album.title}" скачан успешно.')
    else:
        if response_json['code'] == '-2':
            print(f'Достигнут лимит скачивания альбомов. До обнуления лимита осталось: {response_json.get("timeleft")}.')
        else:
            print(f'Возникла ошибка. Код ошибки: {response_json["code"]}.')
            print('Ответ сервера: ', response_json)


