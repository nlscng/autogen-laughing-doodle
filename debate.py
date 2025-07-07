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

async def team_config(topic):
    model = OpenAIChatCompletionClient(model="gpt-4o", api_key=my_current_api_key)

    host = AssistantAgent(
        name="Jane",
        system_message=(
            f"Your name is Jane, the host for a debate about the topic: {topic}. "
            "You will kick off and moderate the debate between two participants: "
            "a supporter agent John and a critic agent Jack. "
            "You will start the debate for the two participants, annouse yourself as the host, introduce the participants, and moderate the debate. "
            "A round is defined as both John and Jack having a turn to speak."
            "At the begining of each round, announce the round number. "
            "And at the begining of the third round, announce that it is the last round."
            "After the last round is complete, thank the audience, summarize the key points made by each participant. "
            "say exactly 'TERMINATE' to end the debate. "
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
        participants=[host, critic, supporter],
        max_turns=20,
        termination_condition=TextMentionTermination(
            text="TERMINATE",
        ),
    )
    return team
    

async def debate(team):
    # Start the debate
    res = await team.run(task="Start the debate!")

    ## The synchronous way to get the messages
    # for one_msg in res.messages:
    #     print("-"*20)
    #     print(f"{one_msg.source}: {one_msg.content}")

    ## The asynchronous way to get the messages
    async for one_msg in team.run_stream(task="Start the debate!"):
        if isinstance(one_msg, TaskResult):
            one_msg = f"Stopping reason: {one_msg.stop_reason}"
            yield one_msg
        else:
            one_msg = f"{one_msg.source}: {one_msg.content}"
            yield one_msg

    # res = await model.create(
    #     messages=[UserMessage(content="Hello, how are you?", source="user")]
    # )
    # print(res)

async def main():
    topic = "Climate Change"
    team = await team_config(topic)
    async for one_msg in debate(team):
        print('-' * 40)
        print(one_msg)

if __name__ == "__main__":
    asyncio.run(main())
    print("Finished running the OpenAI chat completion client.")
