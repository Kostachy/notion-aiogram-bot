from openai import AsyncOpenAI
from config import settings
from openai_functions import insert_task_and_time


class OpenAIHelper:
    def __init__(self):
        self.client = AsyncOpenAI(api_key=settings.OPENAI_TOKEN)

    async def create_assistant(self):
        assistant = await self.client.beta.assistants.create(
            name="Task Assistant",
            instructions="""You are a bot that must analyze the json that was received in response from 
            the Notion database and insert a task along with its start time and end time so that this task 
            does not interfere other tasks that are already in the database.""",
            tools=[{
                "type": "function",
                "function": insert_task_and_time
            }],
            model="gpt-3.5-turbo-1106",
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


openai_client = OpenAIHelper()
