import streamlit as st
import google.generativeai as genai
import os

# 1. ڕێکخستنی لاپەڕە
st.set_page_config(page_title="KomarUniAI", page_icon="🎓", layout="wide")

# 2. CSS بۆ ئەوەی لۆگۆکەت ببێتە Background و دیزاینەکە مۆدێرن بێت
st.markdown("""
    <style>
    .stApp {
        background-image: linear-gradient(rgba(19, 19, 20, 0.85), rgba(19, 19, 20, 0.95)), 
                          url("https://raw.githubusercontent.com/wezh4m1-source/STREAMLIT/main/logo.png");
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
        color: #e3e3e3;
        direction: rtl;
    }
    
    /* ڕێکخستنی ناوچەی نووسین */
    .stChatMessage {
        background-color: rgba(30, 31, 32, 0.7) !important;
        border-radius: 15px !important;
        border: 1px solid rgba(255, 255, 255, 0.1);
    }

    .main-title {
        text-align: center;
        font-size: 55px;
        font-weight: bold;
        background: linear-gradient(to right, #4285f4, #9b72cb, #d96570);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0px;
        padding-top: 20px;
    }

    header, footer {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)

st.markdown('<div class="main-title">KomarUniAI</div>', unsafe_allow_html=True)
st.markdown('<p style="text-align: center; color: #8e918f; font-size: 18px;">Ethics • Knowledge • Skills</p>', unsafe_allow_html=True)

# 3. پەیوەندی سکیور و تێپەڕاندنی سنووردارکردنی ناوچە
if "GEMINI_API_KEY" in st.secrets:
    API_KEY = st.secrets["GEMINI_API_KEY"]
    genai.configure(api_key=API_KEY)
    
    # تاقیکردنەوەی مۆدێلە جیاوازەکان
    @st.cache_resource
    def load_ai_model():
        # لیستکردنی هەموو مۆدێلەکان و تاقیکردنەوەی دانە بە دانە
        for model_name in ['gemini-1.5-flash', 'gemini-pro']:
            try:
                m = genai.GenerativeModel(model_name)
                # تاقیکردنەوەی سێرڤەر
                m.generate_content("hi")
                return m
            except:
                continue
        return None

    model = load_ai_model()
else:
    st.error("کلیلەکە لە Secrets دابنێ!")
    st.stop()

# 4. لۆژیکی چات
if "messages" not in st.session_state:
    st.session_state.messages = []

# پیشاندانی نامەکان
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 5. چارەسەری هەڵەی ناوچە لە کاتی وەڵامدانەوە
if prompt := st.chat_input("لێرە پرسیارەکەت بنووسە..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        if model:
            try:
                # ناردنی پرسیار بە فەرمانی کوردی
                kurdish_context = f"وەک زیرەکی دەستکردی زانکۆی کۆمار، وەڵامی ئەمە بدەرەوە بە کوردییەکی زۆر پاراو: {prompt}"
                response = model.generate_content(kurdish_context)
                st.markdown(response.text)
                st.session_state.messages.append({"role": "assistant", "content": response.text})
            except Exception as e:
                st.error("گووڵ هێشتا ڕێگری دەکات. تکایە پڕۆژەیەک لە ناوچەی 'United States' دروست بکە لە Google Cloud.")
        else:
            st.warning("باکگراوندەکە چالاکە، بەڵام سێرڤەرەکانی گوگل وەڵام نادەنەوە. تکایە کلیلێکی تری 'V1' تاقی بکەرەوە.")
