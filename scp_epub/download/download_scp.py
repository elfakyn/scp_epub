import xmlrpc.client
import os
import json

import constants.download

from download import wikidot

def get_scp_wiki(bypass_cache=False):
    page_list = wikidot.get_page_list(site=constants.download.SITE_NAME, category=constants.download.PAGE_CATEGORY)
    fragment_list = wikidot.get_page_list(site=constants.download.SITE_NAME, category=constants.download.FRAGMENT_CATEGORY)
    scp_pages = wikidot.get_multiple_page_data(site=constants.download.SITE_NAME, pages=page_list)
    scp_fragments = wikidot.get_multiple_page_data(site=constants.download.SITE_NAME, pages=fragment_list)
    return scp_pages, scp_fragments
