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
    
    html, body, [class*="st-"] { 
        font-family: 'Montserrat', sans-serif !important; 
    }
    
    .stApp { 
        background-color: #103b4d; 
        color: #FFFFFF; 
    }
    
    h1, h2, h3, h4, h5, h6, label, p, .stMarkdown {
        color: #FFFFFF !important;
        font-weight: 700;
    }

    /* --- MOBILE RESPONSIVE LOGIC --- */
    
    /* Desktop Version (Default) */
    .main-title-box {
        background-color: #1eb1b1;
        color: #ffffff !important;
        padding: 15px 40px;
        border-radius: 8px;
        font-size: 2.2rem;
        font-weight: 800;
        display: inline-block;
        text-align: center;
    }

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

    /* Mobile Adjustments (Screen width less than 768px) */
    @media (max-width: 768px) {
        .main-title-box {
            font-size: 1.4rem !important; /* Smaller text for mobile */
            padding: 10px 20px !important;
            width: 90% !important; /* Prevent overlapping */
            margin: 10px auto !important;
        }
        .tag-box {
            font-size: 0.8rem !important;
            padding: 5px 15px !important;
        }
        .stImage > img {
            width: 70px !important; /* Smaller logo for mobile */
        }
    }

    /* Button Consistency */
    div.stButton > button {
        width: 100% !important; 
        background-color: #1eb1b1 !important; 
        border-radius: 8px !important;
        height: 4em !important;
        border: none !important;
    }
    div.stButton > button p {
        color: #ffffff !important; 
        font-weight: 800 !important;
        font-size: 1.1rem !important;
    }

    .stTextArea textarea { 
        background-color: #ffffff !important; 
        color: #103b4d !important; 
        border-radius: 8px; 
    }

    hr { border-top: 2px solid #1eb1b1; opacity: 0.2; }
    </style>
    """, unsafe_allow_html=True)

# 3. HEADER SECTION (Optimized for Mobile Stacking)
# On mobile, Streamlit columns stack. We ensure the layout follows a clean order.
if os.path.exists("Logo.png"):
    try:
        img = Image.open("Logo.png")
        # Centering for mobile
        st.markdown('<div style="text-align: left;">', unsafe_allow_html=True)
        st.image(img, width=100)
        st.markdown('</div>', unsafe_allow_html=True)
    except:
        pass

st.markdown('<div class="tag-box">Plan Builder</div>', unsafe_allow_html=True)
st.markdown('<div style="text-align: center; margin-top: 20px;"><div class="main-title-box">Thrive Hub Intelligence</div></div>', unsafe_allow_html=True)

st.divider()

# 4. MAIN INTERFACE
col_left, col_right = st.columns([1, 1.2], gap="large")

with col_left:
    st.markdown("### Input Data")
    client_data = st.text_area(
        label="Paste Chat History or Assessment Data:", 
        height=400, 
        placeholder="e.g., Male, 39, Corporate role..."
    )
    
    if st.button("Generate Plan"):
        if not client_data:
            st.warning("Please enter client data first.")
        else:
            with st.spinner("Processing..."):
                try:
                    client = OpenAI(base_url="https://integrate.api.nvidia.com/v1", api_key=api_key)
                    prompt = f"System: Use {hassan_context}. Input: {client_data}. Task: Generate Plan."
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
        st.info("Results will appear here.")