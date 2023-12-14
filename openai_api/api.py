# import asyncio

from openai import AsyncOpenAI
from openai_api.promts import prompt
from config import settings
# from httpx import AsyncClient

# http_client = AsyncClient(proxies="http://5.189.172.158:3128")
openai_client = AsyncOpenAI(api_key=settings.OPENAI_TOKEN)


async def create_assistant():
    assistant = await openai_client.beta.assistants.update(
        assistant_id="asst_4u5luGi7KoqwjEBewOlF1Y48",
        name="Task Assistant",
        instructions=prompt,
        model="gpt-3.5-turbo-1106",
    )
    return assistant


# if __name__ == "__main__":
#     asyncio.run(create_assistant())
