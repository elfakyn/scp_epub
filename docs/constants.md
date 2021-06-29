# Constants

This file documents constants in [constants.py](scp_epub/constants/constants.py) and what they do.

Almost every string literal and magic number in the entire program is extracted in this file.

## Charset

Character set-related values.

## AWS Execution

This tool may be expanded in the future to run on AWS automatically. This sets some groundwork for that. This is currently not implemented, so enabling AWS use will not work. This may be removed in the future.

Constant | Explanation
--- | ---
`USE_AWS_VARIABLE` | The environment variable that defines whether to use AWS or not
`USE_AWS_TRUE` | The value of `USE_AWS_VARIABLE` that will be interpreted as "True"
`S3_CACHE_BASE_PATH` | The path in the s3 bucket that will be used to store the page cache
`S3_BUCKET_VARIABLE` | The environment variable that defines which s3 bucket data will be stored in
`API_KEY_SECRETSMANAGER_VARIABLE` | The environment variable that contains the name of the SecretsManager secret that will be used.

## Local Execution

This tool is for the most part intended to be run locally. Some of the key file paths are defined relative to the path of the constants file.

To be continued...
