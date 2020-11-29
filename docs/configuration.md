# Configuration

The tool loads configuration information in three ways:

* If the tool is deployed on AWS, the tool will load infrastructure information (bucket names, locations of secrets in AWSSM etc.) from environment variables that are defined in [constants.py](/scp_epub/constants.py)
* The tool also reads configuration directly from [constants.py](/scp_epub/constants.py). This is not meant to be changed by the end user.
* Any configuration around building a book is contained in a book definition file in the [definitions directory](/definitions). This is documented in [book_definition.md](./book_definition.md) and is meant to be edited by the end user.

## Constants file

All specifications regarding the format of the SCP wiki, caching settings, how to process the page contents etc. are defined in [the constants file](/scp_epub/constants.py).
