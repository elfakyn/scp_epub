import boto3


def get_api_key_from_secretsmanager():
    raise NotImplementedError


def retrieve_from_s3_cache(relative_path, item, filetype):
    raise NotImplementedError


def store_in_s3_cache(contents, relative_path, item, filetype):
    raise NotImplementedError
