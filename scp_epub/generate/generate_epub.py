from ebooklib import epub
from lxml.etree import ParserError

import generate.convert_links

import constants.epub
import constants.dirs
import constants.scp

import logging
logger = logging.getLogger()
logger.setLevel(logging.WARN)

def is_valid_page(page_json):
    if len(page_json[constants.scp.CONTENT_KEY]) < constants.scp.MINIMUM_CONTENT_LENGTH:
        return False

    return True

def create_page(page_json):
    if not is_valid_page(page_json):
        return None
    try:
        page = epub.EpubHtml(
            title = page_json[constants.scp.TITLE_KEY],
            file_name=f'{page_json[constants.scp.FILENAME_KEY]}{constants.epub.FILENAME_EXTENSION}',
            content = page_json[constants.scp.CONTENT_KEY],
            lang = constants.epub.LANG,
        )
        logger.debug(f'{page_json[constants.scp.FILENAME_KEY]}: {len(page_json[constants.scp.CONTENT_KEY])}')
        page.add_link(href=constants.epub.STYLESHEET_LOCAL, rel = constants.epub.STYLESHEET_REL, type = constants.epub.STYLESHEET_TYPE)
        return page
    except ParserError:
        logger.warn(f'PARSE FAIL: {page_json[constants.scp.FILENAME_KEY]}')
        return None

def get_stylesheet():
    with open(constants.dirs.STYLESHEET_FILE) as stylesheet_file:
        stylesheet = stylesheet_file.read()
    return stylesheet

def create_ebook(pages_json):
    book = epub.EpubBook()

    pages = [
        page for page in [
            create_page(page_json)
            for page_json in pages_json
            if any(
                tag in constants.scp.ALLOWED_TAGS
                for tag in page_json[constants.scp.TAGS_KEY]
            )
        ]
        if page is not None
    ]
    for page in pages:
        book.add_item(page)

    book.add_item(epub.EpubNcx())
    book.add_item(epub.EpubNav())
    book.spine = ['nav'] + pages

    stylesheet = get_stylesheet()
    css = epub.EpubItem(uid="style", file_name=constants.epub.STYLESHEET_LOCAL, media_type=constants.epub.STYLESHEET_TYPE, content=stylesheet)
    book.add_item(css)

    epub.write_epub(constants.dirs.EPUB_OUTPUT_FILE, book, {'plugins': [generate.convert_links.MyeLinks()]})

    return NotImplemented
