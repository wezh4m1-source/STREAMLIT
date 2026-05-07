import streamlit as st
import google.generativeai as genai
import os

# 1. ڕێکخستنی لاپەڕە
st.set_page_config(page_title="KomarUniAI", page_icon="🎓")

# 2. خوێندنەوەی API Key بە شێوەیەکی سکیور
# ئەگەر لە ستریمڵێت بیستووتە، لە بەشی Secrets دایبنێ
if "GEMINI_API_KEY" in st.secrets:
    api_key = st.secrets["GEMINI_API_KEY"]
else:


genai.configure(api_key=api_key)

# 3. بەکارهێنانی ناوی مۆدێلی گشتگیر (ئەمە دەبێت کار بکات)
try:
    model = genai.GenerativeModel('gemini-1.5-flash')
except:
    model = genai.GenerativeModel('gemini-pro')

st.title("🎓 KomarUniAI")
st.write("بەخێرهاتی بۆ لێکۆڵەری زیرەکی زانکۆی کۆمار")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("چی لێکۆڵینەوەیەک بکەم؟"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            # وەڵامدانەوەی سادە
            response = model.generate_content(prompt)
            st.markdown(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})
        except Exception as e:
            st.error(f"کێشەیەک هەیە: {e}")
