
import json
import os
from ratelimit import limits, sleep_and_retry
import requests
import xmlrpc.client

import download.aws
from download import cache
from constants import constants


_wikidot_client = None


def _create_wikidot_client():
    api_key = _get_api_key()
    return xmlrpc.client.ServerProxy(f'https://{constants.CLIENT_NAME}:{api_key}@{constants.RPC_ENDPOINT}')


def _get_api_key():
    if os.getenv(constants.USE_AWS_VARIABLE) == constants.USE_AWS_TRUE:
        return download.aws.get_api_key_from_secretsmanager()
    else:
        return os.getenv(constants.API_KEY_VARIABLE)


def _get_wikidot_client():
    global _wikidot_client
    if _wikidot_client is None:
        _wikidot_client = _create_wikidot_client()

    return _wikidot_client


def _get_list_of_pages_undecorated(category, **kwargs):
    client = _get_wikidot_client()
    list_of_pages = client.pages.select({
        'site': constants.SITE_NAME,
        'categories': [category]
    })
    return list_of_pages


def _get_page_metadata_undecorated(page, **kwargs):
    client = _get_wikidot_client()
    page_data = client.pages.get_meta({
        'site': constants.SITE_NAME,
        'pages': [page]
    })
    return page_data[page]


def _get_web_page_undecorated(page, **kwargs):
    web_page = requests.get(f'{constants.SITE_DOWNLOAD_HOST}/{page}')
    if web_page.status_code > 200:
        return None
    return web_page.content.decode(constants.ENCODING)


@cache.use_cache(constants.CACHE_PAGE_LIST_DIR, filetype=constants.CACHE_FILETYPE_JSON)
@sleep_and_retry
@limits(calls=constants.RATE_LIMIT_CALLS, period=constants.RATE_LIMIT_PERIOD)
def get_list_of_pages(*args, **kwargs):
    return _get_list_of_pages_undecorated(*args, **kwargs)


@cache.use_cache(constants.CACHE_PAGES_DIR, filetype=constants.CACHE_FILETYPE_JSON)
@sleep_and_retry
@limits(calls=constants.RATE_LIMIT_CALLS, period=constants.RATE_LIMIT_PERIOD)
def get_page_metadata(*args, **kwargs):
    return _get_page_metadata_undecorated(*args, **kwargs)


@cache.use_cache(constants.CACHE_HTML_DIR, filetype=constants.CACHE_FILETYPE_HTML)
@sleep_and_retry
@limits(calls=constants.RATE_LIMIT_WEB_CALLS, period=constants.RATE_LIMIT_WEB_PERIOD)
def get_web_page(*args, **kwargs):
    return _get_web_page_undecorated(*args, **kwargs)
