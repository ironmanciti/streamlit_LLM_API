import os
import openai
import sys
sys.path.append('./')

from dotenv import load_dotenv, find_dotenv
_ = load_dotenv(find_dotenv()) # read local .env file

openai.api_key  = os.environ['OPENAI_API_KEY']

#------------------------------------------------------------

import streamlit as st

from langchain_openai import ChatOpenAI

# LangChain 라이브러리를 사용하여 자연어 처리를 수행하는 간단한 웹 애플리케이션을 만드는 Python 스크립트입니다.

# 사용자 입력에 대한 응답을 반환하는 함수입니다.
def load_answer(question):
    llm = ChatOpenAI(model="gpt-4o-mini")
    answer = llm.invoke(question)
    return answer


# 앱 UI가 시작되는 부분입니다.
st.set_page_config(page_title="LangChain Demo")
st.header("LangChain Demo")

# 사용자 입력을 받는 함수입니다.
def get_text():
    input_text = st.text_input("You: ", key="input")
    return input_text

user_input = get_text()
response = load_answer(user_input)

submit = st.button('Generate')  

# Generate 버튼이 클릭되면
if submit:
    st.subheader("Answer:")
    st.write(response.content)
