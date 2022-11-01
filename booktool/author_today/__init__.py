import requests
import json
from . import parser


class AuthorToday:
    def __init__(self):
        self._webHost = 'https://author.today'
        self._apiHost = 'https://api.author.today'
        self._headers = {
            'Authorization': 'Bearer guest'
        }

    def get_list(self, author_id):
        url = f'{self._webHost}/u/{author_id}/works'
        page = requests.get(url, headers=self._headers).content.decode('utf8')
        books = parser.getBooks(page)
        return books

    def get_book_property(self, book_id):
        url = f'{self._apiHost}/v1/work/{book_id}/meta-info'
        data_raw = requests.get(url, headers=self._headers).content.decode('utf8')
        data = json.loads(data_raw)
        return data

    def get_author_property(self, author_id):
        url = f'{self._webHost}/u/{author_id}'
        page = requests.get(url, headers=self._headers).content.decode('utf8')
        data = parser.getAuthorAbout(page)
        return data
