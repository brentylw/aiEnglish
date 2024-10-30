import streamlit as st
from openai import OpenAI

with st.sidebar:
    st.title("Multi-LLM Chatbot")
    llmodel = st.selectbox("Choose an LLM", ["ChatGPT", "Llama-3", "文心一言", "通义前言"])
    openai_api_key = st.text_input("API Key", key="chatbot_api_key", type="password", value="123")

st.caption("🚀 A Streamlit chatbot")
if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "assistant", "content": "How can I help you?"}]

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

if prompt := st.chat_input():
    if not openai_api_key:
        st.info("Please add your OpenAI API key to continue.")
        st.stop()
    if llmodel == "ChatGPT":
    	model_url = "https://api.gptsapi.net/v1"
    	model = "gpt-4o"
    	#sk-umH9cf34da865f51e5b07d829a28bac29d8cac32594pvwsD

    client = OpenAI(
      base_url=model_url,
      api_key="sk-umH9cf34da865f51e5b07d829a28bac29d8cac32594pvwsD"
  )
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)
    response = client.chat.completions.create(
    	model=model, 
    	messages=st.session_state.messages
    	)
    msg = response.choices[0].message.content
    
    st.session_state.messages.append({"role": "assistant", "content": msg})
    st.chat_message("assistant").write(msg)
