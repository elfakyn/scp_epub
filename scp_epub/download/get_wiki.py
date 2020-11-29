import json
import os

import download.wikidot_api
from constants import constants


def get_scp_wiki(book_definition, refresh=False):
    raise NotImplementedError


def filter_page_list(book_definition):
    raise NotImplementedError


def get_page_metadata(page_name, refresh=False, edge_case=False):
    raise NotImplementedError


def enrich_metadata_with_page_content(page_metadata, refresh=False, edge_case=False):
    raise NotImplementedError


def get_edge_case(page_name):
    json_file = os.path.join(constants.EDGE_CASES_DIR, page_name + '.' + constants.EDGE_CASES_FILETYPE)
    with open(json_file, 'r', encoding=constants.ENCODING) as edge_case:
        page = json.load(edge_case)

    return page
