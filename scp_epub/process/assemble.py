import bs4
import re

from constants import constants
import process.process_page


def process_all_pages(pages):
    page_names = [
        page[constants.PAGE_PATH_KEY]
        for page in pages
    ]

    results = []
    failures = []
    for page in pages:
        try:
            results.append(process.process_page.process_page(page, url_allow_list=page_names))
        except Exception as exception:
            failures.append(exception)

    return results, failures
