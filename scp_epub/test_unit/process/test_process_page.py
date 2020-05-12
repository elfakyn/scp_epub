import unittest
from parameterized import parameterized
import bs4

import process.process_page
import constants.process

class TestProcessPage(unittest.TestCase):
    def create_soup(self, html):
        return bs4.BeautifulSoup(html, "html.parser")

    @parameterized.expand([
        [
            'simple page content',
            '<html><head/><body>outside<div id="page-content">inside</div></body>',
            '<div id="page-content">inside</div>'
        ],
        [
            'not found',
            '<html><head/><body>outside</body>',
            'None'
        ],
    ])
    def test_get_page_content(self, reason, expected_html_string, expected_output_string):
        # Arrange
        expected_page_content_id = 'page-content'

        # Act
        actual_output = process.process_page.get_page_content(expected_html_string, page_content_id=expected_page_content_id)

        # Assert
        self.assertEqual(expected_output_string, str(actual_output))

    @parameterized.expand([
        [
            'nothing to remove',
            '<div class="qux">asdf</div>',
            '<div class="qux">asdf</div>'
        ],
        [
            'complete removal',
            '<div class="foo">asdf</div>',
            ''
        ],
        [
            'nested',
            'outside<div class="foo">qwq<div class="bar">asdf</div>qwrq</div>outside',
            'outsideoutside'
        ],
        [
            'reverse nested',
            'outside<div class="bar">qwq<div class="foo">asdf</div>qwrq</div>outside',
            'outsideoutside'
        ],
    ])
    def test_remove_by_class(self, reason, expected_html_string, expected_output_string):
        # Arrange
        expected_classses_to_remove = [
            'foo',
            'bar'
        ]

        expected_content = self.create_soup(expected_html_string)

        # Act
        actual_output = process.process_page.remove_by_class(expected_content, classes_to_remove=expected_classses_to_remove)

        # Assert
        self.assertEqual(expected_output_string, str(actual_output))

    @parameterized.expand([
        [
            'nothing to remove',
            '<a href="foobar">asdf</a>',
            '<a href="foobar">asdf</a>'
        ],
        [
            'complete removal',
            '<img></img>',
            ''
        ],
        [
            'simple removal',
            'outside<img src="foo.png" class="bar"></img>outside',
            'outsideoutside'
        ],
        [
            'singletag',
            'outside<img src="foo.png" class="bar"/>outside',
            'outsideoutside'
        ],
    ])
    def test_remove_by_tags(self, reason, expected_html_string, expected_output_string):
        # Arrange
        expected_tags_to_remove = [
            'img'
        ]

        expected_content = self.create_soup(expected_html_string)

        # Act
        actual_output = process.process_page.remove_by_tag(expected_content, tags_to_remove=expected_tags_to_remove)

        # Assert
        self.assertEqual(expected_output_string, str(actual_output))
