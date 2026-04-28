import streamlit as st
import os
import datetime
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

# THE BLACK BOX INJECTION ENGINE
def append_to_black_box(case_data, plan_output):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
    new_entry = f"""
# --- BLACK BOX INJECTION {timestamp} ---
[VAULT 1 - CASE Snapshot]
INPUT: {case_data}
DECISION LOGIC: {plan_output}
# ---------------------------------------
"""
    try:
        with open("thrive_brain.txt", "a", encoding="utf-8") as f:
            f.write(new_entry)
        return True
    except Exception as e:
        st.error(f"Write Error: {e}")
        return False

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

    /* --- RESPONSIVE BOX SYSTEM --- */
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

    @media (max-width: 768px) {
        .main-title-box {
            font-size: 1.4rem !important;
            padding: 10px 20px !important;
            width: 90% !important;
            margin: 10px auto !important;
        }
    }

    /* --- BUTTONS --- */
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

    /* Special Styling for Black Box Button */
    .black-box-btn div.stButton > button {
        background-color: #ffffff !important;
        color: #103b4d !important;
        margin-top: 25px !important;
    }
    .black-box-btn div.stButton > button p {
        color: #103b4d !important;
    }

    .stTextArea textarea { 
        background-color: #ffffff !important; 
        color: #103b4d !important; 
        border-radius: 8px; 
    }

    hr { border-top: 2px solid #1eb1b1; opacity: 0.2; }
    </style>
    """, unsafe_allow_html=True)

# 3. HEADER
if os.path.exists("Logo.png"):
    try:
        img = Image.open("Logo.png")
        st.markdown('<div style="text-align: left;">', unsafe_allow_html=True)
        st.image(img, width=100)
        st.markdown('</div>', unsafe_allow_html=True)
    except: pass

st.markdown('<div class="tag-box">Plan Builder</div>', unsafe_allow_html=True)
st.markdown('<div style="text-align: center; margin-top: 20px;"><div class="main-title-box">Thrive Hub Intelligence</div></div>', unsafe_allow_html=True)
st.divider()

# 4. MAIN INTERFACE
col_left, col_right = st.columns([1, 1.2], gap="large")

with col_left:
    st.markdown("### Input Data")
    client_data = st.text_area(label="Input Details:", height=400, placeholder="Paste details...")
    
    if st.button("Generate Plan"):
        if not client_data:
            st.warning("Please enter client data first.")
        else:
            with st.spinner("Consulting the Brain..."):
                try:
                    client = OpenAI(base_url="https://integrate.api.nvidia.com/v1", api_key=api_key)
                    prompt = f"""
                    SYSTEM: You are the Thrive Hub Lead Strategist. 
                    VAULT CONTEXT: {hassan_context}
                    STRICTURES: Tone: Calm Operator. NO AI filler. Use 'Protein Anchors' & 'Metabolic Rhythm'.
                    INPUT: {client_data}
                    """
                    response = client.chat.completions.create(
                        model="meta/llama-3.1-405b-instruct",
                        messages=[{"role": "user", "content": prompt}]
                    )
                    st.session_state.result = response.choices[0].message.content
                    st.session_state.last_input = client_data
                except Exception as e:
                    st.error(f"Error: {e}")

with col_right:
    st.markdown("### Client's Most Suitable Plan")
    if 'result' in st.session_state:
        st.markdown(st.session_state.result)
        
        # THE BLACK BOX INJECTION
        st.markdown('<div class="black-box-btn">', unsafe_allow_html=True)
        if st.button("✅ Save to Black Box (Inject Logic)"):
            if append_to_black_box(st.session_state.last_input, st.session_state.result):
                st.balloons()
                st.success("VAULT UPDATED: Logic Injected into the Black Box.")
        st.markdown('</div>', unsafe_allow_html=True)
        
        st.divider()
        st.code(st.session_state.result, language="markdown")
    else:
        st.info("Input data to predict burnout and build protocol.")