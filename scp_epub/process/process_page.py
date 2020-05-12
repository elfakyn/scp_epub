import bs4

import constants.process

def get_page_content(page_html, page_content_id=constants.process.PAGE_CONTENT_ID):
    html = bs4.BeautifulSoup(page_html, constants.process.BS4_FORMAT)

    return html.find(id=page_content_id)


def remove_by_class(content, classes_to_remove=constants.process.CLASSES_TO_REMOVE):
    for class_to_remove in classes_to_remove:
        for element in content(class_=class_to_remove):
            element.decompose()

    return content

def remove_by_tag(content, tags_to_remove=constants.process.TAGS_TO_REMOVE):
    for tag_to_remove in tags_to_remove:
        for element in content(tag_to_remove):
            element.decompose()

    return content

def unwrap_collapsible_block(content):
    for element in content(class_=constants.process.COLLAPSIBLE_BLOCK_CLASS):
        element.attrs = {'class': constants.process.COLLAPSIBLE_CLASS_NEW}

        collapsible_title = bs4.BeautifulSoup('', constants.process.BS4_FORMAT).new_tag('p', **{'class': constants.process.COLLAPSIBLE_TITLE_CLASS_NEW})
        collapsible_title.string = element.find(class_=constants.process.COLLAPSIBLE_BLOCK_LINK_CLASS).text
        collapsible_content = element.find(class_=constants.process.COLLAPSIBLE_BLOCK_CONTENT_CLASS)

        element.clear()
        element.append(collapsible_title)
        for item in collapsible_content.contents:
            element.append(item)

    return content
