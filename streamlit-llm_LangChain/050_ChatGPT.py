from dotenv import load_dotenv, find_dotenv
_ = load_dotenv(find_dotenv()) # read local .env file
#------------------------------------------------------------

import streamlit as st
from streamlit_chat import message
from langchain import OpenAI
from langchain.chains import ConversationChain
from langchain.chains.conversation.memory import (ConversationBufferMemory, 
                                                  ConversationSummaryMemory, 
                                                  ConversationBufferWindowMemory                 )

if 'conversation' not in st.session_state:
    st.session_state['conversation'] = None
if 'messages' not in st.session_state:
    st.session_state['messages'] = []
    
# Setting page title and header
st.set_page_config(page_title="나만의 ChatGPT", page_icon=":robot_face:")
st.markdown("<h1 style='text-align: center;'>우리 영어로 즐겁게 대화해요</h1>", unsafe_allow_html=True)

st.sidebar.title("😎")
summaries_button = st.sidebar.button("대화 내용 요약")
if summaries_button:
    st.sidebar.write(st.session_state['conversation'].memory.buffer)
    
refresh_button = st.sidebar.button("대화 내용 초기화")
if refresh_button:
    st.session_state['conversation'] = None
    st.session_state['messages'] = []
    
# ChatGPT와의 API 연결
def getresponse(userInput):
    llm = OpenAI(
        temperature=0,
        model_name='text-davinci-003'  #we can also use 'gpt-3.5-turbo'
    )
    # session state에 conversation chain을 초기화하여 저장
    if st.session_state['conversation'] is None:
        st.session_state['conversation'] = ConversationChain(
            llm=llm,
            verbose=True,
            memory=ConversationSummaryMemory(llm=llm)
        )
    response = st.session_state['conversation'].predict(input=userInput)
    #print(st.session_state['conversation'].memory.buffer)
    
    return response

# LLM의 응답 표시를 위한 container
response_container = st.container()
# 사용자 input text box를 위한 container
container = st.container()

with container:  #어떤 container에 대해 form을 사용하고 싶은지 명시
    with st.form(key='my_form', clear_on_submit=True):
        user_input = st.text_area("질문을 영어로 입력하세요:", key='input', height=100)
        submit_button = st.form_submit_button(label='Send')
        if submit_button:
            response = getresponse(user_input)
            with response_container:
                st.write(response)
            st.session_state['messages'].append(user_input)  
            st.session_state['messages'].append(response) 
            #st.write(st.session_state['messages'])
            with response_container:
                for i in range(len(st.session_state['messages'])):
                    if (i % 2) == 0:
                        message(st.session_state['messages'][i], is_user=True, key=str(i) + '_user')    
                    else:
                        message(st.session_state['messages'][i], key=str(i) + '_AI')
            