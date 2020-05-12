import xmlrpc.client
import os
import json

from constants import constants
from constants import constants
import download.filter
import download.wikidot


def get_scp_wiki(bypass_cache_list=False, bypass_cache_pages=False, bypass_cache_web=False, tag_filter=constants.ALLOWED_TAGS):
    page_list = download.wikidot.get_page_list(site=constants.SITE_NAME, category=constants.PAGE_CATEGORY, bypass_cache=bypass_cache_list)
    all_pages = download.wikidot.get_multiple_page_data(site=constants.SITE_NAME, pages=page_list, bypass_cache=bypass_cache_pages)

    wiki_pages = download.filter.filter_tags(all_pages, include_tags=tag_filter)

    for page in wiki_pages:
        if constants.ADDITIONAL_DATA_KEY not in page:
            page[constants.ADDITIONAL_DATA_KEY] = {}

        if page[constants.PAGE_PATH_KEY] in constants.EDGE_CASES:
            with open(os.path.join(constants.EDGE_CASES_DIR, f'{page[constants.PAGE_PATH_KEY]}.html'), 'r') as target_file:
                web_html = target_file.read()

                page[constants.ADDITIONAL_DATA_KEY][constants.EDGE_CASE_KEY] = True
        else:
            web_html = download.wikidot.get_single_web_page(
                host = constants.SITE_HOST,
                path = page[constants.PAGE_PATH_KEY],
                bypass_cache = bypass_cache_web
            )

        page[constants.ADDITIONAL_DATA_KEY][constants.WEB_HTML_KEY] = web_html

    return wiki_pages
