from bs4 import BeautifulSoup
import re
import datetime

def getBooks(page):
    soup = BeautifulSoup(page, 'lxml')
    books = []

    root = soup.find('div', attrs={'id': 'search-results'}).parent.find('div', attrs={'class': 'panel-body'})
    
    for book_elem in root.find_all('div', attrs={'class': 'book-row'}):
        image = book_elem.find('div', {'class': 'cover-image'}).img['src'].split('?')[0]
        title = book_elem.find('div', {'class': 'book-title'}).text.strip()
        annotation = book_elem.find('div', {'class': 'annotation'}).text.strip()
        raw_update = book_elem.find('span', {'class': 'hint-top', 'data-format': 'calendar'})['data-time'].split('.')[0]
        update = datetime.datetime.strptime(raw_update, '%Y-%m-%dT%H:%M:%S')
        size_raw = book_elem.find('div', {'class': 'book-details'}).find_all('span')[0].text
        size = int(''.join(re.findall(r'\d+', size_raw)))
        finished_raw = book_elem.find('div', {'class': 'book-details'})
        finished = len(finished_raw.find_all('span', {'class': 'text-primary'})) == 0
        likes_raw = book_elem.find('span', {'class': 'like-count'}).text
        likes =  int(''.join(re.findall(r'\d+', likes_raw)))
        id = book_elem.find('div', {'class': 'book-title'}).a['href']
        book = {
            'title': title,
            'id': id,
            'image': image,
            'update': update,
            'size': size, #в знаках
            'finished': finished,
            'likes': likes,
            'annotation': annotation,
            'platform': 'author_today'
        }
        books.append(book)
    return books

def getAuthorAbout(page):
    soup = BeautifulSoup(page, 'lxml')
    data = {}
 
    return data
 
