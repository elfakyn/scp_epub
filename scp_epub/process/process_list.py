import download.filter
import constants.process

def pre_process(pages, fragments):
    pages = download.filter.filter_tags(pages, include_tags=constants.process.ALLOWED_TAGS)

    return pages
