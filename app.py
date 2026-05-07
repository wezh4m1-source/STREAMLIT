import streamlit as st
import google.generativeai as genai

# 1. ڕێکخستنی لاپەڕە
st.set_page_config(page_title="KomarUniAI", page_icon="🎓", layout="wide")

# 2. ستایلی تایبەت بۆ ئەوەی لۆگۆکە بە جوانی و گەورەیی دەربکەوێت
st.markdown("""
    <style>
    /* تێکەڵکردنی لۆگۆ و باکگراوند لە بەشی سەرەوە */
    .hero-section {
        background-image: linear-gradient(rgba(19, 19, 20, 0.8), rgba(19, 19, 20, 0.9)), url("https://raw.githubusercontent.com/wezh4m1-source/STREAMLIT/main/Gemini_Generated_Image_.png");
        background-size: cover;
        background-position: center;
        padding: 60px 20px;
        text-align: center;
        border-radius: 0 0 30px 30px;
        margin-top: -60px;
        border-bottom: 2px solid #4285f4;
    }
    
    .stApp {
        background-color: #131314;
        color: #e3e3e3;
        direction: rtl;
    }

    .main-title {
        font-size: 50px;
        font-weight: bold;
        background: linear-gradient(to right, #4285f4, #9b72cb, #d96570);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 10px;
    }

    /* شاردنەوەی شتە زیادەکانی ستریمڵێت */
    header, footer, #MainMenu {visibility: hidden;}
    
    /* ڕێکخستنی سندوقی نووسین */
    .stChatInput {
        bottom: 20px !important;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. نیشاندانی بەشی سەرەوە بە دیزاینێکی جوان
st.markdown(f"""
    <div class="hero-section">
        <div class="main-title">KomarUniAI</div>
        <p style="color: #ffffff; font-size: 20px; font-weight: 300;">زیرەکی دەستکردی زانکۆی کۆمار بۆ زانست و تەکنەلۆژیا</p>
    </div>
    """, unsafe_allow_html=True)

# 4. لۆژیکی API (بە شێوەیەکی سکیور لە Secrets)
if "GEMINI_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
    model = genai.GenerativeModel('gemini-1.5-flash')
else:
    st.error("تکایە API Key لە Secrets دابنێ")
    st.stop()

# 5. شوێنی چات
if "messages" not in st.session_state:
    st.session_state.messages = []

# نیشاندانی نامەکان بە شێوەیەکی ڕێک
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("چی لێکۆڵینەوەیەک بکەم بۆت؟"):
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
