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
    role = f"당신은 브랜드를 통합하고 향상시키는 영향력 있는 블로그를 작성하는 수년간의 경험을 가진 카피라이터입니다. 당신의 임무는 당신에게 제공되는 주제에 대해 블로그를 작성하는 것입니다. SNS에 적합한 형식으로 작성하세요. 세 문장으로 이루어져야 합니다."
    
    response = client.chat.completions.create(
        model=Model,
        messages=[
            {"role": "system", "content": role},
            {"role": "user", "content": topic + additional_text}
        ],
        max_tokens=700,
        temperature=0.9
    )
    
    return response

# 이미지 생성을 위한 함수
def generate_image(prompt):
    
    response = client.images.generate(
        model="dall-e-3",
        prompt=prompt,
        size="1024x1024",
        n=1
    )
    return response

# 이미지를 Base64로 인코딩하는 함수
def encode_image(image_path):
  with open(image_path, "rb") as image_file:
    return base64.b64encode(image_file.read()).decode('utf-8')

# 이미지 설명을 생성하는 함수
def image_vision(base64_image):
    
    response = client.chat.completions.create(
        model= Model,
        messages=[
            {
            "role": "user",
            "content": [
                {"type": "text", "text": "이 이미지의 내용을 설명해줘. 한국어로 설명해줘."},
                {
                "type": "image_url",
                "image_url": {
                    "url": f"data:image/jpeg;base64,{base64_image}",
                },
                },
            ],
            }
        ],
        max_tokens=300,
        )
    return response
    
# 페이지 구성을 와이드 모드로 설정
st.set_page_config(layout="wide")

# 애플리케이션의 제목 설정
st.title('OpenAI API Applications')

# 사이드바에 네비게이션 추가
st.sidebar.title("Applications")
ai_app = st.sidebar.radio("AI app 선택", ("Blog 생성", "Image 생성", "Image 설명"))

# Blog 생성기 선택 시
if ai_app == "Blog 생성":
    st.header("Blog 생성기")
    st.write("Blog 생성을 위한 주제를 입력하세요.")
    
    topic = st.text_area("주제", height=30)
    additional_text = st.text_area("추가 설명", height=30)
    
    if st.button("Blog 생성"):
        st.write("Button Clicked")
        response = generate_blog(topic, additional_text)
        st.text_area("생성된 Blog", value=response.choices[0].message.content, height=700)
        
# Image 생성기 선택 시
elif ai_app == "Image 생성":
    st.header("Image 생성기")
    st.write("이미지 생성을 위한 prompt를 입력하세요.")
    
    prompt = st.text_area("Prompt", height=30)
    
    if st.button("Image 생성") and prompt != "":
        with st.spinner("생성중....."):
            response = generate_image(prompt)
            st.image(response.data[0].url)

# Image 설명 선택 시
elif ai_app == "Image 설명":
    st.header("Vision API")
    st.write("Image를 upload 하세요")
    
    image_file = st.file_uploader("Upload Images", type=["png","jpg","jpeg"])
    
    if image_file is not None:
        file_details = {"filename":image_file.name,
                        "filetype":image_file.type,
                        "filesize":image_file.size}
        st.write(file_details)

        img = Image.open(image_file)
        st.image(img, width=250)
        
        image_path = "data/" + image_file.name
        base64_image = encode_image(image_path)
        response = image_vision(base64_image)
        st.write(response.choices[0].message.content)
else:
    print("Invalid selection")
 