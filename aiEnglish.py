import streamlit as st



home = st.Page(
    "home.py", title="GAI Assisted Language Teaching", icon=":material/bug_report:"
)

moment = st.Page(
    "moment.py",
    title="Mood Moments in Classroom",
    icon=":material/person_add:"
)
chat = st.Page("chatbot.py", title="Chat with LLMs", icon=":material/security:")
chatpdf =  st.Page("chatpdf.py", title="Chat with PDF", icon=":material/security:")

pages = [home, moment, chat, chatpdf]

st.title("AI Assited Language Teaching")


pg = st.navigation(pages)

pg.run()
