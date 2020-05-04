import xmlrpc.client
import os
import json
from ratelimit import limits, sleep_and_retry

import constants.wikidot
import constants.dirs
from download import cache

def get_api_key():
    return os.getenv(constants.wikidot.API_KEY)


def get_wikidot_client():
    api_key = get_api_key()
    wikidot_client = xmlrpc.client.ServerProxy(f'https://{constants.wikidot.CLIENT_NAME}:{api_key}@www.wikidot.com/xml-rpc-api.php')
    return wikidot_client


@cache.file_cache(constants.dirs.PAGE_LIST_FILE)
@sleep_and_retry
@limits(calls=constants.wikidot.RATE_LIMIT_CALLS, period=constants.wikidot.RATE_LIMIT_PERIOD)
def get_page_list(*, site, categories, bypass_cache=False):
    client = get_wikidot_client()
    page_list = client.pages.select({
        "site": site,
        "categories": categories
    })
    return page_list


@cache.file_cache(constants.dirs.PAGES_DIR, use_page_name=True)
@sleep_and_retry
@limits(calls=constants.wikidot.RATE_LIMIT_CALLS, period=constants.wikidot.RATE_LIMIT_PERIOD)
def get_page_data(*, site, page, bypass_cache=False):
    client = get_wikidot_client()
    page_data = client.pages.get_one({
        "site": site,
        "page": page
    })
    return page_data


def get_multiple_page_data(*, site, pages, bypass_cache=False):
    return [get_page_data(site=site, page=page, bypass_cache=bypass_cache) for page in pages]
