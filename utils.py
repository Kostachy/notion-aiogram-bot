from urllib.parse import urlparse


def get_notion_db_id(url: str) -> str:
    parsed_url = urlparse(url)
    return parsed_url.path.replace('/', '')
