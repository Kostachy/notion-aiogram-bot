import logging

from notion_client import APIResponseError, AsyncClient

from config import settings
from utils import safe_get


class NotionHelper:
    def __init__(self):
        self.client = AsyncClient(auth=settings.NOTION_TOKEN)

    async def write_row_in_notion(self, database_id: str, title: str, category: str, priority: str, due_date: str):
        properties = {
            "Title": {
                "id": "title",
                "type": "title",
                "title": [{
                    "text": {
                        "content": title
                    }
                }]
            },
            "Category": {
                "id": "category",
                "type": "select",
                "select": {
                    "name": category
                }
            },
            "Priority": {
                "id": "priority",
                "type": "select",
                "select": {
                    "name": priority
                }
            },
            "Due Date": {
                "id": "Due Date",
                "type": "date",
                "date": {
                    "start": due_date,
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
            title = safe_get(row, 'properties.Title.title.0.text.content')
            category = safe_get(row, 'properties.Category.select.name')
            due_date = safe_get(row, 'properties.Due Date.date.start')
            priority = safe_get(row, 'properties.Priority.select.name')

            simple_rows.append({
                'Title': title,
                'Category': category,
                'Priority': priority,
                'Due date': due_date
            })
        return simple_rows


notion_client = NotionHelper()

# async def main():
#     notion_client = NotionHelper()
#     # notion_db = await notion_client.read_db("ca3b142971f4434cbedc5a78c7e129d7")
#     # result_list = []
#     # for row in notion_db:
#     #     result_list.append(f"{row['Category']}|{row['Title']}|{row['Priority']}|{row['Due date']}")
#     # print(f"exist tasks: {', '.join(map(str, result_list))}")
#
#     await notion_client.write_row_in_notion(database_id="ca3b142971f4434cbedc5a78c7e129d7",
#                                             title="Make some food for dinner",
#                                             category="Food",
#                                             priority="3",
#                                             due_date="2023-12-18")
#
#
# if __name__ == "__main__":
#     asyncio.run(main())
# # ca3b142971f4434cbedc5a78c7e129d7                   work|Finish presentation|1|2023-05-13
