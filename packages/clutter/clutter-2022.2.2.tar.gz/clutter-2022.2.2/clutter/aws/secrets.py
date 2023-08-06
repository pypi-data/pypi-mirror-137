import base64
import json
import logging
import textwrap
import warnings
import boto3
from botocore.exceptions import ClientError

from ..docker import load_secrets

logger = logging.getLogger(__file__)


def get_secrets(
    secret_name,
    region_name="ap-northeast-2",
    load_docker_secret=True,
):
    if load_docker_secret:
        load_secrets()

    # Create a Secrets Manager client
    session = boto3.session.Session()
    client = session.client(service_name="secretsmanager", region_name=region_name)

    try:
        get_secret_value_response = client.get_secret_value(SecretId=secret_name)
    except ClientError as e:
        code = e.response["Error"]["Code"]
        description = textwrap.dedent(ERROR_DESCRIPTIONS["CODE"]).strip("\n")
        logger.error(description)
        raise e
    else:
        if "SecretString" in get_secret_value_response:
            secrets = get_secret_value_response["SecretString"]
            secrets = json.loads(secrets)
        else:
            secrets = base64.b64decode(get_secret_value_response["SecretBinary"])

    return secrets


def list_secrets(shorten=True, region_name="ap-northeast-2"):
    """
    (TODO)
      - filter tags
    """
    # Create a Secrets Manager client
    session = boto3.session.Session()
    client = session.client(service_name="secretsmanager", region_name=region_name)

    opts = {}
    secret_list = []
    while True:
        response = client.list_secrets(**opts)
        secret_list += response.get("SecretList", [])
        next_token = response.get("NextToken")
        if next_token is None:
            break
        opts.update({"NextToken": next_token})

    if shorten:
        return {x["Name"]: x["Description"] for x in secret_list}
    return secret_list


# [DEPRECATED]
def get_secret(secret_name, region_name="ap-northeast-2"):
    _warn = "'get_secret' will be deprecated soon, use 'get_secrets'!"
    warnings.warn(_warn, FutureWarning)

    return get_secrets(secret_name=secret_name, region_name=region_name)


# errors
ERROR_DESCRIPTIONS = {
    "DecryptionFailureException": """
    Secrets Manager can't decrypt the protected secret text using the provided KMS key.
    Deal with the exception here, and/or rethrow at your discretion.
    """,
    "InternalServiceErrorException": """
    An error occurred on the server side.
    Deal with the exception here, and/or rethrow at your discretion.
    """,
    "InvalidParameterException": """
    You provided an invalid value for a parameter.
    Deal with the exception here, and/or rethrow at your discretion.
    """,
    "InvalidRequestException": """
    You provided a parameter value that is not valid for the current state of the resource.
    Deal with the exception here, and/or rethrow at your discretion.
    """,
    "ResourceNotFoundException": """
    We can't find the resource that you asked for.
    Deal with the exception here, and/or rethrow at your discretion.
    """,
}
