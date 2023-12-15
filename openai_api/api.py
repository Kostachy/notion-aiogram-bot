from openai import AsyncOpenAI

from config import settings
from openai_api.promts import prompt

openai_client = AsyncOpenAI(api_key=settings.OPENAI_TOKEN)


async def create_assistant():
    assistant = await openai_client.beta.assistants.update(
        assistant_id=settings.ASSISTANT_ID,
        name="Task Assistant",
        tools=[],
        instructions=prompt,
        model="gpt-3.5-turbo-1106",
    )
    return assistant
