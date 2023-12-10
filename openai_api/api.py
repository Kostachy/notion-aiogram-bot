import asyncio
from pprint import pprint

from openai import AsyncOpenAI
from httpx import AsyncClient


class OpenAIHelper:
    def __init__(self):
        http_cliet = AsyncClient(proxies="http://103.30.182.116:80")
        self.client = AsyncOpenAI(api_key="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", http_client=http_cliet)

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

    async def add_message_to_thread(self, thread, some_json):
        message = await self.client.beta.threads.messages.create(
            thread_id=thread.id,
            role="user",
            content=f"I need to find task and its start and end time in the json: {some_json}"
        )
        return message

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

