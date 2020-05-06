import xmlrpc.client
import os
import json

import constants.wikidot
import constants.scp

from download import wikidot

def get_scp_wiki(bypass_cache=False):
    page_list = wikidot.get_page_list(site=constants.download.SITE_NAME, categories=constants.download.PAGE_CATEGORIES)
    scp_wiki = wikidot.get_multiple_page_data(site=constants.download.SITE_NAME, pages=page_list)
    return scp_wiki
