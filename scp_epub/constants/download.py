import os

########################
# caching
BASE_PATH = os.path.join(os.path.dirname(__file__), '../../build')
DB_PATH = os.path.join(BASE_PATH, 'database')
PAGES_DIR = 'pages'
HTML_DIR = 'web'
PAGE_LIST_DIR = 'lists'

########################
# scraping
SITE_NAME = 'scp-wiki'
SITE_HOST = 'http://scp-wiki.net/printer--friendly'
PAGE_CATEGORY = '_default'
FRAGMENT_CATEGORY = 'fragment'

API_KEY = 'WIKIDOT_API_KEY'
CLIENT_NAME = 'scp-epub'

# Actual rate limit is 240 calls per 60 seconds, we're being conservative
RATE_LIMIT_CALLS = 60
RATE_LIMIT_PERIOD = 30

RATE_LIMIT_WEB_CALLS = 10
RATE_LIMIT_WEB_PERIOD = 5

ALLOWED_TAGS = ['scp', 'tale', 'hub']

EDGE_CASES_DOWNLOAD_DIFFERENT_PAGE = {
    'scp-3125': {
        'host': 'http://scpsandbox2.wdfiles.com',
        'page': 'local--html/scp-3125-unencrypted/19a551ea86bc6d2bd95b6e4cc40758497b7a00e0-11702915221798099076/scpsandbox2.wikidot.com/'
    }
}
