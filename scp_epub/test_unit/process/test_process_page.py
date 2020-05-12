import unittest
from parameterized import parameterized

import process.process_page

class TestProcessPage(unittest.TestCase):
    @parameterized.expand([
        [
            'simple page content',
            '<html><head/><body>outside<div id="page-content">inside</div></body>',
            '<div id="page-content">inside</div>'
        ],
    ])
    def test_get_page_content(self, reason, expected_html, expected_output_string):
        # Arrange
        expected_page_content_id = 'page-content'

        # Act
        actual_output = process.process_page.get_page_contents(expected_html, page_content_id=expected_page_content_id)

        # Assert
        self.assertEqual(expected_output_string, str(actual_output))
