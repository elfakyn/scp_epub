# SCP epub

Creates an epub from the scp wiki

**This is a work in progress with no current ETA.**

You can track the progress in progress.txt

## Running the tool

### Prerequisites

You can run the ebook builder locally in Linux, Windows (using WSL), or Mac.

Resource requirements:

* At least 2 GB of available memory
* At least 2 GB of available storage

You need the following installed:

* Python 3 and pip3
* All the python modules in requirements.txt: `pip3 install -r requirements.txt`

You need the following environment variables:

* `SCP_EPUB_USE_AWS`: this environment variable must be unset: `unset SCP_EPUB_USE_AWS`
* `SCP_EPUB_WIKIDOT_API_KEY`: your read-only Wikidot API Key: `export SCP_EPUB_WIKIDOT_API_KEY=000000000000000000000000000`
