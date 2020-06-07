import unittest
import unittest.mock
import os

import download.cache
import constants

class TestGetCachedContents(unittest.TestCase):
    @unittest.mock.patch('download.cache.retrieve_from_s3_cache')
    @unittest.mock.patch('download.cache.retrieve_from_local_cache')
    def test_get_cached_contents_locally(self, mock_retrieve_from_local_cache, mock_retrieve_from_s3_cache):
        # Arrange
        os.unsetenv(constants.USE_AWS_VARIABLE)
        expected_filetype = 'json'
        expected_relative_path = 'foo/bar/'
        expected_item = 'scp-123'

        # Act
        actual_contents = download.cache.get_cached_contents(expected_relative_path, expected_item, filetype=expected_filetype)

        # Assert
        self.assertEqual(actual_contents, mock_retrieve_from_local_cache.return_value)
        mock_retrieve_from_s3_cache.assert_not_called()
        mock_retrieve_from_local_cache.assert_called_once_with(expected_relative_path, expected_item, expected_filetype)

    @unittest.mock.patch('download.cache.retrieve_from_s3_cache')
    @unittest.mock.patch('download.cache.retrieve_from_local_cache')
    def test_get_cached_contents_s3(self, mock_retrieve_from_local_cache, mock_retrieve_from_s3_cache):
        # Arrange
        os.environ[constants.USE_AWS_VARIABLE] = constants.USE_AWS_TRUE
        expected_filetype = 'json'
        expected_relative_path = 'foo/bar/'
        expected_item = 'scp-123'

        # Act
        actual_contents = download.cache.get_cached_contents(expected_relative_path, expected_item, filetype=expected_filetype)

        # Assert
        self.assertEqual(actual_contents, mock_retrieve_from_s3_cache.return_value)
        mock_retrieve_from_s3_cache.assert_called_once_with(expected_relative_path, expected_item, expected_filetype)
        mock_retrieve_from_local_cache.assert_not_called()
