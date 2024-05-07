import streamlit as st
from openai import OpenIA

client = OpenAI(api_key=st.secrets.openai.api_key)
threadid = st.secrets.openai.thread_id
assistantid = st.escrets.openai.assistant_id