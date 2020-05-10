import xmlrpc.client
import os
import json

import constants.download
import constants.process
import download.filter
import download.wikidot

def get_scp_wiki(bypass_cache_list=False, bypass_cache_pages=False, bypass_cache_web=False):
    page_list = download.wikidot.get_page_list(site=constants.download.SITE_NAME, category=constants.download.PAGE_CATEGORY, bypass_cache=bypass_cache_list)
    all_pages = download.wikidot.get_multiple_page_data(site=constants.download.SITE_NAME, pages=page_list, bypass_cache=bypass_cache_pages)

    wiki_pages = download.filter.filter_tags(all_pages, include_tags=constants.download.ALLOWED_TAGS)

    for page in wiki_pages:
        if constants.process.ADDITIONAL_DATA_KEY not in page:
            page[constants.process.ADDITIONAL_DATA_KEY] = {}

        if page[constants.process.PAGE_PATH_KEY] in constants.download.EDGE_CASES_DOWNLOAD_DIFFERENT_PAGE:
            web_html = download.wikidot.get_single_web_page(
                host=constants.download.EDGE_CASES_DOWNLOAD_DIFFERENT_PAGE[page[constants.process.PAGE_PATH_KEY]]['host'],
                path=constants.download.EDGE_CASES_DOWNLOAD_DIFFERENT_PAGE[page[constants.process.PAGE_PATH_KEY]]['page'],
                bypass_cache = bypass_cache_web
            )
        else:
            web_html = download.wikidot.get_single_web_page(
                host = constants.download.SITE_HOST,
                path = page[constants.process.PAGE_PATH_KEY],
                bypass_cache = bypass_cache_web
            )
            page[constants.process.ADDITIONAL_DATA_KEY][constants.process.EDGE_CASE_KEY] = True

        page[constants.process.ADDITIONAL_DATA_KEY][constants.process.WEB_HTML_KEY] = web_html

    return wiki_pages
