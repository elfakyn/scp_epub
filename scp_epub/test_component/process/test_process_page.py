import unittest
import unittest.mock

from parameterized import parameterized
import bs4
import json
import os
import io

import process.process_page
from constants import constants

TEST_COMPONENT_PROCESS_PAGE_CASES_DIR = 'test_process_page_cases'


class TestProcessPage(unittest.TestCase):
    def setUp(self):
        self.maxDiff = 0

    @parameterized.expand([
        [
            'SCP-1257',
            'scp-1257.html',
            'scp-1257_converted.html',
            ['scp-173', 'scp-682'],
        ],
    ])
    def test_process_page(self, expected_page_title, expected_web_html_file, expected_processed_html_file, expected_url_allow_list):
        # Arrange

        with open(os.path.join(os.path.dirname(__file__), TEST_COMPONENT_PROCESS_PAGE_CASES_DIR, expected_web_html_file), 'r', encoding=constants.ENCODING) as target_file:
            expected_web_html = target_file.read()

        with open(os.path.join(os.path.dirname(__file__), TEST_COMPONENT_PROCESS_PAGE_CASES_DIR, expected_processed_html_file), 'r', encoding=constants.ENCODING) as target_file:
            expected_processed_html = target_file.read()

        # Act
        actual_processed_html = process.process_page.process_page_html(expected_web_html, expected_page_title, expected_url_allow_list)

        # Assert
        self.assertEqual(expected_processed_html, actual_processed_html)
