import os

import streamlit as st
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
MODEL = os.getenv("OPENAI_MODEL", "gpt-4o-mini")

LANGUAGES = {
    "영어": "English",
    "일본어": "Japanese",
    "중국어": "Simplified Chinese",
}


def translate(text: str, language: str) -> str:
    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {
                "role": "system",
                "content": (
                    f"You are a professional translator. Translate the user's text into {language}. "
                    "Output only the translation, without explanations."
                ),
            },
            {"role": "user", "content": text},
        ],
    )
    return response.choices[0].message.content.strip()


st.set_page_config(page_title="번역기", page_icon="🌐")
st.title("🌐 번역기")

text = st.text_area("번역할 글을 입력하세요", height=200)
language = st.radio("번역할 언어", list(LANGUAGES.keys()), horizontal=True)

if st.button("번역하기", type="primary"):
    if not text.strip():
        st.warning("번역할 글을 입력해주세요.")
    else:
        with st.spinner("번역 중..."):
            try:
                result = translate(text, LANGUAGES[language])
                st.subheader(f"{language} 번역 결과")
                st.text_area("결과", result, height=200, label_visibility="collapsed")
            except Exception as e:
                st.error(f"번역 중 오류가 발생했습니다: {e}")
