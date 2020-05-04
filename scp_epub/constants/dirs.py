import os

BASE_PATH = os.path.join(os.path.dirname(__file__), '../../build')
DB_PATH = os.path.join(BASE_PATH, 'database')
EPUB_PATH = os.path.join(BASE_PATH, 'epub_unpacked')


PAGES_DIR = 'pages'

PAGE_LIST_FILE = 'page_list.json'

EPUB_OUTPUT_FILE = os.path.join(BASE_PATH, 'scp_wiki.epub')

RESOURCE_PATH = os.path.join(os.path.dirname(__file__), '../resources')
