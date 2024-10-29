import streamlit as st
from openai import OpenAI
import json

if "tweet" not in st.session_state:
    st.session_state.tweet = ""
if "text_error" not in st.session_state:
    st.session_state.text_error = ""
if "feeling_lucky" not in st.session_state:
    st.session_state.feeling_lucky = False
if "n_requests" not in st.session_state:
    st.session_state.n_requests = 0

st.title("Mood Moments")
name = st.text_input(label="Your Name", placeholder="Nickname ")
topic = st.text_input(label="Topic", placeholder="Listening and Speaking ")
mood = st.text_input(
    label="Mood (e.g. inspirational, funny, serious) (optional)",
    placeholder="inspirational",
)

with st.sidebar:
    st.title("Multi-LLM Chatbot")
    llmodel = st.selectbox("Choose an LLM", ["ChatGPT", "Llama-3", "文心一言", "通义前言"])
    openai_api_key = st.text_input("API Key", key="chatbot_api_key", type="password")


def generate_text(topic: str, mood: str = "", style: str = ""):
    """Generate Tweet text."""
    if st.session_state.n_requests >= 5:
        st.session_state.text_error = "Too many requests. Please wait a few seconds before generating another Tweet."
        logging.info(f"Session request limit reached: {st.session_state.n_requests}")
        st.session_state.n_requests = 1
        return

    st.session_state.tweet = ""
    st.session_state.text_error = ""
    st.session_state.name = ""

    if not topic:
        st.session_state.text_error = "Please enter a topic"
        return

    with text_spinner_placeholder:
        with st.spinner("Please wait while your Tweet is being generated..."):
            mood_prompt = f"{mood} " if mood else ""
            prompt = f"Write a {mood_prompt}Tweet about {topic} in less than 120 characters:\n\n"

            client = OpenAI(
                     base_url="https://api.gptsapi.net/v1",
                     api_key="sk-umH9cf34da865f51e5b07d829a28bac29d8cac32594pvwsD"
                     )
    
            response = client.chat.completions.create(
    	             model= "gpt-4o", 
    	             messages=[{"role": "user", "content": prompt}]
    	             )
            msg = response.choices[0].message.content
            st.session_state.tweet = msg
            
            return msg
def show_moments():
    lines = open("mood_moments.txt", "r",  encoding="utf-8").readlines()
    for msg in lines:
        st.chat_message("user").write(msg.split("\t")[0]+": "+msg.split("\t")[1])

def save_moment():
# Store the nickname and generated message to a text file 
    with open("mood_moments.txt", "a",  encoding="utf-8") as f:  
        f.write(f"{name}\t{tweet}\n") # Store both the name and the message 

st.session_state.feeling_lucky = not st.button(
        label="Generate text",
        type="primary",
        on_click=generate_text,
        args=(topic, mood),
    )


if st.session_state.text_error:
    st.error(st.session_state.text_error)

if st.session_state.tweet:
    st.markdown("""---""")
    tweet = st.text_area(label="Your Mood Moments", value=st.session_state.tweet, height=100)
text_spinner_placeholder = st.empty()
st.button(
     label="save your Moments",
     type="primary",
     on_click=save_moment
    )
st.button(
     label="show all Moments",
     type="primary",
     on_click=show_moments
    )

