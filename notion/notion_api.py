import asyncio
from pprint import pprint

from notion_client import AsyncClient
import json
from utils import safe_get

from config import settings


def write_dict_to_file_as_json(content, file_name):
    content_as_json_str = json.dumps(content)

    with open(file_name, 'w') as f:
        f.write(content_as_json_str)


class NotionHelper:
    def __init__(self):
        self.client = AsyncClient(auth=settings.NOTION_TOKEN)

    async def read_db(self, database_id: str):
        """Func for test"""
        db_rows = await self.client.databases.query(database_id=database_id)
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
            return simple_rows

    async def write_row(self, database_id: str, data: dict) -> None:
        await self.client.pages.create(
            **{
                'parent': {
                    'database_id': database_id
                },
                'properties': data
            }
        )

    async def simple_write(self, data: str):
        await self.client.pages.create(data)

    async def get_db(self, database_id: str):
        db_rows = await self.client.databases.query(database_id=database_id)
        return db_rows


notion_client = NotionHelper()
