from autogen_ext.models.openai import OpenAIChatCompletionClient
from autogen_core.models import UserMessage
from autogen_agentchat.agent import AssistantAgent
from autogen_agentchat.agent import UserAgent
import os
import dotenv
import asyncio

# Load environment variables from .env file
dotenv.load_dotenv()
my_current_api_key = os.getenv("OPENAI_API_KEY")
print(f"Using OpenAI API key: {my_current_api_key}")


async def main():
    model = OpenAIChatCompletionClient(model="gpt-4o", api_key=my_current_api_key)

    topic = "The use of hairgels in modern society"
    supporter = AssistantAgent(
        name="John",
        model=model,
        system_message=(
            f"You are a helpful, supporting assistant named John in a debate about the topic: {topic}, "
            "and you will be debating against a critic agent named Jack."
        ),
        model_client=model,
    )

    critic = AssistantAgent(
        name="Jack",
        model=model,
        system_message=(
            f"You are a critical assistant in a debate about the topic: {topic}, "
            "and you will be debating against a supporter agent. "
        )
        model_client=model,
    )

    res = await model.create(
        messages=[UserMessage(content="Hello, how are you?", source="user")]
    )
    print(res)


if __name__ == "__main__":
    asyncio.run(main())
    print("Finished running the OpenAI chat completion client.")
