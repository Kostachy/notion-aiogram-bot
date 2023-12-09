from notion_client import Client

from pprint import pprint
import json

DB_ID = "ff715c8bdd53406e826a6f0f8d9af46a"


def write_dict_to_file_as_json(content, file_name):
    content_as_json_str = json.dumps(content)

    with open(file_name, 'w') as f:
        f.write(content_as_json_str)


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


def main():
    client = Client(auth="secret_eOEd2ENynh5mQ1ztBDR0G6NIcUId9qxSyJPM0nytukH")
    db_info = client.databases.retrieve(database_id=DB_ID)
    write_dict_to_file_as_json(db_info, 'db_info.json')

    db_rows = client.databases.query(database_id=DB_ID)
    write_dict_to_file_as_json(db_rows, 'db_rows.json')
    pprint(db_rows)

    simple_rows = []
    for row in db_rows['results']:
        task_name = safe_get(row, 'properties.Task_Name.title.0.plain_text')
        start_date = safe_get(row, 'properties.Date.date.start')
        end_date = safe_get(row, 'properties.Date.date.end')
        tags = safe_get(row, 'properties.Tags.multi_select.0.name')

        simple_rows.append({
            'task_name': task_name,
            'tags': tags,
            'start_date': start_date,
            'end_date': end_date
        })

        for i in simple_rows:
            pprint(i)

        write_dict_to_file_as_json(simple_rows, 'simple_rows.json')

if __name__ == "__main__":
    main()
