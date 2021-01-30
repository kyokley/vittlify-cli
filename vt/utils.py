from __future__ import print_function
import textwrap
import os
import base64

from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import padding

from terminaltables import AsciiTable, BorderlessTable
from blessings import Terminal


term = Terminal()


class VittlifyError(Exception):
    pass


def print_table(data, title=None, quiet=False):
    if quiet:
        table_class = BorderlessTable
        title = None
    else:
        table_class = AsciiTable

    if data:
        table = table_class(data)
        if title:
            table.title = term.yellow(title)
        table.inner_heading_row_border = False
        print(table.table)
    else:
        print(term.red("No data found."))


def apply_strikethrough(string):
    return f'{term.dim}{string}{term.normal}'


def wrap_text(text, width=70):
    return '\n'.join([textwrap.fill(line,
                                    width=width,
                                    replace_whitespace=False)
                      for line in text.splitlines()])


def format_row(item,
               shopping_list=None,
               include_comments=False,
               include_category=False):
    # Name + GUID plus cateory and comments if those are included defines the
    # number of columns for display.
    num_columns = sum([
        2, include_category, include_comments])
    wrap_width = min(int((term.width - 8)/num_columns), 70)
    row = []

    comments = item.get('comments')
    category = item.get('category_name') or 'None'

    if comments:
        name = '+ %s' % item['name']
    else:
        name = '  %s' % item['name']
    name = wrap_text(name, width=wrap_width)

    if item.get('done'):
        guid = term.blue(apply_strikethrough(item['guid'][:8]))
        name = term.magenta(apply_strikethrough(name))
        if comments:
            comments = apply_strikethrough(comments)

        if category:
            category = apply_strikethrough(category)
    else:
        guid = term.blue(item['guid'][:8])
        name = term.magenta(name)

    if include_category and shopping_list and shopping_list['categories']:
        row.extend([guid, category, name])
    else:
        row.extend([guid, name])

    if include_comments and comments:
        comments = wrap_text(comments, width=wrap_width)
        row.append(comments)
    return row


def get_encoded_signature(message):
    PRIVATE_KEY_FILENAME = (os.environ.get('VT_PRIVATE_KEY') or
                            os.path.expanduser('~/.ssh/id_rsa')
                            )

    try:
        with open(PRIVATE_KEY_FILENAME, 'rb') as f:
            PRIVATE_KEY = f.read()
    except IOError:
        raise VittlifyError(
            f'Could not find private key at {PRIVATE_KEY_FILENAME}'
        )

    rsaObj = serialization.load_pem_private_key(
        PRIVATE_KEY,
        None,
        default_backend())

    signature = rsaObj.sign(message,
                            padding.PSS(mgf=padding.MGF1(hashes.SHA512()),
                                        salt_length=padding.PSS.MAX_LENGTH),
                            hashes.SHA512())
    return base64.b64encode(signature)


def parse_options(raw_options):
    options = {}
    for val in raw_options:
        arg = val.strip()
        if arg.startswith('--'):
            if arg == '--extended':
                options['extended'] = True
            elif arg == '--quiet':
                options['quiet'] = True
            elif arg == '--unfinished':
                options['unfinished'] = True
            elif arg == '--categories':
                options['include_category'] = True
            elif arg == '--append':
                options['append'] = True
            elif arg == '--delete':
                options['delete'] = True
        elif arg.startswith('-'):
            if 'e' in arg:
                options['extended'] = True

            if 'q' in arg:
                options['quiet'] = True

            if 'u' in arg:
                options['unfinished'] = True

            if 'c' in arg:
                options['include_category'] = True

            if 'a' in arg:
                options['append'] = True

            if 'd' in arg:
                options['delete'] = True

    return options
