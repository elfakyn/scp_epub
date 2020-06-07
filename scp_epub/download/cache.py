import constants
import os

def get_cached_contents(relative_path, item, filetype=constants.CACHE_DEFAULT_FILETYPE):
    if os.getenv(constants.USE_AWS_VARIABLE) == constants.USE_AWS_TRUE:
        return retrieve_from_s3_cache(relative_path, item, filetype)
    else:
        return retrieve_from_local_cache(relative_path, item, filetype)

def retrieve_from_s3_cache(relative_path, item, filetype):
    return NotImplemented

def retrieve_from_local_cache(relative_path, item, filetype):
    return NotImplemented

def store_in_s3_cache(relative_path, item, filetype):
    return NotImplemented

def store_in_local_cache(relative_path, item, filetype):
    return NotImplemented
