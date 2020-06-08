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


def set_cached_contents(contents, relative_path, item, filetype=constants.CACHE_DEFAULT_FILETYPE):
    if filetype == 'json':
        content_string = json.dumps(contents)
    else:
        content_string = contents

    if os.getenv(constants.USE_AWS_VARIABLE) == constants.USE_AWS_TRUE:
        store_in_s3_cache(content_string, relative_path, item, filetype)
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


def retrieve_from_s3_cache(relative_path, item, filetype):
    return NotImplemented


def store_in_s3_cache(contents, relative_path, item, filetype):
    return NotImplemented
