
import json
import os
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


def get_wikidot_client():
    global _wikidot_client
    if _wikidot_client is None:
        _wikidot_client = _create_wikidot_client()

    return _wikidot_client
