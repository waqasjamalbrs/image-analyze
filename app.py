import streamlit as st
import base64
import time
from mistralai import Mistral

# Page configuration
st.set_page_config(page_title="Pixtral Image Analyzer", layout="centered")

st.title("🖼️ Pixtral Image Analyzer")
st.write("Mistral ke `pixtral-12b-2409` model ko test karein.")

# Sidebar for API Key
with st.sidebar:
    st.header("Settings")
    api_key = st.text_input("Mistral API Key", type="password", placeholder="Enter your API key here...")
    st.markdown("[Get your API key from Mistral](https://console.mistral.ai/)")

# Main content area
uploaded_file = st.file_uploader("Upload an Image", type=["png", "jpg", "jpeg"])
user_prompt = st.text_area("Prompt", value="Describe this image in detail.", height=100)

if uploaded_file is not None:
    # Display the uploaded image
    st.image(uploaded_file, caption="Uploaded Image", use_container_width=True)

if st.button("Analyze Image", type="primary"):
    if not api_key:
        st.error("Please enter your Mistral API Key in the sidebar.")
    elif uploaded_file is None:
        st.error("Please upload an image first.")
    elif not user_prompt:
        st.error("Please enter a prompt.")
    else:
        with st.spinner("Analyzing image..."):
            # 1. Convert image to base64
            image_bytes = uploaded_file.read()
            base64_image = base64.b64encode(image_bytes).decode("utf-8")
            
            # Determine mime type
            file_extension = uploaded_file.name.split(".")[-1].lower()
            mime_type = "image/png" if file_extension == "png" else "image/jpeg"
            
            # Format base64 string for Mistral
            image_url = f"data:{mime_type};base64,{base64_image}"

            # 2. Initialize Mistral Client
            client = Mistral(api_key=api_key)

            # 3. Create messages payload
            messages = [
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": user_prompt},
                        {"type": "image_url", "image_url": image_url}
                    ]
                }
            ]

            # 4. Make API Call with Retry Logic
            max_retries = 3
            for attempt in range(max_retries):
                try:
                    response = client.chat.complete(
                        model="pixtral-12b-2409",  # Naya, chota model yahan update kar diya hai
                        messages=messages
                    )
                    
                    # 5. Display Result
                    st.subheader("Analysis Result:")
                    st.write(response.choices[0].message.content)
                    break # Agar code successful ho jaye, toh loop yahin ruk jayega
                    
                except Exception as e:
                    error_msg = str(e)
                    if "429" in error_msg or "Rate limit" in error_msg:
                        if attempt < max_retries - 1:
                            st.warning(f"Rate limit hit. 5 seconds wait kar raha hai... (Attempt {attempt + 1}/{max_retries})")
                            time.sleep(5)
                        else:
                            st.error("Rate limit completely exceeded. Barae meharbani Mistral console mein apne account limits ya credits check karein.")
                    else:
                        st.error(f"An error occurred: {error_msg}")
                        break
