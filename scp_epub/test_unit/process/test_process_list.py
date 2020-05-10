import unittest
import unittest.mock

import process.process_list
import constants.process

class TestPreProcess(unittest.TestCase):
    @unittest.mock.patch('process.process_list.download.filter')
    def test_pre_process(self, mock_filter):
        # Arrange
        expected_pages = unittest.mock.MagicMock()
        expected_fragments = unittest.mock.MagicMock()
        expected_result = mock_filter.filter_tags.return_value
        expected_tags = constants.process.ALLOWED_TAGS

        # Act
        actual_result = process.process_list.pre_process(expected_pages, expected_fragments)

        # Assert
        mock_filter.filter_tags.assert_called_once_with(expected_pages, include_tags=expected_tags)
        self.assertEqual(expected_result, actual_result)
