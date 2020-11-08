import os
import sys
import unittest
import mock
import pytest

from vt.utils import (format_row,
                      print_table,
                      parse_options,
                      apply_strikethrough,
                      get_encoded_signature,
                      term,
                      )

PY3 = sys.version_info[0] == 3


class TestFormatRow:
    @pytest.fixture(autouse=True)
    def setUp(self, mocker):
        mocker.patch.object(term, 'blue', autospec=True)
        mocker.patch.object(term, 'magenta', autospec=True)

        term.blue.return_value = 'guid_Color'
        term.magenta.return_value = 'name_Color'

        self.mock_shopping_list = {'categories': [{'name': 'Type A'},
                                                  {'name': 'Type B'}],
                                   'name': 'list_name'}

    def test_no_comments(self):
        item = {'guid': 'asdf',
                'name': 'test_name'}

        expected = ['guid_Color', 'name_Color']
        actual = format_row(item, self.mock_shopping_list)

        assert expected == actual
        term.blue.assert_called_once_with('asdf')
        term.magenta.assert_called_once_with('  test_name')

    def test_item_with_comments(self):
        item = {'guid': 'asdf',
                'name': 'test_name',
                'comments': 'test_comments'}

        expected = ['guid_Color', 'name_Color']
        actual = format_row(item, self.mock_shopping_list)

        assert expected == actual
        term.blue.assert_called_once_with('asdf')
        term.magenta.assert_called_once_with('+ test_name')

    def test_item_with_comments_include_comments(self):
        item = {'guid': 'asdf',
                'name': 'test_name',
                'comments': 'test_comments'}

        expected = ['guid_Color', 'name_Color', 'test_comments']
        actual = format_row(item, self.mock_shopping_list, include_comments=True)

        assert expected == actual
        term.blue.assert_called_once_with('asdf')
        term.magenta.assert_called_once_with('+ test_name')

    def test_no_comments_done(self):
        item = {'guid': 'asdf',
                'name': 'test_name',
                'done': True}

        expected = ['guid_Color', 'name_Color']
        actual = format_row(item, self.mock_shopping_list)

        assert expected == actual
        term.blue.assert_called_once_with(f'{term.dim}asdf{term.normal}')
        term.magenta.assert_called_once_with(f'  {term.dim}test_name{term.normal}')

    def test_item_with_comments_done(self):
        item = {'guid': 'asdf',
                'name': 'test_name',
                'comments': 'test_comments',
                'done': True}

        expected = ['guid_Color', 'name_Color']
        actual = format_row(item, self.mock_shopping_list)

        assert expected == actual
        term.blue.assert_called_once_with(f'{term.dim}asdf{term.normal}')
        term.magenta.assert_called_once_with(f'+ {term.dim}test_name{term.normal}')

    def test_item_with_comments_include_comments_done(self):
        item = {'guid': 'asdf',
                'name': 'test_name',
                'comments': 'test_comments',
                'done': True}

        expected = ['guid_Color', 'name_Color', 'test_comments']
        actual = format_row(item, self.mock_shopping_list, include_comments=True)

        assert expected == actual
        term.blue.assert_called_once_with(f'{term.dim}asdf{term.normal}')
        term.magenta.assert_called_once_with(f'+ {term.dim}test_name{term.normal}')

    def test_categories(self):
        self.mock_shopping_list['categories'] = ['type A', 'type B']

        item = {'guid': 'asdf',
                'name': 'test_name',
                'comments': 'test_comments',
                'category_name': 'type A',
                'done': True}

        expected = ['guid_Color', 'type A', 'name_Color']
        actual = format_row(item, self.mock_shopping_list, include_comments=False, include_category=True)

        assert expected == actual
        term.blue.assert_called_once_with(f'{term.dim}asdf{term.normal}')
        term.magenta.assert_called_once_with(f'+ {term.dim}test_name{term.normal}')


class TestPrintTable:
    @pytest.fixture(autouse=True)
    def setUp(self, mocker):
        mocker.patch.object(term, 'red', autospec=True)
        mocker.patch.object(term, 'yellow', autospec=True)

        self.AsciiTable_patcher = mock.patch('vt.utils.AsciiTable')
        self.mock_AsciiTable = self.AsciiTable_patcher.start()

        yield
        self.AsciiTable_patcher.stop()

    def test_no_data(self):
        print_table([])
        term.red.assert_called_once_with("No data found.")

    def test_data_no_title(self):
        print_table(['test_data'])

        self.mock_AsciiTable.assert_called_once_with(['test_data'])
        assert self.mock_AsciiTable.return_value.inner_heading_row_border is False

    def test_data_with_title(self):
        print_table(['test_data'], title='test_title')

        self.mock_AsciiTable.assert_called_once_with(['test_data'])
        assert self.mock_AsciiTable.return_value.inner_heading_row_border is False
        term.yellow.assert_called_once_with("test_title")
        assert self.mock_AsciiTable.return_value.title == term.yellow.return_value


class TestParseOptions(unittest.TestCase):
    def test_empty(self):
        raw_options = []
        expected = {}
        actual = parse_options(raw_options)

        assert expected == actual

    def test_extended(self):
        raw_options = ['asdf', '-e']
        expected = {'extended': True}
        actual = parse_options(raw_options)

        assert expected == actual

        raw_options = [ '-e','asdf']
        expected = {'extended': True}
        actual = parse_options(raw_options)

        assert expected == actual

        raw_options = ['asdf', '--extended']
        expected = {'extended': True}
        actual = parse_options(raw_options)

        assert expected == actual

        raw_options = [ '--extended','asdf']
        expected = {'extended': True}
        actual = parse_options(raw_options)

        assert expected == actual

    def test_quiet(self):
        raw_options = ['asdf', '-q']
        expected = {'quiet': True}
        actual = parse_options(raw_options)

        assert expected == actual

        raw_options = [ '-q','asdf']
        expected = {'quiet': True}
        actual = parse_options(raw_options)

        assert expected == actual

        raw_options = ['asdf', '--quiet']
        expected = {'quiet': True}
        actual = parse_options(raw_options)

        assert expected == actual

        raw_options = [ '--quiet','asdf']
        expected = {'quiet': True}
        actual = parse_options(raw_options)

        assert expected == actual

    def test_mixed_options(self):
        raw_options = [ '--extended','asdf', '--quiet']
        expected = {'extended': True,
                    'quiet': True}
        actual = parse_options(raw_options)

        assert expected == actual

        raw_options = [ '-e','asdf', '--quiet']
        expected = {'extended': True,
                    'quiet': True}
        actual = parse_options(raw_options)

        assert expected == actual

    def test_mixed_short_options(self):
        raw_options = [ '-e','asdf', '-q']
        expected = {'extended': True,
                    'quiet': True}
        actual = parse_options(raw_options)

        assert expected == actual

        raw_options = [ '-eq','asdf']
        expected = {'extended': True,
                    'quiet': True}
        actual = parse_options(raw_options)

        assert expected == actual

    def test_categories(self):
        raw_options = ['asdf', '-c']
        expected = {'include_category': True}
        actual = parse_options(raw_options)

        assert expected == actual

        raw_options = ['-c','asdf']
        expected = {'include_category': True}
        actual = parse_options(raw_options)

        assert expected == actual

        raw_options = ['asdf', '--categories']
        expected = {'include_category': True}
        actual = parse_options(raw_options)

        assert expected == actual

        raw_options = [ '--categories','asdf']
        expected = {'include_category': True}
        actual = parse_options(raw_options)

        assert expected == actual

    def test_unfinished(self):
        raw_options = ['asdf', '-u']
        expected = {'unfinished': True}
        actual = parse_options(raw_options)

        assert expected == actual

        raw_options = ['-u','asdf']
        expected = {'unfinished': True}
        actual = parse_options(raw_options)

        assert expected == actual

        raw_options = ['asdf', '--unfinished']
        expected = {'unfinished': True}
        actual = parse_options(raw_options)

        assert expected == actual

        raw_options = [ '--unfinished','asdf']
        expected = {'unfinished': True}
        actual = parse_options(raw_options)

        assert expected == actual

    def test_append(self):
        raw_options = ['asdf', '-a']
        expected = {'append': True}
        actual = parse_options(raw_options)

        assert expected == actual

        raw_options = ['-a','asdf']
        expected = {'append': True}
        actual = parse_options(raw_options)

        assert expected == actual

        raw_options = ['asdf', '--append']
        expected = {'append': True}
        actual = parse_options(raw_options)

        assert expected == actual

        raw_options = [ '--append','asdf']
        expected = {'append': True}
        actual = parse_options(raw_options)

        assert expected == actual

    def test_delete(self):
        raw_options = ['-d']
        expected = {'delete': True}
        actual = parse_options(raw_options)

        assert expected == actual

        raw_options = ['--delete']
        expected = {'delete': True}
        actual = parse_options(raw_options)

        assert expected == actual


@pytest.mark.skip('Not sure what to do about strikethroughs yet')
class TestApplyStrikethrough:
    def test_plain_string(self):
        test_str = 'string'
        expected = '{strike}string{/strike}'

        actual = apply_strikethrough(test_str)
        assert expected == actual

    def test_plain_string_with_spaces(self):
        test_str = 'this is a string'
        expected = '{strike}this{/strike} {strike}is{/strike} {strike}a{/strike} {strike}string{/strike}'

        actual = apply_strikethrough(test_str)
        assert expected == actual

    def test_skip_color_tags(self):
        test_str = 'this is a {yellow}string{/yellow}'
        expected = '{strike}this{/strike} {strike}is{/strike} {strike}a{/strike} {strike}{yellow}string{/yellow}{/strike}'

        actual = apply_strikethrough(test_str)
        assert expected == actual


class TestGetEncodedSignature(unittest.TestCase):
    def setUp(self):
        mock_environ = dict(os.environ)
        mock_environ['VT_PRIVATE_KEY'] = 'test_key_location'

        self.environ_patcher = mock.patch('vt.utils.os.environ', mock_environ)
        self.environ_patcher.start()

        self.open_patcher = mock.patch('builtins.open' if PY3 else '__builtin__.open')
        self.mock_open = self.open_patcher.start()

        self.b64encode_patcher = mock.patch('vt.utils.base64.b64encode')
        self.mock_b64encode = self.b64encode_patcher.start()

        self.load_pem_private_key_patcher = mock.patch('vt.utils.serialization.load_pem_private_key')
        self.mock_load_pem_private_key = self.load_pem_private_key_patcher.start()

        self.default_backend_patcher = mock.patch('vt.utils.default_backend')
        self.mock_default_backend = self.default_backend_patcher.start()

        self.padding_patcher = mock.patch('vt.utils.padding')
        self.mock_padding = self.padding_patcher.start()

        self.hashes_patcher = mock.patch('vt.utils.hashes')
        self.mock_hashes = self.hashes_patcher.start()

    def tearDown(self):
        self.environ_patcher.stop()
        self.open_patcher.stop()
        self.b64encode_patcher.stop()
        self.load_pem_private_key_patcher.stop()
        self.default_backend_patcher.stop()
        self.padding_patcher.stop()
        self.hashes_patcher.stop()

    def test_(self):
        test_message = 'tests message'

        expected = self.mock_b64encode.return_value
        actual = get_encoded_signature(test_message)

        assert expected == actual
        self.mock_b64encode.assert_called_once_with(self.mock_load_pem_private_key.return_value.sign.return_value)
        self.mock_load_pem_private_key.assert_called_once_with(self.mock_open.return_value.__enter__.return_value.read.return_value,
                                                               None,
                                                               self.mock_default_backend.return_value)

        self.mock_load_pem_private_key.return_value.sign.assert_called_once_with(test_message,
                                                                                 self.mock_padding.PSS.return_value,
                                                                                 self.mock_hashes.SHA512.return_value
                                                                                 )
        self.mock_padding.PSS.assert_called_once_with(mgf=self.mock_padding.MGF1.return_value,
                                                      salt_length=self.mock_padding.PSS.MAX_LENGTH)
        self.mock_padding.MGF1.assert_called_once_with(self.mock_hashes.SHA512.return_value)
