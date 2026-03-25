import os
import base64
from PIL import Image
import streamlit as st
from dotenv import load_dotenv
from groq import Groq

# Load environment variables
load_dotenv()

# Initialize Groq client
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# Streamlit page config
st.set_page_config(
    page_title="✨ MCQ Extractor Pro | AI-Powered Text Extraction",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# Custom styling
st.markdown("""
<style>
.main, .stApp {
    background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
}
.stTitle {
    background: linear-gradient(120deg, #2c3e50, #3498db);
    padding: 1.5rem;
    border-radius: 15px;
    color: white;
    text-align: center;
    margin-bottom: 2rem;
}
.stHeader {
    background: linear-gradient(120deg, #3498db, #2980b9);
    padding: 1rem;
    border-radius: 12px;
    color: white;
    margin-bottom: 1.5rem;
}
.extractedContent {
    background: white;
    border-radius: 15px;
    padding: 25px;
    border: 3px solid #3498db;
}
div[data-testid="stButton"] button {
    width: 100%;
    min-height: 65px;
    background: linear-gradient(45deg, #2ecc71, #27ae60);
    color: white;
    font-size: 20px;
    font-weight: bold;
    border-radius: 12px;
}
.footer {
    background: linear-gradient(120deg, #2c3e50, #3498db);
    padding: 1.5rem;
    border-radius: 15px;
    color: white;
    text-align: center;
    margin-top: 2rem;
}
</style>
""", unsafe_allow_html=True)

# Header
st.markdown("""
<div class="stTitle">
    <h1>📚 MCQ Extractor Pro 🤖</h1>
    <p>Powered by Groq Vision AI</p>
</div>
""", unsafe_allow_html=True)

# Welcome message
st.markdown("""
<div style='background:white;padding:1.5rem;border-radius:15px;margin-bottom:2rem;'>
<h4>🎯 Upload an image to extract MCQs or text</h4>
<ul>
<li>🔍 Accurate MCQ extraction</li>
<li>📝 Preserves formatting</li>
<li>⚡ Ultra-fast Groq inference</li>
</ul>
</div>
""", unsafe_allow_html=True)

# Upload image
uploaded_file = st.file_uploader(
    "📤 Drop your image here",
    type=["jpg", "jpeg", "png", "jfif"],
)

# Columns
col1, col2 = st.columns(2)

def extract_with_groq(image_bytes):
    image_base64 = base64.b64encode(image_bytes).decode("utf-8")

    response = client.chat.completions.create(
        model="meta-llama/llama-4-scout-17b-16e-instruct",
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": (
                            "You are an expert at extracting MCQs and text from images. "
                            "Extract all questions exactly as written. "
                            "Do not add answers. Maintain formatting."
                        )
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{image_base64}"
                        }
                    }
                ]
            }
        ]
    )
    return response.choices[0].message.content

with col1:
    st.markdown('<div class="stHeader"><h3>📂 Uploaded Image</h3></div>', unsafe_allow_html=True)

    if uploaded_file:
        image = Image.open(uploaded_file)
        st.image(image, caption="📸 Preview", use_container_width=True)

    extract_button = st.button("🔍 Extract Content ⚡")

with col2:
    st.markdown('<div class="stHeader"><h3>📜 Extracted Content</h3></div>', unsafe_allow_html=True)

    if uploaded_file and extract_button:
        try:
            with st.spinner("🔄 Processing image..."):
                result = extract_with_groq(uploaded_file.getvalue())

            st.balloons()

            st.markdown(
                f'<div class="extractedContent"><pre>{result}</pre></div>',
                unsafe_allow_html=True
            )

            st.download_button(
                label="📋 Download Extracted Content",
                data=result,
                file_name="extracted_content.md",
                mime="text/markdown"
            )

        except Exception as e:
            st.error(f"🚫 Error: {e}")

# Footer
st.markdown("""
<div class="footer">
<h4>🚀 MCQ Extractor Pro</h4>
<p>Built with Streamlit & Groq Vision AI</p>
<p style="font-size:0.8rem;">💡 Tip: Clear, well-lit images give best results</p>
</div>
""", unsafe_allow_html=True)




# import os
# from PIL import Image
# import streamlit as st
# from dotenv import load_dotenv
# import google.generativeai as genai

# # Load environment variables
# load_dotenv()

# # Configure page and styling with custom theme and icon
# st.set_page_config(
#     page_title="✨ MCQ Extractor Pro | AI-Powered Text Extraction",
#     page_icon="📚",
#     layout="wide",
#     initial_sidebar_state="collapsed",
#     menu_items={
#         'Get Help': 'https://github.com/yourusername/mcq-extractor',
#         'Report a bug': 'https://github.com/yourusername/mcq-extractor/issues',
#         'About': '''
#         ### MCQ Extractor Pro
#         An AI-powered tool for extracting MCQs and text from images.
#         '''
#     }
# )

# st.markdown("""
#     <style>
#     /* Global Styles */
#     .main {
#         background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
#         padding: 2rem;
#     }
    
#     /* App Container */
#     .stApp {
#         background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
#     }
    
#     /* Title Styling */
#     .stTitle {
#         background: linear-gradient(120deg, #2c3e50, #3498db);
#         padding: 1.5rem;
#         border-radius: 15px;
#         color: white !important;
#         text-align: center;
#         box-shadow: 0 4px 15px rgba(0,0,0,0.1);
#         margin-bottom: 2rem;
#     }
    
#     /* Header Styling */
#     .stHeader {
#         background: linear-gradient(120deg, #3498db, #2980b9);
#         padding: 1rem;
#         border-radius: 12px;
#         color: white !important;
#         margin-bottom: 1.5rem;
#         box-shadow: 0 4px 10px rgba(0,0,0,0.1);
#     }
    
#     /* Upload Section Styling */
#     .uploadedImage {
#         background: white;
#         border: 3px solid #3498db;
#         border-radius: 15px;
#         padding: 15px;
#         box-shadow: 0 4px 15px rgba(0,0,0,0.1);
#     }
    
#     /* Enhanced Extract Button Styling */
#     div[data-testid="stButton"] button {
#         width: 100%;
#         min-height: 65px;
#         background: linear-gradient(45deg, #2ecc71, #27ae60);
#         color: white;
#         padding: 1rem 2.5rem;
#         border-radius: 12px;
#         font-size: 20px;
#         font-weight: bold;
#         border: none;
#         cursor: pointer;
#         transition: all 0.3s ease;
#         box-shadow: 0 4px 15px rgba(0,0,0,0.1);
#         margin: 1rem 0;
#         letter-spacing: 1px;
#         line-height: 1.5;
#         text-transform: uppercase;
#     }
    
#     div[data-testid="stButton"] button:hover {
#         transform: translateY(-2px);
#         box-shadow: 0 6px 20px rgba(0,0,0,0.15);
#         background: linear-gradient(45deg, #27ae60, #2ecc71);
#         letter-spacing: 2px;
#     }

#     div[data-testid="stButton"] button p {
#         font-size: 20px !important;
#     }

#     /* Extracted Content Styling */
#     .extractedContent {
#         background: white;
#         border-radius: 15px;
#         padding: 25px;
#         border: 3px solid #3498db;
#         box-shadow: 0 4px 15px rgba(0,0,0,0.1);
#     }
    
#     /* Download Button Styling */
#     div[data-testid="stDownloadButton"] button {
#         background: linear-gradient(45deg, #9b59b6, #8e44ad);
#         color: white;
#         padding: 0.8rem 2rem;
#         border-radius: 8px;
#         font-weight: bold;
#         width: 100%;
#         border: none;
#         transition: all 0.3s ease;
#         box-shadow: 0 4px 15px rgba(0,0,0,0.1);
#     }
    
#     div[data-testid="stDownloadButton"] button:hover {
#         transform: translateY(-2px);
#         box-shadow: 0 6px 20px rgba(0,0,0,0.15);
#     }
    
#     /* Status Messages */
#     .stAlert {
#         border-radius: 10px;
#         box-shadow: 0 4px 15px rgba(0,0,0,0.1);
#     }
    
#     /* Footer Styling */
#     .footer {
#         background: linear-gradient(120deg, #2c3e50, #3498db);
#         padding: 1.5rem;
#         border-radius: 15px;
#         color: white;
#         text-align: center;
#         margin-top: 2rem;
#         box-shadow: 0 4px 15px rgba(0,0,0,0.1);
#     }
#     </style>
# """, unsafe_allow_html=True)

# # Configure genai API key
# genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
# model = genai.GenerativeModel("models/gemini-1.5-flash-latest")

# def get_gemini_response(input, image, prompt):
#     response = model.generate_content([input, image[0], prompt])
#     return response.text

# def input_image_details(uploaded_file):
#     if uploaded_file is not None:
#         bytes_data = uploaded_file.getvalue()
#         image_parts = [
#             {
#                 "mime_type": uploaded_file.type,
#                 "data": bytes_data
#             }
#         ]
#         return image_parts
#     else:
#         raise FileNotFoundError("No File Uploaded")

# # App Header with enhanced styling
# st.markdown("""
#     <div class="stTitle">
#         <h1>📚 MCQ Extractor Pro 🤖</h1>
#         <p style="font-size: 1.2rem; margin-top: 0.5rem;">
#             Powered by Advanced AI Technology
#         </p>
#     </div>
# """, unsafe_allow_html=True)

# # Enhanced welcome message
# st.markdown("""
#     <div style='background: white; padding: 1.5rem; border-radius: 15px; margin-bottom: 2rem; box-shadow: 0 4px 15px rgba(0,0,0,0.1);'>
#         <h4>🎯 Welcome to MCQ Extractor Pro!</h4>
#         <p>Transform your images into editable text with our advanced AI technology:</p>
#         <ul>
#             <li>🔍 Precise MCQ extraction</li>
#             <li>📝 Maintains original formatting</li>
#             <li>⚡ Fast and accurate processing</li>
#             <li>💾 Easy export options</li>
#         </ul>
#     </div>
# """, unsafe_allow_html=True)


# # Enhanced welcome message
# st.markdown("""
#     <div style='background: white; padding: 1.5rem; border-radius: 15px; margin-bottom: 2rem; box-shadow: 0 4px 15px rgba(0,0,0,0.1);'>
#         <h4>💨 Please Upload An Image For MCQs Extraction Below 👇!</h4>
#     </div>
# """, unsafe_allow_html=True)

# uploaded_file = st.file_uploader(
#         "📤 Drop your image here",
#         type=["jpg", "jpeg", "png", "jfif"],
#         help="Upload the image containing text such as MCQs or paragraphs."
#     )

# # Create two equal columns
# col1, col2 = st.columns(2)

# with col1:
#     st.markdown('<div class="stHeader"><h3>📂 Uploaded Image</h3></div>', unsafe_allow_html=True)

#     if uploaded_file is not None:
#         image = Image.open(uploaded_file)
#         st.image(image, caption='📸 Preview of uploaded image', use_container_width=True)
#         st.markdown('</div>', unsafe_allow_html=True)

#     status_placeholder = st.empty()

#     # Create the button and handle click logic
#     extract_button = st.button("🔍 Extract Content ⚡", key="extract_button", help="Click to analyze the uploaded image and extract content.")


# with col2:
#     st.markdown('<div class="stHeader"><h3>📜 Extracted Content</h3></div>', unsafe_allow_html=True)
    
#     default_prompt = """
#     You are an expert in extracting text and questions from images. Given an image, identify and extract the content, 
#     maintaining the format for any paragraphs or questions found. Do not specify correct answers.
#     """

#     content_placeholder = st.empty()
#     button_placeholder = st.empty()

#     if uploaded_file is not None and extract_button:
#         try:
#             with status_placeholder:
#                 st.info("🔄 Processing image... Please wait")
            
#             image_data = input_image_details(uploaded_file)
#             response = get_gemini_response(default_prompt, image_data, "Extract the content from the uploaded image.")
            
#             st.balloons()
#             status_placeholder.empty()
            
#             content_placeholder.markdown(
#                 f'<div class="extractedContent"><pre>{response}</pre></div>',
#                 unsafe_allow_html=True
#             )
            
#             button_placeholder.download_button(
#                 label="📋 Download Extracted Content",
#                 data=response,
#                 file_name="extracted_content.md",
#                 mime="text/markdown",
#                 help="Click to download the extracted content as a markdown file"
#             )

#         except Exception as e:
#             status_placeholder.error(f"🚫 Error: {str(e)}")

# # Enhanced Footer
# st.markdown("""
#     <div class="footer">
#         <h4>🚀 MCQ Extractor Pro</h4>
#         <p>Made with ❤️ using Streamlit and Google's Gemini AI</p>
#         <p style="font-size: 0.8rem; margin-top: 0.5rem;">
#             💡 Pro Tip: For best results, ensure your image is clear and well-lit
#         </p>
#     </div>
# """, unsafe_allow_html=True)
