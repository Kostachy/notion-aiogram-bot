import asyncio
from pprint import pprint

from openai import AsyncOpenAI
from httpx import AsyncClient
from config import settings


class OpenAIHelper:
    def __init__(self):
        http_cliet = AsyncClient(proxies="http://5.189.172.158:3128")
        self.client = AsyncOpenAI(api_key=settings.OPENAI_TOKEN, http_client=http_cliet)

    async def create_assistant(self):
        assistant = await self.client.beta.assistants.create(
            name="Task Assistant",
            instructions="You have to analyze and find the task and its start and end time in the json",
            tools=[{
                "type": "function",
                "function": {
                    "name": "get_task_and_time",
                    "description": "Get the the start and end time of the task",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "task_name": "string",
                            "start_date": "string",
                            "end_date": "string"
                        },
                        "required": ["task_name, start_date, end_date"]
                    }
                }
            }],
            model="gpt-3.5-turbo",
        )
        return assistant

    async def create_thread(self):
        thread = await self.client.beta.threads.create()
        return thread

    async def add_message_to_thread(self, thread, message: str):
        await self.client.beta.threads.messages.create(
            thread_id=thread.id,
            role="user",
            content=message
        )

    async def run_assistant(self, thread, assistant):
        run = await self.client.beta.threads.runs.create(
            thread_id=thread.id,
            assistant_id=assistant.id,
        )
        return run

    async def display_assistant_responce(self, thread):
        messages = await self.client.beta.threads.messages.list(
            thread_id=thread.id
        )
        return messages


# async def main():
#     assistant = OpenAIHelper()
#     assistant_object = await assistant.create_assistant()
#     thread = await assistant.create_thread()
#     await assistant.add_message_to_thread(thread, 'dfdfd')
#     await assistant.run_assistant(thread, assistant_object)
#     message = await assistant.display_assistant_responce(thread)
#     print(message)
#
#
# if __name__ == "__main__":
#     asyncio.run(main())
