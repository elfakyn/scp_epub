

def filter_tags(pages, include_tags=None):
    if include_tags is not None:
        pages = [
            page for page in pages
            if 'tags' in page and any(
                included_tag in page['tags'] for included_tag in include_tags
            )
        ]

    return pages
