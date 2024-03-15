from dotenv import load_dotenv
load_dotenv()
import streamlit as st
import os
import base64
import io
from PIL import Image 
import pdf2image
import google.generativeai as genai

genai.configure(api_key = os.getenv("GOOGLE_API_KEY"))

def get_gemini_response(input, pdf_content):
    model=genai.GenerativeModel('gemini-pro-vision')
    response = model.generate_content(input, pdf_content)
    return response.text

def input_pdf_setup(uploaded_file):
    if uploaded_file is not None:
        # convert the pdf to image
        images = pdf2image.convert_from_bytes(uploaded_file.read())
        first_page = images[0]

        # Convert into bytes
        img_byte_arr = io.BytesIO()
        first_page.save(img_byte_arr, format = 'JPEG')
        img_byte_arr = img_byte_arr.getvalue()

        pdf_parts = [
            {
                "mime_type" : "image/jpeg",
                "data" : base64.b64encode(img_byte_arr).decode()
            }
        ]
        return pdf_parts
    else:
        raise FileNotFoundError("No File Uploaded")


# Streamlit App

st.set_page_config(page_title = "ATS Resume Expert")
st.header("ATS Tracking System")
input_text = st.text_area("Job Description :", key = "input")
uploaded_file = st.file_uploader("Upload your resume(PDF)...", type = ["pdf"])

if uploaded_file is not None :
    st.write("PDF Uploaded Successfully")

submit1 = st.button("Tell Me about the resume")
submit2 = st.button("How can I improve my skills")
submit3 = st.button("Percentage match")

input_prompt1 = """
You are an experienced HR with Tech Experiencein the field of data acience, Full stack webdevelopment, Big Data Engineer, Data Analyst, your task is to review 
the provided resume against the job description for these profile. 
Please share your professional evaluation on whether the candidate's profile aligns with the role
and Highlight the strength and weakness of the applicant in relation to the specific job role 
"""

input_prompt3 ="""
You are an skilled ATS scanner with a deep understanding of data acience, Full stack webdevelopment, Big Data Engineer, Data Analyst, and deep ATS functionality,
your task is to evaluste the resume against the provided job description
"""

if submit1: 
    if uploaded_file is not None:
        pdf_content = input_pdf_setup(uploaded_file)
        response = get_gemini_response(input_prompt1, pdf_content)
        st.subheader("The Response is")
        st.write(response)
    else:
        st.write("Please upload the resume")
elif submit2:
    if uploaded_file is not None:
        pdf_content = input_pdf_setup(uploaded_file)
        response = get_gemini_response(input_prompt3, pdf_content)
        st.subheader("The Response is")
        st.write(response)
    else:
        st.write("Please upload the resume")