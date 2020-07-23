import download.wikidot_api
from constants import constants


def get_scp_wiki(tags_to_download, edge_cases):
    return NotImplemented


def get_complete_page(page_name, refresh=False, edge_case=False):
    if (edge_case):
        return NotImplemented

    page = download.wikidot_api.get_page_metadata(page_name, refresh=refresh)

    content = download.wikidot_api.get_web_page(page_name, refresh=refresh)

    page[constants.ADDITIONAL_DATA_KEY] = {
        constants.WEB_HTML_KEY: content
    }

    return page
