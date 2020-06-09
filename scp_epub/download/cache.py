import functools
import json
import os

from constants import constants
import download.aws
import download.utils


def use_cache(relative_path, filetype=constants.CACHE_DEFAULT_FILETYPE):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            normalized_item = download.utils.normalize_string(args[0])

            if 'refresh' in kwargs and kwargs['refresh'] is True:
                cached_contents = None
            else:
                cached_contents = get_cached_contents(relative_path, normalized_item, filetype)

            if cached_contents is not None:
                return cached_contents
            else:
                contents = func(*args, **kwargs)
                set_cached_contents(contents, relative_path, normalized_item, filetype)
                return contents

        return wrapper
    return decorator


def get_cached_contents(relative_path, item, filetype):
    if os.getenv(constants.USE_AWS_VARIABLE) == constants.USE_AWS_TRUE:
        content_string = download.aws.retrieve_from_s3_cache(relative_path, item, filetype)
    else:
        content_string = retrieve_from_local_cache(relative_path, item, filetype)

    if filetype == 'json':
        return json.loads(content_string)
    else:
        return content_string


def set_cached_contents(contents, relative_path, item, filetype):
    if filetype == 'json':
        content_string = json.dumps(contents)
    else:
        content_string = contents

    if os.getenv(constants.USE_AWS_VARIABLE) == constants.USE_AWS_TRUE:
        download.aws.store_in_s3_cache(content_string, relative_path, item, filetype)
    else:
        store_in_local_cache(content_string, relative_path, item, filetype)


def retrieve_from_local_cache(relative_path, item, filetype):
    try:
        filename = item + '.' + filetype
        file_location = os.path.join(constants.LOCAL_CACHE_BASE_PATH, relative_path, filename)
        with open(file_location, 'r', encoding=constants.ENCODING) as local_file:
            contents = local_file.read()

        return contents
    except FileNotFoundError:
        return None


def store_in_local_cache(contents, relative_path, item, filetype):
    filename = item + '.' + filetype
    file_dir = os.path.join(constants.LOCAL_CACHE_BASE_PATH, relative_path)
    file_location = os.path.join(file_dir, filename)

    os.makedirs(file_dir, exist_ok=True)
    with open(file_location, 'w', encoding=constants.ENCODING) as local_file:
        local_file.write(contents)
