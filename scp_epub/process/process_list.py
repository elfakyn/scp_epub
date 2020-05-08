import process.filter
import constants.process

def pre_process(pages, fragments):
    pages = process.filter.filter_tags(pages, include_tags=constants.process.ALLOWED_TAGS)

    return pages
