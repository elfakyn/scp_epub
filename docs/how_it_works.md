# How SCP epub Works

SCP epub takes the entirety of the SCP wiki (running on Wikidot) and converts it into ebook format via a series of separate steps.

1. Download the SCP wiki
2. Convert every page from web format into an ebook-friendly format
3. Organize and assemble the pages in the correct order
4. Create the ebook

The **book definition file** controls exactly what pages to download from the SCP wiki and how to organize the book (steps 1, 3, and 4). The [constants file](scp_epub/constants/constants.py) controls how the pages are converted into ebook format (step 2).

## Downloading the SCP wiki

We'll use [the complete collection definition file](definitions/complete_collection.json) as an example.

First, SCP epub obtains a list of all SCP pages. For example, all pages that we care about (SCP entries, tales, hubs, supplements) are in the same category, `_default`. We get a list of all the pages in the specified categories (usually, `_default` is enough). This uses the Wikidot API and it requires a read-only Wikidot API key.

Then, using the wikidot API, we obtain metadata on all the pages of interest, specified by tags (in this example, scp, tale, hub, and supplement).

Now that we have all the pages of interest and their metadata, we download all of them. Some pages (like scp-3125), however, are super complicated or interactive, so they will not be downloaded and processed. Instead, they are treated as an edge case and they will be replaced by a version that's processed by hand (located in the [edge_cases folder](edge_cases/)). This is OK because the SCP wiki license allows such use.

After we have a list of all the pages we care about, we download their actual contents not through the API, but by scraping the HTML of each web page's "printer-friendly" version. The program implements rate limiting to follow Wikidot rate limits and to also be respectful of the site bandwidth. Rate limits are defined in the constants file.

Because of the way Wikidot works, there is no hierarchy or grouping of pages. This means everything is downloaded in the same directory and is not organized in any way. This will become relevant later.

All downloaded information is cached so that we don't need to re-download stuff all the time. The cached version are found in the `build/cache/` directory that will be created when you first run the program.

## Converting pages into ebook-friendly format

Right now, we have a whole bunch of pages in HTML format, and they contain a lot of unnecessary information such as site headers and footers, web links etc. We need to convert all the pages into an ebook-friendly form. Thankfully, the epub ebook format is basically just a huge ZIP archive containing HTML files. There are certain requirements for a page to be epub-compatible but it is otherwise a straightforward conversion process.

Certain classes and tags need to be removed from the HTML outright. These are defined in the constants file. Currently, we simply remove images, although it would be theoretically possible to include them.

The SCP wiki uses collapsible blocks a lot (where text is hidden until you click on a dropdown). These are incompatible with epub, so they're unwrapped: we get rid of the collapsible blocks but keep the text inside them.

There are a number of other items, such as page headers, block quotes, footnotes, and internal links that all need to be properly converted.

Each page is processed individually and is now converted into ebook-friendly HTML that can be directly assembled into an epub.

## Organizing and assembling the pages

However, we can't do that just yet. The pages need to be put in the correct order.

To be continued...
