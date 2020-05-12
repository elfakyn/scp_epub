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
