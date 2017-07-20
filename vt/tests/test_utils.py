import unittest
import mock

from vt.utils import (format_row,
                      print_table,
                      parse_options,
                      )

class TestFormatRow(unittest.TestCase):
    def setUp(self):
        self.Color_patcher = mock.patch('vt.utils.Color')
        self.mock_Color = self.Color_patcher.start()
        self.mock_shopping_list = {'categories': [{'name': 'Type A'},
                                                  {'name': 'Type B'}],
                                   'name': 'list_name'}

    def tearDown(self):
        self.Color_patcher.stop()

    def test_no_comments(self):
        self.mock_Color.side_effect = ['guid_Color', 'name_Color']

        item = {'guid': 'asdf',
                'name': 'test_name'}

        expected = ['guid_Color', 'name_Color']
        actual = format_row(item, self.mock_shopping_list)

        self.assertEqual(expected, actual)
        self.mock_Color.assert_has_calls([mock.call('{autoblue}asdf{/autoblue}'),
                                          mock.call('{automagenta}  test_name{/automagenta}')])

    def test_item_with_comments(self):
        self.mock_Color.side_effect = ['guid_Color', 'name_Color']

        item = {'guid': 'asdf',
                'name': 'test_name',
                'comments': 'test_comments'}

        expected = ['guid_Color', 'name_Color']
        actual = format_row(item, self.mock_shopping_list)

        self.assertEqual(expected, actual)
        self.mock_Color.assert_has_calls([mock.call('{autoblue}asdf{/autoblue}'),
                                          mock.call('{automagenta}+ test_name{/automagenta}')])

    def test_item_with_comments_include_comments(self):
        self.mock_Color.side_effect = ['guid_Color', 'name_Color', 'comments_Color']

        item = {'guid': 'asdf',
                'name': 'test_name',
                'comments': 'test_comments'}

        expected = ['guid_Color', None, 'name_Color', 'comments_Color']
        actual = format_row(item, self.mock_shopping_list, include_comments=True)

        self.assertEqual(expected, actual)
        self.mock_Color.assert_has_calls([mock.call('{autoblue}asdf{/autoblue}'),
                                          mock.call('{automagenta}+ test_name{/automagenta}')])

    def test_no_comments_done(self):
        self.mock_Color.side_effect = ['guid_Color', 'name_Color']

        item = {'guid': 'asdf',
                'name': 'test_name',
                'done': True}

        expected = ['guid_Color', 'name_Color']
        actual = format_row(item, self.mock_shopping_list)

        self.assertEqual(expected, actual)
        self.mock_Color.assert_has_calls([mock.call('{autoblue}{strike}asdf{/strike}{/autoblue}'),
                                          mock.call('{automagenta}  {strike}test_name{/strike}{/automagenta}')])

    def test_item_with_comments_done(self):
        self.mock_Color.side_effect = ['guid_Color', 'name_Color']

        item = {'guid': 'asdf',
                'name': 'test_name',
                'comments': 'test_comments',
                'done': True}

        expected = ['guid_Color', 'name_Color']
        actual = format_row(item, self.mock_shopping_list)

        self.assertEqual(expected, actual)
        self.mock_Color.assert_has_calls([mock.call('{autoblue}{strike}asdf{/strike}{/autoblue}'),
                                          mock.call('{automagenta}{strike}+{/strike} {strike}test_name{/strike}{/automagenta}')])

    def test_item_with_comments_include_comments_done(self):
        self.mock_Color.side_effect = ['guid_Color', 'name_Color', 'comments_Color']

        item = {'guid': 'asdf',
                'name': 'test_name',
                'comments': 'test_comments',
                'done': True}

        expected = ['guid_Color', None, 'name_Color', 'comments_Color']
        actual = format_row(item, self.mock_shopping_list, include_comments=True)

        self.assertEqual(expected, actual)
        self.mock_Color.assert_has_calls([mock.call('{autoblue}{strike}asdf{/strike}{/autoblue}'),
                                          mock.call('{automagenta}{strike}+{/strike} {strike}test_name{/strike}{/automagenta}'),
                                          mock.call('{strike}test_comments{/strike}')])

class TestPrintTable(unittest.TestCase):
    def setUp(self):
        self.Color_patcher = mock.patch('vt.utils.Color')
        self.mock_Color = self.Color_patcher.start()

        self.AsciiTable_patcher = mock.patch('vt.utils.AsciiTable')
        self.mock_AsciiTable = self.AsciiTable_patcher.start()

    def tearDown(self):
        self.Color_patcher.stop()
        self.AsciiTable_patcher.stop()

    def test_no_data(self):
        print_table([])
        self.mock_Color.assert_called_once_with("{autored}No data found.{/autored}")

    def test_data_no_title(self):
        print_table(['test_data'])

        self.mock_AsciiTable.assert_called_once_with(['test_data'])
        self.assertEqual(self.mock_AsciiTable.return_value.inner_heading_row_border, False)

    def test_data_with_title(self):
        print_table(['test_data'], title='test_title')

        self.mock_AsciiTable.assert_called_once_with(['test_data'])
        self.assertEqual(self.mock_AsciiTable.return_value.inner_heading_row_border, False)
        self.mock_Color.assert_called_once_with("{autoyellow}test_title{/autoyellow}")
        self.assertEqual(self.mock_AsciiTable.return_value.title, self.mock_Color.return_value)

class TestParseOptions(unittest.TestCase):
    def test_empty(self):
        raw_options = []
        expected = {}
        actual = parse_options(raw_options)

        self.assertEqual(expected, actual)

    def test_extended(self):
        raw_options = ['asdf', '-e']
        expected = {'extended': True}
        actual = parse_options(raw_options)

        self.assertEqual(expected, actual)

        raw_options = [ '-e','asdf']
        expected = {'extended': True}
        actual = parse_options(raw_options)

        self.assertEqual(expected, actual)

        raw_options = ['asdf', '--extended']
        expected = {'extended': True}
        actual = parse_options(raw_options)

        self.assertEqual(expected, actual)

        raw_options = [ '--extended','asdf']
        expected = {'extended': True}
        actual = parse_options(raw_options)

        self.assertEqual(expected, actual)

    def test_quiet(self):
        raw_options = ['asdf', '-q']
        expected = {'quiet': True}
        actual = parse_options(raw_options)

        self.assertEqual(expected, actual)

        raw_options = [ '-q','asdf']
        expected = {'quiet': True}
        actual = parse_options(raw_options)

        self.assertEqual(expected, actual)

        raw_options = ['asdf', '--quiet']
        expected = {'quiet': True}
        actual = parse_options(raw_options)

        self.assertEqual(expected, actual)

        raw_options = [ '--quiet','asdf']
        expected = {'quiet': True}
        actual = parse_options(raw_options)

        self.assertEqual(expected, actual)

    def test_mixed_options(self):
        raw_options = [ '--extended','asdf', '--quiet']
        expected = {'extended': True,
                    'quiet': True}
        actual = parse_options(raw_options)

        self.assertEqual(expected, actual)

        raw_options = [ '-e','asdf', '--quiet']
        expected = {'extended': True,
                    'quiet': True}
        actual = parse_options(raw_options)

        self.assertEqual(expected, actual)

    def test_mixed_short_options(self):
        raw_options = [ '-e','asdf', '-q']
        expected = {'extended': True,
                    'quiet': True}
        actual = parse_options(raw_options)

        self.assertEqual(expected, actual)

        raw_options = [ '-eq','asdf']
        expected = {'extended': True,
                    'quiet': True}
        actual = parse_options(raw_options)

        self.assertEqual(expected, actual)
