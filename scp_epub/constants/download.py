import os

########################
# caching
BASE_PATH = os.path.join(os.path.dirname(__file__), '../../build')
DB_PATH = os.path.join(BASE_PATH, 'database')
PAGES_DIR = 'pages'
PAGE_LIST_FILE = 'page_list.json'

########################
# scraping
SITE_NAME = 'scp-wiki'
PAGE_CATEGORIES = ['_default']

API_KEY = 'WIKIDOT_API_KEY'
CLIENT_NAME = 'scp-epub'

# Actual rate limit is 240 calls per 60 seconds, we're being conservative
RATE_LIMIT_CALLS = 60
RATE_LIMIT_PERIOD = 30
