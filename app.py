import streamlit as st
import google.generativeai as genai

# 1. ڕێکخستنی لاپەڕە
st.set_page_config(page_title="KomarUniAI", page_icon="🎓", layout="centered")

# 2. ستایلی دیزاین
st.markdown("""
    <style>
    .stApp { background-color: #131314; color: white; direction: rtl; }
    header, footer {visibility: hidden;}
    .main-title {
        text-align: center;
        font-size: 45px;
        font-weight: bold;
        background: linear-gradient(to right, #4285f4, #9b72cb, #d96570);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 20px;
    }
    .logo-img { display: block; margin: 0 auto; width: 200px; border-radius: 15px; }
    </style>
    """, unsafe_allow_html=True)

# 3. نیشاندانی لۆگۆ و تایتڵ
try:
    st.image("logo.png", width=200)
except:
    st.markdown("<h1 style='text-align:center;'>🎓</h1>", unsafe_allow_html=True)

st.markdown('<div class="main-title">KomarUniAI</div>', unsafe_allow_html=True)

# 4. لۆژیکی سکیور بۆ دۆزینەوەی مۆدێلی کارا
if "GEMINI_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
    
    @st.cache_resource
    def get_best_model():
        # لیستکردنی هەموو ئەو مۆدێلانەی بۆ کلیلی تۆ ئیش دەکەن
        try:
            available_models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
            
            # تاقیکردنەوەی مۆدێلەکان بەپێی باشترین
            for model_id in ['models/gemini-1.5-flash', 'models/gemini-pro', 'models/gemini-1.0-pro']:
                if model_id in available_models:
                    return genai.GenerativeModel(model_id)
            
            # ئەگەر هیچیان نەبوو، یەکەم مۆدێلی بەردەست بەکاربهێنە
            return genai.GenerativeModel(available_models[0])
        except Exception as e:
            return None

    model = get_best_model()
else:
    st.error("تکایە API Key لە Secrets دابنێ.")
    st.stop()

if model is None:
    st.error("هەڵەی 404: هیچ مۆدێلێک بۆ ئەم کلیلە بەردەست نییە. تکایە کلیلێکی نوێ دروست بکە لە Google AI Studio.")
    st.stop()

# 5. چات
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
            # بەکارهێنانی مۆدێلە دۆزراوەکە
            response = model.generate_content(prompt)
            st.markdown(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})
        except Exception as e:
            st.error(f"کێشەیەک لە API هەیە: {e}")
