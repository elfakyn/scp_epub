import getpass
import os
import parameterized.parameterized
import unittest

from constants import constants
import download.get_wiki


DOWNLOAD_PAGE_TEST_CASES_REGULAR = [
    ['scp-123'],
    ['scp-4000'],
    ['scp-173']
]

DOWNLOAD_PAGE_TEST_CASES_EDGE_CASES = [
    ['scp-3125']
]


class TestDownloadPage(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        os.environ[constants.API_KEY_VARIABLE] = getpass.getpass('Wikidot read-only API key: ')
        return super().setUpClass()

    @classmethod
    def tearDownClass(cls):
        del os.environ[constants.API_KEY_VARIABLE]
        return super().tearDownClass()

    def setUp(self):
        self.maxDiff = 500

    @parameterized.parameterized.expand(DOWNLOAD_PAGE_TEST_CASES_REGULAR)
    def test_download_page(self, expected_page_name):
        # Arrange
        expected_page = download.get_wiki.get_complete_page(expected_page_name, refresh=True)

        # Act
        actual_page = download.get_wiki.get_complete_page(expected_page_name, refresh=False)

        # Assert
        self.assertEqual(expected_page, actual_page)
