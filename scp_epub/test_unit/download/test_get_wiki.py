import importlib
import os
import unittest
import unittest.mock

import download.get_wiki
from constants import constants


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
        mock_get_page_metadata.assert_called_once_with(expected_page_name)
        mock_get_web_page.assert_called_once_with(expected_page_name)

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
        expected_edge_case = True

        mock_get_page_metadata.return_value = expected_metadata
        mock_get_web_page.return_value = expected_contents

        # Act
        actual_page = download.get_wiki.get_complete_page(expected_page_name, refresh=expected_refresh, edge_case=expected_edge_case)

        # Assert
        self.assertEqual(expected_page, actual_page)
        mock_get_page_metadata.assert_not_called()
        mock_get_web_page.assert_not_called()
