import streamlit as st
import google.generativeai as genai

# 1. ڕێکخستنی لاپەڕە
st.set_page_config(page_title="KomarUniAI", page_icon="🎓", layout="centered")

# 2. چاککردنی ستایلەکە (لێرەدا هەڵەکە هەبوو)
st.markdown("""
    <style>
    .stApp {
        background-color: #131314;
        color: #e3e3e3;
        direction: rtl;
    }
    .main-title {
        text-align: center;
        font-size: 40px;
        font-weight: bold;
        background: linear-gradient(to right, #4285f4, #9b72cb, #d96570);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    header {visibility: hidden;}
    footer {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)

st.markdown('<div class="main-title">KomarUniAI</div>', unsafe_allow_html=True)
st.markdown('<p style="text-align: center; color: #8e918f;">زیرەکی دەستکردی زانکۆی کۆمار</p>', unsafe_allow_html=True)

# 3. ڕێکخستنی API
API_KEY = "AIzaSyA_hvWBVhBWvTJcE3ScDtJVLPyKNjc1pzg"
genai.configure(api_key=API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

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
        response_placeholder = st.empty()
        full_response = ""
        try:
            response = model.generate_content(prompt, stream=True)
            for chunk in response:
                full_response += chunk.text
                response_placeholder.markdown(full_response + "▌")
            response_placeholder.markdown(full_response)
        except Exception as e:
            st.error(f"Error: {e}")
            
    st.session_state.messages.append({"role": "assistant", "content": full_response})
