import streamlit as st
from pathlib import Path
import google.generativeai as genai
# Fetch API key from Streamlit secrets
api_key = st.secrets["api_key"]

# Configure genai with API key
genai.configure(api_key=api_key)

# Set up the Model configuration
generation_config = {
    "temperature": 0.4,
    "top_p": 1,
    "top_k": 32,
    "max_output_tokens": 1024,
}

# Apply Safety Check
safety_settings = [
    {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
]

# Updated model
model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    safety_settings=safety_settings,
    generation_config=generation_config
)

# System prompt
system_prompt = """
As a highly skilled medical practitioner specializing in image analysis, your task is to examine medical images for a renowned hospital. 
Your expertise is crucial in identifying any anomalies, diseases, or health issues present in the image.

Your Responsibilities:
1. **Detailed Analysis**: Thoroughly analyze each image, focusing on identifying abnormal findings.
2. **Findings Report**: Document all observed anomalies or signs of disease in a structured format.
3. **Recommendations**: Suggest further tests or treatment options based on your analysis.
4. **Treatment Suggestions**: Recommend possible interventions if applicable.

**Important Notes**:
- Only respond if the image pertains to human health issues.
- If the image quality is poor, state: "Unable to determine due to low image quality."
- Always include: "Consult with a doctor before making any medical decision."
Please provide me these 4 Headings: Detailed Analysis, Findings Report, Recommendations, Treatment Suggestions
"""

# Set the page configuration
st.set_page_config(page_title="Dr Image Analytics", page_icon="🤖", layout="wide")

# Custom CSS for styling
st.markdown(
    """
    <style>
        .main-content {
            padding: 2rem;
        }
        .centered-header {
            text-align: center;
            font-size: 36px;
            font-weight: bold;
            color: #007BFF;
            margin-bottom: 1rem;
        }
        .sub-text {
            text-align: center;
            font-size: 18px;
            color: #666666;
            margin-bottom: 2rem;
        }
        .footer {
            position: fixed;
            bottom: 10px;
            width: 100%;
            text-align: center;
            font-size: 14px;
            color: gray;
        }
        .sidebar .sidebar-content {
            padding: 2rem 1rem;
        }
        .sidebar img {
            display: block;
            margin: 0 auto 1rem auto;
        }
        .sidebar h2 {
            font-size: 24px;
            margin-bottom: 1rem;
        }
        .stAlert {
            margin-top: 1rem;
        }
    </style>
    """,
    unsafe_allow_html=True,
)

# Sidebar
with st.sidebar:
    st.image("./logo.jpg", width=100)
    st.title("Dr Image Analytics")
    st.markdown("---")
    st.header("About")
    st.write("""
    Dr Image Analytics is an AI-powered medical image analysis tool. Developed by Wasik Rehman, 
    It uses advanced machine learning algorithms to examine medical images 
    and provide detailed analysis, findings, recommendations, and treatment suggestions. 
    This tool is designed to assist healthcare professionals in making more informed decisions, 
    but it should not replace professional medical advice.
    """)

# Main content
st.markdown("<div class='main-content'>", unsafe_allow_html=True)
st.markdown("<h1 class='centered-header'>🩺 Dr Image Analytics 🔍</h1>", unsafe_allow_html=True)
st.markdown("<p class='sub-text'>An AI-powered tool for analyzing medical images ⚕️📊</p>", unsafe_allow_html=True)

# File uploader
uploaded_file = st.file_uploader("📤 Upload a medical image for analysis", type=["jpg", "jpeg", "png"])
if uploaded_file:
    st.image(uploaded_file, width=300, caption="🖼️ Uploaded Medical Image")

# Generate Report button
if st.button("📑 Generate Report"):
    if uploaded_file is None:
        st.error("⚠️ Please upload an image before generating the report.")
    else:
        image_data = uploaded_file.getvalue()
        image_parts = [{"mime_type": "image/jpeg", "data": image_data}]
        prompt_parts = [image_parts[0], system_prompt]

        st.markdown("<h2 class='centered-header'>📝 Analysis Report</h2>", unsafe_allow_html=True)

        with st.spinner("⏳ Please wait while the report is being generated..."):
            response = model.generate_content(prompt_parts)

        st.success("✅ Report Generated Successfully!")
        st.write(response.text)

st.markdown("</div>", unsafe_allow_html=True)

# Footer with copyright and GitHub link
st.markdown(
    """
    <div class="footer">
        <p>© 2025 All Rights Reserved by <b>Wasik Rehman</b></p>
        <p>🔗 GitHub: <a href="https://github.com/wasik023" target="_blank">@wasik023</a></p>
    </div>
    """,
    unsafe_allow_html=True
)
