import asyncio

from download import download_albums
from parser import parse_albums
from parser_io import choose_albums_to_download
from classes import DownloadLimit

async def main():
    DownloadLimit.get()
    print(DownloadLimit.albums_left, DownloadLimit.last_download_time)
    albums = await parse_albums()
    needed_albums = await choose_albums_to_download(albums)
    await download_albums(albums=needed_albums)


if __name__ == '__main__':
    asyncio.run(main())