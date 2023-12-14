# import asyncio

from openai import AsyncOpenAI
from config import settings
# from httpx import AsyncClient

# http_client = AsyncClient(proxies="http://5.189.172.158:3128")
openai_client = AsyncOpenAI(api_key=settings.OPENAI_TOKEN)


async def create_assistant():
    assistant = await openai_client.beta.assistants.update(
        assistant_id="asst_4u5luGi7KoqwjEBewOlF1Y48",
        name="Test Task Assistant",
        instructions="""You are a bot that must analyze the json that was received in response from 
        the Notion database and insert a task along with its start time and end time so that this task 
        does not interfere other tasks that are already in the json(database).""",
        tools=[{
            "type": "function",
            "function": {
                "name": "insert_task_and_time",
                "description": "A function that takes in a task, start date, end date and inserts it into the JSON from Notion API and the function should return json but with a task and start and end date inserted into it",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "Task name": {
                            "type": "string",
                            "description": "Task name e.g. do homework of call Ryan"
                        },
                        "start_date": {
                            "type": "string",
                            "description": "Start date of the task in ISO 8601 format"
                        },
                        "end_date": {
                            "type": "string",
                            "description": "End date of the task in ISO 8601 format"
                        },
                        "json": {
                            "type": "object",
                            "description": "json from notion db"
                        }
                    },
                    "required": [
                        "task",
                        "start_date",
                        "end_date",
                        "json"
                    ]
                }
            }
        }],
        model="gpt-3.5-turbo-1106",
    )
    return assistant




# if __name__ == "__main__":
#     asyncio.run(create_assistant())