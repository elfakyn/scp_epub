import bs4
import re

from constants import constants

def process_page(page, url_allow_list = None):
    if page[constants.TITLE_SHOWN_KEY] is not None:
        title = page[constants.TITLE_SHOWN_KEY]
    elif page[constants.TITLE_KEY] is not None:
        title = page[constants.TITLE_KEY]
    else:
        title = constants.EMPTY_TITLE

    if constants.WEB_HTML_KEY in page[constants.ADDITIONAL_DATA_KEY]:
        html = page[constants.ADDITIONAL_DATA_KEY][constants.WEB_HTML_KEY]
    else:
        html = page[constants.ADDITIONAL_DATA_KEY][constants.EDGE_CASE_KEY]

    processed_html = process_page_html(html, title, url_allow_list=url_allow_list)

    return {
        constants.PROCESSED_NAME_KEY: page[constants.PAGE_PATH_KEY],
        constants.PROCESSED_TITLE_KEY: title,
        constants.CREATED_AT_KEY: page[constants.PROCESSED_CREATION_DATE_KEY],
        constants.CREATED_BY_KEY: page[constants.PROCESSED_AUTHOR_KEY],
        constants.TAGS_KEY: page[constants.PROCESSED_TAGS_KEY],
        constants.PROCESSED_HTML_KEY: processed_html
    }

def process_page_html(web_html, page_title, url_allow_list=None):
    content = get_page_content(web_html)

    remove_classes(content)
    remove_tags(content)

    unwrap_collapsible_blocks(content)
    unwrap_yui_navset(content)

    divify_blockquotes(content)

    fix_footnotes(content)
    fix_links(content, url_allow_list)

    add_title(content, page_title)

    return str(content)


def get_page_content(page_html, page_content_id=constants.PAGE_CONTENT_ID):
    html = bs4.BeautifulSoup(page_html, constants.BS4_FORMAT)

    return html.find(id=page_content_id)


def remove_classes(content, classes_to_remove=constants.CLASSES_TO_REMOVE):
    for class_to_remove in classes_to_remove:
        for element in content(class_=class_to_remove):
            element.decompose()

def remove_tags(content, tags_to_remove=constants.TAGS_TO_REMOVE):
    for tag_to_remove in tags_to_remove:
        for element in content(tag_to_remove):
            element.decompose()

def unwrap_collapsible_blocks(content):
    for element in content(class_=constants.COLLAPSIBLE_BLOCK_CLASS):
        element.attrs = {'class': constants.COLLAPSIBLE_CLASS_NEW}

        collapsible_title = bs4.BeautifulSoup('', constants.BS4_FORMAT).new_tag('p', **{'class': constants.COLLAPSIBLE_TITLE_CLASS_NEW})
        collapsible_title.string = element.find(class_=constants.COLLAPSIBLE_BLOCK_LINK_CLASS).text
        collapsible_content = element.find(class_=constants.COLLAPSIBLE_BLOCK_CONTENT_CLASS)

        element.clear()
        element.append(collapsible_title)

        for item in collapsible_content.contents[:]:
            element.append(item)

def divify_blockquotes(content):
    for element in content(constants.BLOCKQUOTE_TAG):
        element.name = 'div'
        element.attrs = {'class': constants.BLOCKQUOTE_CLASS_NEW}

def unwrap_yui_navset(content):
    for element in content(class_ = constants.YUI_NAVSET_CLASS):
        element.attrs = {'class': constants.YUI_NAVSET_CLASS_NEW}
        titles = [title.string for title in element.find(class_=constants.YUI_NAVSET_TAB_CLASS)(constants.YUI_NAVSET_TAB_TITLE_IDENTIFIER)]
        element.find(class_ = constants.YUI_NAVSET_TAB_CLASS).decompose()
        element.div.unwrap()
        for tab, title in zip(element('div', recursive=False), titles):
            tab.attrs = {'class': constants.YUI_NAVSET_TAB_CLASS_NEW}
            title_new = bs4.BeautifulSoup('', constants.BS4_FORMAT).new_tag('p', **{'class': constants.YUI_NAVSET_TAB_TITLE_CLASS_NEW})
            title_new.string = title
            tab.insert(0, title_new)

def fix_links(content, url_allow_list = None):
    for element in content(constants.LINK_TAG):
        if constants.HREF_ATTRIBUTE not in element.attrs:
            continue

        link = element.attrs[constants.HREF_ATTRIBUTE]

        if link.startswith('#'):
            continue

        local_link_result = re.search(f'^({constants.SITE_HOST})?/([a-z0-9-]+)$', link)
        if local_link_result is None:
            element.unwrap()
            continue

        relative_link = local_link_result.group(2)

        if url_allow_list is None or relative_link in url_allow_list:
            element.attrs['href'] = get_filename(relative_link)
        else:
            element.unwrap()
            continue

def add_title(content, page_title):
    title_new = bs4.BeautifulSoup('', constants.BS4_FORMAT).new_tag(constants.PAGE_TITLE_TAG, **{'class': constants.PAGE_TITLE_CLASS})
    title_new.string = page_title
    content.insert(0, title_new)

def fix_footnotes(content):
    for footnoteref in content(constants.FOOTNOTEREF_TAG, class_=constants.FOOTNOTEREF_CLASS):
        link = footnoteref.find(constants.LINK_TAG)

        footnote_href_result = re.search("WIKIDOT\.page\.utils\.scrollToReference\('([a-zA-Z0-9-_]+)'\)", link.attrs[constants.ONCLICK_ATTRIBUTE])
        footnote_href = footnote_href_result[1] if footnote_href_result else ''

        link_attributes_new = {
            constants.ID_ATTRIBUTE: link.attrs[constants.ID_ATTRIBUTE],
            constants.HREF_ATTRIBUTE: '#' + footnote_href,
            constants.EPUB_TYPE_ATTRIBUTE: constants.EPUB_TYPE_FOOTNOTEREF
        }

        link.attrs = link_attributes_new

    for footnote in content(class_=constants.FOOTNOTE_CLASS):
        link = footnote.find(constants.LINK_TAG)

        footnoteref_href_result = re.search("WIKIDOT\.page\.utils\.scrollToReference\('([a-zA-Z0-9-_]+)'\)", link.attrs[constants.ONCLICK_ATTRIBUTE])
        footnoteref_href = footnoteref_href_result[1] if footnoteref_href_result else ''

        footnote_attributes_new = {
            constants.CLASS_ATTRIBUTE: footnote.attrs[constants.CLASS_ATTRIBUTE],
            constants.EPUB_TYPE_ATTRIBUTE: constants.EPUB_TYPE_FOOTNOTE,
            constants.ID_ATTRIBUTE: footnote.attrs[constants.ID_ATTRIBUTE]
        }

        link_attributes_new = {
            constants.HREF_ATTRIBUTE: '#' + footnoteref_href
        }

        footnote.attrs = footnote_attributes_new
        link.attrs = link_attributes_new

def get_filename(name):
    return name + constants.LINK_EXTENSION
