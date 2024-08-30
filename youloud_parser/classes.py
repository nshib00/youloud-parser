from dataclasses import dataclass


@dataclass
class Album:
    title: str
    artist: str
    link: str

    def __repr__(self):
        return f'{self.artist} - {self.title}'