import json
import os

import download.wikidot_api
from constants import constants


def get_scp_wiki(tags_to_download, edge_cases):
    return NotImplemented


def get_complete_page(page_name, refresh=False, edge_case=False):
    if (edge_case):
        return get_edge_case(page_name)

    page = download.wikidot_api.get_page_metadata(page_name, refresh=refresh)

    content = download.wikidot_api.get_web_page(page_name, refresh=refresh)

    page[constants.ADDITIONAL_DATA_KEY] = {
        constants.WEB_HTML_KEY: content
    }

    return page


def get_edge_case(page_name):
    json_file = os.path.join(constants.EDGE_CASES_DIR, page_name + '.' + constants.EDGE_CASES_FILETYPE)
    with open(json_file, 'r', encoding=constants.ENCODING) as edge_case:
        page = json.load(edge_case)

    return page
