import requests
from . import parser as samlib_parser
#import logging
import datetime
#from dto import Book
#from typing import TypedDict

#class Book(TypedDict):
#    title: str
#    id: str
#    author: str #samlib:author_id
#    genre: str
#    rate: str
#    size: int #kilo bite
#    annotation: str

class Samlib:
    def __init__(self, host):
        self._host = host #example: http://samlib.ru
        #self.logger = logging.getLogger(__name__+'.Samlib')
        #self.logger.info('created')

    def __get_response(self, url):
        try:
            response = requests.get(url)
            data = response.content.decode('cp1251')
            return data
        except Exception as e:
            pass
        return None

    def __get_header(self, url):
        try:
            r = requests.get(url, stream=True)
            data = ''
            for line in r.iter_lines(decode_unicode=False):
                if line:
                    elem = line.decode('cp1251')
                    data += elem
                    if '<hr size=2 noshade>' in data:
                        break
            return data
        except Exception as e:
            pass
        return None
    
    def __download_file(self, url, local_filename):
        r = requests.get(url, stream=True)
        if(r):
            with open(local_filename, 'wb') as f:
                for chunk in r.iter_content(chunk_size=8192):
                    f.write(chunk)
            return True
        return False

    #public methods

    def get_author_property(self, path):
        author_nickname = path.split('/')[0]
        page = self.__get_response(f'{self._host}/{author_nickname[0]}/{author_nickname}')
        if(page == None):
            return None
        data = samlib_parser.getAuthorAbout(page)
        return data
    
    def get_list(self, author_nickname, section):
        page = self.__get_response(f'{self._host}/{author_nickname[0]}/{author_nickname}/{section}')
        books = samlib_parser.getBooks(page, False)
        out = []
        for elem in books:
            out.append({
                'title': elem['title'],
                'id': author_nickname + '/' + elem['link'][:-6],
                'size': elem['size'],
                'annotation': elem['annotation'],
                'platform': 'samlib'
                })
        return out

    def get_books_from_author(self, author_nickname, include_subsections = False):
        page = self.__get_response(f'{self._host}/{author_nickname[0]}/{author_nickname}')
        if(page == None):
            return None
        
        books = []
        books += samlib_parser.getBooks(page, False)

        if(include_subsections):
            sections = samlib_parser.getSections(page)
            for section in sections:
                sub_page = self.__get_response(f'{self._host}/{author_nickname[0]}/{author_nickname}/{section["link"]}')
                section_books = samlib_parser.getBooks(sub_page, False)
                books += section_books

        return books
    
    def download_book_fb2(self, author_nickname, book_filename):
        url = f'{self._host}/{author_nickname[0]}/{author_nickname}/{book_filename}.fb2.zip'
        if(self.__download_file(url, f'{book_filename}.fb2.zip')):
            return True
        return False
    
    def get_book_property(self, book_id):
        author_nickname, book_filename = book_id.split('/')
        data = {}
        page = self.__get_header(f'{self._host}/{author_nickname[0]}/{author_nickname}/{book_filename}.shtml')
        if(page == None):
            return None
        data = samlib_parser.getBookHeader(page)
        data['author'] = author_nickname
        if data['download']:
            data['download'] = f'{self._host}/{author_nickname[0]}/{author_nickname}/{data["download"]}'
        return data
    
    def get_updates(self, authors_nickname, date = None):
        if date == None:
            date = datetime.date.today().strftime('%Y/%m-%d')
        url = f'{self._host}/logs/{date}.log'
        page = self.__get_response(url)
        updates = {}
        for line in page.split('\n'):
            if(line == ''):
                continue
            raw = line.split('|')
            author = raw[0].split('/')[2]
            if(not author in updates):
                updates[author] = [];
            updates[author].append({
                'author': author,
                'author_title': raw[4],
                'filename': raw[0].split('/')[3],
                #'datetime': raw[2],
                'operaion': raw[1],
                'title': raw[3],
                'timestamp': int(raw[10])
                #'timestamp': datetime.datetime.utcfromtimestamp(int(raw[10])).strftime('%Y-%m-%d %H:%M:%S')
            })
        if(len(authors_nickname) == 0):
            return updates
        out = []
        for nick in authors_nickname:
            if(nick in updates):
                out.append({
                    'author': nick,
                    'updates': updates[nick] 
                })
            else:
                out.append({
                    'author': nick,
                    'updates': []
                })
        return out
