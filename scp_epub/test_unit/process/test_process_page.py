import unittest
from parameterized import parameterized
import bs4

import process.process_page
from constants import constants

class TestProcessPage(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None

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


class TestProcessContentFunctions(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None

    def create_soup(self, html):
        return bs4.BeautifulSoup(html, "html.parser")

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
        expected_output = None

        # Act
        actual_output = process.process_page.remove_classes(expected_content, classes_to_remove=expected_classses_to_remove)

        # Assert
        self.assertEqual(expected_output_string, str(expected_content))
        self.assertEqual(expected_output, actual_output)

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
        expected_output = None

        # Act
        actual_output = process.process_page.remove_tags(expected_content, tags_to_remove=expected_tags_to_remove)

        # Assert
        self.assertEqual(expected_output_string, str(expected_content))
        self.assertEqual(expected_output, actual_output)

    @parameterized.expand([
        [
            'scp-047',
            '''outside<div class="collapsible-block"><div class="collapsible-block-folded"><a class="collapsible-block-link" href="javascript:;">&gt; Show details</a></div><div class="collapsible-block-unfolded" style="display:none"><div class="collapsible-block-unfolded-link"><a class="collapsible-block-link" href="javascript:;">&lt; Hide details</a></div><div class="collapsible-block-content"><ul><li><strong>Pathogenicity:</strong> Severe skin colonisation around sebaceous glands. Modification of skin pH to levels that become toxic to skin cells. Massive inflammation and immune cell infiltration. Eventual breakdown of skin structure leading to sepsis.</li><li><strong>Transmission:</strong> Transmitted by skin-to-skin contact. Can remain active on inorganic surfaces for up to five hours.</li><li><strong>Lethality:</strong> Approximately 40% mortality rate. Runs its course in 2-6 weeks. Very visible symptoms within 5-10 hours; contagious within 2-5 hours.</li><li><strong>Handling:</strong> As soon as visible symptoms form, victims must be quarantined. Deceased victims should be incinerated.</li></ul></div></div></div>''',
            '''outside<div class="collapsible"><p class="collapsible-title">&gt; Show details</p><ul><li><strong>Pathogenicity:</strong> Severe skin colonisation around sebaceous glands. Modification of skin pH to levels that become toxic to skin cells. Massive inflammation and immune cell infiltration. Eventual breakdown of skin structure leading to sepsis.</li><li><strong>Transmission:</strong> Transmitted by skin-to-skin contact. Can remain active on inorganic surfaces for up to five hours.</li><li><strong>Lethality:</strong> Approximately 40% mortality rate. Runs its course in 2-6 weeks. Very visible symptoms within 5-10 hours; contagious within 2-5 hours.</li><li><strong>Handling:</strong> As soon as visible symptoms form, victims must be quarantined. Deceased victims should be incinerated.</li></ul></div>'''
        ],
    ])
    def test_unwrap_collapsible_blocks(self, reason, expected_html_string, expected_output_string):
        # Arrange
        expected_content = self.create_soup(expected_html_string)
        expected_output = None

        # Act
        actual_output = process.process_page.unwrap_collapsible_blocks(expected_content)

        # Assert
        self.assertEqual(expected_output_string, str(expected_content))
        self.assertEqual(expected_output, actual_output)

    @parameterized.expand([
        [
            'simple',
            '''outside<blockquote><p>I love peace. I'd kill to preserve it</p></blockquote>''',
            '''outside<div class="quote"><p>I love peace. I'd kill to preserve it</p></div>'''
        ],
    ])
    def test_divify_blockquotes(self, reason, expected_html_string, expected_output_string):
        # Arrange
        expected_content = self.create_soup(expected_html_string)
        expected_output = None

        # Act
        actual_output = process.process_page.divify_blockquotes(expected_content)

        # Assert
        self.assertEqual(expected_output_string, str(expected_content))
        self.assertEqual(expected_output, actual_output)

    @parameterized.expand([
        [
            'two with nested div',
            '''<div id="wiki-tabview-03edd57ee60acc9ffdcd1050bfe0a7c2" class="yui-navset"><ul class="yui-nav"><li class="selected"><a href="javascript:;"><em>Effect 1509-1</em></a></li><li><a href="javascript:;"><em>Effect 1509-2</em></a></li></ul><div class="yui-content"><div id="wiki-tab-0-0"><div class="inner-div" style="width:300px;"><p>A specimen.</p></div><p>Effect 1509-1 typically.</p></div><div id="wiki-tab-0-1" style="display:none"><p>Effect SCP-1509-2 occurs.</p></div></div></div>''',
            '''<div class="tabview"><div class="tabview-tab"><p class="tab-title">Effect 1509-1</p><div class="inner-div" style="width:300px;"><p>A specimen.</p></div><p>Effect 1509-1 typically.</p></div><div class="tabview-tab"><p class="tab-title">Effect 1509-2</p><p>Effect SCP-1509-2 occurs.</p></div></div>'''
        ],
    ])
    def test_unwrap_navset(self, reason, expected_html_string, expected_output_string):
        # Arrange
        expected_content = self.create_soup(expected_html_string)
        expected_output = None

        # Act
        actual_output = process.process_page.unwrap_yui_navset(expected_content)

        # Assert
        self.assertEqual(expected_output_string, str(expected_content))
        self.assertEqual(expected_output, actual_output)
