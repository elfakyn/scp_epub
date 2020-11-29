# Running tests

To run tests:

* Run tests from the `scp_epub` module directory, not from the root of the repository: `cd scp_epub`
* Unit tests: `python3 -m unittest discover -s test_unit -t .`
* Component tests: `python3 -m unittest discover -s test_component -t .`
* Platform tests: CAUTION! These tests actually do stuff such as download pages! Recommended to run one at a time, as some may take several hours: `python3 -m unittest test_platform/path/to/test_file.py`
  * Note: some platform tests may prompt you for a Wikidot API key.
