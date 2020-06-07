import unittest
import unittest.mock
import os

import download.cache
from constants import constants

class TestGetCachedContents(unittest.TestCase):
    @unittest.mock.patch('json.loads')
    @unittest.mock.patch('download.cache.retrieve_from_s3_cache')
    @unittest.mock.patch('download.cache.retrieve_from_local_cache')
    def test_get_cached_contents_locally(self, mock_retrieve_from_local_cache, mock_retrieve_from_s3_cache, mock_loads):
        # Arrange
        os.environ.pop(constants.USE_AWS_VARIABLE, None)
        expected_filetype = 'html'
        expected_relative_path = 'foo/bar/'
        expected_item = 'scp-123'

        # Act
        actual_contents = download.cache.get_cached_contents(expected_relative_path, expected_item, filetype=expected_filetype)

        # Assert
        self.assertEqual(actual_contents, mock_retrieve_from_local_cache.return_value)
        mock_loads.assert_not_called()
        mock_retrieve_from_s3_cache.assert_not_called()
        mock_retrieve_from_local_cache.assert_called_once_with(expected_relative_path, expected_item, expected_filetype)

    @unittest.mock.patch('json.loads')
    @unittest.mock.patch('download.cache.retrieve_from_s3_cache')
    @unittest.mock.patch('download.cache.retrieve_from_local_cache')
    def test_get_cached_contents_s3(self, mock_retrieve_from_local_cache, mock_retrieve_from_s3_cache, mock_loads):
        # Arrange
        os.environ[constants.USE_AWS_VARIABLE] = constants.USE_AWS_TRUE
        expected_filetype = 'html'
        expected_relative_path = 'foo/bar/'
        expected_item = 'scp-123'

        # Act
        actual_contents = download.cache.get_cached_contents(expected_relative_path, expected_item, filetype=expected_filetype)

        # Assert
        self.assertEqual(actual_contents, mock_retrieve_from_s3_cache.return_value)
        mock_loads.assert_not_called()
        mock_retrieve_from_s3_cache.assert_called_once_with(expected_relative_path, expected_item, expected_filetype)
        mock_retrieve_from_local_cache.assert_not_called()

    @unittest.mock.patch('json.loads')
    @unittest.mock.patch('download.cache.retrieve_from_s3_cache')
    @unittest.mock.patch('download.cache.retrieve_from_local_cache')
    def test_get_cached_contents_load_json(self, mock_retrieve_from_local_cache, mock_retrieve_from_s3_cache, mock_loads):
        # Arrange
        os.environ[constants.USE_AWS_VARIABLE] = constants.USE_AWS_TRUE
        expected_filetype = 'json'
        expected_relative_path = 'foo/bar/'
        expected_item = 'scp-123'

        # Act
        actual_contents = download.cache.get_cached_contents(expected_relative_path, expected_item, filetype=expected_filetype)

        # Assert
        self.assertEqual(actual_contents, mock_loads.return_value)
        mock_loads.assert_called_once_with(mock_retrieve_from_s3_cache.return_value)
        mock_retrieve_from_s3_cache.assert_called_once_with(expected_relative_path, expected_item, expected_filetype)
        mock_retrieve_from_local_cache.assert_not_called()

class TestRetrieveFromLocalCache(unittest.TestCase):
    @unittest.mock.patch('builtins.open')
    def test_retrieve_from_local_cache(self, mock_open):
        # Arrange
        expected_relative_path = 'foo/bar'
        expected_item = 'scp-123'
        expected_filetype = 'json'
        expected_path = os.path.join(constants.LOCAL_CACHE_BASE_PATH, expected_relative_path, expected_item + '.' + expected_filetype)

        # Act
        actual_contents = download.cache.retrieve_from_local_cache(expected_relative_path, expected_item, expected_filetype)

        # Assert
