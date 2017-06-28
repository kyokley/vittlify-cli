import sys

from colorclass import Color
from vittlify_request import (VittlifyError,
                              get_all_shopping_lists,
                              get_shopping_list_info,
                              get_shopping_list_items,
                              get_item,
                              )
from utils import print_table

def display_shopping_list(guid, show_done=False, extended=False):
    shopping_list = get_shopping_list_info(guid)
    data = []
    for item in get_shopping_list_items(guid):
        if (not show_done and not item['done']) or show_done:
            name = '+ ' + item['name'] if item['comments'] else '  ' + item['name']
            row = [Color('{autoblue}%(guid)s{/autoblue}' % {'guid': item['guid'][:8]}),
                   name]
            if extended:
                row.append(item['comments'])

            data.append(row)

    print_table(data, title=shopping_list['name'])

def display_item(guid):
    item = get_item(guid)
    row = [Color('{autoblue}%(guid)s{/autoblue}' % {'guid': item['guid'][:8]}),
           item['name']]

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
                display_shopping_list(guid, extended=True)
            else:
                display_shopping_list(guid)
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

def main():
    if sys.argv[1].lower() == 'show':
        show(sys.argv[2:])

if __name__ == '__main__':
    main()