import unittest

import constants.process
import json

import download.download_scp
import process.filter
import process.listpage_gimmicks

class TestListpagesEdgeCases(unittest.TestCase):
    def test_listpages_stats(self):
        # Arrange
        expected_edge_case_count = 20

        expected_pages, expected_fragments = download.download_scp.get_scp_wiki()
        expected_filtered_pages = process.filter.filter_tags(expected_pages, include_tags=constants.process.ALLOWED_TAGS)
        expected_listpages_params = {
            page['fullname']: process.listpage_gimmicks.get_listpages_params(
                page["content"], params=constants.process.LISTPAGES_PARAMS, include_types=constants.process.LISTPAGES_INCLUDE_TYPES)
            for page in expected_filtered_pages
        }

        # Act
        actual_edge_cases = [
            page_name for (page_name, listpages_params) in expected_listpages_params.items()
            if listpages_params is not None and listpages_params["include_types"] == []
        ]

        # Assert
        self.assertLessEqual(len(actual_edge_cases), expected_edge_case_count, f'Too many ListPages edge cases: {actual_edge_cases}')
