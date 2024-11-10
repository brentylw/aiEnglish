import streamlit as st
st.caption("🚀 welcome")
st.title("徐州 江苏师范大学")

st.write("""
新时代学科教学（英语）专业硕士人才培养研讨会

""")
st.download_button(
        label="Download case_data",
        data=csv_data,
        file_name='case_data.rar'
    )
st.write("Your Language Learning Assistant. By Linwei Yang at Yantai University")
