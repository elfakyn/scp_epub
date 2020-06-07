import unittest
import os

import download.cache
import constants

class TestGetCachedContentsLocally(unittest.TestCase):
    @unittest.mock.patch('download.aws.retrieve_from_s3')
    def test_get_cached_contents_aws(self, mock_retrieve_from_s3):
        # Arrange
        os.environ[constants.
        expected_filetype = 'json'
        expected_relative_path = 'contents/'

        # Act
        actual_contents = download.cache.get_cached_contents(expected_relative_path, filetype=expected_filetype)

        # Assert
        mock_retrieve_from_s3.assert_called_with(expected_relative_path, expected_filetype)
