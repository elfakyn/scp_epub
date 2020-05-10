import xmlrpc.client
import os
import json

import constants.download
import constants.process
import download.filter
import download.wikidot

def get_scp_wiki(bypass_cache=False):
    page_list = download.wikidot.get_page_list(site=constants.download.SITE_NAME, category=constants.download.PAGE_CATEGORY)
    all_pages = download.wikidot.get_multiple_page_data(site=constants.download.SITE_NAME, pages=page_list)

    wiki_pages = download.filter.filter_tags(all_pages, include_tags=constants.download.ALLOWED_TAGS)

    for page in wiki_pages:
        web_html = download.wikidot.get_single_web_page(host = constants.download.SITE_HOST, path=page[constants.process.PAGE_PATH_KEY])

        if constants.process.ADDITIONAL_DATA_KEY not in page:
            page[constants.process.ADDITIONAL_DATA_KEY] = {}

        page[constants.process.ADDITIONAL_DATA_KEY][constants.process.WEB_HTML_KEY] = web_html

    return wiki_pages
