import unittest
from parameterized import parameterized

import download.cache

NORMALIZATION_TEST_CASES = [
    ["fragment:three-farewells-aktus", "fragment_three-farewells-aktus"],
    ["scp-3125", "scp-3125"]
]

class TestNormalizeString(unittest.TestCase):
    @parameterized.expand(NORMALIZATION_TEST_CASES)
    def test_normalize_string(self, expected_raw_string, expected_normalized_string):
        # Arrange

        # Act
        actual_normalized_string = download.cache.normalize_string(expected_raw_string)

        # Assert
        self.assertEqual(expected_normalized_string, actual_normalized_string)
