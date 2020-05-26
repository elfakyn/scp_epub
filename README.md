# SCP epub

Creates an epub from the scp wiki

## Usage

### Setup

You need the following environment variables:

* `WIKIDOT_API_KEY`: your *read-only* wikidot api key

### How to run the tool

## Contributing

### How the tool works

Look in the file `constants/constants.py`. The wiki downloads all pages with the category `PAGE_CATEGORY` if they have one of the tags `ALLOWED_TAGS`. Each page is downloaded twice: once via the API to get the metadata and the unprocessed format, and once via a web request to the printer-friendly page to get a nicely formatted web page.

Some pages have really weird formatting, such as SCP-3125. These are `EDGE_CASES` and are instead sourced directly from this repository.

The downloaded pages (as well as the list of pages) are cached locally. Unless specified with `bypass_cache=True`, these pages are not downloaded again.

The downloaded web pages are then passed through a set of processing steps (`process/process_page.py`). These turn the scp-wiki html into an epub-friendly html. We parse links, handle collapsed blocks, remove images etc. The page HTML parsing/manipulation logic is mostly taken from a different ebook builder, https://github.com/anqxyr/pyscp_ebooks and is designed to be mostly backwards compatible with it.

### Understanding the code

#### Download logic

The download logic is not tested and therefore hard to understand. I'm sorry about that. It gets the list of pages from the API, filters based on allowed tags, and then does two download passes: first it downloads all the pages via the API and then it downloads the rendered html of each page using `requests`.

There's a caching decorator that saves to a local file in the `build` directory. This caching can be bypassed with the flags:

* `bypass_cache_list`: redownloads the page list (any new pages are added to the list and downloaded if not already cached)
* `bypass_cache_pages`: the api downloader will redownload all the pages in the page list
* `bypass_cache_web`: the web downloader will redownload all the pages in the page list

A nice to have would be to download only pages that have been updated since the last download.

#### Page processing logic

There are extensive unit tests in test_unit/process for each processing step that each page goes through.

## Format reference

### Wikidot page API JSON format

* `page_list.json` is an array of wiki page names. Each wiki page name is globally unique. Wikidot wikis are non-hierarchical.
* `pages/<page-name>.json` is of the following structure:

```json
{
  "fullname": "scp-055",
  "created_at": "2008-07-25T15:59:04+00:00",
  "created_by": "xthevilecorruptor",
  "updated_at": "2019-05-03T02:04:14+00:00",
  "updated_by": "Modern_Erasmus",
  "title": "SCP-055",
  "title_shown": "SCP-055",
  "parent_fullname": null,
  "tags": [
    "keter",
    "scp",
    "meta",
    "featured",
    "memory-affecting",
    "heritage",
    "infohazard",
    "antimemetic"
  ],
  "rating": 2733,
  "revisions": 37,
  "parent_title": null,
  "content": "CONTENT IN WIKIDOT FORMAT",
  "html": "CONTENT IN HTML FORMAT",
  "children": 0,
  "comments": 412,
  "commented_at": "2020-04-14T20:34:20+00:00",
  "commented_by": "ZELYNER"
}
```

### Ebook builder JSON format

```json
  {
    "name": "scp-055",
    "title": "SCP-055 Title Thing",
    "created_by": "Author name",
    "created_at": "2020-20-20T20:20:20+20:20",
    "tags": ["list", "of", "tags"],
    "html": "EPUB FRIENDLY PAGE HTML HERE",
  }
```
