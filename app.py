import streamlit as st
import google.generativeai as genai

# 1. ڕێکخستنی سەرەکی لاپەڕە (وەک Gemini)
st.set_page_config(page_title="KomarUniAI", page_icon="🎓", layout="centered")

# 2. ستایلکردنی وێبسایتەکە بە CSS
st.markdown("""
    <style>
    .stApp {
        background-color: #131314;
        color: #e3e3e3;
        direction: rtl;
    }
    .main-title {
        text-align: center;
        font-size: 45px;
        font-weight: bold;
        background: linear-gradient(to right, #4285f4, #9b72cb, #d96570);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        padding-top: 20px;
    }
    .sub-title {
        text-align: center;
        color: #8e918f;
        margin-bottom: 30px;
    }
    /* شاردنەوەی مینیوەکانی ستریمڵێت */
    header, footer, #MainMenu {visibility: hidden;}
    
    /* ستایلی چاتەکان */
    .stChatMessage {
        background-color: #1e1f20 !important;
        border-radius: 20px !important;
        padding: 15px !important;
        margin-bottom: 10px !important;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. پەیوەندی سکیور بە API (خوێندنەوە لە Secrets)
if "GEMINI_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
else:
    st.error("تکایە GEMINI_API_KEY لە بەشی Secrets دابنێ!")
    st.stop()

# 4. دۆزینەوەی مۆدێلی کارا بۆ ئەکاونتەکەت
@st.cache_resource
def get_working_model():
    try:
        # لیستی ئەو مۆدێلانەی بۆ تۆ ڕێپێدراون
        available = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
        for m_name in ['models/gemini-1.5-flash', 'models/gemini-1.5-pro', 'models/gemini-pro']:
            if m_name in available:
                return genai.GenerativeModel(m_name)
        return genai.GenerativeModel(available[0])
    except:
        return genai.GenerativeModel('gemini-pro')

model = get_working_model()

# 5. پێشاندانی لۆگۆ و ناونیشان
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    try:
        st.image("logo.png", width=150) # دڵنیابە فایلی logo.png لە گیتھاب هەیە
    except:
        st.markdown("<h1 style='text-align:center;'>🎓</h1>", unsafe_allow_html=True)

st.markdown('<div class="main-title">KomarUniAI</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">زیرەکی دەستکردی زانکۆی کۆمار بۆ زانست و تەکنەلۆژیا</div>', unsafe_allow_html=True)

# 6. لۆژیکی مێژووی چات
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 7. شوێنی نووسینی نامە
if prompt := st.chat_input("چی لێکۆڵینەوەیەک بکەم بۆت؟"):
    # نیشاندانی نامەی بەکارهێنەر
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # وەڵامدانەوەی AI
    with st.chat_message("assistant"):
        response_placeholder = st.empty()
        full_response = ""
        try:
            # وەڵامدانەوە بە شێوازی Streaming (پیت بە پیت)
            response = model.generate_content(prompt, stream=True)
            for chunk in response:
                full_response += chunk.text
                response_placeholder.markdown(full_response + "▌")
            response_placeholder.markdown(full_response)
        except Exception as e:
            st.error(f"ببورە، هەڵەیەک ڕوویدا: {str(e)}")
            full_response = "Error occurred."
            
    st.session_state.messages.append({"role": "assistant", "content": full_response})
