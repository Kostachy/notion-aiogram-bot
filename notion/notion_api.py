from notion_client import Client
import json


def write_dict_to_file_as_json(content, file_name):
    content_as_json_str = json.dumps(content)

    with open(file_name, 'w') as f:
        f.write(content_as_json_str)


async def read_text(client, page_id):
    response = await client.blocks.children.list(block_id=page_id)
    return response


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


async def read_db(client: Client, database_id: str):
    db_rows = await client.databases.query(database_id=database_id)
    # write_dict_to_file_as_json(db_rows, 'db_rows.json')

    simple_rows = []
    for row in db_rows['results']:
        task_name = safe_get(row, 'properties.Task_Name.title.0.plain_text')
        start_date = safe_get(row, 'properties.Date.date.start')
        end_date = safe_get(row, 'properties.Date.date.end')
        tags = safe_get(row, 'properties.Tags.multi_select.0.name')

        simple_rows.append({
            'Task_Name': task_name,
            'Tags': tags,
            'start_date': start_date,
            'end_date': end_date
        })
        return simple_rows


async def write_row(client: Client, database_id: str, task_name: str, tags: str, start_date: str, end_date: str):
    await client.pages.create(
        **{
            'parent': {
                'database_id': database_id
            },
            'properties': {
                'Task_Name': {'title': [{'text': {'content': task_name}}]},
                "Tags": {"multi_select": [{"name": tags}]},
                'Date': {'date': {'start': start_date, 'end': end_date}}
            }
        }
    )
