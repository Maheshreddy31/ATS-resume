from dotenv import load_dotenv
import streamlit as st
import os
import fitz  # PyMuPDF
import base64
from langchain_groq import ChatGroq  # Importing the ChatGroq class

# Load environment variables
load_dotenv()

# Configure the ChatGroq model
llm = ChatGroq(
    groq_api_key="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",
    model="llama-3.1-70b-Versatile",
    temperature=0.7  # Adjust temperature as needed
)

def get_llama_response(input_text, pdf_content, prompt):
    full_prompt = f"{prompt}\n\nJob Description:\n{input_text}\n\nResume Content:\n{pdf_content}"
    response = llm.invoke(full_prompt)
    return response.content

def input_pdf_setup(uploaded_file):
    if uploaded_file is not None:
        doc = fitz.open(stream=uploaded_file.read(), filetype="pdf")
        first_page = doc.load_page(0)
        text = first_page.get_text("text")
        return text
    else:
        raise FileNotFoundError("No file uploaded")

# Streamlit page configuration
st.set_page_config(page_title="ATS Resume Expert", layout="wide")

# Custom CSS with 3D visuals and colorful interface
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600&display=swap');

    body {
        font-family: 'Poppins', sans-serif;
        background: linear-gradient(to right, #ffecd2 0%, #fcb69f 100%);
        color: #333;
    }
    
    .header {
        background-color: #4CAF50;
        color: white;
        padding: 10px;
        text-align: center;
        border-radius: 10px;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.4);
        animation: pulse 2s infinite;
    }

    @keyframes pulse {
        0% { transform: scale(1); }
        50% { transform: scale(1.05); }
        100% { transform: scale(1); }
    }

    .stButton button {
        background-image: linear-gradient(to right, #ff6e7f, #bfe9ff);
        color: white;
        border: none;
        padding: 10px 20px;
        font-size: 16px;
        border-radius: 50px;
        box-shadow: 0 6px 12px rgba(0, 0, 0, 0.2);
        transition: all 0.3s ease;
    }

    .stButton button:hover {
        background-image: linear-gradient(to right, #bfe9ff, #ff6e7f);
        transform: translateY(-5px);
    }

    .custom-container {
        padding: 20px;
        background: white;
        border-radius: 10px;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
        margin-top: 20px;
    }

    .role-box {
        background-color: #4CAF50;
        color: white;
        padding: 10px;
        border-radius: 10px;
        text-align: center;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
    }

    .stTextInput textarea {
        border-radius: 20px;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
    }

    .stFileUploader label {
        color: #ff6e7f;
        font-weight: bold;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Header with custom styling
st.markdown('<div class="header"><h1>Application Tracking System</h1></div>', unsafe_allow_html=True)

# Container for inputs
with st.container():
    st.markdown('<div class="custom-container">', unsafe_allow_html=True)
    input_text = st.text_area("Enter Job Description:", key="input", height=150)
    uploaded_file = st.file_uploader("Upload Your Resume (PDF, only)", type=["pdf"])
    role = st.selectbox("Select the Role:", ["Data Scientist", "Software Engineer", "Data Analyst", "Product Manager", "Marketing Specialist", "Sales Executive", "Other"], index=0, format_func=lambda x: f"🔍 {x}")
    st.markdown('</div>', unsafe_allow_html=True)

# Role-specific prompts
prompts = {
    "Data Scientist": {
        "check_score": """
        You are an ATS scanner with a deep understanding of data science and ATS functionality. 
        Evaluate the resume against the provided job description and give the percentage match. 
        Provide a summary that includes missing keywords and suggest skills that the candidate could upskill to better match the role.
        """,
        "skill_enhancement": """
        You are a career advisor with deep knowledge of the Data Science field. 
        Analyze the resume and job description and suggest skills or certifications that the candidate should pursue to enhance their fit for the Data Scientist role.
        """,
        "generate_cover_letter": """
        You are an expert in crafting compelling cover letters tailored to specific roles. 
        Create a cover letter based on the resume and the provided job description, highlighting the candidate’s strengths and how they align with the job requirements.
        """
    },
    "Software Engineer": {
        "check_score": """
        You are an ATS scanner with a deep understanding of software engineering and ATS functionality. 
        Evaluate the resume against the provided job description and give the percentage match. 
        Provide a summary that includes missing keywords and suggest skills that the candidate could upskill to better match the role.
        """,
        "skill_enhancement": """
        You are a career advisor with deep knowledge of the Software Engineering field. 
        Analyze the resume and job description and suggest skills or certifications that the candidate should pursue to enhance their fit for the Software Engineer role.
        """,
        "generate_cover_letter": """
        You are an expert in crafting compelling cover letters tailored to specific roles. 
        Create a cover letter based on the resume and the provided job description, highlighting the candidate’s strengths and how they align with the job requirements.
        """
    },
    # Add similar prompts for other roles
}

# Buttons for different actions with 3D effect
col1, col2, col3 = st.columns(3)
with col1:
    submit_check_score = st.button("Check Your Score 🔍")
with col2:
    submit_skill_enhancement = st.button("Skill Enhancement 💡")
with col3:
    submit_generate_cover_letter = st.button("Generate Cover Letter 📝")

# Action for "Check Score"
if submit_check_score and uploaded_file is not None:
    try:
        pdf_content = input_pdf_setup(uploaded_file)
        response = get_llama_response(input_text, pdf_content, prompts[role]["check_score"])
        st.subheader("Check Score Result")
        st.write(response)
    except Exception as e:
        st.error(f"Error: {e}")
elif submit_check_score:
    st.warning("Please upload the resume")

# Action for "Skill Enhancement Suggestions"
if submit_skill_enhancement and uploaded_file is not None:
    try:
        pdf_content = input_pdf_setup(uploaded_file)
        response = get_llama_response(input_text, pdf_content, prompts[role]["skill_enhancement"])
        st.subheader("Skill Enhancement Suggestions")
        st.write(response)
    except Exception as e:
        st.error(f"Error: {e}")
elif submit_skill_enhancement:
    st.warning("Please upload the resume")

# Action for "Generate Cover Letter"
if submit_generate_cover_letter and uploaded_file is not None:
    try:
        pdf_content = input_pdf_setup(uploaded_file)
        response = get_llama_response(input_text, pdf_content, prompts[role]["generate_cover_letter"])
        st.subheader("Generated Cover Letter")
        st.write(response)
    except Exception as e:
        st.error(f"Error: {e}")
elif submit_generate_cover_letter:
    st.warning("Please upload the resume")
