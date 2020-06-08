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
        self.assertEqual(mock_retrieve_from_local_cache.return_value, actual_contents)
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
        self.assertEqual(mock_retrieve_from_s3_cache.return_value, actual_contents)
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
        expected_contents = mock_loads.return_value

        # Act
        actual_contents = download.cache.get_cached_contents(expected_relative_path, expected_item, filetype=expected_filetype)

        # Assert
        self.assertEqual(expected_contents, actual_contents)
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
        expected_cache_file = os.path.join(constants.LOCAL_CACHE_BASE_PATH, expected_relative_path, expected_item + '.' + expected_filetype)
        expected_encoding = constants.ENCODING
        expected_open_type = 'r'
        expected_contents = mock_open.return_value.__enter__.return_value.read.return_value

        # Act
        actual_contents = download.cache.retrieve_from_local_cache(expected_relative_path, expected_item, expected_filetype)

        # Assert
        self.assertEqual(expected_contents, actual_contents)
        mock_open.assert_called_once_with(expected_cache_file, expected_open_type, encoding=expected_encoding)

    @unittest.mock.patch('builtins.open')
    def test_retrieve_from_local_cache_file_not_found(self, mock_open):
        # Arrange
        expected_relative_path = 'foo/bar'
        expected_item = 'scp-123'
        expected_filetype = 'json'
        expected_cache_file = os.path.join(constants.LOCAL_CACHE_BASE_PATH, expected_relative_path, expected_item + '.' + expected_filetype)
        expected_encoding = constants.ENCODING
        expected_open_type = 'r'
        mock_open.return_value.__enter__.side_effect = FileNotFoundError

        expected_contents = None

        # Act
        actual_contents = download.cache.retrieve_from_local_cache(expected_relative_path, expected_item, expected_filetype)

        # Assert
        self.assertEqual(expected_contents, actual_contents)
        mock_open.assert_called_once_with(expected_cache_file, expected_open_type, encoding=expected_encoding)


class TestStoreInLocalCache(unittest.TestCase):
    @unittest.mock.patch('os.makedirs')
    @unittest.mock.patch('builtins.open')
    def test_store_in_local_cache(self, mock_open, mock_makedirs):
        # Arrange
        expected_relative_path = 'foo/bar'
        expected_item = 'scp-123'
        expected_filetype = 'json'
        expected_cache_dir = os.path.join(constants.LOCAL_CACHE_BASE_PATH, expected_relative_path)
        expected_cache_file = os.path.join(constants.LOCAL_CACHE_BASE_PATH, expected_relative_path, expected_item + '.' + expected_filetype)
        expected_encoding = constants.ENCODING
        expected_exist_ok = True
        expected_open_type = 'w'
        expected_contents = 'contents'

        # Act
        actual_contents = download.cache.store_in_local_cache(expected_contents, expected_relative_path, expected_item, expected_filetype)

        # Assert
        mock_makedirs.assert_called_once_with(expected_cache_dir, exist_ok=expected_exist_ok)
        mock_open.assert_called_once_with(expected_cache_file, expected_open_type, encoding=expected_encoding)
        mock_open.return_value.__enter__.return_value.write.assert_called_once_with(expected_contents)
