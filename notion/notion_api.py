from notion_client import Client

from pprint import pprint
import json


# https://www.notion.so/ff715c8bdd53406e826a6f0f8d9af46a?v=5009098538b54e679486c032db69025a&pvs=4

# https://www.notion.so/Getting-Started-494d81541eeb4534abaf10425ab38630?pvs=4
# https://www.notion.so/ca3b142971f4434cbedc5a78c7e129d7?v=db57be347e4c470d94e41a16368e4957&pvs=4
def write_dict_to_file_as_json(content, file_name):
    content_as_json_str = json.dumps(content)

    with open(file_name, 'w') as f:
        f.write(content_as_json_str)


def read_text(client, page_id):
    response = client.blocks.children.list(block_id=page_id)
    return response


def safe_get(data, dot_chained_keys):
    '''
        {'a': {'b': [{'c': 1}]}}
        safe_get(data, 'a.b.0.c') -> 1
    '''
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


def read_db(client: Client):
    db_rows = client.databases.query(database_id=DB_ID)
    write_dict_to_file_as_json(db_rows, 'db_rows.json')

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

        write_dict_to_file_as_json(simple_rows, 'simple_rows.json')


def write_row(client: Client, database_id, task_name, tags, start_date, end_date):
    client.pages.create(
        **{
            'parent': {
                'database_id': database_id
            },
            'properties': {
                'Task_Name': {'title': [{'text': {'content': task_name}}]},
                "Tags": {"multi_select": [{"name": "code"}]},
                'Date': {'date': {'start': start_date, 'end': end_date}}
            }
        }
    )


if __name__ == "__main__":
    client = Client(auth="secret_eOEd2ENynh5mQ1ztBDR0G6NIcUId9qxSyJPM0nytukH")

    DB_ID = "ca3b142971f4434cbedc5a78c7e129d7"
    page_id = "494d81541eeb4534abaf10425ab38630"

    read_db(client)
    pprint(read_text(client, page_id))
    write_row(client, DB_ID, 'Nameee', 'code', '2023-12-09', '2023-12-11')
