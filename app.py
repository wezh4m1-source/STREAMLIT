import streamlit as st
import google.generativeai as genai

# 1. ڕێکخستنی لاپەڕە
st.set_page_config(page_title="KomarUniAI", page_icon="🎓", layout="wide")

# 2. دیزاینی لۆگۆ وەک باکگراوند (زۆر شیک و شەفاف)
st.markdown("""
    <style>
    .stApp {
        background-image: linear-gradient(rgba(19, 19, 20, 0.8), rgba(19, 19, 20, 0.9)), 
                          url("https://raw.githubusercontent.com/wezh4m1-source/STREAMLIT/main/logo.png");
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
        color: white;
        direction: rtl;
    }
    .main-title {
        text-align: center;
        font-size: 55px;
        font-weight: bold;
        background: linear-gradient(to right, #4285f4, #9b72cb, #d96570);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0px;
    }
    header, footer {visibility: hidden;}
    
    /* ڕێکخستنی سندوقی چات */
    .stChatInputContainer {
        padding-bottom: 20px;
    }
    .stChatMessage {
        background-color: rgba(255, 255, 255, 0.05) !important;
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 15px !important;
    }
    </style>
    """, unsafe_allow_html=True)

st.markdown('<div class="main-title">KomarUniAI</div>', unsafe_allow_html=True)
st.markdown('<p style="text-align: center; color: #aaa;">Ethics • Knowledge • Skills</p>', unsafe_allow_html=True)

# 3. لۆژیکی پەیوەندی (بەکارهێنانی API بە سادەیی)
if "GEMINI_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
else:
    st.error("تکایە API Key لە Secrets دابنێ")
    st.stop()

# 4. مێژووی چات
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 5. وەڵامدانەوە (لێرەدا تەنها یەک مۆدێل تاقی دەکەینەوە بەبێ ئاڵۆزی)
if prompt := st.chat_input("چی لێکۆڵینەوەیەک بکەم بۆت؟"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            # بەکارهێنانی مۆدێلی بنەڕەتی gemini-pro کە زۆربەی کات جێگیرە
            model = genai.GenerativeModel('gemini-pro')
            
            # ناردنی پرسیارەکە بە زمانی کوردی
            response = model.generate_content(
                f"تۆ ناوت KomarUniAI یە. وەک کوردێکی شارەزا بە کوردییەکی زۆر پاراو وەڵام بدەرەوە: {prompt}"
            )
            
            if response.text:
                st.markdown(response.text)
                st.session_state.messages.append({"role": "assistant", "content": response.text})
            else:
                st.error("وەڵامەکەت بلۆک کراوە لەلایەن گوگلەوە.")
        except Exception as e:
            # ئەگەر لێرەشدا شکستی هێنا، تەنها یەک مانا دەگەیەنێت...
            st.error("هەڵەی سێرڤەر: Google ڕێگری لە ئایپی ئەم وێبسایتە دەکات.")
            st.info("ئامۆژگاری: پڕۆژەکەت لە Streamlit ڕەش بکەرەوە و دووبارە لە پۆڵدەرێکی تری GitHub دایبنێ تا ئایپییەکەی بگۆڕێت.")
