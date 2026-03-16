import streamlit as st
import base64
from openai import OpenAI

st.set_page_config(page_title="LongCat-Flash-Omni-2603 Image Analyzer", layout="centered")
st.title("🔥 LongCat-Flash-Omni-2603 Image Analyzer")
st.caption("Meituan LongCat Omni Model - Upload image + prompt = instant analysis")

# API Key
if "api_key" not in st.session_state:
    st.session_state.api_key = ""

api_key = st.text_input(
    "LongCat API Key",
    value=st.session_state.api_key,
    type="password",
    help="https://longcat.chat/platform/api_keys se lo"
)
if api_key:
    st.session_state.api_key = api_key

uploaded_file = st.file_uploader(
    "Image upload karo (JPG, PNG, WEBP, BMP, TIFF)",
    type=["jpg", "jpeg", "png", "webp", "bmp", "tiff"]
)

prompt = st.text_area(
    "Prompt likho",
    placeholder="Yeh image mein kya ho raha hai? Detail mein batao...",
    height=100
)

analyze_btn = st.button("🚀 Analyze with LongCat-Flash-Omni-2603", type="primary", use_container_width=True)

if analyze_btn:
    if not api_key:
        st.error("API Key daalo!")
        st.stop()
    if not uploaded_file:
        st.error("Image upload karo!")
        st.stop()
    if not prompt:
        st.error("Prompt likho!")
        st.stop()

    with st.spinner("LongCat-Flash-Omni-2603 analyze kar raha hai..."):
        image_bytes = uploaded_file.read()
        base64_image = base64.b64encode(image_bytes).decode("utf-8")

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
                            "type": "base64",
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
                stream=False,
                temperature=0.7,
                max_tokens=4096,
                extra_body={                  # ← Yeh line error fix karti hai
                    "output_modalities": ["text"]   # sirf text output chahiye (audio nahi)
                }
            )
            
            result = response.choices[0].message.content
            st.success("✅ Analysis complete!")
            st.markdown("### 📸 Analysis Result")
            st.markdown(result)
            
            st.image(uploaded_file, caption="Uploaded Image", use_column_width=True)
            
        except Exception as e:
            st.error(f"Error: {str(e)}")
            st.info("Tips: API key check karo, quota bacha hai? (free 5M tokens daily)")

st.divider()
st.caption("LongCat-Flash-Omni-2603 Ready | GitHub pe push + Streamlit Cloud deploy")
