import streamlit as st
import google.generativeai as genai

# 1. ڕێکخستنی لاپەڕە و دیزاین
st.set_page_config(page_title="KomarUniAI", page_icon="🎓", layout="centered")

st.markdown("""
    <style>
    .stApp { background-color: #131314; color: white; direction: rtl; }
    .main-title { text-align: center; font-size: 40px; font-weight: bold; color: #8ab4f8; }
    header, footer {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)

st.markdown('<div class="main-title">KomarUniAI 🎓</div>', unsafe_allow_html=True)

# 2. پەیوەندی سکیور بە API
if "GEMINI_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
else:
    st.error("تکایە API Key لە بەشی Secrets دابنێ!")
    st.stop()

# 3. فەنکشنی زیرەک بۆ دۆزینەوەی مۆدێلی بەردەست
@st.cache_resource
def load_model():
    # وەرگرتنی لیستی ئەو مۆدێلانەی بۆ کلیلی تۆ ڕێپێدراون
    available_models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
    
    # لیستی مۆدێلەکان بەپێی باشترین (Priority)
    priorities = ['models/gemini-1.5-flash', 'models/gemini-1.5-pro', 'models/gemini-pro']
    
    for model_name in priorities:
        if model_name in available_models:
            return genai.GenerativeModel(model_name)
    
    # ئەگەر هیچ کام لەوانەی سەرەوە نەبوو، یەکەم مۆدێلی بەردەست بەکاربهێنە
    return genai.GenerativeModel(available_models[0])

try:
    model = load_model()
except Exception as e:
    st.error(f"نەتوانرا پەیوەندی بە سێرڤەرەوە بکرێت: {e}")
    st.stop()

# 4. لۆژیکی چات
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
            # بەبێ stream بۆ ئەوەی کەمترین ئەگەری هەڵەی هەبێت
            response = model.generate_content(prompt)
            st.markdown(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})
        except Exception as e:
            st.error(f"هەڵەیەک لە وەڵامدانەوەدا هەیە: {e}")
