import re

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

def get_listpages_params(content):
    module_content = re.search(
        '\[\[\s*module\s*listpages([^[\]]*)\]\]((?:[^[]|\[\[(?!\/module\]\]))*)\[\[\s*\/module\s*\]\]',
        content,
        flags=re.S | re.M | re.I)

    if module_content is None:
        return None

    else:
        params = {}
        if re.search("%%content%%", module_content.group(2), flags=re.S | re.M | re.I) is not None:
            params["embeds_content"] = True
        else:
            params["embeds_content"] = False
        for param in ["limit", "order", "parent", "category", "offset"]:
            match = re.search(f'{param}\s*=\s*"([^"]*)"', module_content.group(1), flags=re.S | re.M | re.I)
            if match is None:
                params[param] = None
            else:
                params[param] = match.group(1)
        return params
