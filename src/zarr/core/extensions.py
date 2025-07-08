import json
import functools
from urllib.parse import urlparse
import urllib3

import jsonschema

def _is_url(url: str) -> bool:
    """Checks whether the input string is a valid URL.

    Args:
        url (str): The string to check.

    Returns:
        bool: True if the input string is a valid URL, False otherwise.
    """
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except ValueError:
        return False


@functools.lru_cache()
def _fetch_remote_schema(input_path: str):
    if _is_url(input_path):
        resp = urllib3.request("GET", input_path)
        data = resp.json()
    else:
        with open(input_path) as f:
            data = json.load(f)
    return data


def validate_extension(extension_data: dict, schema_ref: str) -> str:
    """Validates the extension against the remote JSON schema, returning the top-level
    key to where the schema is stored in the node."""
    schema = _fetch_remote_schema(schema_ref)
    jsonschema.validate(extension_data, schema)
    return schema['required'][0]
