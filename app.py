import streamlit as st
import google.generativeai as genai

# 1. ڕێکخستنی لاپەڕە
st.set_page_config(page_title="KomarUniAI", page_icon="🎓", layout="centered")

# 2. ستایلی دیزاین (CSS)
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
    }
    </style>
    """, unsafe_allow_html=True)

st.markdown('<div class="main-title">KomarUniAI 🎓</div>', unsafe_allow_html=True)

# 3. ڕێکخستنی API و باشترکردنی زمان (System Instruction)
if "GEMINI_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
    
    # لێرەدا فەرمان بە AI یەکە دەدەین چۆن ڕەفتار بکات
    instruction = """
    تۆ ناوت KomarUniAI یە، زیرەکی دەستکردی تایبەت بە زانکۆی کۆماریت (KUST). 
    دەبێت تەنها بە زمانی کوردی (سۆرانی) وەڵام بدەیتەوە. 
    هەوڵ بدە زمانی کوردییەکت زۆر پاراو و ڕەوان بێت و وەک وەرگێڕانی ئامێری دەرنەکەوێت. 
    ئەگەر بابەتەکە زانستی بوو، زاراوە ئینگلیزییەکان لەناو کەوانە دابنێ.
    وەک هاوڕێیەکی ژیر و یارمەتیدەر بۆ خوێندکارانی زانکۆی کۆمار قسە بکە.
    """
    
    model = genai.GenerativeModel(
        model_name='gemini-1.5-flash',
        system_instruction=instruction
    )
else:
    st.error("تکایە API Key لە Secrets دابنێ.")
    st.stop()

# 4. سیستەمی چات
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
            # ناردنی پرسیارەکە بۆ مۆدێلەکە
            response = model.generate_content(prompt)
            st.markdown(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})
        except Exception as e:
            st.error(f"Error: {e}")
