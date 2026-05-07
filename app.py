import streamlit as st
import google.generativeai as genai

# 1. ڕێکخستنی لاپەڕە بە ستایلی مۆدێرن
st.set_page_config(page_title="KomarUniAI", page_icon="🎓", layout="centered")

# 2. ستایلی CSS بۆ جوانکردنی وێبسایتەکە
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
        margin-bottom: 5px;
    }
    .logo-container { display: flex; justify-content: center; margin-bottom: 20px; }
    /* باشترکردنی وێنای نامەکان */
    .stChatMessage { border-radius: 15px; margin-bottom: 10px; }
    </style>
    """, unsafe_allow_html=True)

# 3. نیشاندانی لۆگۆی زانکۆ (logo.png)
st.markdown('<div class="logo-container">', unsafe_allow_html=True)
try:
    # لێرەدا وێنەکە بە قەبارەیەکی ڕێک دەردەکەوێت
    st.image("logo.png", width=220) 
except:
    st.markdown("<h1 style='text-align:center;'>🎓</h1>", unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

st.markdown('<div class="main-title">KomarUniAI</div>', unsafe_allow_html=True)
st.markdown('<p style="text-align: center; color: #8e918f;">زیرەکی دەستکردی زانکۆی کۆمار بۆ زانست و تەکنەلۆژیا</p>', unsafe_allow_html=True)

# 4. ڕێکخستنی API و باشترکردنی زمانی کوردی
if "GEMINI_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
    
    # فەرمانکردن بە AI بۆ بەکارهێنانی کوردییەکی پاراو
    instruction = (
        "تۆ وەک لێکۆڵەرێکی ژیر لە زانکۆی کۆمار (KUST) وەڵام دەدەیتەوە. "
        "زمانی سەرەکیت کوردییە (سۆرانی). وەڵامەکانت دەبێت زۆر ڕەوان و سادە و دۆستانە بن. "
        "هەرگیز وەک وەرگێڕی Google قسە مەکە. ئەگەر وشەی زانستیت بەکارهێنا، ئینگلیزییەکەی لەناو کەوانە بنووسە."
    )
    
    model = genai.GenerativeModel(
        model_name='gemini-1.5-flash',
        system_instruction=instruction
    )
else:
    st.error("تکایە API Key لە Secrets دابنێ")
    st.stop()

# 5. سیستەمی مێژووی چات
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 6. وەرگرتنی پرسیار و وەڵامدانەوە
if prompt := st.chat_input("لێرە پرسیارەکەت بنووسە..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            # وەڵامدانەوەی ڕاستەوخۆ بە زمانی کوردی چاککراو
            response = model.generate_content(prompt)
            st.markdown(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})
        except Exception as e:
            # چارەسەری هەڵەی 404 ئەگەر ڕوویدا بە گۆڕینی مۆدێل
            st.error(f"ببورە، کێشەیەک ڕوویدا. دڵنیابە مۆدێلی 1.5 Flash لە ئەکاونتەکەت چالاکە.")
