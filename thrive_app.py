import streamlit as st
import os
from openai import OpenAI
from dotenv import load_dotenv
from PIL import Image
import io

# 1. LOAD THE BRAIN & ENVIRONMENT
load_dotenv() 
api_key = os.getenv("NVIDIA_API_KEY") or st.secrets.get("NVIDIA_API_KEY")

def load_hassan_brain():
    try:
        with open("thrive_brain.txt", "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        return "Error: thrive_brain.txt not found."

hassan_context = load_hassan_brain()

# 2. THRIVE HUB BRANDED CONFIG
st.set_page_config(page_title="Thrive Hub Intelligence", page_icon="⚡", layout="wide")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@400;700;800&display=swap');
    
    /* Global Reset */
    html, body, [class*="st-"] { 
        font-family: 'Montserrat', sans-serif !important; 
    }
    
    .stApp { 
        background-color: #103b4d; 
        color: #FFFFFF; 
    }
    
    /* FIX: Ensure all headers and labels are bright white and visible */
    h1, h2, h3, h4, h5, h6, label, p, .stMarkdown {
        color: #FFFFFF !important;
        font-weight: 700;
    }

    /* Input Area Styling */
    .stTextArea textarea { 
        background-color: #ffffff !important; 
        color: #103b4d !important; 
        border-radius: 8px; 
        font-weight: 400 !important;
    }

    /* --- HARMONIZED BOX SYSTEM --- */
    
    /* 1. Main Title Box */
    .main-title-box {
        background-color: #1eb1b1;
        color: #ffffff !important;
        padding: 15px 40px;
        border-radius: 8px;
        font-size: 2.2rem;
        font-weight: 800;
        display: inline-block;
        text-align: center;
        line-height: 1.2;
    }

    /* 2. Plan Builder Tag */
    .tag-box {
        background-color: #1eb1b1;
        color: #ffffff !important;
        padding: 8px 20px;
        border-radius: 8px;
        font-size: 1rem;
        font-weight: 800;
        display: inline-block;
        margin-top: 10px;
    }

    /* 3. Generate Plan Button (Matching Title Box Logic) */
    div.stButton > button {
        width: 100% !important; 
        background-color: #1eb1b1 !important; 
        border-radius: 8px !important;
        height: 4em !important;
        border: none !important;
        transition: 0.3s;
    }
    
    div.stButton > button p {
        color: #ffffff !important; 
        font-weight: 800 !important;
        font-size: 1.2rem !important;
        margin: 0 !important;
    }

    div.stButton > button:hover { 
        background-color: #179393 !important; 
    }

    hr { border-top: 2px solid #1eb1b1; opacity: 0.2; margin: 20px 0; }
    </style>
    """, unsafe_allow_html=True)

# 3. HEADER SECTION
# Balancing the top: Logo/Tag on Left, Large Title Centered
h_left, h_mid, h_right = st.columns([1, 3, 1])

with h_left:
    if os.path.exists("Logo.png"):
        try:
            img = Image.open("Logo.png")
            st.image(img, width=110)
        except:
            st.write("")
    st.markdown('<div class="tag-box">Plan Builder</div>', unsafe_allow_html=True)

with h_mid:
    st.markdown('<div style="text-align: center;"><div class="main-title-box">Thrive Hub Intelligence</div></div>', unsafe_allow_html=True)

st.divider()

# 4. MAIN INTERFACE
col_left, col_right = st.columns([1, 1.2], gap="large")

with col_left:
    st.markdown("### Input Data")
    client_data = st.text_area(
        label="Paste Chat History or Assessment Data:", 
        height=450, 
        placeholder="e.g., Male, 39, Corporate role, high stress..."
    )
    
    if st.button("Generate Plan"):
        if not client_data:
            st.warning("Please enter client data first.")
        else:
            with st.spinner("Hassan is building the protocol..."):
                try:
                    client = OpenAI(base_url="https://integrate.api.nvidia.com/v1", api_key=api_key)
                    prompt = f"System: Use {hassan_context}. Input: {client_data}. Task: Generate Plan (Rule 4, 5, 7, 8)."
                    response = client.chat.completions.create(
                        model="meta/llama-3.1-405b-instruct",
                        messages=[{"role": "user", "content": prompt}]
                    )
                    st.session_state.result = response.choices[0].message.content
                except Exception as e:
                    st.error(f"Error: {e}")

with col_right:
    st.markdown("### Client's Most Suitable Plan")
    if 'result' in st.session_state:
        st.markdown(st.session_state.result)
        st.divider()
        st.code(st.session_state.result, language="markdown")
    else:
        # Fixed visibility for the helper info box
        st.info("Provide client details on the left to generate the protocol.")