import re

import constants.process

def get_page_fragment_mapping(fragment_list):
    mapping = {}
    for fragment in fragment_list:
        if fragment['parent_fullname'] is None:
            continue
        if fragment['parent_fullname'] in mapping:
            mapping[fragment['parent_fullname']].append(fragment['fullname'])
        else:
            mapping[fragment['parent_fullname']] = [fragment['fullname']]

    return mapping

def get_listpages_results(listpages_params, full_page_list, full_fragment_list):
    return NotImplemented

def get_listpages_params(content, params = constants.process.LISTPAGES_PARAMS, include_types=constants.process.LISTPAGES_INCLUDE_TYPES):
    if content is None:
        return None

    module_content = re.search(
        '\[\[\s*module\s*listpages([^[\]]*)\]\]((?:[^[]|\[\[(?!\/module\]\]))*)\[\[\s*\/module\s*\]\]',
        content,
        flags=re.S | re.M | re.I)

    if module_content is None:
        return None

    else:
        results = {}
        results["include_types"] = []
        for include_type in include_types:
            if re.search(f'%%{include_type}%%', module_content.group(2), flags=re.S | re.M | re.I) is not None:
                results["include_types"].append(include_type)
        for param in params:
            match = re.search(f'{param}\s*=\s*"([^"]*)"', module_content.group(1), flags=re.S | re.M | re.I)
            if match is None:
                results[param] = None
            else:
                results[param] = match.group(1)
        return results
