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
quiz =  st.Page("quiz.py", title="Quiz maker", icon=":material/security:")
voicechat =  st.Page("voicechat.py", title="Voice Chat", icon=":material/security:")
keyword = st.Page("keyword.py", title="Keyword analysis", icon=":material/bug_report:")
pages = [home, moment, chat, quiz, voicechat, keyword]

st.title("AI Assited Language Teaching")


pg = st.navigation(pages)

pg.run()
