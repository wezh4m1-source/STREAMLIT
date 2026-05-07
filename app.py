import streamlit as st
import google.generativeai as genai

# خوێندنەوەی کلیلەکە لە Secrets (دڵنیابە لە ستریمڵێت سەیڤت کردووە)
if "GEMINI_API_KEY" in st.secrets:
    API_KEY = st.secrets["GEMINI_API_KEY"]
    genai.configure(api_key=API_KEY)
else:
    st.error("تکایە API Key لە Secrets دابنێ")
    st.stop()

# لێرەدا ناوی مۆدێلەکە بەبێ وشەی models/ بنووسە
# ئەگەر 1.5-flash کاری نەکرد، gemini-1.0-pro تاقی بکەرەوە
try:
    model = genai.GenerativeModel('gemini-1.5-flash')
except Exception:
    model = genai.GenerativeModel('gemini-pro')

st.title("🎓 KomarUniAI")

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
            # بەکارهێنانی generate_content بە سادەیی
            response = model.generate_content(prompt)
            if response.text:
                st.markdown(response.text)
                st.session_state.messages.append({"role": "assistant", "content": response.text})
            else:
                st.warning("وەڵامەکە بەتاڵ بوو، لەوانەیە کێشەی Safety Filter هەبێت.")
        except Exception as e:
            st.error(f"هەڵەیەک ڕوویدا: {e}")
