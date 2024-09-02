# ![Logo](https://github.com/user-attachments/assets/5a199bf7-9963-475d-9995-b4fec00dc518) Youloud Parser

<p align="center">
<img src="https://img.shields.io/badge/python-3.9 | 3.10 | 3.11 | 3.12-blue?logo=python&logoColor=white">
<img src="https://img.shields.io/badge/code--style-black-black">
<img src="https://img.shields.io/github/downloads/nshib00/youloud-parser/total.svg">
<img src="https://img.shields.io/github/v/release/nshib00/youloud-parser.svg">
<img src="https://img.shields.io/github/license/nshib00/wiffy.svg">
<p>

Консольное приложение на Python для скачивания альбомов с сайта [youloud.ru](https://youloud.ru).

![Снимок экрана 2024-09-01 224737](https://github.com/user-attachments/assets/3cdc2c31-8887-4dde-a46c-dbb99d78f4c9)
d
## Возможности

- **Удобный поиск по альбомам:** не нужно для скачивания альбома открывать его страницу и нажимать на кнопку, как на сайте. 
- **Скачивание альбомов в обход лимита без подписки** (3 альбома, обновляется через 2 часа). [*(есть нюанс)*](https://github.com/nshib00/youloud-parser/new/main?filename=README.md#%D0%BF%D1%80%D0%B8%D0%BC%D0%B5%D1%87%D0%B0%D0%BD%D0%B8%D1%8F)
- **Скачивание нескольких альбомов сразу.** Достаточно выбрать несколько альбомов в меню и начать скачивание.
- **Автоматическая конвертация скачанных альбомов** из формата `.ggj` в формат `.zip`.
- **Автоматическое переименование альбомов** по формату: `<исполнитель> - <название альбома> <(год)>.zip`.

## Как установить

Перейдите на страницу [последнего релиза](https://github.com/nshib00/youloud-parser/releases/latest).

## Как запустить в Python

Программа использует инструмент для управления зависимостями **Poetry**. Если у вас нет Poetry, установите через pip:

`pip install poetry`

Далее выполните:
```
git clone https://github.com/nshib00/youloud-parser.git
cd youloud-parser
poetry shell
poetry install
python youloud_parser/main.py
```

## Примечания

Несмотря на то, что зачастую можно скачать более 3 альбомов за сессию, временное ограничение на скачивание может появляться. При этом программа выведет сообщение:

`Достигнут лимит скачивания альбомов. До обнуления лимита осталось: <время>.`

В данном случае:
- Используйте VPN или другие способы обхода со сменой IP-адреса. 
- Попробуйте скачать альбомы снова через указанное время или позже, ограничение по вашему IP к этому времени должно быть снято.

## Лицензия

В проекте используется лицензия [MIT](https://github.com/nshib00/youloud-parser/blob/main/LICENSE).
