import os

ENCODING = 'utf-8'

########################
# AWS Execution
USE_AWS_VARIABLE = 'SCP_EPUB_USE_AWS'
USE_AWS_TRUE = 'TRUE'
S3_CACHE_BASE_PATH = 'cache/'
S3_BUCKET_VARIABLE = 'SCP_EPUB_S3_BUCKET'
API_KEY_SECRETSMANAGER_VARIABLE = 'SCP_EPUB_API_KEY_SECRET'

########################
# Local execution

LOCAL_CACHE_BASE_PATH = os.path.join(os.path.dirname(__file__), '../../build/cache')
API_KEY_VARIABLE = 'SCP_EPUB_WIKIDOT_API_KEY'

########################
# Caching paths

CACHE_FILETYPE_JSON = 'json'
CACHE_FILETYPE_HTML = 'html'
CACHE_DEFAULT_FILETYPE = CACHE_FILETYPE_JSON
CACHE_PAGES_DIR = 'pages/'
CACHE_HTML_DIR = 'web/'
CACHE_PAGE_LIST_DIR = 'lists/'

########################
# Scraping
SITE_NAME = 'scp-wiki'
SITE_HOST = 'http://scp-wiki.net'
SITE_DOWNLOAD_HOST = 'http://scp-wiki.net/printer--friendly'

CLIENT_NAME = 'scp-epub'
RPC_ENDPOINT = 'www.wikidot.com/xml-rpc-api.php'

# Wikidot rate limit is 240 calls per 60 seconds, we're being conservative
RATE_LIMIT_CALLS = 60
RATE_LIMIT_PERIOD = 30

RATE_LIMIT_WEB_CALLS = 10
RATE_LIMIT_WEB_PERIOD = 5

EDGE_CASES_DIR = os.path.join(os.path.dirname(__file__), '../../edge_cases')
EDGE_CASES_FILETYPE = 'json'

######################
# Processing pages

PAGE_PATH_KEY = 'fullname'
TITLE_SHOWN_KEY = 'title_shown'
TITLE_KEY = 'title'
CREATED_BY_KEY = 'created_by'
CREATED_AT_KEY = 'created_at'
TAGS_KEY = 'tags'
ADDITIONAL_DATA_KEY = 'scp_epub_additional_data'
WEB_HTML_KEY = 'web_html'

PROCESSED_NAME_KEY = 'name'
PROCESSED_TITLE_KEY = 'title'
PROCESSED_AUTHOR_KEY = 'created_by'
PROCESSED_CREATION_DATE_KEY = 'created_at'
PROCESSED_TAGS_KEY = 'tags'
PROCESSED_HTML_KEY = 'html'

EMPTY_TITLE = '███████████'
EMPTY_AUTHOR = 'Unknown'
EMPTY_TIMESTAMP = 'Unknown'


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

HREF_ATTRIBUTE = 'href'
ID_ATTRIBUTE = 'id'
EPUB_TYPE_ATTRIBUTE = 'epub:type'
ONCLICK_ATTRIBUTE = 'onclick'
CLASS_ATTRIBUTE = 'class'

LINK_CLASS_NEW = 'link'
LINK_EXTENSION = '.xhtml'

PAGE_TITLE_TAG = 'p'
PAGE_TITLE_CLASS = 'page-title'

FOOTNOTEREF_TAG = 'sup'
FOOTNOTEREF_CLASS = 'footnoteref'

FOOTNOTE_CLASS = 'footnote-footer'

EPUB_TYPE_FOOTNOTEREF = 'noteref'
EPUB_TYPE_FOOTNOTE = 'footnote'

FOOTNOTE_HREF_PATTERN = r"WIKIDOT\.page\.utils\.scrollToReference\('([a-zA-Z0-9-_]+)'\)"

######################
# Assembling pages

DEFAULT_BASED_ON = 'name'
