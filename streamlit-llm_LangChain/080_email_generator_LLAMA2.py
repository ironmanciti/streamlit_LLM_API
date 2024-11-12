from dotenv import load_dotenv, find_dotenv
_ = load_dotenv(find_dotenv()) # read local .env file
#------------------------------------------------------------

import streamlit as st
from langchain.prompts import PromptTemplate
from langchain.llms import CTransformers
from langchain.llms import OpenAI

#Function to get the response back
def getLLMResponse(form_input, email_sender, email_recipient, email_style):
    #llm = OpenAI(temperature=.9, model="text-davinci-003")

    # Wrapper for Llama-2-7B-Chat, Running Llama 2 on CPU

    #양자화는 weight를 16비트 부동 소수점에서 8비트 정수로 변환하여 모델 크기를 줄여서, 
    #리소스가 제한된 장치에 효율적으로 배포하고 성능을 유지합니다.

    #C Transformers는 Llama, GPT4All-J, MPT 및 Falcon과 같은 인기 모델 중 다양한 오픈 소스 모델을 지원합니다.

    #C Transformers는 GGML 라이브러리를 사용하여 C/C++로 구현된 변환기 모델에 대한 바인딩을 제공하는 Python 라이브러리입니다.
    llm = CTransformers(model='models/llama-2-7b-chat.ggmlv3.q8_0.bin',  #https://huggingface.co/TheBloke/Llama-2-7B-Chat-GGML/tree/main
                    model_type='llama',
                    config={'max_new_tokens': 256,
                            'temperature': 0.01})
    
    #PROMPT 구축을 위한 템플릿
    template = """
    Write a email with {style} style and includes topic :{email_topic}.\n\nSender: {sender}\nRecipient: {recipient}
    \n\nEmail Text:
    
    """

    #final PROMPT 생성
    prompt = PromptTemplate(
    input_variables=["style","email_topic","sender","recipient"],
    template=template,)

  
    #LLM을 이용한 response 생성
    response=llm(prompt.format(email_topic=form_input, sender=email_sender, recipient=email_recipient, style=email_style))
    print(response)

    return response


st.set_page_config(page_title="Generate Emails",
                    page_icon='📧',
                    layout='centered',
                    initial_sidebar_state='collapsed')
st.header("Generate Emails 📧")

form_input = st.text_area('Enter the email topic', height=275)

#Creating columns for the UI - To receive inputs from user
col1, col2, col3 = st.columns([10, 10, 5])
with col1:
    email_sender = st.text_input('Sender Name')
with col2:
    email_recipient = st.text_input('Recipient Name')
with col3:
    email_style = st.selectbox('Writing Style',
            ('Formal', 'Appreciating', 'Not Satisfied', 'Neutral'),
            index=0)

submit = st.button("Generate")

if submit:
    st.write(getLLMResponse(form_input, email_sender, email_recipient, email_style))
