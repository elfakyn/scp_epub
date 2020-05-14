import bs4

from constants import constants

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
        for item in collapsible_content.contents:
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
