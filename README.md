# SCP epub

Creates an epub from the scp wiki

## Setup

You need the following environment variables:

* `WIKIDOT_API_KEY`: your *read-only* wikidot api key

## JSON format

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
