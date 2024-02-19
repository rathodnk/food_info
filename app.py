import streamlit as st
import google.generativeai as genai
import os
from dotenv import load_dotenv
from PIL import Image

load_dotenv()

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def get_gemini_resp(inpt_prompt,img):
    model = genai.GenerativeModel('gemini-pro-vision')
    resp = model.generate_content([inpt_prompt,img])
    return resp.text

def inpt_img(uploaded_image):
    if uploaded_image is not None:
        image_parts = [
            {
                "mime_type": uploaded_image.type,
                "data": uploaded_image.getvalue() 
            }
        ]
        return image_parts
    else:
        raise FileNotFoundError("No Image Uploaded.")

def main():
    # Title
    st.title('Image Viewer')

    #Upload an image
    uploaded_image = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png", "webp"])

    # Check the type of the uploaded image
    if uploaded_image is not None:
        # Open the image using PIL
        image = Image.open(uploaded_image)
        # Display the image
        st.image(image, use_column_width=True)
        submit = st.button("Food Info")
        inpt_prompt = """
            You are an expert in nutritionist where you need to see the food items from the image and calculate the total calories, protein, vitamins & minerals and some other important Nutrients available in the food 
            
            start with Title (i.e. Name of the food) or suggest name by looking items (if the proper name is not identify) in bold

            then food item individually also provide the details of every food items with calories, protein and also weight of that serving if possible in grams(even if this is an estimation) compulsory in below tabular format 

            1. Item 1 |  no of calories | protein | Nutrients
            2. Item 2 |  no of calories | protein | Nutrients
            ----
            ----

            Finally you  can also mention whether the food is "healthy or not" along with Digestion of the food if possible mention some workout to burn the calories and some minor explanation. 
        """
        if submit:
            img = inpt_img(uploaded_image)
            response = get_gemini_resp(inpt_prompt,img)
            st.write(response)

if __name__ == "__main__":
    main()