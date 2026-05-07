import streamlit as st
import google.generativeai as genai

# --- ڕێکخستنی لاپەڕە ---
st.set_page_config(page_title="KomarUniAI", layout="centered")

# --- دیزاینی لۆگۆ وەک باکگراوند ---
st.markdown("""
    <style>
    .stApp {
        background-image: linear-gradient(rgba(19, 19, 20, 0.85), rgba(19, 19, 20, 0.95)), 
                          url("https://raw.githubusercontent.com/wezh4m1-source/STREAMLIT/main/logo.png");
        background-size: cover;
        background-attachment: fixed;
        color: white;
        direction: rtl;
    }
    header, footer {visibility: hidden;}
    .main-title {
        text-align: center;
        font-size: 50px;
        font-weight: bold;
        background: linear-gradient(45deg, #4285f4, #9b72cb);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0px;
    }
    </style>
    """, unsafe_allow_html=True)

st.markdown('<div class="main-title">KomarUniAI 🎓</div>', unsafe_allow_html=True)
st.markdown('<p style="text-align: center; color: #bbb;">Ethics • Knowledge • Skills</p>', unsafe_allow_html=True)

# --- ڕێکخستنی سکیور ---
if "GEMINI_API_KEY" in st.secrets:
    api_key = st.secrets["GEMINI_API_KEY"]
    genai.configure(api_key=api_key)
else:
    st.error("API Key نەدۆزرایەوە!")
    st.stop()

# --- لۆژیکی پەیوەندی (بۆ تێپەڕاندنی هەڵەی 404) ---
def generate_response(user_input):
    # لێرەدا فەرمان دەکەین بە زمانی سادەی کوردی وەڵام بداتەوە
    full_prompt = f"تۆ لێکۆڵەرێکی کوردی لە زانکۆی کۆمار. زۆر بە کوردییەکی شیرین و پاراو وەڵامی ئەمە بدەرەوە: {user_input}"
    
    # تاقیکردنەوەی مۆدێلەکان یەکە بە یەکە بەبێ ڕێنمایی سیستەم (بۆ تێپەڕاندنی سنووری وڵات)
    for model_name in ['gemini-pro', 'gemini-1.5-flash']:
        try:
            model = genai.GenerativeModel(model_name)
            response = model.generate_content(full_prompt)
            return response.text
        except:
            continue
    return "ببورە، سێرڤەرەکانی Google لە ناوچەی تۆدا ڕێگەیان پێنەدراوە. تکایە کلیلێکی نوێ تاقی بکەرەوە یان پڕۆژەیەکی نوێ لە AI Studio دروست بکە."

# --- سیستەمی چات ---
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

for message in st.session_state.chat_history:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("لێرە پرسیارەکەت بنووسە..."):
    st.session_state.chat_history.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("خەریکە بیر دەکەمەوە..."):
            answer = generate_response(prompt)
            st.markdown(answer)
            st.session_state.chat_history.append({"role": "assistant", "content": answer})
