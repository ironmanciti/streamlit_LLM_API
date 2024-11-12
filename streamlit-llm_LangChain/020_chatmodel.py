import os
import openai
import sys
sys.path.append('./')

from dotenv import load_dotenv, find_dotenv
_ = load_dotenv(find_dotenv()) # read local .env file

openai.api_key  = os.environ['OPENAI_API_KEY']

#------ Streamlit 의 sessionMessage를 이용한 Chatbot 작성 ---------------

import streamlit as st

from langchain_openai import ChatOpenAI
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage

llm = ChatOpenAI(model="gpt-4o-mini")

# streamlit UI 시작
st.set_page_config(page_title="LangChain Demo")
st.header("저는 당신의 챗봇입니다.")

# "sessionMessages" 키가 st.session_state에 없으면 초기화합니다.
# 이때 시스템 메시지를 포함한 기본 메시지 리스트를 생성합니다.
if "sessionMessages" not in st.session_state:
    st.session_state.sessionMessages = [
        SystemMessage(content="당신은 유용한 도우미입니다.") 
    ]

# 사용자가 입력한 질문을 기반으로 답변을 생성하는 함수
def load_answer(question):
    # 사용자가 입력한 질문을 HumanMessage 형태로 세션 메시지 리스트에 추가
    st.session_state.sessionMessages.append(HumanMessage(content=question))
    
    # 세션 메시지 리스트를 기반으로 챗봇 모델에서 답변을 생성
    assistant_answer = llm(st.session_state.sessionMessages)
    
    # 생성된 AI의 응답을 AIMessage 형태로 세션 메시지 리스트에 추가
    st.session_state.sessionMessages.append(AIMessage(content=assistant_answer.content))
    
    # 챗봇 모델이 생성한 답변 반환
    return assistant_answer.content

def get_text():
    input_text = st.text_input(label="You: ", key="입력하세요")
    return input_text

user_input = get_text()
submit = st.button('Generate')

if submit:
    response = load_answer(user_input)
    st.subheader("Answer:")
    st.write(response)  

