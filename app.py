import streamlit as st
import google.generativeai as genai

# ١. خوێندنەوەی کلیلەکە بە شێوەی سکیور لە Secrets
if "GEMINI_API_KEY" in st.secrets:
    API_KEY = st.secrets["GEMINI_API_KEY"]
    genai.configure(api_key=API_KEY)
else:
    st.error("تکایە API Key لە بەشی Secrets دابنێ!")
    st.stop()

# ٢. مۆدێلەکە (بە وەشانی جێگیر)
model = genai.GenerativeModel('gemini-1.5-flash')

# ٣. ستایلی Gemini و دیزاین
st.markdown("""
    <style>
    .stApp { background-color: #131314; color: white; direction: rtl; }
    .main-title { text-align: center; font-size: 40px; color: #8ab4f8; font-weight: bold; }
    header, footer {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)

st.markdown('<div class="main-title">KomarUniAI</div>', unsafe_allow_html=True)

# ٤. لۆژیکی چات
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("بنووسە بۆ لێکۆڵینەوە..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            response = model.generate_content(prompt)
            st.markdown(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})
        except Exception as e:
            st.error(f"Error: {e}")
