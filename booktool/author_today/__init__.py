import requests
from . import parser

def get_response(url):
    try:
        response = requests.get(url)
        data = response.content.decode('utf-8')
        return data
    except Exception as e:
        pass
    return None



class AuthorToday:
    def __init__(self):
        self._webHost = 'https://author.today'
        self._apiHost = 'https://api.author.today'
    def get_list(self, author_nickname):
        url = f'{self._webHost}/u/{author_nickname}/works'
        page = get_response(url)
        books = parser.getBooks(page)
        return books
    def get_book_property(self, book_id):
        return {}
        
