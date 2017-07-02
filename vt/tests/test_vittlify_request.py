import unittest
import mock
from vt.vittlify_request import (_send_request,
                                 VittlifyError,
                                 get_all_shopping_lists,
                                 get_shopping_list_info,
                                 get_shopping_list_items,
                                 get_all_shopping_list_items,
                                 get_completed,
                                 get_item,
                                 add_item,
                                 modify_item,
                                 complete_item,
                                 )

class TestSendRequest(unittest.TestCase):
    def setUp(self):
        self.VITTLIFY_URL_patcher = mock.patch('vt.vittlify_request.VITTLIFY_URL', 'VITTLIFY_URL/')
        self.VITTLIFY_URL_patcher.start()

        self.json_patcher = mock.patch('vt.vittlify_request.json')
        self.mock_json = self.json_patcher.start()

        self.get_encoded_signature_patcher = mock.patch('vt.vittlify_request.get_encoded_signature')
        self.mock_get_encoded_signature = self.get_encoded_signature_patcher.start()

        self.requests_patcher = mock.patch('vt.vittlify_request.requests')
        self.mock_requests = self.requests_patcher.start()

    def tearDown(self):
        self.json_patcher.stop()
        self.get_encoded_signature_patcher.stop()
        self.requests_patcher.stop()
        self.VITTLIFY_URL_patcher.stop()

    def test_get(self):
        test_data = {'data': 'test_data'}
        expected = self.mock_requests.get.return_value.json.return_value
        actual = _send_request('get', test_data)

        self.assertEqual(expected, actual)
        self.mock_json.dumps.assert_called_once_with(test_data)
        self.mock_get_encoded_signature.assert_called_once_with(self.mock_json.dumps.return_value)
        self.mock_requests.get.assert_called_once_with('VITTLIFY_URL/vt/',
                                                       json={'message': self.mock_json.dumps.return_value,
                                                             'signature': self.mock_get_encoded_signature.return_value})

    def test_put(self):
        test_data = {'data': 'test_data'}
        expected = self.mock_requests.put.return_value.json.return_value
        actual = _send_request('put', test_data)

        self.assertEqual(expected, actual)
        self.mock_json.dumps.assert_called_once_with(test_data)
        self.mock_get_encoded_signature.assert_called_once_with(self.mock_json.dumps.return_value)
        self.mock_requests.put.assert_called_once_with('VITTLIFY_URL/vt/',
                                                       json={'message': self.mock_json.dumps.return_value,
                                                             'signature': self.mock_get_encoded_signature.return_value})

    def test_raises_vittlify_error_for_404(self):
        test_data = {'data': 'test_data'}

        self.mock_requests.get.return_value.status_code = 404
        self.assertRaises(VittlifyError,
                          _send_request,
                          'get',
                          test_data)

    def test_raises_vittlify_error_for_409(self):
        test_data = {'data': 'test_data'}

        self.mock_requests.get.return_value.status_code = 409
        self.assertRaises(VittlifyError,
                          _send_request,
                          'get',
                          test_data)

class TestGetAllShoppingLists(unittest.TestCase):
    def setUp(self):
        self.USERNAME_patcher = mock.patch('vt.vittlify_request.USERNAME', 'USERNAME')
        self.USERNAME_patcher.start()

        self._send_request_patcher = mock.patch('vt.vittlify_request._send_request')
        self.mock_send_request = self._send_request_patcher.start()

    def tearDown(self):
        self.USERNAME_patcher.stop()
        self._send_request_patcher.stop()

    def test_(self):
        expected = self.mock_send_request.return_value
        actual = get_all_shopping_lists()

        self.assertEqual(expected, actual)
        self.mock_send_request.assert_called_once_with('GET', {'endpoint': 'all lists',
                                                               'username': 'USERNAME'})

class TestGetShoppingListInfo(unittest.TestCase):
    def setUp(self):
        self.USERNAME_patcher = mock.patch('vt.vittlify_request.USERNAME', 'USERNAME')
        self.USERNAME_patcher.start()

        self._send_request_patcher = mock.patch('vt.vittlify_request._send_request')
        self.mock_send_request = self._send_request_patcher.start()

    def tearDown(self):
        self.USERNAME_patcher.stop()
        self._send_request_patcher.stop()

    def test_(self):
        test_guid = 'test_guid'
        expected = self.mock_send_request.return_value
        actual = get_shopping_list_info(test_guid)

        self.assertEqual(expected, actual)
        self.mock_send_request.assert_called_once_with('GET', {'endpoint': 'list',
                                                               'username': 'USERNAME',
                                                               'guid': 'test_guid'})

class TestGetShoppingListItems(unittest.TestCase):
    def setUp(self):
        self.USERNAME_patcher = mock.patch('vt.vittlify_request.USERNAME', 'USERNAME')
        self.USERNAME_patcher.start()

        self._send_request_patcher = mock.patch('vt.vittlify_request._send_request')
        self.mock_send_request = self._send_request_patcher.start()

    def tearDown(self):
        self.USERNAME_patcher.stop()
        self._send_request_patcher.stop()

    def test_(self):
        test_guid = 'test_guid'
        expected = self.mock_send_request.return_value
        actual = get_shopping_list_items(test_guid)

        self.assertEqual(expected, actual)
        self.mock_send_request.assert_called_once_with('GET', {'endpoint': 'list items',
                                                               'username': 'USERNAME',
                                                               'guid': 'test_guid'})

class TestGetAllShoppingListItems(unittest.TestCase):
    def setUp(self):
        self.USERNAME_patcher = mock.patch('vt.vittlify_request.USERNAME', 'USERNAME')
        self.USERNAME_patcher.start()

        self._send_request_patcher = mock.patch('vt.vittlify_request._send_request')
        self.mock_send_request = self._send_request_patcher.start()

    def tearDown(self):
        self.USERNAME_patcher.stop()
        self._send_request_patcher.stop()

    def test_(self):
        test_guid = 'test_guid'
        expected = self.mock_send_request.return_value
        actual = get_all_shopping_list_items(test_guid)

        self.assertEqual(expected, actual)
        self.mock_send_request.assert_called_once_with('GET', {'endpoint': 'list all items',
                                                               'username': 'USERNAME',
                                                               'guid': 'test_guid'})

class TestGetCompleted(unittest.TestCase):
    def setUp(self):
        self.USERNAME_patcher = mock.patch('vt.vittlify_request.USERNAME', 'USERNAME')
        self.USERNAME_patcher.start()

        self._send_request_patcher = mock.patch('vt.vittlify_request._send_request')
        self.mock_send_request = self._send_request_patcher.start()

    def tearDown(self):
        self.USERNAME_patcher.stop()
        self._send_request_patcher.stop()

    def test_(self):
        expected = self.mock_send_request.return_value
        actual = get_completed()

        self.assertEqual(expected, actual)
        self.mock_send_request.assert_called_once_with('GET', {'endpoint': 'completed',
                                                               'username': 'USERNAME'})

class TestGetItem(unittest.TestCase):
    def setUp(self):
        self.USERNAME_patcher = mock.patch('vt.vittlify_request.USERNAME', 'USERNAME')
        self.USERNAME_patcher.start()

        self._send_request_patcher = mock.patch('vt.vittlify_request._send_request')
        self.mock_send_request = self._send_request_patcher.start()

    def tearDown(self):
        self.USERNAME_patcher.stop()
        self._send_request_patcher.stop()

    def test_(self):
        test_guid = 'test_guid'
        expected = self.mock_send_request.return_value
        actual = get_item(test_guid)

        self.assertEqual(expected, actual)
        self.mock_send_request.assert_called_once_with('GET', {'endpoint': 'item',
                                                               'username': 'USERNAME',
                                                               'guid': test_guid})

class TestCompleteItem(unittest.TestCase):
    def setUp(self):
        self.USERNAME_patcher = mock.patch('vt.vittlify_request.USERNAME', 'USERNAME')
        self.USERNAME_patcher.start()

        self._send_request_patcher = mock.patch('vt.vittlify_request._send_request')
        self.mock_send_request = self._send_request_patcher.start()

    def tearDown(self):
        self.USERNAME_patcher.stop()
        self._send_request_patcher.stop()

    def test_complete(self):
        test_guid = 'test_guid'
        expected = self.mock_send_request.return_value
        actual = complete_item(test_guid)

        self.assertEqual(expected, actual)
        self.mock_send_request.assert_called_once_with('PUT', {'endpoint': 'complete',
                                                               'username': 'USERNAME',
                                                               'guid': test_guid})

    def test_uncomplete(self):
        test_guid = 'test_guid'
        expected = self.mock_send_request.return_value
        actual = complete_item(test_guid, uncomplete=True)

        self.assertEqual(expected, actual)
        self.mock_send_request.assert_called_once_with('PUT', {'endpoint': 'uncomplete',
                                                               'username': 'USERNAME',
                                                               'guid': test_guid})

class TestModifyItem(unittest.TestCase):
    def setUp(self):
        self.USERNAME_patcher = mock.patch('vt.vittlify_request.USERNAME', 'USERNAME')
        self.USERNAME_patcher.start()

        self._send_request_patcher = mock.patch('vt.vittlify_request._send_request')
        self.mock_send_request = self._send_request_patcher.start()

    def tearDown(self):
        self.USERNAME_patcher.stop()
        self._send_request_patcher.stop()

    def test_(self):
        test_guid = 'test_guid'
        comments = 'test_comments'
        expected = self.mock_send_request.return_value
        actual = modify_item(test_guid, comments)

        self.assertEqual(expected, actual)
        self.mock_send_request.assert_called_once_with('PUT', {'endpoint': 'modify',
                                                               'username': 'USERNAME',
                                                               'guid': test_guid,
                                                               'comments': comments})

class TestAddItem(unittest.TestCase):
    def setUp(self):
        self.USERNAME_patcher = mock.patch('vt.vittlify_request.USERNAME', 'USERNAME')
        self.USERNAME_patcher.start()

        self._send_request_patcher = mock.patch('vt.vittlify_request._send_request')
        self.mock_send_request = self._send_request_patcher.start()

    def tearDown(self):
        self.USERNAME_patcher.stop()
        self._send_request_patcher.stop()

    def test_(self):
        test_guid = 'test_guid'
        comments = 'test_comments'
        name = 'test_name'

        expected = self.mock_send_request.return_value
        actual = add_item(test_guid, name, comments=comments)

        self.assertEqual(expected, actual)
        self.mock_send_request.assert_called_once_with('POST', {'endpoint': 'add item',
                                                                'username': 'USERNAME',
                                                                'guid': test_guid,
                                                                'comments': comments,
                                                                'name': name})
