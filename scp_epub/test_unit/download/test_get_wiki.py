import importlib
import json
import os
import unittest
import unittest.mock

import download.get_wiki
from constants import constants


class TestGetScpWiki(unittest.TestCase):
    @unittest.mock.patch('download.get_wiki.get_filtered_page_list')
    @unittest.mock.patch('download.get_wiki.get_complete_page')
    def test_get_scp_wiki(self, mock_get_complete_page, mock_get_filtered_page_list):
        # Arrange
        expected_page_list = [
            'scp-123', 'an-interesting-tale', 'something-else'
        ]
        expected_get_complete_page_calls = [
            unittest.mock.call(item)
            for item in expected_page_list
        ]

        expected_scp_wiki = [
            {
                constants.PAGE_PATH_KEY: item
            }
            for item in expected_page_list
        ]

        expected_category = "_default"
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
                "category": expected_category,
                "tags_to_download": expected_tags,
                "edge_cases": expected_edge_cases
            }
        }

        # Act
        actual_scp_wiki = download.get_wiki.get_scp_wiki()

        # Assert
        self.assertEqual(expected_scp_wiki, actual_scp_wiki)
        mock_get_filtered_page_list.assert_called_once_with(expected_book_definition)
        mock_get_complete_page.assert_has_calls(expected_get_complete_page_calls)


class TestGetCompletePage(unittest.TestCase):
    @unittest.mock.patch('download.wikidot_api.get_web_page')
    @unittest.mock.patch('download.wikidot_api.get_page_metadata')
    def test_get_complete_page_normal(self, mock_get_page_metadata, mock_get_web_page):
        # Arrange
        expected_page_name = 'a-funny-tale'

        expected_metadata = {
            'fullname': expected_page_name
        }
        expected_contents = 'contents'

        expected_page = {
            'fullname': expected_page_name,
            constants.ADDITIONAL_DATA_KEY: {
                constants.WEB_HTML_KEY: expected_contents
            }
        }

        expected_refresh = False
        expected_edge_case = False

        mock_get_page_metadata.return_value = expected_metadata
        mock_get_web_page.return_value = expected_contents

        # Act
        actual_page = download.get_wiki.get_complete_page(expected_page_name, refresh=expected_refresh, edge_case=expected_edge_case)

        # Assert
        self.assertEqual(expected_page, actual_page)
        mock_get_page_metadata.assert_called_once_with(expected_page_name, refresh=expected_refresh)
        mock_get_web_page.assert_called_once_with(expected_page_name, refresh=expected_refresh)

    @unittest.mock.patch('download.wikidot_api.get_web_page')
    @unittest.mock.patch('download.wikidot_api.get_page_metadata')
    def test_get_complete_page_refresh(self, mock_get_page_metadata, mock_get_web_page):
        # Arrange
        expected_page_name = 'a-funny-tale'

        expected_metadata = {
            'fullname': expected_page_name
        }
        expected_contents = 'contents'

        expected_page = {
            'fullname': expected_page_name,
            constants.ADDITIONAL_DATA_KEY: {
                constants.WEB_HTML_KEY: expected_contents
            }
        }

        expected_refresh = False
        expected_edge_case = False

        mock_get_page_metadata.return_value = expected_metadata
        mock_get_web_page.return_value = expected_contents

        # Act
        actual_page = download.get_wiki.get_complete_page(expected_page_name, refresh=expected_refresh, edge_case=expected_edge_case)

        # Assert
        self.assertEqual(expected_page, actual_page)
        mock_get_page_metadata.assert_called_once_with(expected_page_name, refresh=expected_refresh)
        mock_get_web_page.assert_called_once_with(expected_page_name, refresh=expected_refresh)

    @unittest.mock.patch('download.get_wiki.get_edge_case')
    @unittest.mock.patch('download.wikidot_api.get_web_page')
    @unittest.mock.patch('download.wikidot_api.get_page_metadata')
    def test_get_complete_page_edge_case(self, mock_get_page_metadata, mock_get_web_page, mock_get_edge_case):
        # Arrange
        expected_page_name = 'a-funny-tale'

        expected_metadata = {
            'fullname': expected_page_name
        }
        expected_contents = 'contents'

        expected_page = {
            'fullname': expected_page_name,
            constants.ADDITIONAL_DATA_KEY: {
                constants.WEB_HTML_KEY: expected_contents
            }
        }

        expected_refresh = False
        expected_edge_case = True

        mock_get_edge_case.return_value = expected_page

        # Act
        actual_page = download.get_wiki.get_complete_page(expected_page_name, refresh=expected_refresh, edge_case=expected_edge_case)

        # Assert
        self.assertEqual(expected_page, actual_page)
        mock_get_page_metadata.assert_not_called()
        mock_get_web_page.assert_not_called()


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
