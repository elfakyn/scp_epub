
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
