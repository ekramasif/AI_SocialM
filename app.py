### Health Management APP
from dotenv import load_dotenv

load_dotenv() ## load all the environment variables

import streamlit as st
import os
import google.generativeai as genai
from PIL import Image

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

## Function to load Google Gemini Pro Vision API And get response

def get_gemini_repsonse(input,image,prompt):
    model=genai.GenerativeModel('gemini-pro-vision')
    response=model.generate_content([input,image[0],prompt])
    return response.text

def input_image_setup(uploaded_file):
    # Check if a file has been uploaded
    if uploaded_file is not None:
        # Read the file into bytes
        bytes_data = uploaded_file.getvalue()

        image_parts = [
            {
                "mime_type": uploaded_file.type,  # Get the mime type of the uploaded file
                "data": bytes_data
            }
        ]
        return image_parts
    else:
        raise FileNotFoundError("No file uploaded")
    
##initialize our streamlit app

st.set_page_config(page_title="Gemini Social Media post description App")

st.header("Gemini Social Media post description App")
input=st.text_input("Input Prompt: ",key="input")
uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])
image=""   
if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image.", use_column_width=True)


submit=st.button("Write the Description")

# input_prompt="""Imagine you're a skilled content writer crafting enticing product descriptions for 
#                 an e-commerce platform. Your task is to create a captivating product description for 
#                 products. Dive into the image, draw inspiration from the product's features, and employ 
#                 persuasive language to highlight the benefits of these sustainable shoes. 
#                 Incorporate essential details like materials, style, and sizing information to engage 
#                 potential customers effectively.
#                 """

input_prompt="""Imagine you're a social media content writer for an e-commerce store specializing in any Product Category.                Inspect the product image provided. Identify key features and benefits.
                Craft a captivating one-sentence caption highlighting the product's value proposition.
                Include relevant details like:
                Material (if applicable)
                Functionality/Use case
                Color(s)
                Size options (if applicable)
                Special features (unique selling points)
                Use persuasive language to entice viewers and encourage them to:
                Learn more about the product (link in bio?)
                Visit the website for purchase
                Engage with the post (likes, comments)
                Maintain the brand's voice and tone (informative, playful, luxurious, etc.)
                Include relevant hashtags to increase discoverability."""

## If submit button is clicked

if submit:
    image_data=input_image_setup(uploaded_file)
    response=get_gemini_repsonse(input_prompt,image_data,input)
    st.subheader("The Response is")
    st.write(response)


