import streamlit as st
import google.generativeai as genai

# 1. ڕێکخستنی لاپەڕە
st.set_page_config(page_title="KomarUniAI", page_icon="🎓", layout="centered")

# 2. ستایلی CSS بۆ لۆگۆ و دیزاین
st.markdown("""
    <style>
    .stApp { background-color: #131314; color: white; direction: rtl; }
    header, footer {visibility: hidden;}
    
    .header-banner {
        width: 100%;
        height: 200px;
        background-image: linear-gradient(rgba(0,0,0,0.5), rgba(0,0,0,0.5)), url("https://raw.githubusercontent.com/wezh4m1-source/STREAMLIT/main/logo.png");
        background-size: contain;
        background-repeat: no-repeat;
        background-position: center;
        margin-bottom: 20px;
    }
    
    .main-title {
        text-align: center;
        font-size: 45px;
        font-weight: bold;
        background: linear-gradient(to right, #4285f4, #9b72cb, #d96570);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. نیشاندانی بانەر و تایتڵ
st.markdown('<div class="header-banner"></div>', unsafe_allow_html=True)
st.markdown('<div class="main-title">KomarUniAI</div>', unsafe_allow_html=True)

# 4. ڕێکخستنی مۆدێل
if "GEMINI_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
    # بەکارهێنانی وەشانی جێگیر بۆ ڕێگری لە 404
    model = genai.GenerativeModel('gemini-1.5-flash')
else:
    st.warning("تکایە API Key لە Secrets دابنێ.")
    st.stop()

# 5. سیستەمی چات
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
            response = model.generate_content(prompt)
            st.markdown(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})
        except Exception as e:
            st.error(f"Error: {e}")
