import streamlit as st
import asyncio
from debate import team_config, debate

st.title("Agents Debate!")

topic = st.text_input("Enter the debate topic", "Climate Change")

clicked = st.button("Start Debate", type="primary")

chat = st.container()

if clicked:
    chat.empty()  # Clear the chat area

    async def main():
        team = await team_config(topic)
        with chat:
            async for one_msg in debate(team):
                if one_msg.startswith("Jane"): ## female emoji 
                    with st.chat_message(name="Jane", avatar="https://openmoji.org/library/emoji-1F469/"):
                        st.write(one_msg)
                elif one_msg.startswith("John"): ## thumbs up emoji
                    with st.chat_message(name="John", avatar="https://openmoji.org/library/emoji-1F44D/"):
                        st.write(one_msg)
                elif one_msg.startswith("Jack"): ## thumbs down emoji
                    with st.chat_message(name="Jack", avatar="https://openmoji.org/library/emoji-1F44E/"):
                        st.write(one_msg)
    asyncio.run(main())

    st.balloons() # Celebrate the end of the debate