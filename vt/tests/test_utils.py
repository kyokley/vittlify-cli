import unittest
import mock

from vt.utils import format_row

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
        self.mock_Color.side_effect = ['guid_Color', 'name_Color']

        item = {'guid': 'asdf',
                'name': 'test_name',
                'comments': 'test_comments',
                'done': True}

        expected = ['guid_Color', 'name_Color', '{strike}test_comments{/strike}']
        actual = format_row(item, include_comments=True)

        self.assertEqual(expected, actual)
        self.mock_Color.assert_has_calls([mock.call('{strike}{autoblue}asdf{/autoblue}{/strike}'),
                                          mock.call('{strike}{automagenta}+ test_name{/automagenta}{/strike}')])
