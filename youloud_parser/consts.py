from fake_useragent import UserAgent


SITE_URL = 'https://youloud.ru'

ALBUMS_REQUEST_HEADERS = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/png,image/svg+xml,*/*;q=0.8',
    'User-Agent': UserAgent().random,
}