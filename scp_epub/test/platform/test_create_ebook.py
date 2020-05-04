import unittest
import json
import os

from generate import generate_epub

class TestCreateEbook(unittest.TestCase):
    def test_create_ebook_single_page(self):
        # Arrange
        expected_page_path = '../samples/scp_055.json'
        with open(os.path.join(os.path.dirname(__file__), expected_page_path), 'r') as expected_page_file:
            expected_page_json = json.load(expected_page_file)

        expected_pages_json = [expected_page_json]
        expected_return_value = None

        # Act
        actual_return_value = generate_epub.create_ebook(expected_pages_json)

        # Assert
        self.assertEqual(expected_return_value, actual_return_value)
