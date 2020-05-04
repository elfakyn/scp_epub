# This is shamelessly stolen straight from http://docs.sourcefabric.org/projects/ebooklib/en/latest/plugins.html

try:
    from urlparse import urlparse, urljoin
except ImportError:
    from urllib.parse import urlparse, urljoin

from lxml import  etree

from ebooklib.plugins.base import BasePlugin
from ebooklib.utils import parse_html_string

class MyeLinks(BasePlugin):
    NAME = 'My Links'

    def html_before_write(self, book, chapter):
        try:
            tree = parse_html_string(chapter.content)
        except:
            return

        root = tree.getroottree()

        if len(root.find('body')) != 0:
            body = tree.find('body')

            for _link in body.xpath('//a'):
                _u = urlparse(_link.get('href', ''))

                # Let us care only for internal links at the moment
                if _u.scheme == '':
                    if _u.path != '':
                        _link.set('href', '%s.xhtml' % _u.path.lstrip('/'))

                    if _u.fragment != '':
                        _link.set('href', urljoin(_link.get('href'), '#%s' % _u.fragment))

                    if _link.get('name') != None:
                        _link.set('id', _link.get('name'))
                        etree.strip_attributes(_link, 'name')

        chapter.content = etree.tostring(tree, pretty_print=True, encoding='utf-8')
