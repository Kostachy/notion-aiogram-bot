import logging

from openai import AsyncOpenAI

from config import settings
from openai_api.promts import prompt

openai_client = AsyncOpenAI(api_key=settings.OPENAI_TOKEN)


async def create_assistant():
    assistant = await openai_client.beta.assistants.create(
        name="New Task Assistant",
        tools=[{"type": "code_interpreter"}],
        instructions=prompt,
        model="gpt-3.5-turbo-1106",
    )
    return assistant.id


async def update_assistant():
    assistant = await openai_client.beta.assistants.update(
        assistant_id=settings.ASSISTANT_ID,
        name="Task Assistant",
        tools=[{"type": "code_interpreter"}],
        instructions=prompt,
        model="gpt-3.5-turbo-1106",
    )
    return assistant



