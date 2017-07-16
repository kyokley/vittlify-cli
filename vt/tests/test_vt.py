import shlex
import unittest
import mock
import requests

from vt.vt import (display_shopping_list,
                   display_item,
                   display_all_shopping_lists,
                   COMPLETED,
                   NOT_COMPLETED,
                   ALL,
                   show,
                   complete,
                   modify,
                   add,
                   move,
                   run,
                   )

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
        display_shopping_list(guid=guid, mode=NOT_COMPLETED)

        self.mock_get_shopping_list_info.assert_called_once_with(guid)
        self.mock_get_shopping_list_items.assert_called_once_with(guid)
        self.mock_format_row.assert_has_calls([mock.call({'name': 'item1'}, include_comments=False),
                                               mock.call({'name': 'item2'}, include_comments=False),
                                               mock.call({'name': 'item3'}, include_comments=False)])
        self.mock_print_table.assert_called_once_with(['formatted_row_1',
                                                       'formatted_row_2',
                                                       'formatted_row_3'], title='test_list')

    def test_all(self):
        guid = 'test_guid'
        display_shopping_list(guid=guid, mode=ALL)

        self.mock_get_shopping_list_info.assert_called_once_with(guid)
        self.mock_get_all_shopping_list_items.assert_called_once_with(guid)
        self.mock_format_row.assert_has_calls([mock.call({'name': 'item1'}, include_comments=False),
                                               mock.call({'name': 'item2'}, include_comments=False),
                                               mock.call({'name': 'item3'}, include_comments=False)])
        self.mock_print_table.assert_called_once_with(['formatted_row_1',
                                                       'formatted_row_2',
                                                       'formatted_row_3'], title='test_list')

    def test_completed(self):
        guid = 'test_guid'
        display_shopping_list(guid=guid, mode=COMPLETED)

        self.assertFalse(self.mock_get_shopping_list_info.called)
        self.mock_get_completed.assert_called_once_with()
        self.mock_format_row.assert_has_calls([mock.call({'name': 'item1'}, include_comments=False),
                                               mock.call({'name': 'item2'}, include_comments=False),
                                               mock.call({'name': 'item3'}, include_comments=False)])
        self.mock_print_table.assert_called_once_with(['formatted_row_1',
                                                       'formatted_row_2',
                                                       'formatted_row_3'], title='Recently Completed')

    def test_not_completed_extended(self):
        guid = 'test_guid'
        display_shopping_list(guid=guid, mode=NOT_COMPLETED, extended=True)

        self.mock_get_shopping_list_info.assert_called_once_with(guid)
        self.mock_get_shopping_list_items.assert_called_once_with(guid)
        self.mock_format_row.assert_has_calls([mock.call({'name': 'item1'}, include_comments=True),
                                               mock.call({'name': 'item2'}, include_comments=True),
                                               mock.call({'name': 'item3'}, include_comments=True)])
        self.mock_print_table.assert_called_once_with(['formatted_row_1',
                                                       'formatted_row_2',
                                                       'formatted_row_3'], title='test_list')

    def test_all_extended(self):
        guid = 'test_guid'
        display_shopping_list(guid=guid, mode=ALL, extended=True)

        self.mock_get_shopping_list_info.assert_called_once_with(guid)
        self.mock_get_all_shopping_list_items.assert_called_once_with(guid)
        self.mock_format_row.assert_has_calls([mock.call({'name': 'item1'}, include_comments=True),
                                               mock.call({'name': 'item2'}, include_comments=True),
                                               mock.call({'name': 'item3'}, include_comments=True)])
        self.mock_print_table.assert_called_once_with(['formatted_row_1',
                                                       'formatted_row_2',
                                                       'formatted_row_3'], title='test_list')

    def test_completed_extended(self):
        guid = 'test_guid'
        display_shopping_list(guid=guid, mode=COMPLETED, extended=True)

        self.assertFalse(self.mock_get_shopping_list_info.called)
        self.mock_get_completed.assert_called_once_with()
        self.mock_format_row.assert_has_calls([mock.call({'name': 'item1'}, include_comments=True),
                                               mock.call({'name': 'item2'}, include_comments=True),
                                               mock.call({'name': 'item3'}, include_comments=True)])
        self.mock_print_table.assert_called_once_with(['formatted_row_1',
                                                       'formatted_row_2',
                                                       'formatted_row_3'], title='Recently Completed')

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
        self.mock_format_row.assert_called_once_with(self.mock_get_item.return_value, include_comments=True)
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
        self.mock_format_row.assert_has_calls([mock.call({'name': 'list1'}),
                                               mock.call({'name': 'list2'}),
                                               mock.call({'name': 'list3'}),])
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

class TestShowDefaultList(unittest.TestCase):
    def setUp(self):
        self.DEFAULT_LIST_patcher = mock.patch('vt.vt.DEFAULT_LIST', 'default_list')
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
        show(args)

        self.mock_display_shopping_list.assert_called_once_with(guid='default_list')

    def test_list_no_guid(self):
        args = shlex.split("list")
        show(args)

        self.mock_display_shopping_list.assert_called_once_with(guid='default_list')

    def test_list_empty_guid_extended(self):
        args = shlex.split("list '' -e")
        show(args)

        self.mock_display_shopping_list.assert_called_once_with(guid='default_list', extended=True)

    def test_list_no_guid_extended(self):
        args = shlex.split("list -e")
        show(args)

        self.mock_display_shopping_list.assert_called_once_with(guid='default_list', extended=True)

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


class TestComplete(unittest.TestCase):
    def setUp(self):
        self.complete_item_patcher = mock.patch('vt.vt.complete_item')
        self.mock_complete_item = self.complete_item_patcher.start()

        self.Color_patcher = mock.patch('vt.vt.Color')
        self.mock_Color = self.Color_patcher.start()

        self.display_shopping_list_patcher = mock.patch('vt.vt.display_shopping_list')
        self.mock_display_shopping_list = self.display_shopping_list_patcher.start()

        self.mock_complete_item.return_value = {'name': 'test_name'}

    def tearDown(self):
        self.complete_item_patcher.stop()
        self.Color_patcher.stop()

    def test_complete(self):
        args = shlex.split("test_guid")
        complete(args)

        self.mock_complete_item.assert_called_once_with('test_guid',
                                                        uncomplete=False)
        self.mock_Color.assert_called_once_with('Marked {strike}{automagenta}test_name{/automagenta}{/strike} as done.')

    def test_uncomplete(self):
        args = shlex.split("test_guid")
        complete(args, uncomplete=True)

        self.mock_complete_item.assert_called_once_with('test_guid',
                                                        uncomplete=True)
        self.mock_Color.assert_called_once_with('Marked {automagenta}test_name{/automagenta} undone.')

    def test_done_extended(self):
        args = shlex.split("-e")
        complete(args)

        self.mock_display_shopping_list.assert_called_once_with(extended=True, mode=COMPLETED)

    def test_completed_no_extended(self):
        args = shlex.split("")
        complete(args)

        self.mock_display_shopping_list.assert_called_once_with(mode=COMPLETED)

    def test_completed_extended(self):
        args = shlex.split("--extended")
        complete(args)

        self.mock_display_shopping_list.assert_called_once_with(extended=True, mode=COMPLETED)

class TestModify(unittest.TestCase):
    def setUp(self):
        self.modify_item_patcher = mock.patch('vt.vt.modify_item')
        self.mock_modify_item = self.modify_item_patcher.start()

        self.display_item_patcher = mock.patch('vt.vt.display_item')
        self.mock_display_item = self.display_item_patcher.start()

    def tearDown(self):
        self.modify_item_patcher.stop()
        self.display_item_patcher.stop()

    def test_(self):
        args = shlex.split("test_guid this is a comment")
        modify(args)
        self.mock_modify_item.assert_called_once_with('test_guid',
                                                      'this is a comment')
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
        self.mock_format_row.assert_called_once_with(self.mock_add_item.return_value)
        self.mock_print_table.assert_called_once_with([self.mock_format_row.return_value])

    def test_with_guid(self):
        args = shlex.split("test_guid 'this is a new item'")
        add(args)
        self.mock_add_item.assert_called_once_with('test_guid', 'this is a new item')
        self.mock_format_row.assert_called_once_with(self.mock_add_item.return_value)
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
        self.mock_format_row.assert_called_once_with(self.mock_add_item.return_value)
        self.mock_print_table.assert_called_once_with([self.mock_format_row.return_value])

class TestMove(unittest.TestCase):
    def setUp(self):
        self.move_item_patcher = mock.patch('vt.vt.move_item')
        self.mock_move_item = self.move_item_patcher.start()

        self.Color_patcher = mock.patch('vt.vt.Color')
        self.mock_Color = self.Color_patcher.start()

    def tearDown(self):
        self.move_item_patcher.stop()
        self.Color_patcher.stop()

    def test_(self):
        args = shlex.split('test_guid to_list_guid')
        move(args)
        self.mock_move_item.assert_called_once_with('test_guid', 'to_list_guid')
        self.mock_Color.assert_called_once_with('Moved item {autoblue}test_guid{/autoblue} to list {autoblue}to_list_guid{/autoblue}')

class TestRun(unittest.TestCase):
    def setUp(self):
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

        self.Color_patcher = mock.patch('vt.vt.Color')
        self.mock_Color = self.Color_patcher.start()

        self.SHOW_TRACEBACK_patcher = mock.patch('vt.vt.SHOW_TRACEBACK', False)
        self.SHOW_TRACEBACK_patcher.start()

        self.PROXY_patcher = mock.patch('vt.vt.PROXY', False)
        self.PROXY_patcher.start()

        self.VITTLIFY_URL_patcher = mock.patch('vt.vt.VITTLIFY_URL', 'vittlify_url')
        self.VITTLIFY_URL_patcher.start()

    def tearDown(self):
        self.show_patcher.stop()
        self.complete_patcher.stop()
        self.modify_patcher.stop()
        self.add_patcher.stop()
        self.move_patcher.stop()
        self.Color_patcher.stop()
        self.SHOW_TRACEBACK_patcher.stop()
        self.PROXY_patcher.stop()
        self.VITTLIFY_URL_patcher.stop()

    def test_list(self):
        test_args = shlex.split('list test_guid')
        run(test_args)
        self.mock_show.assert_called_once_with(test_args)
        self.assertFalse(self.mock_complete.called)
        self.assertFalse(self.mock_modify.called)
        self.assertFalse(self.mock_add.called)
        self.assertFalse(self.mock_move.called)

    def test_lists(self):
        test_args = shlex.split('lists')
        run(test_args)
        self.mock_show.assert_called_once_with(test_args)
        self.assertFalse(self.mock_complete.called)
        self.assertFalse(self.mock_modify.called)
        self.assertFalse(self.mock_add.called)
        self.assertFalse(self.mock_move.called)

    def test_item(self):
        test_args = shlex.split('item test_guid')
        run(test_args)
        self.mock_show.assert_called_once_with(test_args)
        self.assertFalse(self.mock_complete.called)
        self.assertFalse(self.mock_modify.called)
        self.assertFalse(self.mock_add.called)
        self.assertFalse(self.mock_move.called)

    def test_show(self):
        test_args = shlex.split('show test_guid')
        run(test_args)
        self.mock_show.assert_called_once_with(test_args)
        self.assertFalse(self.mock_complete.called)
        self.assertFalse(self.mock_modify.called)
        self.assertFalse(self.mock_add.called)
        self.assertFalse(self.mock_move.called)

    def test_done(self):
        test_args = shlex.split('done test_guid')
        expected = ['test_guid']
        run(test_args)
        self.assertFalse(self.mock_show.called)
        self.mock_complete.assert_called_once_with(expected)
        self.assertFalse(self.mock_modify.called)
        self.assertFalse(self.mock_add.called)
        self.assertFalse(self.mock_move.called)

    def test_complete(self):
        test_args = shlex.split('complete test_guid')
        expected = ['test_guid']
        run(test_args)
        self.assertFalse(self.mock_show.called)
        self.mock_complete.assert_called_once_with(expected)
        self.assertFalse(self.mock_modify.called)
        self.assertFalse(self.mock_add.called)
        self.assertFalse(self.mock_move.called)

    def test_undone(self):
        test_args = shlex.split('undone test_guid')
        expected = ['test_guid']
        run(test_args)
        self.assertFalse(self.mock_show.called)
        self.mock_complete.assert_called_once_with(expected, uncomplete=True)
        self.assertFalse(self.mock_modify.called)
        self.assertFalse(self.mock_add.called)
        self.assertFalse(self.mock_move.called)

    def test_uncomplete(self):
        test_args = shlex.split('uncomplete test_guid')
        expected = ['test_guid']
        run(test_args)
        self.assertFalse(self.mock_show.called)
        self.mock_complete.assert_called_once_with(expected, uncomplete=True)
        self.assertFalse(self.mock_modify.called)
        self.assertFalse(self.mock_add.called)
        self.assertFalse(self.mock_move.called)

    def test_modify(self):
        test_args = shlex.split("modify test_guid 'these are comments'")
        expected = ['test_guid', 'these are comments']
        run(test_args)
        self.assertFalse(self.mock_show.called)
        self.assertFalse(self.mock_complete.called)
        self.mock_modify.assert_called_once_with(expected)
        self.assertFalse(self.mock_add.called)
        self.assertFalse(self.mock_move.called)

    def test_edit(self):
        test_args = shlex.split("edit test_guid 'these are comments'")
        expected = ['test_guid', 'these are comments']
        run(test_args)
        self.assertFalse(self.mock_show.called)
        self.assertFalse(self.mock_complete.called)
        self.mock_modify.assert_called_once_with(expected)
        self.assertFalse(self.mock_add.called)
        self.assertFalse(self.mock_move.called)

    def test_comment(self):
        test_args = shlex.split("comment test_guid 'these are comments'")
        expected = ['test_guid', 'these are comments']
        run(test_args)
        self.assertFalse(self.mock_show.called)
        self.assertFalse(self.mock_complete.called)
        self.mock_modify.assert_called_once_with(expected)
        self.assertFalse(self.mock_add.called)
        self.assertFalse(self.mock_move.called)

    def test_comments(self):
        test_args = shlex.split("comments test_guid 'these are comments'")
        expected = ['test_guid', 'these are comments']
        run(test_args)
        self.assertFalse(self.mock_show.called)
        self.assertFalse(self.mock_complete.called)
        self.mock_modify.assert_called_once_with(expected)
        self.assertFalse(self.mock_add.called)
        self.assertFalse(self.mock_move.called)

    def test_add(self):
        test_args = shlex.split("add 'this is a new item'")
        expected = ['this is a new item']
        run(test_args)
        self.assertFalse(self.mock_show.called)
        self.assertFalse(self.mock_complete.called)
        self.assertFalse(self.mock_modify.called)
        self.mock_add.assert_called_once_with(expected)
        self.assertFalse(self.mock_move.called)

    def test_move(self):
        test_args = shlex.split("move old_guid new_guid")
        expected = ['old_guid', 'new_guid']
        run(test_args)
        self.assertFalse(self.mock_show.called)
        self.assertFalse(self.mock_complete.called)
        self.assertFalse(self.mock_modify.called)
        self.assertFalse(self.mock_add.called)
        self.mock_move.assert_called_once_with(expected)

    def test_mv(self):
        test_args = shlex.split("mv old_guid new_guid")
        expected = ['old_guid', 'new_guid']
        run(test_args)
        self.assertFalse(self.mock_show.called)
        self.assertFalse(self.mock_complete.called)
        self.assertFalse(self.mock_modify.called)
        self.assertFalse(self.mock_add.called)
        self.mock_move.assert_called_once_with(expected)

    def test_index_error(self):
        self.mock_add.side_effect = IndexError()

        test_args = shlex.split("add 'this is a new item'")
        run(test_args)
        self.mock_Color.assert_called_once_with('{autored}Incorrect number of arguments provided{/autored}')

    def test_connection_error(self):
        self.mock_add.side_effect = requests.exceptions.ConnectionError()

        test_args = shlex.split("add 'this is a new item'")
        run(test_args)
        self.mock_Color.assert_called_once_with('{autored}Unable to connect to Vittlify instance at vittlify_url{/autored}')

    def test_http_error(self):
        self.mock_add.side_effect = requests.exceptions.HTTPError('500 Message')

        test_args = shlex.split("add 'this is a new item'")
        run(test_args)
        self.mock_Color.assert_called_once_with('{autored}Server responded with 500 Message{/autored}')
