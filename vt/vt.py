import sys

from colorclass import Color
from vittlify_request import (VittlifyError,
                              get_all_shopping_lists,
                              get_shopping_list_info,
                              get_shopping_list_items,
                              get_all_shopping_list_items,
                              get_item,
                              get_completed,
                              complete_item,
                              )
from utils import print_table

(COMPLETED,
 NOT_COMPLETED,
 ALL) = range(3)

def display_shopping_list(guid=None, extended=False, mode=NOT_COMPLETED):
    data = []
    name = ''

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
        name = '+ ' + item['name'] if item['comments'] else '  ' + item['name']
        name = Color('{automagenta}%s{/automagenta}' % name)
        row = [Color('{autoblue}%(guid)s{/autoblue}' % {'guid': item['guid'][:8]})]

        if mode == ALL and item['done']:
            name = Color('{strike}%s{/strike}' % name)

        row.append(name)

        if extended:
            comments = item['comments']
            if mode == ALL and item['done']:
                comments = Color('{strike}%s{/strike}' % comments)
            row.append(comments)

        data.append(row)

    print_table(data, title=title)

def display_item(guid):
    item = get_item(guid)
    name = Color('{automagenta}%s{/automagenta}' % item['name'])
    row = [Color('{autoblue}%(guid)s{/autoblue}' % {'guid': item['guid'][:8]}),
           name]

    if item['comments']:
        row.append(item['comments'])
    print_table([row])

def display_all_shopping_lists():
    shopping_lists = get_all_shopping_lists()
    data = []
    for shopping_list in shopping_lists:
        data.append([Color('{autoblue}%(guid)s{/autoblue}' % {'guid': shopping_list['guid'][:8]}),
                     shopping_list['name']])

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

def main():
    if sys.argv[1].lower() == 'show':
        show(sys.argv[2:])
    elif sys.argv[1].lower() in ('done', 'complete'):
        complete(sys.argv[2:])
    elif sys.argv[1].lower() in ('undone', 'uncomplete'):
        complete(sys.argv[2:], uncomplete=True)

if __name__ == '__main__':
    main()
