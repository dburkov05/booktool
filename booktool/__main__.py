import argparse

import json

import samlib
import author_today

class Samlib:
    def __init__(self):
        self._api = samlib.Samlib('http://samlib.ru')

    def get_property(self, path):
        path = path.split('/')[1:]
        author = path[0]
        book = None
        if len(path) > 1:
            book = path[1] 
        if book:
            data = self._api.get_book_property('/'.join(path))
        else:
            data = self._api.get_author_property(author)
        return data

    def get_list(self, path):
        return self._api.get_list(path.split('/')[1], '')

class AuthorToday:
    def __init__(self):
        self._api = author_today.AuthorToday()
    def get_property(self, path):
        return {}
    def get_list(self, path):
        return self._api.get_list(path.split('/')[1])

endpoint = {}

endpoint['samlib'] = Samlib()
endpoint['at'] = AuthorToday()

def get_list(args):
    path = args.path
    if path.split('/')[0] in endpoint:
        return endpoint[path.split('/')[0]].get_list(path)
    else:
        return {'error': 'нет такой платформы'}

def get_prop(args):
    path = args.path
    if path.split('/')[0] in endpoint:
        return endpoint[path.split('/')[0]].get_property(path)
    else:
        return {'error': 'нет такой платформы'}
   

def bind_get_list(root):
    parser = root.add_parser('list')
    parser.set_defaults(_func=get_list)
    
    parser.add_argument('path', type=str)

    return parser

def bind_get_prop(root):
    parser = root.add_parser('prop')
    parser.set_defaults(_func=get_prop)
    
    parser.add_argument('path', type=str)

    return parser

def bind_get(root):
    parser = root.add_parser('get')
    parser.set_defaults(_func=lambda args: parser.print_help())
    subparsers = parser.add_subparsers()
    
    bind_get_list(subparsers)
    bind_get_prop(subparsers)

    return parser

def get_main_parser():
    parser = argparse.ArgumentParser(prog='book-cli', description='')
    parser.set_defaults(_func=lambda args: parser.print_help())
    subparsers = parser.add_subparsers()
    
    bind_get(subparsers)

    return parser

def main():
    """
    The main entry point of the application
    """

    parser = get_main_parser()
    args = parser.parse_args()
    data = args._func(args)
    #print('[END]', args)
    print(json.dumps(data, indent=4, ensure_ascii=False, default=str))

if __name__ == '__main__':
    main()
