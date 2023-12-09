from notion_client import Client

from pprint import pprint

DB_ID = "ff715c8bdd53406e826a6f0f8d9af46a"


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
    # https://www.notion.so/ff715c8bdd53406e826a6f0f8d9af46a?v=5009098538b54e679486c032db69025a&pvs=4
    db_rows = client.databases.query(database_id=DB_ID)
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


if __name__ == "__main__":
    main()
