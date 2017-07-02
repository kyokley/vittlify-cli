import unittest
import mock

from vt.utils import format_row, print_table

class TestFormatRow(unittest.TestCase):
    def setUp(self):
        self.Color_patcher = mock.patch('vt.utils.Color')
        self.mock_Color = self.Color_patcher.start()

    def tearDown(self):
        self.Color_patcher.stop()

    def test_no_comments(self):
        self.mock_Color.side_effect = ['guid_Color', 'name_Color']

        item = {'guid': 'asdf',
                'name': 'test_name'}

        expected = ['guid_Color', 'name_Color']
        actual = format_row(item)

        self.assertEqual(expected, actual)
        self.mock_Color.assert_has_calls([mock.call('{autoblue}asdf{/autoblue}'),
                                          mock.call('{automagenta}  test_name{/automagenta}')])

    def test_item_with_comments(self):
        self.mock_Color.side_effect = ['guid_Color', 'name_Color']

        item = {'guid': 'asdf',
                'name': 'test_name',
                'comments': 'test_comments'}

        expected = ['guid_Color', 'name_Color']
        actual = format_row(item)

        self.assertEqual(expected, actual)
        self.mock_Color.assert_has_calls([mock.call('{autoblue}asdf{/autoblue}'),
                                          mock.call('{automagenta}+ test_name{/automagenta}')])

    def test_item_with_comments_include_comments(self):
        self.mock_Color.side_effect = ['guid_Color', 'name_Color']

        item = {'guid': 'asdf',
                'name': 'test_name',
                'comments': 'test_comments'}

        expected = ['guid_Color', 'name_Color', 'test_comments']
        actual = format_row(item, include_comments=True)

        self.assertEqual(expected, actual)
        self.mock_Color.assert_has_calls([mock.call('{autoblue}asdf{/autoblue}'),
                                          mock.call('{automagenta}+ test_name{/automagenta}')])

    def test_no_comments_done(self):
        self.mock_Color.side_effect = ['guid_Color', 'name_Color']

        item = {'guid': 'asdf',
                'name': 'test_name',
                'done': True}

        expected = ['guid_Color', 'name_Color']
        actual = format_row(item)

        self.assertEqual(expected, actual)
        self.mock_Color.assert_has_calls([mock.call('{strike}{autoblue}asdf{/autoblue}{/strike}'),
                                          mock.call('{strike}{automagenta}  test_name{/automagenta}{/strike}')])

    def test_item_with_comments_done(self):
        self.mock_Color.side_effect = ['guid_Color', 'name_Color']

        item = {'guid': 'asdf',
                'name': 'test_name',
                'comments': 'test_comments',
                'done': True}

        expected = ['guid_Color', 'name_Color']
        actual = format_row(item)

        self.assertEqual(expected, actual)
        self.mock_Color.assert_has_calls([mock.call('{strike}{autoblue}asdf{/autoblue}{/strike}'),
                                          mock.call('{strike}{automagenta}+ test_name{/automagenta}{/strike}')])

    def test_item_with_comments_include_comments_done(self):
        self.mock_Color.side_effect = ['guid_Color', 'name_Color', 'comments_Color']

        item = {'guid': 'asdf',
                'name': 'test_name',
                'comments': 'test_comments',
                'done': True}

        expected = ['guid_Color', 'name_Color', 'comments_Color']
        actual = format_row(item, include_comments=True)

        self.assertEqual(expected, actual)
        self.mock_Color.assert_has_calls([mock.call('{strike}{autoblue}asdf{/autoblue}{/strike}'),
                                          mock.call('{strike}{automagenta}+ test_name{/automagenta}{/strike}'),
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
