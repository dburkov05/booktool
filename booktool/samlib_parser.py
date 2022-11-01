from bs4 import BeautifulSoup
import re

def getAuthorAbout(page: str):
  data = {
    'name': None,
    'title': None,
    'email': None,
    'birthday': None,
    'updated': None,
    'address': None,
    'size': None,
    'visitors': None,
    'rate': None,
    'friends': 0,
    'friend_of': 0,
    'about': None,
    'annotation': None,
  }

  soup = BeautifulSoup(page, 'lxml')

  data['name'] = soup.h3.contents[0][:-1]
  data['title'] = soup.h3.font.text  
  
  #html_table = soup.find_all('font', color='#393939', text='Обновлялось:')[0].parent.parent.parent.parent.text.split('\n')
  html_table = soup.find_all('table', bgcolor="#e0e0e0")[0].text.split('\n')
  raw_table = {}

  for line in html_table:
    line = line.strip()
    if(line == ''):
      continue
    key = line.split(':')[0]
    value = ':'.join(line.split(':')[1:]).strip()
    raw_table[key] = value

  if('Aдpeс' in raw_table):
    data['email'] = raw_table['Aдpeс']
  if('Родился' in raw_table):
    data['birthday'] = raw_table['Родился']
  if('Обновлялось' in raw_table):
    data['updated'] = raw_table['Обновлялось']
  if('Живет' in raw_table):
    data['address'] = raw_table['Живет']
  if('Объем' in raw_table):
    data['size'] = raw_table['Объем']
  if('Рейтинг' in raw_table):
    data['rate'] = raw_table['Рейтинг']
  if('Посетителей за год' in raw_table):
    data['visitors'] = int(raw_table['Посетителей за год'])
  if('Посетителей за год' in raw_table):
    data['visitors'] = int(raw_table['Посетителей за год'])
  if('Friends/Friend Of' in raw_table):
    friends = raw_table['Friends/Friend Of'].split('/')
    data['friends'] = int(friends[0])
    data['friend_of'] = int(friends[1])

  if(len(soup.find_all('font', text='Об авторе:')) > 0):
    about_elem = soup.find_all('font', text='Об авторе:')[0]
    data['about'] = about_elem.parent.parent.find_all('i')[0].text.strip().replace('\n', ' ');
  if(len(soup.find_all('font', text='Аннотация к разделу:')) > 0):
    annot_elem = soup.find_all('font', text='Аннотация к разделу:')[0]
    data['annotation'] = annot_elem.parent.parent.find_all('i')[-1].text.strip().replace('\n', ' ');
  
  return data

def getBooks(page, splitting = True):
  soup = BeautifulSoup(page, 'lxml')

  #print(soup.find_all('font', text='Аннотация к разделу:'))

  books_sections = []
  
  if(splitting):
    list_of_elements = soup.dl.find_all(['dl', 'gr0'])
  else:
    list_of_elements = soup.dl.find_all('dl')
    books_sections.append({
      'books': []
    })
  
  for raw_book_elem in list_of_elements:
  
    if(raw_book_elem.name == 'gr0'):
      title = raw_book_elem.parent.text[:-1]
      text = ''
      if(len(raw_book_elem.parent.find_all('font', color='#393939')) == 0):
        text = raw_book_elem.parent.parent.parent.parent.find_all('font', size='-1')[0].text
      books_sections.append({
        'title': title,
        'text': text,
        'books': []
      })
      continue
    
    book_elem = raw_book_elem.dt
      
    if(book_elem == None):
      continue
    else:
      book_elem = book_elem.li
    
    if(book_elem == None):
      continue
  
    data = {
      'title': None,
      'link': None,
      'rate': None,
      'genre': None,
      'size': None,
      'annotation': None
    }  
    
    for elem in book_elem.find_all('a'):
      if(len(elem['href'].split('/')) > 1):
        continue
      data['title'] = elem.text
      data['link'] = elem['href']
      
      if(elem.find_next_sibling() != None):
        data['size'] = int(elem.find_next_sibling().text[:-1])
    
    if(book_elem.small):
      elems = list(book_elem.small)
      if('Оценка:' in elems):
        data['rate'] = elems[elems.index('Оценка:')+1].text
      for i in range(len(elems)):
        if(elems[i].name != None or elems[i].text.strip() == '' or elems[i].text.strip() == 'Оценка:'):
          continue
        data['genre'] = '|'.join(list(map(lambda x: x.lower(), elems[i].text.strip().replace(' ', '').split(','))))
    
    annotation = ''
    
    for elem in book_elem.find_all('dd', recursive=False):
      apps_flag = False
      for el2 in elem.find_all('a'):
        if(el2.text.count('Иллюстрации/приложения:') > 0):
          apps_flag = True
        #print('a', el2['href'], el2.text)
      if(apps_flag):
        annotation += '\n'.join(list(map(lambda x: x.strip(), list(elem.strings)))[:-1])
      else:
        annotation += elem.text + '\n'
      
      #print('dd', elem)
      #print('   a', elem.a)
      #print('   s', list(elem.strings))
    
    data['annotation'] = annotation.strip()
    
    #print('ANNOTATION', annotation.strip())
    
    #print(book_elem.find_all('a'))
    #print(book_elem.find_all('dd'))
    
    #print('Book:', data)
    
    #print('#' * 20)
    
    books_sections[-1]['books'].append(data)
  
  if(splitting):
    return books_sections
  else:
    return books_sections[0]['books']

def getSections(page):
  soup = BeautifulSoup(page, 'lxml')
  raw_sections = soup.find_all('font', attrs = {'size': '+1'})
  sections = []

  for elem in raw_sections:
    a = elem.find_all('a')
    if(len(a) > 1):
      if(len(a[1]['href'].split('/')) > 1 and a[1]['href'].split('/')[1] == 'type'):
        continue
      name, count = list(elem.stripped_strings)
      link = a[1]['href']
      sections.append({
        'name': name,
        'link': link,
        'count': int(count[1:-1]),
        'annotation': elem.parent.find_all('i')[0].text
      })
  return sections

def getBookHeader(page):
  data = {
    'author': None,
    'title': None,
    'copyright': None,
    'download': None,
    'genres': [],
    'created': None,
    'updated': None,
    'annotation': None,
  }
  
  soup = BeautifulSoup(page, 'lxml')
  
  root = soup.find_all('table')[2]
  
  annotation_candidaates = root.find_all('font', color='#555555')
  
  if(len(annotation_candidaates) > 0):
    data["annotation"] = annotation_candidaates[0].text
  
  #print(root.ul.find_all('li'))
  
  download_a = root.find_all('a', href=(lambda x: x.count('.fb2.zip') > 0))
  
  if(len(download_a) > 0):
    data['download'] = download_a[0]['href']
  
  janres_a = root.find_all('a', href=(lambda x: x.count('/janr/index_janr') > 0))
  
  for janr in janres_a:
    data['genres'].append(janr.text.lower())
  
  reg = r'Размещен: \d\d/\d\d/\d{4}, изменен: \d\d/\d\d/\d{4}'
  
  for li_elem in root.ul.find_all('li'):
    match = re.search(reg, li_elem.text)
    if(match):
      created, updated = re.findall(r'\d\d/\d\d/\d{4}', match[0])
      data['created'] = created
      data['updated'] = updated
    if(li_elem.text.count('Copyright') > 0):
      data['copyright'] = li_elem.a.text
  
  data['title'] = soup.center.h2.text
  return data
