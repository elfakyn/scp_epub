import importlib
import json
import os
import unittest
import unittest.mock

import download.get_wiki
from constants import constants


class TestGetScpWiki(unittest.TestCase):
    def test_get_scp_wiki(self):
        # Arrange
        expected_refresh = False

        expected_categories = "_default"
        expected_tags = [
            "scp",
            "tale",
            "hub",
            "supplement"
        ]
        expected_edge_cases = [
            "scp-3125"
        ]
        expected_book_definition = {
            "download": {
                "categories": expected_categories,
                "tags_to_download": expected_tags,
                "edge_cases": expected_edge_cases
            }
        }

        # Act
        actual_scp_wiki = download.get_wiki.get_scp_wiki(expected_book_definition, expected_refresh)

        # Assert


class TestGetEdgeCase(unittest.TestCase):
    @unittest.mock.patch('builtins.open')
    def test_retrieve_from_local_cache(self, mock_open):
        # Arrange
        expected_relative_path = constants.EDGE_CASES_DIR
        expected_item = 'scp-1234'
        expected_filetype = constants.EDGE_CASES_FILETYPE
        expected_file = os.path.join(expected_relative_path, expected_item + '.' + constants.EDGE_CASES_FILETYPE)
        expected_encoding = constants.ENCODING
        expected_open_type = 'r'
        expected_contents = {'a': 'b'}
        expected_encoded_contents = json.dumps(expected_contents)
        mock_open.return_value.__enter__.return_value.read.return_value = expected_encoded_contents

        # Act
        actual_contents = download.get_wiki.get_edge_case(expected_item)

        # Assert
        self.assertEqual(expected_contents, actual_contents)
        mock_open.assert_called_once_with(expected_file, expected_open_type, encoding=expected_encoding)
