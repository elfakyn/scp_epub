import os
import json
import functools
import re

from constants import constants


def normalize_string(raw_string):
    return re.sub('[^a-z0-9\-]', '_', raw_string)


def file_cache(relative_path, name_based_on_argument, filetype='json'):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            cache_file = os.path.join(constants.DB_PATH, relative_path, f'{normalize_string(kwargs[name_based_on_argument])}.{filetype}')

            if ('bypass_cache' in kwargs and kwargs['bypass_cache']) or not (os.path.exists(cache_file) and os.path.isfile(cache_file)):
                contents = func(*args, **kwargs)
                os.makedirs(os.path.dirname(cache_file), exist_ok=True)
                with open(cache_file, 'w') as target_file:
                    if filetype == 'json':
                        json.dump(contents, target_file, indent=2)
                    else:
                        target_file.write(contents)
            else:
                with open(cache_file, 'r') as target_file:
                    if filetype == 'json':
                        contents = json.load(target_file)
                    else:
                        contents = target_file.read()

            return contents
        return wrapper
    return decorator
