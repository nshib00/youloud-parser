import asyncio

from loguru import logger

from youloud_parser.download import download_albums
from youloud_parser.exceptions import NoAlbumsError
from youloud_parser.parser import parse_albums
from youloud_parser.parser_io import (
    choose_albums_to_download,
    print_error_message,
    print_info_message,
    print_no_albums_message,
    print_program_stop_message,
    print_start_message,
)

logger.remove(0)
logger.add("logs.log", level="INFO", rotation="100KB", retention="1 day", compression="zip")


@logger.catch
async def main():
    print_start_message()
    print_info_message()
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
            if e.args:
                logger.error(f"{e.__class__.__name__}: {e}")
            else:
                logger.error(f"{e.__class__.__name__}")


if __name__ == "__main__":
    asyncio.run(main())
