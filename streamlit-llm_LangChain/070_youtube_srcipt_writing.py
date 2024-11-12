from dotenv import load_dotenv, find_dotenv
_ = load_dotenv(find_dotenv()) # read local .env file
#------------------------------------------------------------

import streamlit as st 
from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain.tools import DuckDuckGoSearchRun

# Button Style 지정
st.markdown("""
<style>
div.stButton > button:first-child {
    background-color: #0099ff;
    color:#ffffff;
}
div.stButton > button:hover {
    background-color: #00ff00;
    color:#FFFFFF;
    }
</style>""", unsafe_allow_html=True)

# 두 개의 열을 생성
col1, col2 = st.columns([1, 4])  # 이 배열은 각 열의 너비 비율을 나타냅니다.
# 첫 번째 열에 YouTube 이미지를 추가
col1.image('./Youtube.jpg', width=150)  # width 값을 조정하여 이미지 크기를 변경할 수 있습니다.
# 두 번째 열에 "Script Writing Tool" 텍스트를 추가
col2.write("# 동영상 대본 생성기")

# Function to generate video script
def generate_script(prompt, video_length, creativity):
    # OpenAI LLM
    llm = OpenAI(temperature=creativity, model_name='gpt-3.5-turbo') 
    
    # 'Title' 생성 template
    title_template = PromptTemplate(
        input_variables = ['subject'], 
        template='YouTube 동영상의 제목을 정해주세요. {subject}.'
        )

    # 검색 엔진을 사용하여 'video script'를 생성하기 위한 템플릿
    script_template = PromptTemplate(
        input_variables = ['title', 'DuckDuckGo_Search','duration'], 
        template='이 제목을 바탕으로 YouTube 동영상용 대본을 만들어 보세요. {DuckDuckGo_Search} 검색 데이터를 이용하여 제목: {title}인 {duration}분 분량의 동영상 대본을 한글로 작성해 주세요.'
    )
    
    #'Title' & 'Video Script' 생성을 위한 체인 
    title_chain = LLMChain(llm=llm, prompt=title_template, verbose=True)
    script_chain = LLMChain(llm=llm, prompt=script_template, verbose=True)

    # https://python.langchain.com/docs/modules/agents/tools/integrations/ddg
    search = DuckDuckGoSearchRun()

    # 'Title' 생성을 위한 체인 실행
    title = title_chain.run(prompt)

    # 검색 엔진 'DuckDuckGo'의 도움을 받아 'Video Script'를 위해 생성한 체인을 실행
    search_result = search.run(prompt) 
    script = script_chain.run(title=title, DuckDuckGo_Search=search_result, duration=video_length)

    return search_result, title, script

# Captures User Inputs
prompt = st.text_input('동영상의 주제를 입력하세요.',key="prompt")  # The box for the text prompt
video_length = st.text_input('예상 시간 🕒 (분)',key="video_length")  # The box for the text prompt
creativity = st.slider('Temperature ✨ - (0 LOW || 1 HIGH)', 0.0, 1.0, 0.2,step=0.1)

submit = st.button("대본을 생성합니다.")

if submit:  # submit 버튼을 누르면
    search_result, title, script = generate_script(prompt, video_length, creativity)
    # success message
    st.success('결과에 만족하시기 바랍니다. ❤️')

    #Display Title
    st.subheader("제목:🔥")
    st.write(title)

    #Display Video Script
    st.subheader("동영상 대본:📝")
    st.write(script)

    # 검색 엔진 결과 표시
    st.subheader("검토 - DuckDuckGo Search:🔍")
    with st.expander('Show me 👀'): 
        st.info(search_result)
