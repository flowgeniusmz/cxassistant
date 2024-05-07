import streamlit as st
from openai import OpenAI
import time

client = OpenAI(api_key=st.secrets.openai.api_key)
threadid = st.secrets.openai.thread_id
assistantid = st.escrets.openai.assistant_id

displaymessages = [{"role": "assistant", "content": "Welcome to AlmyCX - how can I help?"}]

def append_display_message(role, content):
    displaymessages.append({"role": role, "content": content})

def display_chat_message(role, content):
    with st.chat_message(name=role):
        st.markdown(body=content)

    append_display_message(role=role, content=content)

def create_thread_message(role, content):
    message = client.beta.threads.messages.create(thread_id=threadid, role=role, content=content)
    messageid = message.id
    return messageid

chatcontainer = st.container(border=True, height=500)
promptcontainer = st.container(border=False, height=100)


with chatcontainer:
    for displaymessage in displaymessages:
        display_chat_message(role=displaymessage['role'], content=displaymessage['content'])

with promptcontainer:
    if prompt := st.chat_input(placeholder="Enter question here"):
        display_chat_message(role="user", content=prompt)
        create_thread_message(role="user", content=prompt)
        run = client.beta.threads.runs.create(thread_id = threadid, assistant_id=assistantid)
        while run.status != "completed":
            time.sleep(2)
            run = client.beta.threads.runs.retrieve(thread_id=threadid, run_id=run.id)
            if run.status == "completed":
                threadmessages = client.beta.threads.messages.list(thread_id=threadid)
                for threadmessage in threadmessages:
                    if threadmessage.role == "assistant" and threadmessage.run_id == run.id:
                        display_chat_message(role="assistant", content=threadmessage.content[0].text.value)
                        


