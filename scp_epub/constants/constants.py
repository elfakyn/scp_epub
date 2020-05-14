import os

########################
# caching
BASE_PATH = os.path.join(os.path.dirname(__file__), '../../build')
DB_PATH = os.path.join(BASE_PATH, 'database')
PAGES_DIR = 'pages'
HTML_DIR = 'web'
PAGE_LIST_DIR = 'lists'

CHARSET = 'utf-8'

########################
# scraping
SITE_NAME = 'scp-wiki'
SITE_HOST = 'http://scp-wiki.net'
SITE_DOWNLOAD_HOST = 'http://scp-wiki.net/printer--friendly'
PAGE_CATEGORY = '_default'

API_KEY = 'WIKIDOT_API_KEY'
CLIENT_NAME = 'scp-epub'

# Actual rate limit is 240 calls per 60 seconds, we're being conservative
RATE_LIMIT_CALLS = 60
RATE_LIMIT_PERIOD = 30

RATE_LIMIT_WEB_CALLS = 10
RATE_LIMIT_WEB_PERIOD = 5

ALLOWED_TAGS = ['scp', 'tale', 'hub']

EDGE_CASES_DIR = os.path.join(os.path.dirname(__file__), '../../edge_cases')
EDGE_CASES = [
    'scp-3125'
]

######################
# process

ADDITIONAL_DATA_KEY = 'scp_epub_additional_data'

WEB_HTML_KEY = 'web_html'

PAGE_PATH_KEY = 'fullname'
EDGE_CASE_KEY = 'substitute_html'

BS4_FORMAT = 'lxml'

PAGE_CONTENT_ID = 'page-content'

CLASSES_TO_REMOVE = [
    'heritage-rating-module',
    'heritage-emblem',
    'page-rate-widget-box',
    'scp-image-block',
    'image',
    'scp-image-caption',
    'footer-wikiwalk-nav'
]

TAGS_TO_REMOVE = [
    'img'
]

COLLAPSIBLE_BLOCK_CLASS = 'collapsible-block'
COLLAPSIBLE_BLOCK_LINK_CLASS = 'collapsible-block-link'
COLLAPSIBLE_BLOCK_CONTENT_CLASS = 'collapsible-block-content'

COLLAPSIBLE_CLASS_NEW = 'collapsible'
COLLAPSIBLE_TITLE_CLASS_NEW = 'collapsible-title'

BLOCKQUOTE_TAG = 'blockquote'
BLOCKQUOTE_CLASS_NEW = 'quote'

YUI_NAVSET_CLASS = 'yui-navset'
YUI_NAVSET_CLASS_NEW = 'tabview'
YUI_NAVSET_TAB_CLASS = 'yui-nav'
YUI_NAVSET_TAB_CLASS_NEW = 'tabview-tab'
YUI_NAVSET_TAB_TITLE_IDENTIFIER = 'em'
YUI_NAVSET_TAB_TITLE_CLASS_NEW = 'tab-title'

LINK_TAG = 'a'
HREF_PROPERTY = 'href'
LINK_CLASS_NEW = 'link'
LINK_EXTENSION = '.xhtml'
