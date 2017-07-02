import sys
import requests
import os

from colorclass import Color
from vittlify_request import (VittlifyError,
                              get_all_shopping_lists,
                              get_shopping_list_info,
                              get_shopping_list_items,
                              get_all_shopping_list_items,
                              get_item,
                              get_completed,
                              complete_item,
                              modify_item,
                              add_item,
                              VITTLIFY_URL,
                              )
from utils import print_table, format_row

SHOW_TRACEBACK = os.environ.get('VT_SHOW_TRACEBACK', 'false').lower() == 'true'
DEFAULT_LIST = os.environ.get('VT_DEFAULT_LIST', '')

(COMPLETED,
 NOT_COMPLETED,
 ALL) = range(3)

def display_shopping_list(guid=None, extended=False, mode=NOT_COMPLETED):
    data = []

    if mode == NOT_COMPLETED:
        shopping_list = get_shopping_list_info(guid)
        title = shopping_list['name']
        items = get_shopping_list_items(guid)
    elif mode == COMPLETED:
        items = get_completed()
        title = 'Recently Completed'
    elif mode == ALL:
        shopping_list = get_shopping_list_info(guid)
        title = shopping_list['name']
        items = get_all_shopping_list_items(guid)

    for item in items:
        data.append(format_row(item, include_comments=extended))

    print_table(data, title=title)

def display_item(guid):
    item = get_item(guid)
    print_table([format_row(item, include_comments=True)])

def display_all_shopping_lists():
    shopping_lists = get_all_shopping_lists()
    data = []
    for shopping_list in shopping_lists:
        data.append(format_row(shopping_list))

    print_table(data, title='All Lists')

def show(args):
    cmd = args.pop(0).lower()
    options = args

    if cmd == 'list':
        guid = options.pop(0)

        if not guid:
            raise ValueError('Incorrect number of arguments')

        try:
            if 'extended' in options:
                display_shopping_list(guid=guid, extended=True, mode=ALL)
            else:
                display_shopping_list(guid=guid)
        except VittlifyError as e:
            print(Color("{autored}%s{/autored}" % e))

    elif cmd == 'lists':
        try:
            display_all_shopping_lists()
        except VittlifyError as e:
            print(Color("{autored}%s{/autored}" % e))
    elif cmd == 'item':
        guid = options.pop(0)

        if not guid:
            raise ValueError('Incorrect number of arguments')

        try:
            display_item(guid)
        except VittlifyError as e:
            print(Color("{autored}%s{/autored}" % e))
    elif cmd in ('done', 'completed'):
        if 'extended' in options:
            display_shopping_list(extended=True, mode=COMPLETED)
        else:
            display_shopping_list(mode=COMPLETED)

def complete(args, uncomplete=False):
    guid = args.pop(0)
    resp = complete_item(guid, uncomplete=uncomplete)

    if not uncomplete:
        print Color('Marked {strike}{automagenta}%s{/automagenta}{/strike} as done.' % resp['name'])
    else:
        print Color('Marked {automagenta}%s{/automagenta} undone.' % resp['name'])

def modify(args):
    guid = args.pop(0).lower()
    comments = ' '.join(args)
    modify_item(guid, comments)
    display_item(guid)

def add(args):
    if len(args) == 1:
        if DEFAULT_LIST:
            guid = DEFAULT_LIST
        else:
            raise IndexError
    else:
        guid = args.pop(0).lower()
    name = args.pop(0)

    item = add_item(guid, name)
    print_table([format_row(item)])

def main():
    try:
        if sys.argv[1].lower() == 'show':
            show(sys.argv[2:])
        elif sys.argv[1].lower() in ('list', 'lists', 'item'):
            show(sys.argv[1:])
        elif sys.argv[1].lower() in ('done', 'complete'):
            complete(sys.argv[2:])
        elif sys.argv[1].lower() in ('undone', 'uncomplete'):
            complete(sys.argv[2:], uncomplete=True)
        elif sys.argv[1].lower() in ('modify', 'edit', 'comment', 'comments'):
            modify(sys.argv[2:])
        elif sys.argv[1].lower() in ('add',):
            add(sys.argv[2:])
    except IndexError:
        print(Color('{autored}Incorrect number of arguments provided{/autored}'))
        if SHOW_TRACEBACK:
            raise
    except requests.exceptions.ConnectionError:
        print(Color('{autored}Unable to connect to Vittlify instance at %s{/autored}' % VITTLIFY_URL))
        if SHOW_TRACEBACK:
            raise
    except requests.exceptions.HTTPError as e:
        print(Color('{autored}Server responded with %s{/autored}' % e.message))
        if SHOW_TRACEBACK:
            raise

if __name__ == '__main__':
    main()
