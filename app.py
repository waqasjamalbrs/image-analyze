import streamlit as st
import base64
from openai import OpenAI

st.set_page_config(page_title="LongCat-Flash-Omni-2603 Image Analyzer", layout="centered")
st.title("🔥 LongCat-Flash-Omni-2603 Image Analyzer")
st.caption("Meituan LongCat Omni Model - Upload image + prompt = instant analysis")

# API Key input (pehle baar save ho jayega session mein)
if "api_key" not in st.session_state:
    st.session_state.api_key = ""

api_key = st.text_input(
    "LongCat API Key (Bearer wala nahi, sirf key)",
    value=st.session_state.api_key,
    type="password",
    help="https://longcat.chat/platform/api_keys se lo (free quota milta hai)"
)
if api_key:
    st.session_state.api_key = api_key

# Image upload
uploaded_file = st.file_uploader(
    "Image upload karo (JPG, PNG, WEBP, etc.)",
    type=["jpg", "jpeg", "png", "webp", "bmp", "tiff"],
    help="Direct upload → base64 mein convert hoga"
)

# Prompt
prompt = st.text_area(
    "Prompt likho (kuch bhi pooch sakte ho)",
    placeholder="Yeh image mein kya ho raha hai? Step by step explain karo...",
    height=100
)

analyze_btn = st.button("🚀 Analyze with LongCat-Flash-Omni-2603", type="primary", use_container_width=True)

if analyze_btn:
    if not api_key:
        st.error("API Key daalo pehle!")
        st.stop()
    if not uploaded_file:
        st.error("Image upload karo!")
        st.stop()
    if not prompt:
        st.error("Prompt likho!")
        st.stop()

    with st.spinner("LongCat-Flash-Omni-2603 soch raha hai... (Omni model hai, thoda time lag sakta hai)"):
        # Image ko base64 mein convert
        image_bytes = uploaded_file.read()
        base64_image = base64.b64encode(image_bytes).decode("utf-8")

        # OpenAI client (LongCat base URL)
        client = OpenAI(
            base_url="https://api.longcat.chat/openai",
            api_key=api_key
        )

        messages = [
            {
                "role": "system",
                "content": [{"type": "text", "text": "You are a helpful and accurate assistant."}]
            },
            {
                "role": "user",
                "content": [
                    {
                        "type": "input_image",
                        "input_image": {
                            "type": "base64",          # base64 support confirmed
                            "data": base64_image
                        }
                    },
                    {
                        "type": "text",
                        "text": prompt
                    }
                ]
            }
        ]

        try:
            response = client.chat.completions.create(
                model="LongCat-Flash-Omni-2603",
                messages=messages,
                output_modalities=["text"],   # sirf text chahiye
                stream=False,
                temperature=0.7,
                max_tokens=4096
            )
            
            result = response.choices[0].message.content
            st.success("✅ Analysis complete!")
            st.markdown("### 📸 Analysis Result")
            st.markdown(result)
            
            # Original image preview
            st.image(uploaded_file, caption="Uploaded Image", use_column_width=True)
            
        except Exception as e:
            st.error(f"Error: {str(e)}")
            st.info("Tips: API key sahi hai? Quota bacha hai? (daily free 5M tokens)")

# Footer
st.divider()
st.caption("Made for LongCat-Flash-Omni-2603 | GitHub pe daal do aur Streamlit Cloud pe deploy karo 🚀")
