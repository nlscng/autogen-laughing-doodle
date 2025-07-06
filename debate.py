from autogen_ext.models.openai import OpenAIChatCompletionClient
from autogen_core.models import UserMessage
from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.teams import RoundRobinGroupChat
import os
import dotenv
import asyncio
from autogen_agentchat.agents import BaseChatAgent
from autogen_agentchat.base import TaskResult
from autogen_agentchat.conditions import TextMentionTermination

# Load environment variables from .env file
dotenv.load_dotenv()
my_current_api_key = os.getenv("OPENAI_API_KEY")
print(f"Using OpenAI API key: {my_current_api_key}")


async def main():
    model = OpenAIChatCompletionClient(model="gpt-4o", api_key=my_current_api_key)

    topic = "The use of hairgels in modern society"
    host = AssistantAgent(
        name="Jane",
        system_message=(
            f"You are a host for a debate about the topic: {topic}, with"
            " a supporter agent named John and a critic agent named Jack. "
            "You will start the debate, introduce the participants, and moderate the debate. "
            "Give each debater 3 rounds to present their arguments, "
            "At the begining of each round, announce the round number. "
            "And at the begining of the last round, announce that it is the last round."
            "After each of the debaters has 3 rounds, summarize the key points made by each participant. "
            "say exactly 'TERMINATE' to end the debate. "
            "And remember to thank the audience for their participation before you say 'TERMINATE'."
        ),
        model_client=model,
    )

    supporter = AssistantAgent(
        name="John",
        system_message=(
            f"You are a helpful, supporting assistant named John in a debate about the topic: {topic}, "
            "and you will be debating against a critic agent named Jack."
        ),
        model_client=model,
    )

    critic = AssistantAgent(
        name="Jack",
        system_message=(
            f"You are a critical assistant in a debate about the topic: {topic}, "
            "and you will be debating against a supporter agent. "
        ),
        model_client=model,
    )

    team = RoundRobinGroupChat(
        participants=[host, supporter, critic],
        max_turns=8,
        termination_condition=TextMentionTermination(
            text="TERMINATE",
        ),
    )

    # Start the debate
    res = await team.run(task="Start the debate!")

    ## The synchronous way to get the messages
    # for one_msg in res.messages:
    #     print("-"*20)
    #     print(f"{one_msg.source}: {one_msg.content}")

    ## The asynchronous way to get the messages
    async for one_msg in team.run_stream(task="Start the debate!"):
        print("-" * 40)
        if isinstance(one_msg, TaskResult):
            print(f"Stopping reason: {one_msg.stop_reason}")
        else:
            print(f"{one_msg.source}: {one_msg.content}")

    # res = await model.create(
    #     messages=[UserMessage(content="Hello, how are you?", source="user")]
    # )
    # print(res)


if __name__ == "__main__":
    asyncio.run(main())
    print("Finished running the OpenAI chat completion client.")
