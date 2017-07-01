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
        #import pdb; pdb.set_trace()
        actual = format_row(item)

        self.assertEqual(expected, actual)
        self.mock_Color.assert_has_calls([mock.call('{autoblue}asdf{/autoblue}'),
                                         mock.call('{automagenta}  test_name{/automagenta}')])
