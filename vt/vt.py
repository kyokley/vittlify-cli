from __future__ import print_function
import sys
import requests
import os

from enum import Enum
from blessings import Terminal
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
                               categorize_item,
                               VITTLIFY_URL,
                               PROXY,
                               )
from .utils import (print_table,
                    format_row,
                    VittlifyError,
                    parse_options,
                    apply_strikethrough,
                    )
from .help import (GENERAL_HELP,
                   LISTS_HELP,
                   LIST_HELP,
                   DONE_HELP,
                   UNDONE_HELP,
                   COMMENT_HELP,
                   MOVE_HELP,
                   CATEGORIES_HELP,
                   CATEGORIZE_HELP,
                   )

term = Terminal()

SHOW_TRACEBACK = os.environ.get('VT_SHOW_TRACEBACK', 'false').lower() == 'true'
DEFAULT_LIST = os.environ.get('VT_DEFAULT_LIST', '')


class StrEnum(str, Enum):
    @classmethod
    def from_string(cls, str_type):
        if str_type is not None:
            for enum_type in cls:
                if enum_type.value.lower() == str_type.strip().lower():
                    return enum_type
        return None

    def __str__(self):
        return self.value


class Status(StrEnum):
    COMPLETED = 'COMPLETED'
    NOT_COMPLETED = 'NOT_COMPLETED'
    ALL = 'ALL'


def display_shopping_list(guid=None,
                          extended=False,
                          mode=Status.ALL,
                          quiet=False,
                          unfinished=False,
                          include_category=False,
                          no_wrap=False,
                          ):
    data = []

    shopping_list = None
    if mode == Status.NOT_COMPLETED or unfinished:
        shopping_list = get_shopping_list_info(guid)
        title = shopping_list['name']
        items = get_shopping_list_items(guid)
    elif mode == Status.COMPLETED:
        items = get_completed()
        title = 'Recently Completed'
    elif mode == Status.ALL:
        shopping_list = get_shopping_list_info(guid)
        title = shopping_list['name']
        items = get_all_shopping_list_items(guid)

    for item in items:
        data.append(format_row(item,
                               shopping_list,
                               include_comments=extended,
                               include_category=include_category,
                               no_wrap=no_wrap))

    print_table(data, title=title, quiet=quiet)


def display_item(guid, no_wrap=False):
    item = get_item(guid)
    print_table([
        format_row(item, None, include_comments=True, no_wrap=no_wrap)
    ])


def display_all_shopping_lists(no_wrap=False):
    shopping_lists = get_all_shopping_lists()
    data = []
    for shopping_list in shopping_lists:
        data.append(format_row(shopping_list, None, no_wrap=no_wrap))

    print_table(data, title='All Lists')


def display_shopping_list_categories(guid):
    shopping_list = get_shopping_list_info(guid)
    list_categories = shopping_list.get('categories')

    data = []

    if not list_categories:
        print(
            term.red(
                f"No categories found for {shopping_list['name']}."))
    else:
        for category in list_categories:
            data.append([category['name']])
        print_table(data, title=shopping_list['name'])


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
            print(term.red(f"{e}"))

    elif cmd == 'lists':
        try:
            display_all_shopping_lists()
        except VittlifyError as e:
            print(term.red(f"{e}"))
    elif cmd in ('show', 'item'):
        guid = raw_options.pop(0)

        if not guid:
            raise IndexError('Incorrect number of arguments')

        try:
            display_item(guid)
        except VittlifyError as e:
            print(term.red(f"{e}"))


def complete(args, uncomplete=False):
    raw_options = args
    options = parse_options(raw_options)

    arg_count = 0
    for val in args:
        if not val.strip().startswith('-'):
            arg_count += 1

    if not arg_count:
        display_shopping_list(mode=Status.COMPLETED, **options)
    else:
        while args:
            guid = args.pop(0)
            resp = complete_item(guid, uncomplete=uncomplete)

            if not uncomplete:
                print(
                    f'Marked {term.magenta}{apply_strikethrough(resp["name"])}{term.normal} as done.')
            else:
                print(
                    f'Marked {term.magenta}{resp["name"]}{term.normal} undone.'
                )


def modify(args):
    options = parse_options(args)
    guid = args.pop(0).lower()

    comments = ' '.join(
        [arg for arg in args if not arg.startswith('-') or ' ' in arg])
    modify_item(guid, comments, **options)
    display_item(guid)


def add(args, no_wrap=False):
    if len(args) == 1:
        if DEFAULT_LIST:
            guid = DEFAULT_LIST
        else:
            raise IndexError
    else:
        guid = args.pop(0).lower()
    name = args.pop(0)

    item = add_item(guid, name)
    print_table([format_row(item, no_wrap=no_wrap)])


def move(args):
    guid = args.pop(0).lower()
    to_guid = args.pop(0).lower()
    move_item(guid, to_guid)
    print(
        f'Moved item {term.blue}{guid}{term.normal} to list {term.blue}{to_guid}{term.normal}')


def categories(args):
    guid = args.pop(0).lower() if len(args) > 0 else None

    if not guid:
        guid = DEFAULT_LIST

    if not guid:
        raise IndexError('Incorrect number of arguments')

    try:
        display_shopping_list_categories(guid)
    except VittlifyError as e:
        print(term.red(f"{e}"))


def categorize(args):
    if len(args) != 2:
        raise IndexError('Incorrect number of arguments. Expected 2, got %s' % len(args))

    guid = args.pop(0).lower()
    category_name = args.pop(0).lower()

    try:
        item = categorize_item(guid, category_name)
        print(f'Set item {term.blue}{item["name"]}{term.normal} to category {term.blue}{category_name.title()}{term.normal}')
    except VittlifyError as e:
        print(term.red(f"{e}"))


def help(args):
    help_str = ''

    if not args:
        help_str = GENERAL_HELP
    elif args[0].lower() == 'lists':
        help_str = LISTS_HELP
    elif args[0].lower() == 'list':
        help_str = LIST_HELP
    elif args[0].lower() in ('done', 'complete'):
        help_str = DONE_HELP
    elif args[0].lower() in ('undone', 'uncomplete'):
        help_str = UNDONE_HELP
    elif args[0].lower() in ('modify', 'edit', 'comment', 'comments'):
        help_str = COMMENT_HELP
    elif args[0].lower() in ('move', 'mv'):
        help_str = MOVE_HELP
    elif args[0].lower() in ('categories',):
        help_str = CATEGORIES_HELP
    elif args[0].lower() in ('categorize', 'label'):
        help_str = CATEGORIZE_HELP
    else:
        help_str = GENERAL_HELP

    return help_str


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
        elif args[0].lower() in ('categories',):
            categories(args[1:])
        elif args[0].lower() in ('categorize', 'label'):
            categorize(args[1:])
        elif args[0].lower() in ('help',):
            print(help(args[1:]))
        else:
            print(GENERAL_HELP)
    except IndexError:
        print(term.red('Incorrect number of arguments provided'))
        if SHOW_TRACEBACK:
            raise
        else:
            print(GENERAL_HELP)
        sys.exit(1)
    except requests.exceptions.ConnectionError:
        print(
            term.red(
                f'Unable to connect to Vittlify instance at {VITTLIFY_URL}'))
        if PROXY:
            print(term.red(f'Attempted to use proxy at {PROXY}'))
        if SHOW_TRACEBACK:
            raise
        sys.exit(1)
    except requests.exceptions.HTTPError as e:
        print(term.red(f'Server responded with {e}'))
        if SHOW_TRACEBACK:
            raise
        sys.exit(1)
    except VittlifyError as e:
        print(term.red(f"{e}"))
        sys.exit(1)


def main():
    run(sys.argv[1:])


if __name__ == '__main__':
    main()
