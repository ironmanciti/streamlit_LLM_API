import streamlit as st
import os
from openai import OpenAI
import sys
sys.path.append('./')
from PIL import Image
import base64

from dotenv import load_dotenv, find_dotenv
_ = load_dotenv(find_dotenv()) #  로컬 .env 파일 읽기

client = OpenAI()

Model = "gpt-4o-mini"

def generate_blog(topic, additional_text):
    pass

# 이미지 생성을 위한 함수
def generate_image(prompt):
    pass

# 이미지를 Base64로 인코딩하는 함수
def encode_image(image_path):
  with open(image_path, "rb") as image_file:
    return base64.b64encode(image_file.read()).decode('utf-8')

def image_vision(base64_image):
    pass
    
# 페이지 구성을 와이드 모드로 설정

# 애플리케이션의 제목 설정

# 사이드바에 네비게이션 추가

# Blog 생성기 선택 시
if ai_app == "Blog 생성":
    pass
        
# # Image 생성기 선택 시
elif ai_app == "Image 생성":
    pass
        
# # Image 설명 선택 시
elif ai_app == "Image 설명":
    pass
        
else:
    print("Invalid selection")
 