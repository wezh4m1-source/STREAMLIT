import streamlit as st
import google.generativeai as genai

# 1. ڕێکخستنی لاپەڕە
st.set_page_config(page_title="KomarUniAI", page_icon="🎓", layout="centered")

# 2. CSS بۆ دیزاین و ڕاست-بۆ-چەپ
st.markdown("""
    <style>
    .stApp { background-color: #131314; color: white; direction: rtl; }
    header, footer {visibility: hidden;}
    .main-title {
        text-align: center; font-size: 45px; font-weight: bold;
        background: linear-gradient(to right, #4285f4, #9b72cb, #d96570);
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;
    }
    .logo-container { display: flex; justify-content: center; margin-bottom: 20px; }
    </style>
    """, unsafe_allow_html=True)

# 3. لۆگۆ (قەبارەی گونجاو)
st.markdown('<div class="logo-container">', unsafe_allow_html=True)
try:
    st.image("logo.png", width=200)
except:
    st.write("🎓")
st.markdown('</div>', unsafe_allow_html=True)

st.markdown('<div class="main-title">KomarUniAI</div>', unsafe_allow_html=True)

# 4. لۆژیکی دۆزینەوەی مۆدێلی گونجاو (بۆ ڕێگری لە 404)
if "GEMINI_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
    
    # فەنکشن بۆ دۆزینەوەی مۆدێلی کارا
    @st.cache_resource
    def load_best_model():
        # لیستێک لەو مۆدێلانەی ئەگەری کارکردنیان زۆرە
        test_models = ['gemini-1.5-flash', 'gemini-pro', 'gemini-1.0-pro']
        instruction = "تۆ ناوت KomarUniAI یە. بە زمانی کوردییەکی زۆر پاراو و شیرین وەڵام بدەرەوە."
        
        for m_name in test_models:
            try:
                m = genai.GenerativeModel(model_name=m_name, system_instruction=instruction)
                # تاقیکردنەوەیەکی خێرا بۆ زانینی ئیشکردن
                m.generate_content("hi")
                return m
            except:
                continue
        return None

    model = load_best_model()
else:
    st.error("تکایە API Key لە Secrets دابنێ")
    st.stop()

if not model:
    st.error("هیچ مۆدێلێک وەڵام ناداتەوە. ئەگەری زۆرە کێشەکە لە Region یان Billing بێت لە Google Cloud.")
    st.stop()

# 5. مێژووی چات
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 6. وەرگرتنی پرسیار
if prompt := st.chat_input("چی لێکۆڵینەوەیەک بکەم؟"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            # ناردنی پرسیارەکە بە ڕێنمایی کوردی
            response = model.generate_content(prompt)
            st.markdown(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})
        except Exception as e:
            st.error(f"هەڵەیەک ڕوویدا: {e}")
