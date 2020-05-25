import unittest
import unittest.mock

from parameterized import parameterized
import bs4
import json

import process.process_page
from constants import constants

class TestProcessPage(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None

    @unittest.mock.patch('process.process_page.process_page_html')
    def test_process_page(self, mock_process_page_html):
        # Arrange
        expected_url_allow_list = None

        expected_fullname = "personal-log-of-iceberg"
        expected_title = "Personal Log of █████ \"Iceberg\" ████"
        expected_title_shown = "Personal Log of █████ \"Iceberg\" ████"
        expected_created_at = "2008-10-16T21:06:01+00:00"
        expected_created_by = "unknown"
        expected_tags = [
            "doctor-kondraki",
            "doctor-iceberg",
            "doctor-gears",
            "tale"
        ]
        expected_web_html = "<html>blablabla</html>"
        expected_substitute_html = None
        expected_processed_html = "<div>processed html</div>"

        expected_processed_title = expected_title_shown

        mock_process_page_html.return_value = expected_processed_html

        expected_page = {
            "fullname": expected_fullname,
            "created_at": expected_created_at,
            "created_by": expected_created_by,
            "updated_at": "2019-09-15T01:08:04+00:00",
            "updated_by": "Elogee FishTruck",
            "title": expected_title,
            "title_shown": expected_title_shown,
            "parent_fullname": None,
            "tags": expected_tags,
            "rating": 38,
            "revisions": 36,
            "parent_title": None,
            "content": "",
            "children": 0,
            "comments": 5,
            "commented_at": "2015-09-16T18:15:32+00:00",
            "commented_by": "Decibelles",
            "scp_epub_additional_data": {
                "web_html": expected_web_html
            }
        }

        expected_processed_page = {
            "name": expected_fullname,
            "title": expected_processed_title,
            "created_by": expected_created_by,
            "created_at": expected_created_at,
            "tags": expected_tags,
            "html": expected_processed_html,
        }

        # Act
        actual_processed_page = process.process_page.process_page(expected_page, url_allow_list=expected_url_allow_list)

        # Assert
        mock_process_page_html.assert_called_once_with(expected_web_html, expected_processed_title, url_allow_list = expected_url_allow_list)
        self.assertEqual(expected_processed_page, actual_processed_page)

    @unittest.mock.patch('process.process_page.process_page_html')
    def test_process_page_edge_case(self, mock_process_page_html):
        # Arrange
        expected_url_allow_list = None

        expected_fullname = "personal-log-of-iceberg"
        expected_title = "Personal Log of █████ \"Iceberg\" ████"
        expected_title_shown = "Personal Log of █████ \"Iceberg\" ████"
        expected_created_at = "2008-10-16T21:06:01+00:00"
        expected_created_by = "unknown"
        expected_tags = [
            "doctor-kondraki",
            "doctor-iceberg",
            "doctor-gears",
            "tale"
        ]
        expected_web_html = None
        expected_substitute_html = "<html>blablabla</html>"
        expected_processed_html = "<div>processed html</div>"

        expected_processed_title = expected_title_shown

        mock_process_page_html.return_value = expected_processed_html

        expected_page = {
            "fullname": expected_fullname,
            "created_at": expected_created_at,
            "created_by": expected_created_by,
            "updated_at": "2019-09-15T01:08:04+00:00",
            "updated_by": "Elogee FishTruck",
            "title": expected_title,
            "title_shown": expected_title_shown,
            "parent_fullname": None,
            "tags": expected_tags,
            "rating": 38,
            "revisions": 36,
            "parent_title": None,
            "content": "",
            "children": 0,
            "comments": 5,
            "commented_at": "2015-09-16T18:15:32+00:00",
            "commented_by": "Decibelles",
            "scp_epub_additional_data": {
                "substitute_html": expected_substitute_html
            }
        }

        expected_processed_page = {
            "name": expected_fullname,
            "title": expected_processed_title,
            "created_by": expected_created_by,
            "created_at": expected_created_at,
            "tags": expected_tags,
            "html": expected_processed_html,
        }

        # Act
        actual_processed_page = process.process_page.process_page(expected_page, url_allow_list=expected_url_allow_list)

        # Assert
        mock_process_page_html.assert_called_once_with(expected_substitute_html, expected_processed_title, url_allow_list=expected_url_allow_list)
        self.assertEqual(expected_processed_page, actual_processed_page)

class TestGetPageContent(unittest.TestCase):
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
        [
            'multiple_items_spurious_newline',
            '''<div class="collapsible-block"><div class="collapsible-block-folded"><a class="collapsible-block-link" href="javascript:;">+ Document S-1257-11</a></div><div class="collapsible-block-unfolded" style="display:none"><div class="collapsible-block-unfolded-link"><a class="collapsible-block-link" href="javascript:;">- Document S-1257-11</a></div><div class="collapsible-block-content">\n<blockquote><ul><li>Season 3, Episode 3, “Tyler’s Date”: Episode manifests three months after initial containment. One line in the script implies the assassination of American President Jimmy Carter in late 1978 or early 1979.</li><li>Season 4, Episode 1, “Bad Touch pt. 2”: Second half of a “special episode” ending season three. Eric, a young classmate of Danny’s, is the target of a sexual predator using what appears to be anomalous items manufactured by Doctor Wondertainment to lure his victims.</li><li>Season 5, Episode 10, “The Senior Trip”: Episode mentions a scandal where 10 members of the UK House of Commons had been publicly revealed as members of a cult that bears a strong resemblance to the Church of the Broken God.</li><li>Season 6, Episode 1, “The Freshmen”: The title of SCP-1257 is changed to <em>Danny</em>. The premise of the series changes as well, dropping the Tyler character and sending Danny to college in New York City with five of his classmates from High School.<sup class="footnoteref"><a class="footnoteref" href="javascript:;" id="footnoteref-4" onclick="WIKIDOT.page.utils.scrollToReference('footnote-4')">4</a></sup> The University Lab appears to have specimens of SCP-███, SCP-███ and SCP-███.</li><li>Season 6, Episode 11, “The ████████”: Plot of the episode concerns Eric’s suspicions that one of their dormmates might be secretly one of the “████████.” This turns out to be a misunderstanding. From context, the “████████” appear to prey on young women and have become endemic in [REDACTED] and seem to be the result of a containment breach of [REDACTED] in Mexico City.</li><li>Season 7, Episode 2, “Eric’s Midterm Caper”: When this episode manifested in SCP-1257-3-12, a new advertisement appeared during the second break for Marshall, Carter, and Dark Ltd. The ad promoted [REDACTED] services for [REDACTED].</li><li>Season 10, Episode 1, “The Job Hunt”: Hour-long “special” introducing another change in premise.<sup class="footnoteref"><a class="footnoteref" href="javascript:;" id="footnoteref-5" onclick="WIKIDOT.page.utils.scrollToReference('footnote-5')">5</a></sup> One scene implies that the Global Occult Coalition has become public enough to run “want ads” in the local newspaper.</li><li>Season 10, Episode 2, “The New Guy”: The show’s title is officially changed to <em>Agent Danny of the SCP</em>.<sup class="footnoteref"><a class="footnoteref" href="javascript:;" id="footnoteref-6" onclick="WIKIDOT.page.utils.scrollToReference('footnote-6')">6</a></sup> Danny has been employed as Level 1 security at Site-19, and through a series of mishaps, prevents a containment breach of <a href="/scp-173">SCP-173</a>.</li><li>Season 10, Episode 5, “D-Class Act”: Danny mis-hears a co-worker’s conversation and becomes convinced he has been mistakenly reassigned to D-Class by the HR Department.</li><li>Season 10, Episode 11, “Leaping Lizards”: [REDACTED] <a href="/scp-682">SCP-682</a> [REDACTED].</li></ul><p><em><strong>Note:</strong> Details of SCP-1257 episodes past Season 10 are only available with the approval of the Intelligence Department.</em></p></blockquote></div></div></div>''',
            '''<div class="collapsible"><p class="collapsible-title">+ Document S-1257-11</p>\n<blockquote><ul><li>Season 3, Episode 3, “Tyler’s Date”: Episode manifests three months after initial containment. One line in the script implies the assassination of American President Jimmy Carter in late 1978 or early 1979.</li><li>Season 4, Episode 1, “Bad Touch pt. 2”: Second half of a “special episode” ending season three. Eric, a young classmate of Danny’s, is the target of a sexual predator using what appears to be anomalous items manufactured by Doctor Wondertainment to lure his victims.</li><li>Season 5, Episode 10, “The Senior Trip”: Episode mentions a scandal where 10 members of the UK House of Commons had been publicly revealed as members of a cult that bears a strong resemblance to the Church of the Broken God.</li><li>Season 6, Episode 1, “The Freshmen”: The title of SCP-1257 is changed to <em>Danny</em>. The premise of the series changes as well, dropping the Tyler character and sending Danny to college in New York City with five of his classmates from High School.<sup class="footnoteref"><a class="footnoteref" href="javascript:;" id="footnoteref-4" onclick="WIKIDOT.page.utils.scrollToReference('footnote-4')">4</a></sup> The University Lab appears to have specimens of SCP-███, SCP-███ and SCP-███.</li><li>Season 6, Episode 11, “The ████████”: Plot of the episode concerns Eric’s suspicions that one of their dormmates might be secretly one of the “████████.” This turns out to be a misunderstanding. From context, the “████████” appear to prey on young women and have become endemic in [REDACTED] and seem to be the result of a containment breach of [REDACTED] in Mexico City.</li><li>Season 7, Episode 2, “Eric’s Midterm Caper”: When this episode manifested in SCP-1257-3-12, a new advertisement appeared during the second break for Marshall, Carter, and Dark Ltd. The ad promoted [REDACTED] services for [REDACTED].</li><li>Season 10, Episode 1, “The Job Hunt”: Hour-long “special” introducing another change in premise.<sup class="footnoteref"><a class="footnoteref" href="javascript:;" id="footnoteref-5" onclick="WIKIDOT.page.utils.scrollToReference('footnote-5')">5</a></sup> One scene implies that the Global Occult Coalition has become public enough to run “want ads” in the local newspaper.</li><li>Season 10, Episode 2, “The New Guy”: The show’s title is officially changed to <em>Agent Danny of the SCP</em>.<sup class="footnoteref"><a class="footnoteref" href="javascript:;" id="footnoteref-6" onclick="WIKIDOT.page.utils.scrollToReference('footnote-6')">6</a></sup> Danny has been employed as Level 1 security at Site-19, and through a series of mishaps, prevents a containment breach of <a href="/scp-173">SCP-173</a>.</li><li>Season 10, Episode 5, “D-Class Act”: Danny mis-hears a co-worker’s conversation and becomes convinced he has been mistakenly reassigned to D-Class by the HR Department.</li><li>Season 10, Episode 11, “Leaping Lizards”: [REDACTED] <a href="/scp-682">SCP-682</a> [REDACTED].</li></ul><p><em><strong>Note:</strong> Details of SCP-1257 episodes past Season 10 are only available with the approval of the Intelligence Department.</em></p></blockquote></div>'''

        ]
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

    @parameterized.expand([
        [
            'no links',
            '''asdf''',
            '''asdf'''
        ],
        [
            'non-href anchors',
            '''asdf<a>asdf</a>asdf<a name="asdf">asdf</a>''',
            '''asdf<a>asdf</a>asdf<a name="asdf">asdf</a>'''
        ],
        [
            'expanded internal link',
            '''<p>This is by <a href="http://scp-wiki.net/scp-3281">Autonomic (AARS821)</a> RAISA. <strong>AAR</strong></p>''',
            '''<p>This is by <a href="scp-3281.xhtml">Autonomic (AARS821)</a> RAISA. <strong>AAR</strong></p>'''
        ],
        [
            'other internal link',
            '''<p>This is by <a href="http://scp-wiki.net/scp-1234">Autonomic (AARS821)</a> RAISA. <strong>AAR</strong></p>''',
            '''<p>This is by <a href="scp-1234.xhtml">Autonomic (AARS821)</a> RAISA. <strong>AAR</strong></p>'''
        ],
        [
            'implicit internal link',
            '''<p>This is by <a href="/scp-3281">Autonomic (AARS821)</a> RAISA. <strong>AAR</strong></p>''',
            '''<p>This is by <a href="scp-3281.xhtml">Autonomic (AARS821)</a> RAISA. <strong>AAR</strong></p>'''
        ],
        [
            'external link',
            '''<p>This is by <a href="http://wikipedia.org/scp-3281">Autonomic (AARS821)</a> RAISA. <strong>AAR</strong></p>''',
            '''<p>This is by Autonomic (AARS821) RAISA. <strong>AAR</strong></p>'''
        ],
        [
            'multiple links',
            '''<p>This is by <a href="/scp-3281">Autonomic (AARS821)</a> RAISA. <strong>AAR</strong></p>asdf<p>This is by <a href="http://scp-wiki.net/scp-3281">Autonomic (AARS821)</a> RAISA. <strong>AAR</strong></p><p>This is by <a href="http://wikipedia.org/scp-3281">Autonomic (AARS821)</a> RAISA. <strong>AAR</strong></p>''',
            '''<p>This is by <a href="scp-3281.xhtml">Autonomic (AARS821)</a> RAISA. <strong>AAR</strong></p>asdf<p>This is by <a href="scp-3281.xhtml">Autonomic (AARS821)</a> RAISA. <strong>AAR</strong></p><p>This is by Autonomic (AARS821) RAISA. <strong>AAR</strong></p>'''
        ],
        [
            'not in book',
            '''<a href="http://scp-wiki.net/scp-11111">asdf</a>''',
            '''asdf'''
        ],
        [
            'not in book, implicit',
            '''<a href="/scp-11111">asdf</a>''',
            '''asdf'''
        ],
        [
            'ignore footnote links',
            '''<p><strong>Special Containment Procedures:</strong> SCP-1-800-J can be easily and safely stored anywhere in your home! SCP-1-800-J can be used safely by any member of the family<sup class="footnoteref"><a epub:type="noteref" href="#footnote-1" id="footnoteref-1">1</a></sup>! No stains! No mess! No permanent physical or mental trauma!</p> <p>Companies like Marshall, Carter, and Dark Ltd. and Dr. Wondertainment would charge you FORTUNES for similar products. But SCP-1-800-J is only $19.99! That's right! SCP-1-800-J is only $19.99<sup class="footnoteref"><a epub:type="noteref" href="#footnote-2" id="footnoteref-2">2</a></sup>!</p> <div class="footnotes-footer"> <div class="title">Footnotes</div> <div class="footnote-footer" epub:type="footnote" id="footnote-1"><a href="#footnoteref-1">1</a>. Even Grandma!</div> <div class="footnote-footer" epub:type="footnote" id="footnote-2"><a href="#footnoteref-2">2</a>. Plus shipping and handling</div> </div>''',
            '''<p><strong>Special Containment Procedures:</strong> SCP-1-800-J can be easily and safely stored anywhere in your home! SCP-1-800-J can be used safely by any member of the family<sup class="footnoteref"><a epub:type="noteref" href="#footnote-1" id="footnoteref-1">1</a></sup>! No stains! No mess! No permanent physical or mental trauma!</p> <p>Companies like Marshall, Carter, and Dark Ltd. and Dr. Wondertainment would charge you FORTUNES for similar products. But SCP-1-800-J is only $19.99! That's right! SCP-1-800-J is only $19.99<sup class="footnoteref"><a epub:type="noteref" href="#footnote-2" id="footnoteref-2">2</a></sup>!</p> <div class="footnotes-footer"> <div class="title">Footnotes</div> <div class="footnote-footer" epub:type="footnote" id="footnote-1"><a href="#footnoteref-1">1</a>. Even Grandma!</div> <div class="footnote-footer" epub:type="footnote" id="footnote-2"><a href="#footnoteref-2">2</a>. Plus shipping and handling</div> </div>'''
        ]
    ])
    def test_fix_links(self, reason, expected_html_string, expected_output_string):
        # Arrange
        expected_url_allow_list = ['scp-3281', 'scp-1234']

        expected_content = self.create_soup(expected_html_string)
        expected_output = None

        # Act
        actual_output = process.process_page.fix_links(expected_content, url_allow_list=expected_url_allow_list)

        # Assert
        self.assertEqual(expected_output_string, str(expected_content))
        self.assertEqual(expected_output, actual_output)

    @parameterized.expand([
        [
            'no links',
            '''asdf''',
            '''asdf'''
        ],
        [
            'non-href anchors',
            '''asdf<a>asdf</a>asdf<a name="asdf">asdf</a>''',
            '''asdf<a>asdf</a>asdf<a name="asdf">asdf</a>'''
        ],
        [
            'not in book, implicit',
            '''<a href="/scp-11111">asdf</a>''',
            '''<a href="scp-11111.xhtml">asdf</a>'''
        ],
    ])
    def test_fix_links_no_whitelist(self, reason, expected_html_string, expected_output_string):
        # Arrange
        expected_url_allow_list = None

        expected_content = self.create_soup(expected_html_string)
        expected_output = None

        # Act
        actual_output = process.process_page.fix_links(expected_content, url_allow_list=expected_url_allow_list)

        # Assert
        self.assertEqual(expected_output_string, str(expected_content))
        self.assertEqual(expected_output, actual_output)

    @parameterized.expand([
        [
            'simple add title',
            '''asdf''',
            '''<p class="page-title">Hi there!</p>asdf'''
        ],
        [
            'some other tags',
            '''<div class="foo">asdf</div>''',
            '''<p class="page-title">Hi there!</p><div class="foo">asdf</div>'''
        ]
    ])
    def test_add_title(self, reason, expected_html_string, expected_output_string):
        # Arrange
        expected_title = 'Hi there!'

        expected_content = self.create_soup(expected_html_string)
        expected_output = None

        # Act
        actual_output = process.process_page.add_title(expected_content, expected_title)

        # Assert
        self.assertEqual(expected_output_string, str(expected_content))
        self.assertEqual(expected_output, actual_output)

    @parameterized.expand([
        [
            'just the noteref',
            '''<sup class="footnoteref"><a id="footnoteref-1"href="javascript:;" class="footnoteref"onclick="WIKIDOT.page.utils.scrollToReference('footnote-1')">1</a></sup>''',
            '''<sup class="footnoteref"><a epub:type="noteref" href="#footnote-1" id="footnoteref-1">1</a></sup>'''
        ],
        [
            'just the footnote',
            '''<div class="footnote-footer" id="footnote-1"><a href="javascript:;"onclick="WIKIDOT.page.utils.scrollToReference('footnoteref-1')">1</a>. Even Grandma!</div>''',
            '''<div class="footnote-footer" epub:type="footnote" id="footnote-1"><a href="#footnoteref-1">1</a>. Even Grandma!</div>'''
        ],
        [
            'noterefs and footnotes',
            '''<p><strong>Special Containment Procedures:</strong> SCP-1-800-J can be easily and safely stored anywhere in your home! SCP-1-800-J can be used safely by any member of the family<sup class="footnoteref"><a id="footnoteref-1" href="javascript:;" class="footnoteref" onclick="WIKIDOT.page.utils.scrollToReference('footnote-1')">1</a></sup>! No stains! No mess! No permanent physical or mental trauma!</p> <p>Companies like Marshall, Carter, and Dark Ltd. and Dr. Wondertainment would charge you FORTUNES for similar products. But SCP-1-800-J is only $19.99! That's right! SCP-1-800-J is only $19.99<sup class="footnoteref"><a id="footnoteref-2" href="javascript:;" class="footnoteref" onclick="WIKIDOT.page.utils.scrollToReference('footnote-2')">2</a></sup>!</p> <div class="footnotes-footer"> <div class="title">Footnotes</div> <div class="footnote-footer" id="footnote-1"><a href="javascript:;" onclick="WIKIDOT.page.utils.scrollToReference('footnoteref-1')">1</a>. Even Grandma!</div> <div class="footnote-footer" id="footnote-2"><a href="javascript:;" onclick="WIKIDOT.page.utils.scrollToReference('footnoteref-2')">2</a>. Plus shipping and handling</div> </div>''',
            '''<p><strong>Special Containment Procedures:</strong> SCP-1-800-J can be easily and safely stored anywhere in your home! SCP-1-800-J can be used safely by any member of the family<sup class="footnoteref"><a epub:type="noteref" href="#footnote-1" id="footnoteref-1">1</a></sup>! No stains! No mess! No permanent physical or mental trauma!</p> <p>Companies like Marshall, Carter, and Dark Ltd. and Dr. Wondertainment would charge you FORTUNES for similar products. But SCP-1-800-J is only $19.99! That's right! SCP-1-800-J is only $19.99<sup class="footnoteref"><a epub:type="noteref" href="#footnote-2" id="footnoteref-2">2</a></sup>!</p> <div class="footnotes-footer"> <div class="title">Footnotes</div> <div class="footnote-footer" epub:type="footnote" id="footnote-1"><a href="#footnoteref-1">1</a>. Even Grandma!</div> <div class="footnote-footer" epub:type="footnote" id="footnote-2"><a href="#footnoteref-2">2</a>. Plus shipping and handling</div> </div>'''
        ],
    ])
    def test_fix_footnotes(self, reason, expected_html_string, expected_output_string):
        # Arrange
        expected_content = self.create_soup(expected_html_string)
        expected_output = None

        # Act
        actual_output = process.process_page.fix_footnotes(expected_content)

        # Assert
        self.assertEqual(expected_output_string, str(expected_content))
        self.assertEqual(expected_output, actual_output)

class TestHelpers(unittest.TestCase):
    def test_get_filename_from_name(self):
        # Arrange
        expected_name = 'scp-1234'
        expected_filename = 'scp-1234.xhtml'

        # Act
        actual_filename = process.process_page.get_filename(expected_name)

        # Assert
        self.assertEqual(expected_filename, actual_filename)
