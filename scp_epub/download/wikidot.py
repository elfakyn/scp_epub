import xmlrpc.client
import os
import json
import requests
from ratelimit import limits, sleep_and_retry


from constants import constants
from download import cache

def get_api_key():
    return os.getenv(constants.API_KEY)


def get_wikidot_client():
    api_key = get_api_key()
    wikidot_client = xmlrpc.client.ServerProxy(f'https://{constants.CLIENT_NAME}:{api_key}@www.wikidot.com/xml-rpc-api.php')
    return wikidot_client


@cache.file_cache(constants.PAGE_LIST_DIR, name_based_on_argument="category")
@sleep_and_retry
@limits(calls=constants.RATE_LIMIT_CALLS, period=constants.RATE_LIMIT_PERIOD)
def get_page_list(*, site, category, bypass_cache=False):
    client = get_wikidot_client()
    page_list = client.pages.select({
        "site": site,
        "categories": [category]
    })
    return page_list


@cache.file_cache(constants.PAGES_DIR, name_based_on_argument="page")
@sleep_and_retry
@limits(calls=constants.RATE_LIMIT_CALLS, period=constants.RATE_LIMIT_PERIOD)
def get_page_data(*, site, page, bypass_cache=False):
    client = get_wikidot_client()
    page_data = client.pages.get_one({
        "site": site,
        "page": page
    })
    return page_data

@cache.file_cache(constants.HTML_DIR, name_based_on_argument="path", filetype='html')
@sleep_and_retry
@limits(calls=constants.RATE_LIMIT_WEB_CALLS, period=constants.RATE_LIMIT_WEB_PERIOD)
def get_single_web_page(*, host, path, bypass_cache=False):
    web_page = requests.get(f'{host}/{path}')
    if web_page.status_code > 200:
        return ''
    return web_page.content.decode(constants.CHARSET)

def get_multiple_page_data(*, site, pages, bypass_cache=False):
    return [get_page_data(site=site, page=page, bypass_cache=bypass_cache) for page in pages]
