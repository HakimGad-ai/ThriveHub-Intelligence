import streamlit as st
import os
import datetime
from openai import OpenAI
from dotenv import load_dotenv

# 1. ENVIRONMENT & VAULT INIT
load_dotenv() 
api_key = os.getenv("NVIDIA_API_KEY") or st.secrets.get("NVIDIA_API_KEY")

def load_file(filename):
    try:
        with open(filename, "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        return f"Error: {filename} not found."

def append_to_brain(case_data, plan_output):
    ts = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
    entry = f"\n# --- BRAIN INJECTION {ts} ---\nINPUT: {case_data}\nOUTPUT: {plan_output}\n# ------------------\n"
    try:
        with open("thrive_brain.txt", "a", encoding="utf-8") as f:
            f.write(entry)
        return True
    except Exception as e:
        st.error(f"Write Error: {e}")
        return False

# Load Strategic Context
hassan_context = load_file("thrive_brain.txt")
hassan_identity = load_file("thrive_identity.txt")

# 2. BRANDED UI CONFIG (REINSTATED ORIGINAL)
st.set_page_config(page_title="Thrive Hub Intelligence", page_icon="⚡", layout="wide")

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
        padding: 12px 25px; border-radius: 8px;
        font-weight: 800; display: inline-block; font-size: 1.1rem;
        border: 1px solid rgba(30, 177, 177, 0.3);
    }
    @media (max-width: 768px) {
        .main-title-box { font-size: 1.4rem !important; width: 95% !important; padding: 10px !important; }
        .mission-navy-box { font-size: 0.9rem !important; width: 100%; text-align: center; }
    }
    div.stButton > button {
        width: 100% !important; background-color: #1eb1b1 !important; 
        border-radius: 8px !important; height: 4em !important; border: none !important;
    }
    div.stButton > button p { color: #ffffff !important; font-weight: 800 !important; font-size: 1.1rem !important; }
    .stTextArea textarea { background-color: #ffffff !important; color: #103b4d !important; border-radius: 8px; }
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
    client_data = st.text_area("Paste Input:", height=400, placeholder="e.g., Hakim, 39, Perfectionist, Sleeps 7h but wakes twice...")
    
    if st.button("Generate Plan"):
        if client_data:
            with st.spinner("Analyzing Root Causes..."):
                try:
                    client = OpenAI(base_url="https://integrate.api.nvidia.com/v1", api_key=api_key)
                    system_message = f"IDENTITY: {hassan_identity}\nBRAIN LOGIC: {hassan_context}"
                    
                    response = client.chat.completions.create(
                        model="meta/llama-3.1-70b-instruct", 
                        messages=[
                            {"role": "system", "content": system_message},
                            {"role": "user", "content": f"Analyze and build strategy: {client_data}"}
                        ],
                        temperature=0.1,
                        stream=True
                    )
                    
                    with col_right:
                        placeholder = st.empty()
                        full_response = ""
                        for chunk in response:
                            if chunk.choices[0].delta.content:
                                full_response += chunk.choices[0].delta.content
                                placeholder.markdown(full_response + "▌")
                        
                        placeholder.markdown(full_response)
                        st.session_state.result = full_response
                        st.session_state.last_input = client_data
                except Exception as e:
                    st.error(f"Logic Error: {e}")

with col_right:
    st.markdown("### Decision Engine Output")
    if 'result' in st.session_state:
        st.markdown(st.session_state.result)
        if st.button("Save to Brain"):
            if append_to_brain(st.session_state.last_input, st.session_state.result):
                st.balloons(); st.success("Logic Injected into the Thrive Hub Brain.")
        st.code(st.session_state.result, language="markdown")
    elif not client_data:
        st.markdown('<div style="margin-top: 40px;"><div class="mission-navy-box">Success Shouldn\'t Come at The Cost of Health</div></div>', unsafe_allow_html=True)