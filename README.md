# SCP epub

Creates an epub from the scp wiki

**This is a work in progress with no current ETA.**

You can track the progress in progress.txt

## Running the tool locally

This tool normally runs on AWS, however you can run it locally without worrying about any cloud functionality.

### Prerequisites

You can run the ebook builder locally in Linux or Mac. You can also run the tool in Windows using WSL.

Resource requirements:

* At least 2 GB of available memory
* At least 2 GB of available storage

You need the following installed:

* Python 3 and pip3
* All the python modules in requirements.txt: `pip3 install -r requirements.txt`

You need the following environment variables:

* `SCP_EPUB_USE_AWS`: this environment variable must be unset: `unset SCP_EPUB_USE_AWS`
* `SCP_EPUB_WIKIDOT_API_KEY`: your read-only Wikidot API Key: `export SCP_EPUB_WIKIDOT_API_KEY=000000000000000000000000000`

## Contributing

### Running tests

The behavior of this tool is documented via tests.

This project uses 3 types of tests:

* Unit tests, located in [test_unit](/scp_epub/test_unit). These tests are small scale, usually function-level.
* Component tests, located in [test_component](/scp_epub/test_component). These tests test the behavior of an entire component such as the entire html parser as a whole.
* Platform tests, located in [test_platform](/scp_epub/test_platform). Platform tests test the tool, or big parts of the tool, end-to-end. **These tests actually do things, such as download files, hit the API, write to disk, access cloud infrastructure etc. They are extremely resource intensive and may take several hours to run.**

To run tests:

* Run tests from the `scp_epub` module directory, not from the root of the repository: `cd scp_epub`
* Unit tests: `python3 -m unittest discover -s test_unit -t .`
* Component tests: `python3 -m unittest discover -s test_component -t .`
* Platform tests: you usually want to run only the test you're interested in, otherwise you'll be here all day: `python3 -m unittest test_platform/path/to/test_file.py`
  * Note: some platform tests may prompt you for a Wikidot API key.

### Editing tool parameters

The tool loads configuration information in three ways:

* If the tool is deployed on AWS, the tool will load infrastructure information (bucket names, locations of secrets in AWSSM etc.) from environment variables that are defined in [constants.py](/scp_epub/constants.py)
* The tool also reads configuration directly from [constants.py](/scp_epub/constants.py). This is not end-user-editable
* Any configuration around building a book is contained in a book definition file in the [definitions directory](/definitions). This is documented separately and is meant to be edited by the end user

## AWS Infrastructure (this bit isn't implemented yet)

If you want to spin up your own infrastructure, you have a little more work ahead of you. The infrastructure for the tool is Terraform-based and you need good working knowledge of AWS and Terraform to get it going in your environment.

There are two terraform modules:

* [infrastructure/build/main.tf](/infrastructure/build/main.tf) creates the epub and stores it in s3
* [infrastructure/save_to_mega/main.tf](/infrastructure/save_to_mega/main.tf) takes the file from s3 and stores it in Mega

For each piece of infrastructure you will want to change the following:

* Either completely remove the backend configuration or change it to match your setup.
* Change the default values in variables.tf
