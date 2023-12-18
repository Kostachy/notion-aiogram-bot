import logging

from notion_client import APIResponseError, AsyncClient
from config import settings
from utils import safe_get


class NotionHelper:
    def __init__(self):
        self.client = AsyncClient(auth=settings.NOTION_TOKEN)

    async def write_row_in_notion(self, database_id: str, task_name: str, start_date: str, end_date: str):
        properties = {
            "Task name": {
                "id": "title",
                "type": "title",
                "title": [{
                    "text": {
                        "content": task_name
                    }
                }]
            },
            "Date": {
                "id": "Date",
                "type": "date",
                "date": {
                    "start": start_date,
                    "end": end_date,
                }
            }
        }
        try:
            await self.client.pages.create(
                **{
                    'parent': {
                        'database_id': database_id
                    },
                    'properties': properties
                }
            )
        except APIResponseError as err:
            logging.error(f"Notion API error - {err}")
            raise APIResponseError

    async def get_db(self, database_id: str):
        db_rows = await self.client.databases.query(database_id=database_id)
        return db_rows

    async def read_db(self, database_id: str):
        db_rows = await self.client.databases.query(database_id=database_id)

        simple_rows = []
        for row in db_rows['results']:
            task_name = safe_get(row, 'properties.Task name.title.0.text.content')
            start_date = safe_get(row, 'properties.Date.date.start')
            end_date = safe_get(row, 'properties.Date.date.end')

            simple_rows.append({
                'task_name': task_name,
                'start_date': start_date,
                'end_date': end_date
            })
        return simple_rows


notion_client = NotionHelper()

# async def main():
#     notion_client = NotionHelper()
#     notion_db = await notion_client.read_db("29884a3519a44d979f97ae1c994cd3aa")
#     # result_list = []
#     # for row in notion_db:
#     #     result_list.append(f"{row['Category']}|{row['Title']}|{row['Priority']}|{row['Due date']}")
#     # print(f"exist tasks: {', '.join(map(str, result_list))}")
#
#     # await notion_client.write_row_in_notion(database_id="ca3b142971f4434cbedc5a78c7e129d7",
#     #                                         title="Make some food for dinner",
#     #                                         category="Food",
#     #                                         priority="3",
#     #                                         due_date="2023-12-18")
#
#
# if __name__ == "__main__":
#     asyncio.run(main())
# # # ca3b142971f4434cbedc5a78c7e129d7                   work|Finish presentation|1|2023-05-13
