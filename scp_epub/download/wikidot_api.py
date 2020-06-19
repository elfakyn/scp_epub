
import json
import os
import requests
import xmlrpc.client

import download.aws
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


def _get_page_data_undecorated(page, **kwargs):
    return NotImplemented

def _get_page_direct_web_download_undecorated(page, **kwargs):
    return NotImplemented
