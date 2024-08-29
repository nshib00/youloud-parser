from dataclasses import dataclass
import json
import time


@dataclass
class Album:
    title: str
    artist: str
    link: str

    def __repr__(self):
        return f'{self.artist} - {self.title}'
    

class DownloadLimit:
    MAX_ALBUMS_LIMIT: int = 3

    albums_left: int = MAX_ALBUMS_LIMIT
    last_download_time: int | None = None


    @classmethod
    def get(cls) -> None:
        with open('limit.json') as file:
            limit_data = json.load(file)
        cls.albums_left = limit_data['albums_left']
        cls.last_download_time = limit_data['last_download_in']


    @classmethod
    def save(cls) -> None:
        limit_data = {
            'albums_left': cls.albums_left,
            'last_download_in': cls.last_download_time
        }
        with open('limit.json', 'w', encoding='utf-8') as file:
            json.dump(limit_data, file, indent=4)

    
    @classmethod
    def update(cls) -> None:
        cls.albums_left -= 1
        cls.last_download_time = int(time())
        cls.save()


    @classmethod
    def is_active(cls) -> bool:
        return not(
            cls.albums_left == 0 and int(time()) - cls.last_download_time > 7200
        )
    
    @classmethod
    def reset_if_inactive(cls) -> None:
        if not cls.is_active():
            cls.albums_left = cls.MAX_ALBUMS_LIMIT
