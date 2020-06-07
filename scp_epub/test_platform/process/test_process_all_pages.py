import unittest
import unittest.mock

from parameterized import parameterized
import bs4
import json
import os
import io

import download.download_scp
import process.assemble

class TestProcessAllPages(unittest.TestCase):
    def setUp(self):
        self.maxDiff = 500

    def test_process_all_pages(self):
        # Arrange
        expected_max_failures = 0
        expected_failures = []
        expected_definition = {
            "download": {
                "download_tags": [
                    "scp",
                    "tale",
                    "hub",
                    "supplement"
                ],
                "edge_cases": [
                    "scp-3125"
                ]
            },
        }
        expected_pages = download.get_wiki.get_pages_from_book_definition(expected_definition)

        # Act
        actual_processed_pages, actual_failures = process.assemble.process_all_pages(expected_pages)

        # Assert
        self.assertLessEqual(len(actual_failures), expected_max_failures)
        self.assertEqual(expected_failures, actual_failures)
