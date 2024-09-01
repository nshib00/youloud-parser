import asyncio

from youloud_parser.download import download_albums
from youloud_parser.parser import parse_albums
from youloud_parser.parser_io import choose_albums_to_download, print_error_message, print_no_albums_message, print_program_stop_message
from youloud_parser.exceptions import NoAlbumsError


async def main():
    while True:
        try:
            albums = await parse_albums()
            needed_albums = await choose_albums_to_download(albums)
            await download_albums(albums=needed_albums)
        except NoAlbumsError:
            print_no_albums_message()
        except KeyboardInterrupt:
            print_program_stop_message()
            break
        except Exception as e:
            print_error_message(error=e)


if __name__ == '__main__':
    asyncio.run(main())