import json
from urllib.parse import urlparse


def get_notion_db_id(url: str) -> str:
    parsed_url = urlparse(url)
    return parsed_url.path.replace('/', '')


def safe_get(data, dot_chained_keys):
    """
        {'a': {'b': [{'c': 1}]}}
        safe_get(data, 'a.b.0.c') -> 1
    """
    keys = dot_chained_keys.split('.')
    for key in keys:
        try:
            if isinstance(data, list):
                data = data[int(key)]
            else:
                data = data[key]
        except (KeyError, TypeError, IndexError):
            return None
    return data


def write_dict_to_file_as_json(content, file_name):
    content_as_json_str = json.dumps(content)

    with open(file_name, 'w') as f:
        f.write(content_as_json_str)
