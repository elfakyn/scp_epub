import importlib
import os
import unittest
import unittest.mock

import download.wikidot_api
from constants import constants

class TestGetApiKey(unittest.TestCase):
    @unittest.mock.patch('download.aws.get_api_key_from_secretsmanager')
    def test_get_api_key_locally(self, mock_get_api_key_from_secretsmanager):
        # Arrange
        expected_api_key = '000000000000000000000000000'
        os.environ.pop(constants.USE_AWS_VARIABLE, None)
        os.environ[constants.API_KEY_VARIABLE] = expected_api_key

        # Act
        actual_api_key = download.wikidot_api._get_api_key()

        # Assert
        mock_get_api_key_from_secretsmanager.assert_not_called()
        self.assertEqual(expected_api_key, actual_api_key)

    @unittest.mock.patch('download.aws.get_api_key_from_secretsmanager')
    def test_get_api_key_with_aws(self, mock_get_api_key_from_secretsmanager):
        # Arrange
        expected_api_key = '000000000000000000000000000'
        os.environ[constants.USE_AWS_VARIABLE] = constants.USE_AWS_TRUE
        os.environ.pop(constants.API_KEY_VARIABLE, None)

        mock_get_api_key_from_secretsmanager.return_value = expected_api_key

        # Act
        actual_api_key = download.wikidot_api._get_api_key()

        # Assert
        mock_get_api_key_from_secretsmanager.assert_called_once_with()
        self.assertEqual(expected_api_key, actual_api_key)

class TestWikidotClient(unittest.TestCase):
    @classmethod
    def tearDownClass(cls):
        importlib.reload(download.wikidot_api)
        return super().tearDownClass()

    def setUp(self):
        importlib.reload(download.wikidot_api)

    @unittest.mock.patch('download.wikidot_api._create_wikidot_client')
    def test_get_wikidot_client_only_once(self, mock_create_wikidot_client):
        # Arrange
        expected_wikidot_client = download.wikidot_api._get_wikidot_client()

        # Act
        actual_wikidot_client = download.wikidot_api._get_wikidot_client()

        # Assert
        mock_create_wikidot_client.assert_called_once_with()
        self.assertIs(expected_wikidot_client, actual_wikidot_client)

    @unittest.mock.patch('xmlrpc.client')
    @unittest.mock.patch('download.wikidot_api._get_api_key')
    def test_create_wikidot_client(self, mock_get_api_key, mock_xmlrpc_client):
        # Arrange
        expected_api_key = '00000000000000000'
        expected_endpoint = f'https://{constants.CLIENT_NAME}:{expected_api_key}@{constants.RPC_ENDPOINT}'

        mock_get_api_key.return_value = expected_api_key
        expected_client = mock_xmlrpc_client.ServerProxy.return_value

        # Act
        actual_client = download.wikidot_api._create_wikidot_client()

        # Assert
        mock_get_api_key.assert_called_once_with()
        mock_xmlrpc_client.ServerProxy.assert_called_once_with(expected_endpoint)
        self.assertEqual(expected_client, actual_client)

class TestGetListOfPagesUndecorated(unittest.TestCase):
    @unittest.mock.patch('download.wikidot_api._get_wikidot_client')
    def test_get_list_of_pages(self, mock_get_wikidot_client):
        # Arrange
        expected_site = constants.SITE_NAME
        expected_category = constants.PAGE_CATEGORY
        expected_client = mock_get_wikidot_client.return_value
        expected_select_call = {
            'site': expected_site,
            'categories': [expected_category]
        }
        expected_list_of_pages = expected_client.pages.select.return_value

        # Act
        actual_list_of_pages = download.wikidot_api._get_list_of_pages_undecorated(expected_category)

        # Assert
        mock_get_wikidot_client.assert_called_once_with()
        expected_client.pages.select.assert_called_once_with(expected_select_call)
        self.assertEqual(expected_list_of_pages, actual_list_of_pages)
