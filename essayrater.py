import streamlit as st
from openai import OpenAI
from io import BytesIO
from PIL import Image
import base64
import baiduocr

api_key = "sk-umH9cf34da865f51e5b07d829a28bac29d8cac32594pvwsD"
if 'history' not in st.session_state:
    st.session_state['history'] = [{'role': 'system', 'content': ''}]

st.markdown('# Handwriting Essay Rater')
api_key = st.text_input('OpenAI API Key', value='111', type='password')

# display chat
for msg in st.session_state['history'][1:]:
    if msg['role'] == 'user':
        with st.chat_message('user'):
            for i in msg['content']:
                if i['type'] == 'text':
                    st.write(i['text'])
                else:
                    with st.expander('Attached Image'):
                        img = Image.open(BytesIO(base64.b64decode(i['image_url']['url'][23:])))
                        st.image(img)
    else:
        with st.chat_message('assistant'):
            msg_content = ''.join(['  ' + char if char == '\n' else char for char in msg['content']])  # fixes display issue
            st.markdown('Assistant: ' + msg_content)

# get user inputs
text_input = st.text_input('Prompt', '', key=st.session_state['counters'][0])
img_input = st.file_uploader('Images', accept_multiple_files=True, key=st.session_state['counters'][1])

# set up button layout
st.markdown(
    """
    <style>
        [data-testid="column"]
        {
            width: calc(33.3333% - 1rem) !important;
            flex: 1 1 calc(33.3333% - 1rem) !important;
            min-width: calc(33% - 1rem) !important;
        }
        div[data-testid="column"]:nth-of-type(2)
        {
            text-align: right;
        }
    </style>
    """, unsafe_allow_html=True
)
cols = st.columns(2)


