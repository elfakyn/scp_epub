import xmlrpc.client
import os
import json

import constants.wikidot
import constants.scp

from download import wikidot

def get_all_pages(bypass_cache=False):
    page_list = wikidot.get_page_list(site=constants.scp.SITE_NAME, categories=constants.scp.PAGE_CATEGORIES)
    scp_wiki = wikidot.get_multiple_page_data(site=constants.scp.SITE_NAME, pages=page_list)
