import streamlit as st
import os
import datetime
from openai import OpenAI
from dotenv import load_dotenv
from PIL import Image

# 1. LOAD THE BRAIN
load_dotenv() 
api_key = os.getenv("NVIDIA_API_KEY")

def load_hassan_brain():
    try:
        with open("thrive_brain.txt", "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        return "Error: thrive_brain.txt not found."

def append_to_brain(case_data, plan_output):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
    new_entry = f"\n# --- BRAIN INJECTION {timestamp} ---\nINPUT: {case_data}\nOUTPUT: {plan_output}\n# ------------------\n"
    with open("thrive_brain.txt", "a", encoding="utf-8") as f:
        f.write(new_entry)
    return True

hassan_context = load_hassan_brain()

# 2. BRANDED UI
st.set_page_config(page_title="Thrive Hub Intelligence", layout="wide")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@400;700;800&display=swap');
    html, body, [class*="st-"] { font-family: 'Montserrat', sans-serif !important; }
    .stApp { background-color: #103b4d; color: #FFFFFF; }
    
    h1, h2, h3, h4, h5, h6, label, p, .stMarkdown { color: #FFFFFF !important; font-weight: 700; }

    .main-title-box {
        background-color: #1eb1b1; color: #ffffff !important;
        padding: 15px 40px; border-radius: 8px;
        font-size: 2.2rem; font-weight: 800; display: inline-block; text-align: center;
    }

    .tag-box {
        background-color: #1eb1b1; color: #ffffff !important;
        padding: 8px 20px; border-radius: 8px;
        font-size: 1rem; font-weight: 800; display: inline-block; margin-top: 10px;
    }

    .mission-navy-box {
        background-color: #0b2d3b; color: #ffffff !important;
        padding: 10px 20px; border-radius: 8px;
        font-weight: 800; display: inline-block; font-size: 1.1rem;
        border: 1px solid rgba(30, 177, 177, 0.3);
    }

    div.stButton > button {
        width: 100% !important; background-color: #1eb1b1 !important; 
        border-radius: 8px !important; height: 4em !important; border: none !important;
    }
    div.stButton > button p { color: #ffffff !important; font-weight: 800 !important; font-size: 1.1rem !important; }

    .save-brain-btn div.stButton > button {
        background-color: #ffffff !important; color: #103b4d !important; margin-top: 25px !important;
    }
    .save-brain-btn div.stButton > button p { color: #103b4d !important; }

    .stTextArea textarea { background-color: #ffffff !important; color: #103b4d !important; border-radius: 8px; }
    div[data-testid="stCodeBlock"] { display: none !important; }
    hr { border-top: 2px solid #1eb1b1; opacity: 0.2; }
    </style>
    """, unsafe_allow_html=True)

# 3. HEADER
if os.path.exists("Logo.png"):
    st.image("Logo.png", width=100)
st.markdown('<div class="tag-box">Plan Builder</div>', unsafe_allow_html=True)
st.markdown('<div style="text-align: center; margin-top: 20px;"><div class="main-title-box">Thrive Hub Intelligence</div></div>', unsafe_allow_html=True)
st.divider()

# 4. INTERFACE
col_left, col_right = st.columns([1, 1.2], gap="large")

with col_left:
    st.markdown("### Input Data")
    client_data = st.text_area("Paste Input:", height=400, placeholder="e.g., Male, 39, Corporate role...")
    
    if st.button("Generate Plan"):
        if not client_data:
            st.warning("Please enter client data first.")
        else:
            with st.spinner("Analyzing Training Bank..."):
                try:
                    # FIX: Using the most stable high-reasoning model endpoint
                    client = OpenAI(base_url="https://integrate.api.nvidia.com/v1", api_key=api_key)
                    prompt = f"""
                    SYSTEM: You are the Thrive Hub Lead Strategist (Hassan).
                    VAULT CONTEXT (Your Training Bank): 
                    {hassan_context}
                    
                    STRICT INSTRUCTION: 
                    Do NOT give general advice. Use the specific Nutrition, Training, and Sleep protocols found in the Vaults above.
                    If the Vault is empty, focus on 'Protein Anchors' and 'Metabolic Rhythm' rules.
                    
                    FORMAT:
                    1. Strategy Overview
                    2. Specific Nutrition/Sleep Levers
                    3. Arabic Summary (Egyptian Style)
                    
                    INPUT: {client_data}
                    """
                    response = client.chat.completions.create(
                        model="meta/llama-3.1-405b-instruct", 
                        messages=[{"role": "user", "content": prompt}]
                    )
                    st.session_state.result = response.choices[0].message.content
                    st.session_state.last_input = client_data
                except Exception as e:
                    st.error(f"API Connection Error: {e}")

with col_right:
    st.markdown("### Client's Most Suitable Plan")
    if 'result' in st.session_state:
        st.markdown(st.session_state.result)
        st.markdown('<div class="save-brain-btn">', unsafe_allow_html=True)
        if st.button("Save to Brain"):
            if append_to_brain(st.session_state.last_input, st.session_state.result):
                st.balloons()
                st.success("Logic Injected into Brain.")
        st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.markdown('<div style="margin-top: 40px;"><div class="mission-navy-box">Success Shouldn\'t Come at The Cost of Health</div></div>', unsafe_allow_html=True)