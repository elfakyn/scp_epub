

def filter_tags(pages, include_tags=None):
    if include_tags is not None:
        pages = [
            page if any(
                included_tag in page['tags'] for included_tag in include_tags
            )
            for page in pages
        ]

    return pages
