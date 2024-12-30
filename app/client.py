import streamlit as st
from PIL import Image
from models.text import load_multi_modal_model, generate_image_caption

st.set_page_config(
       page_title="Image Caption Generator",
       page_icon="📷",
       layout="centered",  # You can also choose "wide"
       initial_sidebar_state="auto",  # Or "expanded", "collapsed"
   )

st.title("Image Caption Generator")


# Caching the model loading
@st.cache_resource
def get_model():
    with st.spinner("Loading model..."):
        processor, model = load_multi_modal_model()
        return processor, model


processor, model = get_model()

# Configurable API URL
# api_url = st.secrets.get("API_URL", "http://localhost:8000/generate/caption")

uploaded_file = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    try:
        image = Image.open(uploaded_file)
        st.image(image, use_container_width=True)
    except Exception:
        st.error("Invalid image file. Please upload a valid image.")
    else:
        if st.button("Generate Image Caption"):
            with st.spinner("Generating caption..."):
                try:
                    caption = generate_image_caption(processor, model, image)
                    st.success(f"Generated Caption: '{caption}'")
                except Exception as e:
                    st.error(f"Failed to generate caption: {e}")
        # if st.button("Generate Image Caption"):
        #     with st.spinner("Generating caption..."):
        #         files = {"image": uploaded_file.getvalue()}  # Send image data
        #         try:
        #             response = requests.post(api_url, files=files)
        #             response.raise_for_status()
        #         except requests.exceptions.RequestException as e:
        #             st.error(f"Failed to generate caption: {e}")
        #         else:
        #             result = response.json()
        #             caption = result.get("caption", "No caption received")
        #             st.success(f"Generated Caption: '{caption}'")
