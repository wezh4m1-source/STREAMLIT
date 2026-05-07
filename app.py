import streamlit as st
import google.generativeai as genai

# 1. ڕێکخستنی لاپەڕە
st.set_page_config(page_title="KomarUniAI", page_icon="🎓", layout="centered")

# 2. دیزاینی CSS بۆ شاردنەوەی شتە زیادەکان و ڕێکخستنی لۆگۆ
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
    .logo-container { display: flex; justify-content: center; margin-bottom: 20px; }
    </style>
    """, unsafe_allow_html=True)

# 3. پیشاندانی لۆگۆ (بە قەبارەیەکی ڕێک)
st.markdown('<div class="logo-container">', unsafe_allow_html=True)
try:
    st.image("logo.png", width=200) # لێرە قەبارەکەی چاک کراوە
except:
    st.markdown("<h1 style='text-align:center;'>🎓</h1>", unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

st.markdown('<div class="main-title">KomarUniAI</div>', unsafe_allow_html=True)
st.markdown('<p style="text-align: center; color: #8e918f;">زیرەکی دەستکردی زانکۆی کۆمار</p>', unsafe_allow_html=True)

# 4. ڕێکخستنی API
if "GEMINI_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
else:
    st.error("تکایە کلیلەکە لە Secrets دابنێ")
    st.stop()

# هەوڵدان بۆ بەکارهێنانی مۆدێلە جیاوازەکان بۆ ڕێگری لە هەڵەی 404
@st.cache_resource
def load_model():
    models_to_try = ['gemini-1.5-flash', 'gemini-1.5-flash-latest', 'gemini-pro']
    for m in models_to_try:
        try:
            model = genai.GenerativeModel(m)
            # تاقیکردنەوەیەکی بچووک بۆ دڵنیایی لە کارکردن
            model.generate_content("test")
            return model
        except:
            continue
    return None

model = load_model()

if model is None:
    st.error("هەڵەی 404: هیچ مۆدێلێک بۆ ئەم کلیلە (API Key) کار ناکات. تکایە کلیلێکی نوێ دروست بکە.")
    st.stop()

# 5. سیستەمی چات
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("چی لێکۆڵینەوەیەک بکەم بۆت؟"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            response = model.generate_content(prompt)
            st.markdown(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})
        except Exception as e:
            st.error(f"کێشەیەک ڕوویدا: {e}")
