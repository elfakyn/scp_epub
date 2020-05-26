import unittest
import unittest.mock

from parameterized import parameterized
import bs4
import json
import os
import io

import process.assemble
import constants.constants
import constants.test

class TestProcessAllPages(unittest.TestCase):
    @unittest.mock.patch('process.process_page.process_page')
    def test_process_all_pages(self, mock_process_page):
        # Arrange
        expected_page_names = ['a-1', 'b-2']
        expected_processed_pages = ['result 1', 'result 2']
        expected_failures = []


        mock_process_page.side_effect = expected_processed_pages

        expected_pages = [
            {
                constants.constants.PAGE_PATH_KEY: page_name
            }
            for page_name in expected_page_names
        ]

        expected_calls = [
            unittest.mock.call(
                {
                    constants.constants.PAGE_PATH_KEY: page_name
                },
                url_allow_list = expected_page_names
            )
            for page_name in expected_page_names
        ]

        # Act
        actual_processed_pages, actual_failures = process.assemble.process_all_pages(expected_pages)

        # Assert
        self.assertEqual(expected_processed_pages, actual_processed_pages)
        self.assertEqual(expected_failures, actual_failures)
        mock_process_page.assert_has_calls(expected_calls)

    @unittest.mock.patch('process.process_page.process_page')
    def test_process_all_pages_errors(self, mock_process_page):
        # Arrange
        expected_page_names = ['a-1', 'b-2']
        expected_processed_pages = ['result 2']

        expected_error = ValueError()
        expected_failures = [expected_error]

        mock_process_page.side_effect = [expected_error, 'result 2']

        expected_pages = [
            {
                constants.constants.PAGE_PATH_KEY: page_name
            }
            for page_name in expected_page_names
        ]

        expected_calls = [
            unittest.mock.call(
                {
                    constants.constants.PAGE_PATH_KEY: page_name
                },
                url_allow_list=expected_page_names
            )
            for page_name in expected_page_names
        ]

        # Act
        actual_processed_pages, actual_failures = process.assemble.process_all_pages(expected_pages)

        # Assert
        self.assertEqual(expected_processed_pages, actual_processed_pages)
        self.assertEqual(expected_failures, actual_failures)
        mock_process_page.assert_has_calls(expected_calls)
