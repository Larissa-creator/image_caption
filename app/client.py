import streamlit as st
from PIL import Image
import requests

st.title("Image Caption Generator")

uploaded_file = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, use_container_width=True)

    if st.button("Generate Image Caption"):
        # api_url = "http://localhost:8000/generate/caption"
        api_url = "https://larissa-creator-image-caption-appclient-fnym1e.streamlit.app/generate/caption"
        files = {"image": uploaded_file.getvalue()}  # Send image data
        response = requests.post(api_url, files=files)

        if response.status_code == 200:
            caption = response.json().get("caption", "No caption received")
            st.success(f"Generated Caption: '{caption}'")
        else:
            # Handle API errors
            st.error("Failed to generate caption. Please try again.")
