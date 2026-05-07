import streamlit as st
import google.generativeai as genai

# 1. ڕێکخستنی سەرەکی
st.set_page_config(page_title="KomarUniAI", page_icon="🎓", layout="centered")

# 2. CSS بۆ دیزاینێکی سادە و پرۆفیشناڵ
st.markdown("""
    <style>
    .stApp { background-color: #131314; color: white; direction: rtl; }
    header, footer {visibility: hidden;}
    .main-title {
        text-align: center;
        font-size: 40px;
        font-weight: bold;
        background: linear-gradient(to right, #4285f4, #9b72cb, #d96570);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. پیشاندانی لۆگۆ
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    try:
        st.image("logo.png", use_container_width=True)
    except:
        st.markdown("<h1 style='text-align:center;'>🎓</h1>", unsafe_allow_html=True)

st.markdown('<div class="main-title">KomarUniAI</div>', unsafe_allow_html=True)
st.markdown('<p style="text-align: center; color: #8e918f;">زیرەکی دەستکردی زانکۆی کۆمار</p>', unsafe_allow_html=True)

# 4. لۆژیکی بنبڕکردنی هەڵەی Region
if "GEMINI_API_KEY" in st.secrets:
    api_key = st.secrets["GEMINI_API_KEY"]
    genai.configure(api_key=api_key)
    
    # بەکارهێنانی مۆدێلی جێگیر و سادە بەبێ System Instruction ی قورس
    model = genai.GenerativeModel('gemini-pro') 
else:
    st.error("API Key نەدۆزرایەوە لە Secrets!")
    st.stop()

# 5. سیستەمی چات
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("لێرە پرسیارەکەت بنووسە..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            # ناردنی ڕێنماییەکە لەناو خودی پرسیارەکەدا (Prompt Engineering)
            # ئەمە باشترین ڕێگەیە بۆ ئەوەی کوردییەکەی پاراو بێت بەبێ هەڵەی سێرڤەر
            kurdish_prompt = f"وەک زیرەکی دەستکردی زانکۆی کۆمار، زۆر بە کوردییەکی پاراو و ڕەوان وەڵامی ئەمە بدەرەوە: {prompt}"
            
            response = model.generate_content(kurdish_prompt)
            st.markdown(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})
        except Exception as e:
            st.error("گووڵ ڕێگری لەم داواکارییە دەکات. تکایە پڕۆژەیەکی نوێ (New Project) لە AI Studio دروست بکە و کلیلێکی تری لێ وەربگرە.")
