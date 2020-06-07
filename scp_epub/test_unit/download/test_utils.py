import download.utils
import unittest
from parameterized import parameterized


NORMALIZATION_TEST_CASES = [
    ["fragment:three-farewells-aktus", "fragment_three-farewells-aktus"],
    ["scp-3125", "scp-3125"]
]

class TestNormalizeString(unittest.TestCase):
    @parameterized.expand(NORMALIZATION_TEST_CASES)
    def test_normalize_string(self, expected_raw_string, expected_normalized_string):
        # Arrange

        # Act
        actual_normalized_string = download.utils.normalize_string(expected_raw_string)

        # Assert
        self.assertEqual(expected_normalized_string, actual_normalized_string)


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
        actual_filtered_pages = download.utils.filter_tags(expected_pages)

        # Assert
        self.assertEqual(expected_filtered_pages, actual_filtered_pages)

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
        actual_filtered_pages = download.utils.filter_tags(expected_pages, include_tags=expected_include_tags)

        # Assert
        self.assertEqual(expected_filtered_pages, actual_filtered_pages)
