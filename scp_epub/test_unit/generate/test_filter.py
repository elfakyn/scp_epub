import unittest

import generate.filter

class TestFilterPages(unittest.TestCase):
    def test_filter_tags_no_rule(self):
        # Arrange
        expected_pages = [
            {'tags': ['scp', 'meta']},
            {'tags': ['tale', 'antimemetic']},
            {'tags': ['_sys']},
            {'tags': []},
            {'content': 'whatnot'},
            {}
        ]

        expected_filtered_pages = [
            {'tags': ['scp', 'meta']},
            {'tags': ['tale', 'antimemetic']},
            {'tags': ['_sys']},
            {'tags': []},
            {'content': 'whatnot'},
            {}
        ]

        expected_tag_filter = None

        # Act
        actual_filtered_pages = generate.filter.filter_tags(expected_pages)

        # Assert
        self.assertEqual(actual_filtered_pages, expected_filtered_pages)

    def test_filter_tags_include_tags(self):
        # Arrange
        expected_pages = [
            {'tags': ['scp', 'meta']},
            {'tags': ['hub', 'mtf']},
            {'tags': ['tale', 'antimemetic']},
            {'tags': ['_sys']},
            {'tags': []},
            {'content': 'whatnot'},
            {},
        ]

        expected_filtered_pages = [
            {'tags': ['scp', 'meta']},
            {'tags': ['tale', 'antimemetic']},
        ]

        expected_tag_filter = None
        expected_include_tags = ['scp', 'tale']

        # Act
        actual_filtered_pages = generate.filter.filter_tags(expected_pages, include_tags=expected_include_tags)

        # Assert
        self.assertEqual(actual_filtered_pages, expected_filtered_pages)
