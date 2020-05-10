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

RATE_LIMIT_WEB_CALLS = 5
RATE_LIMIT_WEB_PERIOD = 5

ALLOWED_TAGS = ['scp', 'tale', 'hub']
