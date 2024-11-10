import streamlit as st
from openai import OpenAI
from io import BytesIO
from PIL import Image
import base64
import baiduocr


if 'history' not in st.session_state:
    st.session_state['history'] = [{'role': 'system', 'content': ''}]

st.markdown('# Handwriting Essay Rater')
api_key = "sk-umH9cf34da865f51e5b07d829a28bac29d8cac32594pvwsD"
# display chat
for msg in st.session_state['history'][1:]:
    if msg['role'] == 'user':
        with st.chat_message('user'):
            st.write(msg['content'])
    else:
        with st.chat_message('assistant'):
            msg_content = ''.join(['  ' + char if char == '\n' else char for char in msg['content']])  # fixes display issue
            st.markdown('Assistant: ' + msg_content)

# get user inputs
prom = st.text_area(label, value="Rate the essays.")
img_input = st.file_uploader('Images', accept_multiple_files=True)

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
with cols[0]:
    if st.button('Send'):
        
        if not (img_input):
            st.warning('You can\'t just send nothing!')
            st.stop()
        msg = {'role': 'user', 'content': []}
        for img in img_input:
            if img.name.split('.')[-1].lower() not in ['png', 'jpg', 'jpeg', 'gif', 'webp']:
                st.warning('Only .jpg, .png, .gif, or .webp are supported')
                st.stop()
            encoded_img = base64.b64encode(img.read()).decode('utf-8')
            result = baiduocr.ocr_image(encoded_img)
            msg['content'].append({'type': 'text', 'text': prom +":"+result})

        st.session_state['history'].append(msg)
        history = (
            st.session_state['history']
            if st.session_state['history'][0]['content']
            else st.session_state['history'][1:]
        )

        client = OpenAI(base_url="https://api.gptsapi.net/v1", api_key=api_key)
        response = client.chat.completions.create(
                model = "gpt-4o",
                messages=history
            )
        mymsg = response.choices[0].message.content

        st.session_state['history'].append(
            {'role': 'assistant', 'content': mymsg}
        )

        st.rerun()

# clear chat history
with cols[1]:
    if st.button('Clear'):
        st.session_state['history'] = [st.session_state['history'][0]]
        st.rerun()

