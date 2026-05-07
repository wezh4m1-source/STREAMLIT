import streamlit as st
import google.generativeai as genai

# 1. ڕێکخستنی لاپەڕە
st.set_page_config(page_title="KomarUniAI", page_icon="🎓", layout="wide")

# 2. دیزاینی مۆدێرن: لۆگۆ وەک باکگراوند + ستایلی چات
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
    
    .main-title {
        text-align: center;
        font-size: 50px;
        font-weight: bold;
        background: linear-gradient(to right, #4285f4, #9b72cb, #d96570);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        padding-top: 20px;
    }

    /* ستایلکردنی سندوقی چات بۆ ئەوەی لەگەڵ باکگراوندەکە بگونجێت */
    .stChatMessage {
        background-color: rgba(30, 31, 32, 0.8) !important;
        border-radius: 15px !important;
        border: 1px solid rgba(255, 255, 255, 0.1);
        margin-bottom: 10px;
    }

    header, footer {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)

st.markdown('<div class="main-title">KomarUniAI</div>', unsafe_allow_html=True)
st.markdown('<p style="text-align: center; color: #8e918f; font-size: 18px;">Ethics • Knowledge • Skills</p>', unsafe_allow_html=True)

# 3. لۆژیکی پەیوەندی سکیور و تێپەڕاندنی بلۆکی ناوچە
if "GEMINI_API_KEY" in st.secrets:
    api_key = st.secrets["GEMINI_API_KEY"]
    genai.configure(api_key=api_key)
    
    # بەکارهێنانی وەشانی جێگیری gemini-pro کە کەمترین کێشەی Region ی هەیە
    try:
        model = genai.GenerativeModel('gemini-pro')
    except:
        st.error("کێشەیەک لە بارکردنی مۆدێلەکە هەیە.")
else:
    st.error("تکایە API Key لە Secrets دابنێ!")
    st.stop()

# 4. سیستەمی مێژووی چات
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 5. وەڵامدانەوە بە زمانی کوردی پاراو
if prompt := st.chat_input("لێرە پرسیارەکەت بنووسە..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            # فێڵی Prompt Engineering بۆ ئەوەی کوردییەکەی زۆر باش بێت
            full_prompt = (
                "تۆ زیرەکی دەستکردی زانکۆی کۆماریت. "
                "وەڵامی ئەم پرسیارە بدەرەوە بە کوردییەکی زۆر پاراو و ڕەوان: " + prompt
            )
            response = model.generate_content(full_prompt)
            
            if response:
                st.markdown(response.text)
                st.session_state.messages.append({"role": "assistant", "content": response.text})
        except Exception as e:
            st.error("ببورە، سێرڤەرەکانی Google هێشتا ڕێگری دەکەن. ئەمە دەسەلمێنێت کە دەبێت کلیلێکی نوێ لە 'پڕۆژەیەکی نوێ' دروست بکەیت.")
