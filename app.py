import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="KomarUniAI", layout="centered")

# ستایلی سادە
st.markdown("""
    <style>
    .stApp { background-color: #131314; color: white; direction: rtl; }
    .title { text-align: center; color: #8ab4f8; font-size: 40px; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

st.markdown('<div class="title">KomarUniAI</div>', unsafe_allow_html=True)

# بەکارهێنانی مۆدێلی جێگیر
API_KEY = "AIzaSyA_hvWBVhBWvTJcE3ScDtJVLPyKNjc1pzg"
genai.configure(api_key=API_KEY)

# لێرە ناوی مۆدێلەکەمان گۆڕی بۆ نوێترین وەشانی فلاش
model = genai.GenerativeModel('models/gemini-1.5-flash')

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("بنووسە..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            # وەڵامدانەوەی سادە بێ ستریمینگ بۆ ئەوەی کێشە نەدات
            response = model.generate_content(prompt)
            st.markdown(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})
        except Exception as e:
            st.error(f"Error: {e}")
