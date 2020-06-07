from constants import constants
import os
import json

def get_cached_contents(relative_path, item, filetype=constants.CACHE_DEFAULT_FILETYPE):
    if os.getenv(constants.USE_AWS_VARIABLE) == constants.USE_AWS_TRUE:
        content_string = retrieve_from_s3_cache(relative_path, item, filetype)
    else:
        content_string = retrieve_from_local_cache(relative_path, item, filetype)

    if filetype == 'json':
        return json.loads(content_string)
    else:
        return content_string

def retrieve_from_s3_cache(relative_path, item, filetype):
    return NotImplemented

def retrieve_from_local_cache(relative_path, item, filetype):
    return NotImplemented

def store_in_s3_cache(relative_path, item, filetype):
    return NotImplemented

def store_in_local_cache(relative_path, item, filetype):
    return NotImplemented
