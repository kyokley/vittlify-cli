import shlex
import unittest
import mock
import requests
import pytest

from vt.vt import (display_shopping_list,
                   display_item,
                   display_all_shopping_lists,
                   display_shopping_list_categories,
                   Status,
                   show,
                   complete,
                   modify,
                   add,
                   move,
                   run,
                   categories,
                   help,
                   term,
                   )

from vt.utils import VittlifyError


class TestDisplayShoppingList(unittest.TestCase):
    def setUp(self):
        self.get_shopping_list_info_patcher = mock.patch('vt.vt.get_shopping_list_info')
        self.mock_get_shopping_list_info = self.get_shopping_list_info_patcher.start()

        self.get_shopping_list_items_patcher = mock.patch('vt.vt.get_shopping_list_items')
        self.mock_get_shopping_list_items = self.get_shopping_list_items_patcher.start()

        self.get_completed_patcher = mock.patch('vt.vt.get_completed')
        self.mock_get_completed = self.get_completed_patcher.start()

        self.get_all_shopping_list_items_patcher = mock.patch('vt.vt.get_all_shopping_list_items')
        self.mock_get_all_shopping_list_items = self.get_all_shopping_list_items_patcher.start()

        self.format_row_patcher = mock.patch('vt.vt.format_row')
        self.mock_format_row = self.format_row_patcher.start()

        self.print_table_patcher = mock.patch('vt.vt.print_table')
        self.mock_print_table = self.print_table_patcher.start()

        test_shopping_list = {'name': 'test_list'}
        self.mock_get_shopping_list_info.return_value = test_shopping_list

        test_items = [{'name': 'item1'},
                      {'name': 'item2'},
                      {'name': 'item3'},
                      ]

        self.mock_get_shopping_list_items.return_value = test_items
        self.mock_get_all_shopping_list_items.return_value = test_items
        self.mock_get_completed.return_value = test_items

        self.mock_format_row.side_effect = ['formatted_row_1',
                                            'formatted_row_2',
                                            'formatted_row_3']

    def tearDown(self):
        self.get_shopping_list_info_patcher.stop()
        self.get_shopping_list_items_patcher.stop()
        self.get_completed_patcher.stop()
        self.get_all_shopping_list_items_patcher.stop()
        self.format_row_patcher.stop()
        self.print_table_patcher.stop()

    def test_not_completed(self):
        guid = 'test_guid'
        display_shopping_list(guid=guid, mode=Status.NOT_COMPLETED)

        self.mock_get_shopping_list_info.assert_called_once_with(guid)
        self.mock_get_shopping_list_items.assert_called_once_with(guid)
        self.mock_format_row.assert_has_calls([mock.call({'name': 'item1'}, {'name': 'test_list'}, include_category=False, include_comments=False, no_wrap=False),
                                               mock.call({'name': 'item2'}, {'name': 'test_list'}, include_category=False, include_comments=False, no_wrap=False),
                                               mock.call({'name': 'item3'}, {'name': 'test_list'}, include_category=False, include_comments=False, no_wrap=False)])
        self.mock_print_table.assert_called_once_with(['formatted_row_1',
                                                       'formatted_row_2',
                                                       'formatted_row_3'], title='test_list', quiet=False)

    def test_all(self):
        guid = 'test_guid'
        display_shopping_list(guid=guid, mode=Status.ALL)

        self.mock_get_shopping_list_info.assert_called_once_with(guid)
        self.mock_get_all_shopping_list_items.assert_called_once_with(guid)
        self.mock_format_row.assert_has_calls([mock.call({'name': 'item1'}, {'name': 'test_list'}, include_category=False, include_comments=False, no_wrap=False),
                                               mock.call({'name': 'item2'}, {'name': 'test_list'}, include_category=False, include_comments=False, no_wrap=False),
                                               mock.call({'name': 'item3'}, {'name': 'test_list'}, include_category=False, include_comments=False, no_wrap=False)])
        self.mock_print_table.assert_called_once_with(['formatted_row_1',
                                                       'formatted_row_2',
                                                       'formatted_row_3'], title='test_list', quiet=False)

    def test_completed(self):
        guid = 'test_guid'
        display_shopping_list(guid=guid, mode=Status.COMPLETED)

        self.assertFalse(self.mock_get_shopping_list_info.called)
        self.mock_get_completed.assert_called_once_with()
        self.mock_format_row.assert_has_calls([mock.call({'name': 'item1'}, None, include_category=False, include_comments=False, no_wrap=False),
                                               mock.call({'name': 'item2'}, None, include_category=False, include_comments=False, no_wrap=False),
                                               mock.call({'name': 'item3'}, None, include_category=False, include_comments=False, no_wrap=False)])
        self.mock_print_table.assert_called_once_with(['formatted_row_1',
                                                       'formatted_row_2',
                                                       'formatted_row_3'], title='Recently Completed', quiet=False)

    def test_not_completed_extended(self):
        guid = 'test_guid'
        display_shopping_list(guid=guid, mode=Status.NOT_COMPLETED, extended=True)

        self.mock_get_shopping_list_info.assert_called_once_with(guid)
        self.mock_get_shopping_list_items.assert_called_once_with(guid)
        self.mock_format_row.assert_has_calls([mock.call({'name': 'item1'}, {'name': 'test_list'}, include_category=False, include_comments=True, no_wrap=False),
                                               mock.call({'name': 'item2'}, {'name': 'test_list'}, include_category=False, include_comments=True, no_wrap=False),
                                               mock.call({'name': 'item3'}, {'name': 'test_list'}, include_category=False, include_comments=True, no_wrap=False)])
        self.mock_print_table.assert_called_once_with(['formatted_row_1',
                                                       'formatted_row_2',
                                                       'formatted_row_3'], title='test_list', quiet=False)

    def test_all_extended(self):
        guid = 'test_guid'
        display_shopping_list(guid=guid, mode=Status.ALL, extended=True)

        self.mock_get_shopping_list_info.assert_called_once_with(guid)
        self.mock_get_all_shopping_list_items.assert_called_once_with(guid)
        self.mock_format_row.assert_has_calls([mock.call({'name': 'item1'}, {'name': 'test_list'}, include_category=False, include_comments=True, no_wrap=False),
                                               mock.call({'name': 'item2'}, {'name': 'test_list'}, include_category=False, include_comments=True, no_wrap=False),
                                               mock.call({'name': 'item3'}, {'name': 'test_list'}, include_category=False, include_comments=True, no_wrap=False)])
        self.mock_print_table.assert_called_once_with(['formatted_row_1',
                                                       'formatted_row_2',
                                                       'formatted_row_3'], title='test_list', quiet=False)

    def test_completed_extended(self):
        guid = 'test_guid'
        display_shopping_list(guid=guid, mode=Status.COMPLETED, extended=True)

        self.assertFalse(self.mock_get_shopping_list_info.called)
        self.mock_get_completed.assert_called_once_with()
        self.mock_format_row.assert_has_calls([mock.call({'name': 'item1'}, None, include_category=False, include_comments=True, no_wrap=False),
                                               mock.call({'name': 'item2'}, None, include_category=False, include_comments=True, no_wrap=False),
                                               mock.call({'name': 'item3'}, None, include_category=False, include_comments=True, no_wrap=False)])
        self.mock_print_table.assert_called_once_with(['formatted_row_1',
                                                       'formatted_row_2',
                                                       'formatted_row_3'], title='Recently Completed', quiet=False)


class TestDisplayItem(unittest.TestCase):
    def setUp(self):
        self.get_item_patcher = mock.patch('vt.vt.get_item')
        self.mock_get_item = self.get_item_patcher.start()

        self.format_row_patcher = mock.patch('vt.vt.format_row')
        self.mock_format_row = self.format_row_patcher.start()

        self.print_table_patcher = mock.patch('vt.vt.print_table')
        self.mock_print_table = self.print_table_patcher.start()

        self.test_guid = 'test_guid'

    def tearDown(self):
        self.get_item_patcher.stop()
        self.format_row_patcher.stop()
        self.print_table_patcher.stop()

    def test_(self):
        display_item(self.test_guid)
        self.mock_get_item.assert_called_once_with(self.test_guid)
        self.mock_format_row.assert_called_once_with(self.mock_get_item.return_value, None, include_comments=True, no_wrap=False)
        self.mock_print_table.assert_called_once_with([self.mock_format_row.return_value])

class TestDisplayAllShoppingLists(unittest.TestCase):
    def setUp(self):
        self.get_all_shopping_lists_patcher = mock.patch('vt.vt.get_all_shopping_lists')
        self.mock_get_all_shopping_lists = self.get_all_shopping_lists_patcher.start()

        self.format_row_patcher = mock.patch('vt.vt.format_row')
        self.mock_format_row = self.format_row_patcher.start()

        self.print_table_patcher = mock.patch('vt.vt.print_table')
        self.mock_print_table = self.print_table_patcher.start()

        self.mock_get_all_shopping_lists.return_value = [{'name': 'list1'},
                                                         {'name': 'list2'},
                                                         {'name': 'list3'},]

        self.mock_format_row.side_effect = ['formatted_row_1',
                                            'formatted_row_2',
                                            'formatted_row_3']

    def tearDown(self):
        self.get_all_shopping_lists_patcher.stop()
        self.format_row_patcher.stop()

    def test_(self):
        display_all_shopping_lists()
        self.mock_get_all_shopping_lists.assert_called_once_with()
        self.mock_format_row.assert_has_calls([mock.call({'name': 'list1'}, None, no_wrap=False),
                                               mock.call({'name': 'list2'}, None, no_wrap=False),
                                               mock.call({'name': 'list3'}, None, no_wrap=False),])
        self.mock_print_table.assert_called_once_with(['formatted_row_1',
                                                       'formatted_row_2',
                                                       'formatted_row_3'],
                                                      title='All Lists')

class TestShowNoDefaultList(unittest.TestCase):
    def setUp(self):
        self.DEFAULT_LIST_patcher = mock.patch('vt.vt.DEFAULT_LIST', '')
        self.DEFAULT_LIST_patcher.start()

        self.display_shopping_list_patcher = mock.patch('vt.vt.display_shopping_list')
        self.mock_display_shopping_list = self.display_shopping_list_patcher.start()

        self.display_all_shopping_lists_patcher = mock.patch('vt.vt.display_all_shopping_lists')
        self.mock_display_all_shopping_lists = self.display_all_shopping_lists_patcher.start()

        self.display_item_patcher = mock.patch('vt.vt.display_item')
        self.mock_display_item = self.display_item_patcher.start()

    def tearDown(self):
        self.DEFAULT_LIST_patcher.stop()
        self.display_shopping_list_patcher.stop()
        self.display_all_shopping_lists_patcher.stop()
        self.display_item_patcher.stop()

    def test_list_empty_guid(self):
        args = shlex.split("list ''")
        self.assertRaises(IndexError,
                          show,
                          args)

    def test_list_no_guid(self):
        args = shlex.split("list")
        self.assertRaises(IndexError,
                          show,
                          args)

    def test_list_empty_guid_extended(self):
        args = shlex.split("list '' -e")
        self.assertRaises(IndexError,
                          show,
                          args)

    def test_list_no_guid_extended(self):
        args = shlex.split("list -e")
        self.assertRaises(IndexError,
                          show,
                          args)

    def test_list_no_extended(self):
        args = shlex.split("list test_guid")
        show(args)

        self.mock_display_shopping_list.assert_called_once_with(guid='test_guid')

    def test_list_extended(self):
        args = shlex.split("list test_guid -e")
        show(args)

        self.mock_display_shopping_list.assert_called_once_with(guid='test_guid',
                                                                extended=True,
                                                                )

    def test_lists(self):
        args = shlex.split("lists")
        show(args)

        self.mock_display_all_shopping_lists.assert_called_once_with()

    def test_item_no_guid(self):
        args = shlex.split("item")
        self.assertRaises(IndexError,
                          show,
                          args)

    def test_item_empty_guid(self):
        args = shlex.split("item ''")
        self.assertRaises(IndexError,
                          show,
                          args)

    def test_item(self):
        args = shlex.split("item test_guid")
        show(args)

        self.mock_display_item.assert_called_once_with('test_guid')


class TestShowDefaultList:
    @pytest.fixture(autouse=True)
    def setUp(self, mocker):
        self.DEFAULT_LIST_patcher = mock.patch('vt.vt.DEFAULT_LIST', 'default_list')
        self.DEFAULT_LIST_patcher.start()

        self.parse_options_patcher = mock.patch('vt.vt.parse_options')
        self.mock_parse_options = self.parse_options_patcher.start()

        self.display_shopping_list_patcher = mock.patch('vt.vt.display_shopping_list')
        self.mock_display_shopping_list = self.display_shopping_list_patcher.start()

        self.display_all_shopping_lists_patcher = mock.patch('vt.vt.display_all_shopping_lists')
        self.mock_display_all_shopping_lists = self.display_all_shopping_lists_patcher.start()

        self.display_shopping_list_categories_patcher = mock.patch('vt.vt.display_shopping_list_categories')
        self.mock_display_shopping_list_categories = self.display_shopping_list_categories_patcher.start()

        mocker.patch.object(term, 'red', autospec=True)

        self.display_item_patcher = mock.patch('vt.vt.display_item')
        self.mock_display_item = self.display_item_patcher.start()

        self.mock_parse_options.return_value = {}

        yield
        self.DEFAULT_LIST_patcher.stop()
        self.parse_options_patcher.stop()
        self.display_shopping_list_patcher.stop()
        self.display_all_shopping_lists_patcher.stop()
        self.display_item_patcher.stop()
        self.display_shopping_list_categories_patcher.stop()

    def test_list_empty_guid(self):
        args = shlex.split("list ''")
        show(args)

        self.mock_display_shopping_list.assert_called_once_with(guid='default_list')

    def test_list_no_guid(self):
        args = shlex.split("list")
        show(args)

        self.mock_display_shopping_list.assert_called_once_with(guid='default_list')

    def test_list_empty_guid_extended(self):
        self.mock_parse_options.return_value = {'extended': True}

        args = shlex.split("list '' -e")
        show(args)

        self.mock_display_shopping_list.assert_called_once_with(guid='default_list', extended=True)

    def test_list_no_guid_extended(self):
        self.mock_parse_options.return_value = {'extended': True}

        args = shlex.split("list -e")
        show(args)

        self.mock_display_shopping_list.assert_called_once_with(guid='default_list', extended=True)

    def test_list_no_extended(self):
        args = shlex.split("list test_guid")
        show(args)

        self.mock_display_shopping_list.assert_called_once_with(guid='test_guid')

    def test_list_extended(self):
        self.mock_parse_options.return_value = {'extended': True}

        args = shlex.split("list test_guid -e")
        show(args)

        self.mock_display_shopping_list.assert_called_once_with(guid='test_guid',
                                                                extended=True,
                                                                )

    def test_lists(self):
        args = shlex.split("lists")
        show(args)

        self.mock_display_all_shopping_lists.assert_called_once_with()

    def test_item_no_guid(self):
        args = shlex.split("item")
        with pytest.raises(IndexError):
            show(args)

    def test_item_empty_guid(self):
        args = shlex.split("item ''")
        with pytest.raises(IndexError):
            show(args)

    def test_item(self):
        args = shlex.split("item test_guid")
        show(args)

        self.mock_display_item.assert_called_once_with('test_guid')

    def test_display_list_categories(self):
        self.mock_parse_options.return_value = {'categories': [{'name': 'type A'},
                                                               {'name': 'type B'}]}

        args = shlex.split("test_guid")
        categories(args)

        self.mock_display_shopping_list_categories.assert_called_once_with('test_guid')

    def test_display_list_categories_raises(self):
        self.mock_parse_options.return_value = {'categories': [{'name': 'type A'},
                                                               {'name': 'type B'}]}
        self.mock_display_shopping_list_categories.side_effect = VittlifyError('Got an error')

        args = shlex.split("test_guid")
        categories(args)

        term.red.assert_called_once_with('Got an error')
        self.mock_display_shopping_list_categories.assert_called_once_with('test_guid')

    def test_display_shopping_list_raises(self):
        self.mock_display_shopping_list.side_effect = VittlifyError('Got an error')

        args = shlex.split("list test_guid")
        show(args)

        term.red.assert_called_once_with('Got an error')
        self.mock_display_shopping_list.assert_called_once_with(guid='test_guid')

    def test_display_item_raises(self):
        self.mock_display_item.side_effect = VittlifyError('Got an error')

        args = shlex.split("show test_guid")
        show(args)

        term.red.assert_called_once_with('Got an error')

    def test_display_all_shopping_lists_raises(self):
        self.mock_display_all_shopping_lists.side_effect = VittlifyError('Got an error')
        args = shlex.split("lists")
        show(args)

        self.mock_display_all_shopping_lists.assert_called_once_with()
        term.red.assert_called_once_with('Got an error')


class TestComplete:
    @pytest.fixture(autouse=True)
    def setUp(self, mocker):
        self.complete_item_patcher = mock.patch('vt.vt.complete_item')
        self.mock_complete_item = self.complete_item_patcher.start()

        self.mock_print = mocker.patch('builtins.print')

        self.display_shopping_list_patcher = mock.patch('vt.vt.display_shopping_list')
        self.mock_display_shopping_list = self.display_shopping_list_patcher.start()

        self.apply_strikethrough_patcher = mock.patch('vt.vt.apply_strikethrough')
        self.mock_apply_strikethrough = self.apply_strikethrough_patcher.start()

        self.mock_complete_item.return_value = {'name': 'test_name'}
        self.mock_apply_strikethrough.return_value = 'struck_through'

        yield

        self.complete_item_patcher.stop()
        self.apply_strikethrough_patcher.stop()

    def test_complete(self):
        args = shlex.split("test_guid")
        complete(args)

        self.mock_complete_item.assert_called_once_with('test_guid',
                                                        uncomplete=False)
        self.mock_apply_strikethrough.assert_called_once_with('test_name')
        self.mock_print.assert_called_once_with(f'Marked {term.magenta}struck_through{term.normal} as done.')

    def test_uncomplete(self):
        args = shlex.split("test_guid")
        complete(args, uncomplete=True)

        self.mock_complete_item.assert_called_once_with('test_guid',
                                                        uncomplete=True)
        self.mock_print.assert_called_once_with(f'Marked {term.magenta}test_name{term.normal} undone.')

    def test_done_extended(self):
        args = shlex.split("-e")
        complete(args)

        self.mock_display_shopping_list.assert_called_once_with(extended=True,
                                                                mode=Status.COMPLETED)

    def test_completed_no_extended(self):
        args = shlex.split("")
        complete(args)

        self.mock_display_shopping_list.assert_called_once_with(mode=Status.COMPLETED)

    def test_completed_extended(self):
        args = shlex.split("--extended")
        complete(args)

        self.mock_display_shopping_list.assert_called_once_with(extended=True, mode=Status.COMPLETED)


class TestModify(unittest.TestCase):
    def setUp(self):
        self.modify_item_patcher = mock.patch('vt.vt.modify_item')
        self.mock_modify_item = self.modify_item_patcher.start()

        self.display_item_patcher = mock.patch('vt.vt.display_item')
        self.mock_display_item = self.display_item_patcher.start()

    def tearDown(self):
        self.modify_item_patcher.stop()
        self.display_item_patcher.stop()

    def test_no_options(self):
        args = shlex.split("test_guid this is a comment")
        modify(args)
        self.mock_modify_item.assert_called_once_with('test_guid',
                                                      'this is a comment')
        self.mock_display_item.assert_called_once_with('test_guid')

    def test_with_short_options(self):
        args = shlex.split("test_guid -a this is a comment")
        modify(args)
        self.mock_modify_item.assert_called_once_with('test_guid',
                                                      'this is a comment',
                                                      append=True)
        self.mock_display_item.assert_called_once_with('test_guid')

    def test_with_options(self):
        args = shlex.split("test_guid --append this is a comment")
        modify(args)
        self.mock_modify_item.assert_called_once_with('test_guid',
                                                      'this is a comment',
                                                      append=True)
        self.mock_display_item.assert_called_once_with('test_guid')


class TestAddDefaultList(unittest.TestCase):
    def setUp(self):
        self.DEFAULT_LIST_patcher = mock.patch('vt.vt.DEFAULT_LIST', 'default_list')
        self.DEFAULT_LIST_patcher.start()

        self.add_item_patcher = mock.patch('vt.vt.add_item')
        self.mock_add_item = self.add_item_patcher.start()

        self.format_row_patcher = mock.patch('vt.vt.format_row')
        self.mock_format_row = self.format_row_patcher.start()

        self.print_table_patcher = mock.patch('vt.vt.print_table')
        self.mock_print_table = self.print_table_patcher.start()

    def tearDown(self):
        self.add_item_patcher.stop()
        self.DEFAULT_LIST_patcher.stop()
        self.format_row_patcher.stop()
        self.print_table_patcher.stop()

    def test_no_guid(self):
        args = shlex.split("'this is a new item'")
        add(args)
        self.mock_add_item.assert_called_once_with('default_list', 'this is a new item')
        self.mock_format_row.assert_called_once_with(self.mock_add_item.return_value, no_wrap=False)
        self.mock_print_table.assert_called_once_with([self.mock_format_row.return_value])

    def test_with_guid(self):
        args = shlex.split("test_guid 'this is a new item'")
        add(args)
        self.mock_add_item.assert_called_once_with('test_guid', 'this is a new item')
        self.mock_format_row.assert_called_once_with(self.mock_add_item.return_value, no_wrap=False)
        self.mock_print_table.assert_called_once_with([self.mock_format_row.return_value])


class TestAddNoDefaultList(unittest.TestCase):
    def setUp(self):
        self.DEFAULT_LIST_patcher = mock.patch('vt.vt.DEFAULT_LIST', None)
        self.DEFAULT_LIST_patcher.start()

        self.add_item_patcher = mock.patch('vt.vt.add_item')
        self.mock_add_item = self.add_item_patcher.start()

        self.format_row_patcher = mock.patch('vt.vt.format_row')
        self.mock_format_row = self.format_row_patcher.start()

        self.print_table_patcher = mock.patch('vt.vt.print_table')
        self.mock_print_table = self.print_table_patcher.start()

    def tearDown(self):
        self.add_item_patcher.stop()
        self.DEFAULT_LIST_patcher.stop()
        self.format_row_patcher.stop()
        self.print_table_patcher.stop()

    def test_no_guid(self):
        args = shlex.split("'this is a new item'")
        self.assertRaises(IndexError,
                          add,
                          args)

    def test_with_guid(self):
        args = shlex.split("test_guid 'this is a new item'")
        add(args)
        self.mock_add_item.assert_called_once_with('test_guid', 'this is a new item')
        self.mock_format_row.assert_called_once_with(self.mock_add_item.return_value, no_wrap=False)
        self.mock_print_table.assert_called_once_with([self.mock_format_row.return_value])


class TestMove:
    @pytest.fixture(autouse=True)
    def setUp(self, mocker):
        self.move_item_patcher = mock.patch('vt.vt.move_item')
        self.mock_move_item = self.move_item_patcher.start()

        self.mock_print = mocker.patch('builtins.print')

        yield
        self.move_item_patcher.stop()

    def test_(self):
        args = shlex.split('test_guid to_list_guid')
        move(args)
        self.mock_move_item.assert_called_once_with('test_guid', 'to_list_guid')
        self.mock_print.assert_called_once_with(f'Moved item {term.blue}test_guid{term.normal} to list {term.blue}to_list_guid{term.normal}')


class TestRun:
    @pytest.fixture(autouse=True)
    def setUp(self, mocker):
        self.show_patcher = mock.patch('vt.vt.show')
        self.mock_show = self.show_patcher.start()

        self.complete_patcher = mock.patch('vt.vt.complete')
        self.mock_complete = self.complete_patcher.start()

        self.modify_patcher = mock.patch('vt.vt.modify')
        self.mock_modify = self.modify_patcher.start()

        self.add_patcher = mock.patch('vt.vt.add')
        self.mock_add = self.add_patcher.start()

        self.move_patcher = mock.patch('vt.vt.move')
        self.mock_move = self.move_patcher.start()

        mocker.patch.object(term, 'red', autospec=True)

        self.SHOW_TRACEBACK_patcher = mock.patch('vt.vt.SHOW_TRACEBACK', False)
        self.SHOW_TRACEBACK_patcher.start()

        self.PROXY_patcher = mock.patch('vt.vt.PROXY', False)
        self.PROXY_patcher.start()

        self.VITTLIFY_URL_patcher = mock.patch('vt.vt.VITTLIFY_URL', 'vittlify_url')
        self.VITTLIFY_URL_patcher.start()

        self.help_patcher = mock.patch('vt.vt.help')
        self.mock_help = self.help_patcher.start()

        yield
        self.show_patcher.stop()
        self.complete_patcher.stop()
        self.modify_patcher.stop()
        self.add_patcher.stop()
        self.move_patcher.stop()
        self.SHOW_TRACEBACK_patcher.stop()
        self.PROXY_patcher.stop()
        self.VITTLIFY_URL_patcher.stop()
        self.help_patcher.stop()

    def test_list(self):
        test_args = shlex.split('list test_guid')
        run(test_args)
        self.mock_show.assert_called_once_with(test_args)
        assert not self.mock_complete.called
        assert not self.mock_modify.called
        assert not self.mock_add.called
        assert not self.mock_move.called
        assert not self.mock_help.called

    def test_lists(self):
        test_args = shlex.split('lists')
        run(test_args)
        self.mock_show.assert_called_once_with(test_args)
        assert not self.mock_complete.called
        assert not self.mock_modify.called
        assert not self.mock_add.called
        assert not self.mock_move.called
        assert not self.mock_help.called

    def test_item(self):
        test_args = shlex.split('item test_guid')
        run(test_args)
        self.mock_show.assert_called_once_with(test_args)
        assert not self.mock_complete.called
        assert not self.mock_modify.called
        assert not self.mock_add.called
        assert not self.mock_move.called
        assert not self.mock_help.called

    def test_show(self):
        test_args = shlex.split('show test_guid')
        run(test_args)
        self.mock_show.assert_called_once_with(test_args)
        assert not self.mock_complete.called
        assert not self.mock_modify.called
        assert not self.mock_add.called
        assert not self.mock_move.called
        assert not self.mock_help.called

    def test_done(self):
        test_args = shlex.split('done test_guid')
        expected = ['test_guid']
        run(test_args)
        assert not self.mock_show.called
        self.mock_complete.assert_called_once_with(expected)
        assert not self.mock_modify.called
        assert not self.mock_add.called
        assert not self.mock_move.called
        assert not self.mock_help.called

    def test_complete(self):
        test_args = shlex.split('complete test_guid')
        expected = ['test_guid']
        run(test_args)
        assert not self.mock_show.called
        self.mock_complete.assert_called_once_with(expected)
        assert not self.mock_modify.called
        assert not self.mock_add.called
        assert not self.mock_move.called
        assert not self.mock_help.called

    def test_undone(self):
        test_args = shlex.split('undone test_guid')
        expected = ['test_guid']
        run(test_args)
        assert not self.mock_show.called
        self.mock_complete.assert_called_once_with(expected, uncomplete=True)
        assert not self.mock_modify.called
        assert not self.mock_add.called
        assert not self.mock_move.called
        assert not self.mock_help.called

    def test_uncomplete(self):
        test_args = shlex.split('uncomplete test_guid')
        expected = ['test_guid']
        run(test_args)
        assert not self.mock_show.called
        self.mock_complete.assert_called_once_with(expected, uncomplete=True)
        assert not self.mock_modify.called
        assert not self.mock_add.called
        assert not self.mock_move.called
        assert not self.mock_help.called

    def test_modify(self):
        test_args = shlex.split("modify test_guid 'these are comments'")
        expected = ['test_guid', 'these are comments']
        run(test_args)
        assert not self.mock_show.called
        assert not self.mock_complete.called
        self.mock_modify.assert_called_once_with(expected)
        assert not self.mock_add.called
        assert not self.mock_move.called
        assert not self.mock_help.called

    def test_edit(self):
        test_args = shlex.split("edit test_guid 'these are comments'")
        expected = ['test_guid', 'these are comments']
        run(test_args)
        assert not self.mock_show.called
        assert not self.mock_complete.called
        self.mock_modify.assert_called_once_with(expected)
        assert not self.mock_add.called
        assert not self.mock_move.called
        assert not self.mock_help.called

    def test_comment(self):
        test_args = shlex.split("comment test_guid 'these are comments'")
        expected = ['test_guid', 'these are comments']
        run(test_args)
        assert not self.mock_show.called
        assert not self.mock_complete.called
        self.mock_modify.assert_called_once_with(expected)
        assert not self.mock_add.called
        assert not self.mock_move.called
        assert not self.mock_help.called

    def test_comments(self):
        test_args = shlex.split("comments test_guid 'these are comments'")
        expected = ['test_guid', 'these are comments']
        run(test_args)
        assert not self.mock_show.called
        assert not self.mock_complete.called
        self.mock_modify.assert_called_once_with(expected)
        assert not self.mock_add.called
        assert not self.mock_move.called
        assert not self.mock_help.called

    def test_add(self):
        test_args = shlex.split("add 'this is a new item'")
        expected = ['this is a new item']
        run(test_args)
        assert not self.mock_show.called
        assert not self.mock_complete.called
        assert not self.mock_modify.called
        self.mock_add.assert_called_once_with(expected)
        assert not self.mock_move.called
        assert not self.mock_help.called

    def test_move(self):
        test_args = shlex.split("move old_guid new_guid")
        expected = ['old_guid', 'new_guid']
        run(test_args)
        assert not self.mock_show.called
        assert not self.mock_complete.called
        assert not self.mock_modify.called
        assert not self.mock_add.called
        assert not self.mock_help.called
        self.mock_move.assert_called_once_with(expected)

    def test_mv(self):
        test_args = shlex.split("mv old_guid new_guid")
        expected = ['old_guid', 'new_guid']
        run(test_args)
        assert not self.mock_show.called
        assert not self.mock_complete.called
        assert not self.mock_modify.called
        assert not self.mock_add.called
        assert not self.mock_help.called
        self.mock_move.assert_called_once_with(expected)

    def test_index_error(self):
        self.mock_add.side_effect = IndexError()

        test_args = shlex.split("add 'this is a new item'")
        with pytest.raises(SystemExit):
            run(test_args)
        term.red.assert_called_once_with('Incorrect number of arguments provided')

    def test_connection_error(self):
        self.mock_add.side_effect = requests.exceptions.ConnectionError()

        test_args = shlex.split("add 'this is a new item'")
        with pytest.raises(SystemExit):
            run(test_args)
        term.red.assert_called_once_with('Unable to connect to Vittlify instance at vittlify_url')

    def test_http_error(self):
        self.mock_add.side_effect = requests.exceptions.HTTPError('500 Message')

        test_args = shlex.split("add 'this is a new item'")
        with pytest.raises(SystemExit):
            run(test_args)
        term.red.assert_called_once_with('Server responded with 500 Message')

    def test_help(self):
        test_args = shlex.split("help command")
        expected = ['command']
        run(test_args)
        assert not self.mock_show.called
        assert not self.mock_complete.called
        assert not self.mock_modify.called
        assert not self.mock_add.called
        assert not self.mock_move.called
        self.mock_help.assert_called_once_with(expected)


class TestDisplayShoppingListCategories:
    @pytest.fixture(autouse=True)
    def setUp(self, mocker):
        self.get_shopping_list_info_patcher = mock.patch('vt.vt.get_shopping_list_info')
        self.mock_get_shopping_list_info = self.get_shopping_list_info_patcher.start()

        self.print_table_patcher = mock.patch('vt.vt.print_table')
        self.mock_print_table = self.print_table_patcher.start()

        mocker.patch.object(term, 'red', autospec=True)

        self.mock_get_shopping_list_info.return_value = {'name': 'test_list'}

        yield
        self.get_shopping_list_info_patcher.stop()
        self.print_table_patcher.stop()

    def test_no_categories(self):
        display_shopping_list_categories('test_guid')
        self.mock_get_shopping_list_info.assert_called_once_with('test_guid')

        term.red.assert_called_once_with("No categories found for test_list.")

    def test_has_categories(self):
        self.mock_get_shopping_list_info.return_value = {'name': 'test_list',
                                                         'categories': [{'name': 'type A'},
                                                                        {'name': 'type B'},
                                                                        ],
                                                         }

        display_shopping_list_categories('test_guid')
        self.mock_print_table.assert_called_once_with([['type A'], ['type B']],
                                                      title='test_list')


class TestHelp(unittest.TestCase):
    def setUp(self):
        self.general_help_patcher = mock.patch('vt.vt.GENERAL_HELP')
        self.mock_general_help = self.general_help_patcher.start()

        self.lists_help_patcher = mock.patch('vt.vt.LISTS_HELP')
        self.mock_lists_help = self.lists_help_patcher.start()

        self.list_help_patcher = mock.patch('vt.vt.LIST_HELP')
        self.mock_list_help = self.list_help_patcher.start()

        self.done_help_patcher = mock.patch('vt.vt.DONE_HELP')
        self.mock_done_help = self.done_help_patcher.start()

        self.undone_help_patcher = mock.patch('vt.vt.UNDONE_HELP')
        self.mock_undone_help = self.undone_help_patcher.start()

        self.comment_help_patcher = mock.patch('vt.vt.COMMENT_HELP')
        self.mock_comment_help = self.comment_help_patcher.start()

        self.move_help_patcher = mock.patch('vt.vt.MOVE_HELP')
        self.mock_move_help = self.move_help_patcher.start()

        self.categories_help_patcher = mock.patch('vt.vt.CATEGORIES_HELP')
        self.mock_categories_help = self.categories_help_patcher.start()

        self.categorize_help_patcher = mock.patch('vt.vt.CATEGORIZE_HELP')
        self.mock_categorize_help = self.categorize_help_patcher.start()

    def tearDown(self):
        self.general_help_patcher.stop()
        self.lists_help_patcher.stop()
        self.list_help_patcher.stop()
        self.done_help_patcher.stop()
        self.undone_help_patcher.stop()
        self.comment_help_patcher.stop()
        self.move_help_patcher.stop()
        self.categories_help_patcher.stop()
        self.categorize_help_patcher.stop()

    def test_no_args(self):
        expected = self.mock_general_help
        actual = help([])

        self.assertEqual(expected, actual)

    def test_unknown_command(self):
        expected = self.mock_general_help
        actual = help(['unknown command'])

        self.assertEqual(expected, actual)

    def test_lists(self):
        expected = self.mock_lists_help
        actual = help(['lists'])

        self.assertEqual(expected, actual)

    def test_list(self):
        expected = self.mock_list_help
        actual = help(['list'])

        self.assertEqual(expected, actual)

    def test_done(self):
        expected = self.mock_done_help
        actual = help(['done'])

        self.assertEqual(expected, actual)

    def test_complete(self):
        expected = self.mock_done_help
        actual = help(['complete'])

        self.assertEqual(expected, actual)

    def test_undone(self):
        expected = self.mock_undone_help
        actual = help(['undone'])

        self.assertEqual(expected, actual)

    def test_uncomplete(self):
        expected = self.mock_undone_help
        actual = help(['uncomplete'])

        self.assertEqual(expected, actual)

    def test_comment(self):
        expected = self.mock_comment_help
        actual = help(['comment'])

        self.assertEqual(expected, actual)

    def test_modify(self):
        expected = self.mock_comment_help
        actual = help(['modify'])

        self.assertEqual(expected, actual)

    def test_comments(self):
        expected = self.mock_comment_help
        actual = help(['comments'])

        self.assertEqual(expected, actual)

    def test_edit(self):
        expected = self.mock_comment_help
        actual = help(['edit'])

        self.assertEqual(expected, actual)

    def test_move(self):
        expected = self.mock_move_help
        actual = help(['move'])

        self.assertEqual(expected, actual)

    def test_mv(self):
        expected = self.mock_move_help
        actual = help(['mv'])

        self.assertEqual(expected, actual)

    def test_categories(self):
        expected = self.mock_categories_help
        actual = help(['categories'])

        self.assertEqual(expected, actual)

    def test_categorize(self):
        expected = self.mock_categorize_help
        actual = help(['categorize'])

        self.assertEqual(expected, actual)

    def test_label(self):
        expected = self.mock_categorize_help
        actual = help(['label'])

        self.assertEqual(expected, actual)
