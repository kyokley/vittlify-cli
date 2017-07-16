from __future__ import print_function
import sys
import requests
import os

from colorclass import Color
from .vittlify_request import (get_all_shopping_lists,
                              get_shopping_list_info,
                              get_shopping_list_items,
                              get_all_shopping_list_items,
                              get_item,
                              get_completed,
                              complete_item,
                              modify_item,
                              add_item,
                              move_item,
                              VITTLIFY_URL,
                              PROXY,
                              )
from .utils import (print_table,
                    format_row,
                    VittlifyError,
                    parse_options,
                    )

SHOW_TRACEBACK = os.environ.get('VT_SHOW_TRACEBACK', 'false').lower() == 'true'
DEFAULT_LIST = os.environ.get('VT_DEFAULT_LIST', '')

(COMPLETED,
 NOT_COMPLETED,
 ALL) = range(3)

def display_shopping_list(guid=None, extended=False, mode=ALL):
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
    raw_options = args
    options = parse_options(raw_options)

    if cmd == 'list':
        guid = None

        for i in range(len(raw_options)):
            if raw_options[i].startswith('-'):
                continue
            else:
                guid = raw_options[i]

        if not guid:
            guid = DEFAULT_LIST

        if not guid:
            raise IndexError('Incorrect number of arguments')

        try:
            display_shopping_list(guid=guid, **options)
        except VittlifyError as e:
            print(Color("{autored}%s{/autored}" % e))

    elif cmd == 'lists':
        try:
            display_all_shopping_lists()
        except VittlifyError as e:
            print(Color("{autored}%s{/autored}" % e))
    elif cmd in ('show', 'item'):
        guid = raw_options.pop(0)

        if not guid:
            raise IndexError('Incorrect number of arguments')

        try:
            display_item(guid)
        except VittlifyError as e:
            print(Color("{autored}%s{/autored}" % e))

def complete(args, uncomplete=False):
    raw_options = args
    options = parse_options(raw_options)

    arg_count = 0
    for val in args:
        if not val.strip().startswith('-'):
            arg_count += 1

    if not arg_count:
        display_shopping_list(mode=COMPLETED, **options)
    else:
        guid = args.pop(0)
        resp = complete_item(guid, uncomplete=uncomplete)

        if not uncomplete:
            print(Color('Marked {strike}{automagenta}%s{/automagenta}{/strike} as done.' % resp['name']))
        else:
            print(Color('Marked {automagenta}%s{/automagenta} undone.' % resp['name']))

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

def move(args):
    guid = args.pop(0).lower()
    to_guid = args.pop(0).lower()
    move_item(guid, to_guid)
    print(Color('Moved item {autoblue}%s{/autoblue} to list {autoblue}%s{/autoblue}' % (guid, to_guid)))

def run(args):
    try:
        if args[0].lower() in ('list', 'lists', 'item', 'show'):
            show(args)
        elif args[0].lower() in ('done', 'complete'):
            complete(args[1:])
        elif args[0].lower() in ('undone', 'uncomplete'):
            complete(args[1:], uncomplete=True)
        elif args[0].lower() in ('modify', 'edit', 'comment', 'comments'):
            modify(args[1:])
        elif args[0].lower() in ('add',):
            add(args[1:])
        elif args[0].lower() in ('move', 'mv'):
            move(args[1:])
    except IndexError:
        print(Color('{autored}Incorrect number of arguments provided{/autored}'))
        if SHOW_TRACEBACK:
            raise
    except requests.exceptions.ConnectionError:
        print(Color('{autored}Unable to connect to Vittlify instance at %s{/autored}' % VITTLIFY_URL))
        if PROXY:
            print(Color('{autored}Attempted to use proxy at %s{/autored}' % PROXY))
        if SHOW_TRACEBACK:
            raise
    except requests.exceptions.HTTPError as e:
        print(Color('{autored}Server responded with %s{/autored}' % e.message))
        if SHOW_TRACEBACK:
            raise
    except VittlifyError as e:
        print(Color('{autored}%s{/autored}' % e))

def main():
    run(sys.argv[1:])

if __name__ == '__main__':
    main()
