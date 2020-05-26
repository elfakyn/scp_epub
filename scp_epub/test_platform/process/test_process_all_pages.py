import unittest
import unittest.mock

from parameterized import parameterized
import bs4
import json
import os
import io

import download.download_scp
import process.assemble
import constants.constants
import constants.test

class TestProcessAllPages(unittest.TestCase):
    def setUp(self):
        self.maxDiff = 500

    def test_process_all_pages(self):
        # Arrange
        expected_max_failures = 0
        expected_failures = []
        expected_pages = download.download_scp.get_scp_wiki()

        # Act
        actual_processed_pages, actual_failures = process.assemble.process_all_pages(expected_pages)

        # Assert
        self.assertLessEqual(len(actual_failures), expected_max_failures)
        self.assertEqual(expected_failures, actual_failures)
