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
    def setUp(self):
        importlib.reload('download.wikidot_api')

    @unittest.mock.patch('download.wikidot_api.get_wikidot_client')
    def test_client_closure(self, mock_get_wikidot_client):
        # Arrange
        expected_client = download.wikidot_api.client()

        # Act
        actual_client = download.wikidot_api.client()

        # Assert
        self.assertIs(expected_client(), actual_client())
