import os
import json
import functools
import re

import constants.download


def normalize_string(raw_string):
    return re.sub('[^a-z0-9\-]', '_', raw_string)


def file_cache(relative_path, name_based_on_argument):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            cache_file = os.path.join(constants.download.DB_PATH, relative_path, f'{normalize_string(kwargs[name_based_on_argument])}.json')

            if ('bypass_cache' in kwargs and kwargs['bypass_cache']) or not (os.path.exists(cache_file) and os.path.isfile(cache_file)):
                contents = func(*args, **kwargs)
                os.makedirs(os.path.dirname(cache_file), exist_ok=True)
                with open(cache_file, 'w+') as target_file:
                    json.dump(contents, target_file, indent=2)
            else:
                with open(cache_file, 'r+') as target_file:
                    contents = json.load(target_file)

            return contents
        return wrapper
    return decorator
