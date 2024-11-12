from dotenv import load_dotenv, find_dotenv
_ = load_dotenv(find_dotenv()) # read local .env file
#------------------------------------------------------------

import streamlit as st
import pandas as pd
from langchain.agents import create_pandas_dataframe_agent
from langchain.llms import OpenAI

st.title("CSV 파일 분석")
st.header("여기에 CSV 파일을 업로드하세요:")

# Capture the CSV file
data = st.file_uploader("CSV 파일 업로드", type="csv")
df = pd.read_csv(data)
print(len(df))

llm = OpenAI()

# Create a Pandas DataFrame agent.
agent = create_pandas_dataframe_agent(llm, df, verbose=True)

query = st.text_area("쿼리를 입력하세요")
button = st.button("응답 생성")

if button:
    # Get Response
    answer = agent.run(query)
    st.write(answer)