import os
import json
import functools

import constants.dirs

def file_cache(relative_path, use_page_name=False):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            absolute_path = os.path.join(constants.download.DB_PATH, relative_path)
            if use_page_name:
                absolute_path = os.path.join(absolute_path, f'{kwargs["page"]}.json')

            if ('bypass_cache' in kwargs and kwargs['bypass_cache']) or not (os.path.exists(absolute_path) and os.path.isfile(absolute_path)):
                contents = func(*args, **kwargs)
                os.makedirs(os.path.dirname(absolute_path), exist_ok=True)
                with open(absolute_path, 'w+') as target_file:
                    json.dump(contents, target_file, indent=2)
            else:
                with open(absolute_path, 'r+') as target_file:
                    contents = json.load(target_file)

            return contents
        return wrapper
    return decorator
