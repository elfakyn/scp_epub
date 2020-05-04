import xmlrpc.client
import os

import constants.wikidot

def get_api_key():
    return os.getenv(constants.wikidot.API_KEY_VAR)

def get_wikidot_client():
    api_key = get_api_key()
    wikidot_client = xmlrpc.client.ServerProxy(f'https://{constants.wikidot.CLIENT_NAME}:{api_key}@www.wikidot.com/xml-rpc-api.php')
    return wikidot_client

