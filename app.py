import streamlit as st
import requests
import base64
from PIL import Image
import io

# Page Config
st.set_page_config(page_title="LongCat Image Analyzer", layout="centered")

st.title("🐱 LongCat-Flash-Omni-2603 Analyzer")
st.info("Pehle apni API Key enter karein, uske baad image upload ka option milega.")

# 1. API Key Input
api_key = st.text_input("Enter your LongCat API Key:", type="password")

if api_key:
    st.success("API Key detected! Ab aap image analyze kar sakte hain.")
    
    # 2. Image Upload Option (Sirf API key ke baad dikhega)
    uploaded_file = st.file_uploader("Upload an image (PNG, JPG, JPEG)", type=["png", "jpg", "jpeg"])
    user_prompt = st.text_area("Analysis Prompt:", value="Describe this image in detail.")

    if uploaded_file is not None:
        # Display Image
        image = Image.open(uploaded_file)
        st.image(image, caption='Uploaded Image', use_column_width=True)

        if st.button("Analyze Image"):
            with st.spinner("Analyzing with LongCat-Flash-Omni-2603..."):
                try:
                    # Convert image to Base64
                    buffered = io.BytesIO()
                    image.save(buffered, format="PNG")
                    img_str = base64.b64encode(buffered.getvalue()).decode()

                    # API Request
                    url = "https://api.longcat.chat" # Confirm base URL from docs
                    headers = {
                        "Authorization": f"Bearer {api_key}",
                        "Content-Type": "application/json"
                    }
                    
                    payload = {
                        "model": "LongCat-Flash-Omni-2603",
                        "messages": [
                            {
                                "role": "user",
                                "content": [
                                    {
                                        "type": "input_image",
                                        "input_image": {
                                            "type": "base64",
                                            "data": [img_str]
                                        }
                                    },
                                    {
                                        "type": "text",
                                        "text": user_prompt
                                    }
                                ]
                            }
                        ],
                        "stream": False
                    }

                    response = requests.post(url, headers=headers, json=payload)
                    
                    if response.status_code == 200:
                        result = response.json()
                        st.subheader("Analysis Result:")
                        st.write(result['choices'][0]['message']['content'])
                    else:
                        st.error(f"Error: {response.status_code} - {response.text}")

                except Exception as e:
                    st.error(f"An unexpected error occurred: {e}")
else:
    st.warning("Please provide a valid API key to proceed.")
