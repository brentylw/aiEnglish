import streamlit as st



request_2 = st.Page(
    "request/request_2.py", title="Request 2", icon=":material/bug_report:"
)

admin_1 = st.Page(
    "admin/admin_1.py",
    title="Mood Moments in Classroom",
    icon=":material/person_add:"
)
admin_2 = st.Page("request/request_1.py", title="Chat with LLMs", icon=":material/security:")


pages = [ request_2, admin_1, admin_2]

st.title("AI Assited Language Teaching")


pg = st.navigation(pages)


pg.run()
