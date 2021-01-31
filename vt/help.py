GENERAL_HELP = '''
Usage:
    vt <command> [options]

Commands:
    lists       Get all lists
    list        Return items of a specific list
    item        Return a specific item
    show        Alias for item
    done        Mark an item done
    complete    Alias for done
    undone      Mark an item undone
    uncomplete  Alias for undone
    modify      Modify item by providing a comment
    edit        Alias for modify
    comment     Alias for modify
    comments    Alias for modify
    add         Create a new item
    move        Associate an item with a new list
    mv          Alias for move
    categories  Return a list of valid categories for a given list
    categorize  Provide a category for a given item
    label       Alias for categorize
    help        Get help on a command
'''

LISTS_HELP = '''
Usage:
    vt lists

Description:
    Return all lists
'''

LIST_HELP = '''
Usage:
    vt list [GUID] [options]

Description:
    Return all items of a specified list. GUID may be either the unique identifier of
    a list or the name of the list if it is unique. If no GUID is provided, use the
    default list defined in the VT_DEFAULT_LIST environment variable.

Options:
    -e, --extended      Show extended information about items.
    -u, --unfinished    Only display items that have not been completed yet.
    -c, --categories    Include item categories in output.
    -q, --quiet         Quiet mode. Remove any extraneous output.
    -W, --no-wrap       Do not apply any text wrapping to output.
'''

DONE_HELP = '''
Usage:
    vt done [GUID] ...
    vt complete [GUID] ...

Description:
    Mark an item done. When run without a GUID, display all recently completed items.
'''

UNDONE_HELP = '''
Usage:
    vt undone [GUID] ...
    vt uncomplete [GUID] ...

Description:
    Mark an item undone. When run without a GUID, display all recently completed items.
'''

COMMENT_HELP = '''
Usage:
    vt modify GUID [options] [comment]
    vt comment GUID [options] [comment]
    vt comments GUID [options] [comment]
    vt edit GUID [options] [comment]

Description:
    Add a comment to the specified item. No comment should be provided when using the -d flag.

Options:
    -a, --append       Append comment rather than overwriting.
    -d, --delete       Remove comment from item.
'''

ADD_HELP = '''
Usage:
    vt add [GUID] item

Description:
    Create a new item. GUID is the unique identifier for the list the item will be placed on.
    When GUID is not provided, use the default list defined in VT_DEFAULT_LIST environment variable.
'''

MOVE_HELP = '''
Usage:
    vt move ITEM LIST
    vt mv ITEM LIST

Description:
    Move item to a new list where ITEM is the guid of the item and LIST is the guid of the new list.
'''

CATEGORIES_HELP = '''
Usage:
    vt categories [GUID]

Description:
    Display the available categories for a list. GUID is the unique identifier for a list.
    When GUID is not provided, use the default list defined in VT_DEFAULT_LIST environment variable.
'''

CATEGORIZE_HELP = '''
Usage:
    vt categorize GUID CATEGORY
    vt label GUID CATEGORY

Description:
    Assign CATEGORY to the item specified by GUID.
'''
