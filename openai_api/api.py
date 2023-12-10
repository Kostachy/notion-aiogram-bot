import asyncio

from openai import AsyncOpenAI
from httpx import AsyncClient

http_cliet = AsyncClient(proxies="http://51.79.229.202:3128")
client = AsyncOpenAI(api_key="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", http_client=http_cliet)


async def create_assistant():
    assistant = await client.beta.assistants.create(
        name="Task Assistant",
        instructions="",
        tools=[{"type": "function"}],
        model="gpt-4-1106-preview",
    )
    return assistant



if __name__ == "__main__":
    asyncio.run(create_assistant())
