import shlex
import unittest
import mock

from vt.vt import (display_shopping_list,
                   display_item,
                   display_all_shopping_lists,
                   COMPLETED,
                   NOT_COMPLETED,
                   ALL,
                   show,
                   complete,
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

class TestShow(unittest.TestCase):
    def setUp(self):
        self.display_shopping_list_patcher = mock.patch('vt.vt.display_shopping_list')
        self.mock_display_shopping_list = self.display_shopping_list_patcher.start()

        self.display_all_shopping_lists_patcher = mock.patch('vt.vt.display_all_shopping_lists')
        self.mock_display_all_shopping_lists = self.display_all_shopping_lists_patcher.start()

        self.display_item_patcher = mock.patch('vt.vt.display_item')
        self.mock_display_item = self.display_item_patcher.start()

    def tearDown(self):
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

    def test_list_no_extended(self):
        args = shlex.split("list test_guid")
        show(args)

        self.mock_display_shopping_list.assert_called_once_with(guid='test_guid')

    def test_list_extended(self):
        args = shlex.split("list test_guid extended")
        show(args)

        self.mock_display_shopping_list.assert_called_once_with(guid='test_guid',
                                                                extended=True,
                                                                mode=ALL)

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

    def test_done_no_extended(self):
        args = shlex.split("done test_guid")
        show(args)

        self.mock_display_shopping_list.assert_called_once_with(mode=COMPLETED)

    def test_done_extended(self):
        args = shlex.split("done test_guid extended")
        show(args)

        self.mock_display_shopping_list.assert_called_once_with(extended=True, mode=COMPLETED)

    def test_completed_no_extended(self):
        args = shlex.split("completed test_guid")
        show(args)

        self.mock_display_shopping_list.assert_called_once_with(mode=COMPLETED)

    def test_completed_extended(self):
        args = shlex.split("completed test_guid extended")
        show(args)

        self.mock_display_shopping_list.assert_called_once_with(extended=True, mode=COMPLETED)

class TestComplete(unittest.TestCase):
    def setUp(self):
        self.complete_item_patcher = mock.patch('vt.vt.complete_item')
        self.mock_complete_item = self.complete_item_patcher.start()

        self.Color_patcher = mock.patch('vt.vt.Color')
        self.mock_Color = self.Color_patcher.start()

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
