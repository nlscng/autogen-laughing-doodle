import streamlit as st

st.title("Agetngs Debate!")

topic = st.text_input("Enter the debate topic", "Climate Change")

clicked = st.button("Start Debate", type="primary")

if clicked:
    st.write("Debate started on the topic:", topic)
