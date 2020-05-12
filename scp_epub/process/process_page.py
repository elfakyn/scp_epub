import bs4

import constants.process

def get_page_contents(page_html, page_content_id=constants.process.PAGE_CONTENT_ID):
    html = bs4.BeautifulSoup(page_html, constants.process.BS4_FORMAT)

    return html.find(id=page_content_id)
