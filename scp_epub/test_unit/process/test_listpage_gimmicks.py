import unittest
from parameterized import parameterized

import process.listpage_gimmicks

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
        actual_mapping = process.listpage_gimmicks.get_page_fragment_mapping(expected_fragment_list)

        # Assert
        self.assertEqual(expected_mapping, actual_mapping)

class TestListpages(unittest.TestCase):
    @parameterized.expand([
        [
            "NoneType",
            None,
            None
        ],
        [
            "No matches",
            "[[include component:heritage-rating]]\n\n**Item #:** SCP-055 \n\n**Object Class:** Keter \n\n",
            None
        ],
        [
            "Normal",
            "[[>]]\n[[module Rate]]\n[[/>]]\n\n[!--\n  This page is just a container, which can show one of several\n  fragment pages depending on the offset in the URL.\n\n  See: <http://www.scp-wiki.net/listpages-magic-and-you>\n\n  To edit the fragments which can appear here, visit:\n  Offset 0: <http://scp-wiki.wikidot.com/fragment:antimemetics-division-hub-main>\n  Offset 1: <http://scp-wiki.wikidot.com/fragment:antimemetics-division-hub-marion>\n  Offset 2: <http://scp-wiki.wikidot.com/fragment:antimemetics-division-hub-adam>\n--]\n\n[[module ListPages category=\"fragment\" parent=\".\" limit=\"1\" order=\"created_at\" offset=\"@URL|0\"]]\n%%content%%\n[[/module]]",
            {
                "category": "fragment",
                "parent": ".",
                "limit": "1",
                "order": "created_at",
                "offset": "@URL|0",
                "include_types": ["content"]
            }
        ],
        [
            "Missing items, extra whitespace",
            '[[ module LiStpAgEs   limit = "1"    order = "random"  category="fragme manet"\n\n]]%%content%%[[/module]]',
            {
                "category": "fragme manet",
                "parent": None,
                "limit": "1",
                "order": "random",
                "offset": None,
                "include_types": ["content"]
            }
        ],
        [
            "Junk surrounding content",
            '[[ module LiStpAgEs   limit = "1"    order = "random"  category="fragme manet"\n\n]]something else other stuff %%stuff%%\n %%info%%%%content%% again other stuff \n[[/module]]',
            {
                "category": "fragme manet",
                "parent": None,
                "limit": "1",
                "order": "random",
                "offset": None,
                "include_types": ["content"]
            }
        ],
        [
            "Nested items",
            '[[ module LiStpAgEs   limit = "1"    order = "random"  category="fragme manet"\n\n]]something else [[title]] [[/title]] [[stuff/]]other stuff %%stuff%%\n %%info%%%%content%% again other stuff \n[[/module]]',
            {
                "category": "fragme manet",
                "parent": None,
                "limit": "1",
                "order": "random",
                "offset": None,
                "include_types": ["content"]
            }
        ],
        [
            "List embeds",
            '[[ module listpages   limit = "1"    order = "random"  category="fragme manet"\n\n]]%%title%%[[/module]]',
            {
                "category": "fragme manet",
                "parent": None,
                "limit": "1",
                "order": "random",
                "offset": None,
                "include_types": ["title"]
            }
        ],
        [
            "list and content embeds",
            '[[ module listpages   limit = "1"    order = "random"  category="fragme manet"\n\n]]%%title%%%%content%%[[/module]]',
            {
                "category": "fragme manet",
                "parent": None,
                "limit": "1",
                "order": "random",
                "offset": None,
                "include_types": ["content", "title"]
            }
        ]
    ])

    def test_get_listpages_params(self, reason, expected_content, expected_results):
        # Arrange
        expected_params = ["category", "parent", "limit", "order", "offset"]
        expected_include_types = ["content", "title"]

        # Act
        actual_results = process.listpage_gimmicks.get_listpages_params(expected_content, params=expected_params, include_types=expected_include_types)

        # Assert
        self.assertEqual(expected_results, actual_results)
