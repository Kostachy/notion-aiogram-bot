import asyncio
from pprint import pprint

from openai import AsyncOpenAI
from httpx import AsyncClient
# from config import settings


class OpenAIHelper:
    def __init__(self):
        http_cliet = AsyncClient(proxies="http://5.189.172.158:3128")
        self.client = AsyncOpenAI(api_key="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", http_client=http_cliet)

    async def create_assistant(self):
        assistant = await self.client.beta.assistants.create(
            name="Task Assistant",
            instructions="",
            tools=[{
                "type": "function",
                "function": {
                    "name": "get_weather",
                    "description": "Determine weather in my location",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "location": {
                                "type": "string",
                                "description": "Country, city or other places"
                            },
                            "unit": {
                                "type": "string",
                                "enum": [
                                    "c",
                                    "f"
                                ]
                            }
                        },
                        "required": [
                            "location"
                        ]
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

    async def all(self):
        """Test function for undestanding how to work with functions"""
        assistant = await self.client.beta.assistants.create(
            name="Task Assistant",
            instructions="",
            tools=[{
                "type": "function",
                "function": {
                    "name": "get_weather",
                    "description": "Determine weather in my location",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "location": {
                                "type": "string",
                                "description": "Country, city or other places"
                            },
                        },
                        "required": [
                            "location"
                        ]
                    }
                }
            }],
            model="gpt-3.5-turbo",
        )
        thread = await self.client.beta.threads.create()
        await self.client.beta.threads.messages.create(
            thread_id=thread.id,
            role="user",
            content='What is the weather in Russia?'
        )
        run = await self.client.beta.threads.runs.create(
            thread_id=thread.id,
            assistant_id=assistant.id,
        )
        run = await self.client.beta.threads.runs.retrieve(run_id=run.id,
                                                           thread_id=thread.id)
        print(run.status)
        while run.status not in ["completed", "failed", "requires_action"]:
            run = await self.client.beta.threads.runs.retrieve(run_id=run.id,
                                                               thread_id=thread.id)
            print(run.status)
            await asyncio.sleep(3)

        tools_to_call = run.required_action.submit_tool_outputs.tool_calls
        print(tools_to_call[0].model_dump_json())

        tools_array = []
        for tool in tools_to_call:
            tool_call_id = tool.id
            function_name = tool.function
            function_args = tool.function.arguments
            print("Tool ID: ", tool_call_id)
            print("Function name: ", function_name)
            print("Function args:", function_args)

            output = False
            if function_name == "get_weather":
                output = True

            tools_array.append({"tool_call_id": tool_call_id, "output": output})
        print(tools_array)

        run = self.client.beta.threads.runs.submit_tool_outputs(
            thread_id=thread.id,
            run_id=run.id,
            tool_outputs=tools_array
        )

        messages = self.client.beta.threads.messages.list(
            thread_id=thread.id
        )

        for message in messages:
            pprint(message.role + ":" + message.content[0].text.value)


openai_client = OpenAIHelper()

# if __name__ == "__main__":
#     asyncio.run(openai_client.all())
