from autogen_ext.models.openai import OpenAIChatCompletionClient
from autogen_core.models import UserMessage
import os
import dotenv
import asyncio

# Load environment variables from .env file
dotenv.load_dotenv()
my_current_api_key = os.getenv("OPENAI_API_KEY")
print(f"Using OpenAI API key: {my_current_api_key}")

async def main():
    model = OpenAIChatCompletionClient(
        model="gpt-4o",
        api_key=my_current_api_key
    )

    res = await model.create(messages=[UserMessage(content="Hello, how are you?", source="user")])
    print(res)
 

if __name__ == "__main__":
    asyncio.run(main())
    print("Finished running the OpenAI chat completion client.")