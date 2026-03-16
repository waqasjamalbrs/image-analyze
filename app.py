import streamlit as st
import requests
import base64
from PIL import Image
import io

st.set_page_config(page_title="LongCat Image Analyzer", layout="centered")

st.title("🐱 LongCat-Flash-Omni-2603")
st.markdown("---")

# 1. API Key Input (Sidebar for better UI)
api_key = st.sidebar.text_input("Enter LongCat API Key:", type="password")

if api_key:
    # 2. Image Upload (Only shows after API key)
    uploaded_file = st.file_uploader("Upload Image (Max 5MB recommended)", type=["png", "jpg", "jpeg"])
    user_prompt = st.text_area("What do you want to know about this image?", value="Describe this image in detail.")

    if uploaded_file:
        # Preview Image
        image = Image.open(uploaded_file)
        st.image(image, caption='Uploaded Preview', use_column_width=True)

        if st.button("Analyze Now"):
            with st.spinner("Talking to LongCat..."):
                try:
                    # Convert to Base64 (Standard PNG/JPG)
                    buffered = io.BytesIO()
                    # JPEG format use kar rahe hain taake size mazeed kam ho
                    image.save(buffered, format="JPEG", quality=90)
                    img_str = base64.b64encode(buffered.getvalue()).decode('utf-8')

                    # --- CORRECT API PAYLOAD STRUCTURE ---
                    url = "https://api.longcat.chat"
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
                                            "data": [img_str]  # Note: LongCat expects data as an ARRAY
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

                    response = requests.post(url, headers=headers, json=payload, timeout=60)
                    
                    if response.status_code == 200:
                        res_data = response.json()
                        st.success("Analysis Complete!")
                        st.write(res_data['choices'][0]['message']['content'])
                    else:
                        # Detailed Error for Debugging
                        st.error(f"Server Response {response.status_code}: {response.text}")
                        
                except Exception as e:
                    st.error(f"Connection Error: {str(e)}")
else:
    st.info("👈 Please enter your API Key in the sidebar to start.")

