import streamlit as st
import google.generativeai as genai

# ١. ڕێکخستنی لاپەڕەکە (وەک Gemini)
st.set_page_config(page_title="KomarUniAI", page_icon="🎓", layout="centered")

# ٢. بەکارهێنانی CSS بۆ ئەوەی ڕووکارەکەی ڕێک وەک Gemini بێت
st.markdown("""
    <style>
    /* باکگراوندی تاریک */
    .stApp {
        background-color: #131314;
        color: #e3e3e3;
        direction: rtl;
    }
    
    /* شێوازی تایتڵ و لۆگۆ */
    .header-container {
        text-align: center;
        padding: 20px;
    }
    
    .main-title {
        font-size: 45px;
        font-weight: bold;
        background: linear-gradient(to right, #4285f4, #9b72cb, #d96570, #131314);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 5px;
    }

    /* شاردنەوەی نیشانەکانی Streamlit بۆ ئەوەی ببێتە وێبسایتێکی فەرمی */
    header {visibility: hidden;}
    footer {visibility: hidden;}
    #MainMenu {visibility: hidden;}
    
    /* ستایلکردنی چاتەکان */
    .stChatMessage {
        background-color: #1e1f20 !important;
        border-radius: 20px !important;
        padding: 15px !important;
        margin-bottom: 10px !important;
    }
    </style>
    """, unsafe_allow_index=True)

# ٣. پیشاندانی لۆگۆ و ناوی پڕۆژە
# تێبینی: وێنەی logo.png دەبێت لەگەڵ کۆدەکە لە گیتھاب بێت
st.markdown("""
    <div class="header-container">
        <h1 class="main-title">KomarUniAI</h1>
        <p style="color: #8e918f; font-size: 18px;">زیرەکی دەستکردی زانکۆی کۆمار بۆ لێکۆڵینەوە</p>
    </div>
    """, unsafe_allow_index=True)

# ٤. ڕێکخستنی API
API_KEY = "AIzaSyA_hvWBVhBWvTJcE3ScDtJVLPyKNjc1pzg"
genai.configure(api_key=API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

# ٥. میمۆری چات
if "messages" not in st.session_state:
    st.session_state.messages = []

# نیشاندانی چاتەکانی پێشوو
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# ٦. شوێنی نووسینی پرسیار
if prompt := st.chat_input("چی لێکۆڵینەوەیەک بکەم بۆت؟"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        response_placeholder = st.empty()
        full_response = ""
        try:
            # وەڵامدانەوە بە شێوازی Streaming (پیت بە پیت وەک Gemini)
            response = model.generate_content(prompt, stream=True)
            for chunk in response:
                full_response += chunk.text
                response_placeholder.markdown(full_response + "▌")
            response_placeholder.markdown(full_response)
        except Exception as e:
            st.error(f"کێشەیەک ڕوویدا: {e}")
            
    st.session_state.messages.append({"role": "assistant", "content": full_response})