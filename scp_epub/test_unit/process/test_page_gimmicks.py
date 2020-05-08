import unittest

import process.page_gimmicks

class TestFragmentGimmicks(unittest.TestCase):
    def test_get_page_fragment_mapping(self):
        # Arrange
        expected_fragment_list = [
            {
                'fullname': 'fragment:djkaktus-s-proposal-iii-11',
                'parent_fullname': 'djkaktus-s-proposal-iii'
            },
            {
                'fullname': 'fragment:djkaktus-s-proposal-iii-8',
                'parent_fullname': 'djkaktus-s-proposal-iii'
            },
            {
                'fullname': 'fragment:antimemetics-division-hub-main',
                'parent_fullname': 'antimemetics-division-hub'
            },
            {
                'fullname': 'fragment:no-parent',
                'parent_fullname': None
            },
            {
                'fullname': 'fragment:nested-parent-1',
                'parent_fullname': 'main'
            },
            {
                'fullname': 'fragment:nested-parent-2',
                'parent_fullname': 'fragment:nested-parent-1'
            },
        ]

        expected_mapping = {
            'djkaktus-s-proposal-iii': ['fragment:djkaktus-s-proposal-iii-11', 'fragment:djkaktus-s-proposal-iii-8'],
            'antimemetics-division-hub': ['fragment:antimemetics-division-hub-main'],
            'main': ['fragment:nested-parent-1'],
            'fragment:nested-parent-1': ['fragment:nested-parent-2']
        }

        # Act
        actual_mapping = process.page_gimmicks.get_page_fragment_mapping(expected_fragment_list)

        # Assert
        self.assertEqual(expected_mapping, actual_mapping)
