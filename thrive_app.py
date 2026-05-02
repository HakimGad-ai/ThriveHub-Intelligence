import streamlit as st
import os
import datetime
import hashlib
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

def get_input_hash(text):
    return hashlib.md5(text.encode()).hexdigest()

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

# Load Context
hassan_context = load_file("thrive_brain.txt")
hassan_identity = load_file("thrive_identity.txt")

# 2. BRANDED UI CONFIG
st.set_page_config(page_title="Thrive Hub Intelligence", page_icon="⚡", layout="wide")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@400;700;800&display=swap');
    
    html, body, [class*="st-"] { font-family: 'Montserrat', sans-serif !important; }
    .stApp { background-color: #103b4d; color: #FFFFFF; }
    
    /* TARGETED BRAND STYLING */
    .stMarkdown p, h1, h2, h3, h4 { color: #FFFFFF !important; font-weight: 700 !important; }

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
        margin-top: 40px;
    }

    div.stButton > button {
        width: 100% !important; background-color: #1eb1b1 !important; 
        border-radius: 8px !important; height: 4em !important; border: none !important;
    }
    div.stButton > button p { color: #ffffff !important; font-weight: 800 !important; }

    .stTextArea textarea { background-color: #ffffff !important; color: #103b4d !important; border-radius: 8px; }

    /* --- UPLOADER VISIBILITY FIX --- */
    [data-testid="stFileUploader"] {
        background-color: #f0f2f6 !important;
        padding: 15px !important;
        border-radius: 8px !important;
    }
    
    /* TARGETING THE LABEL TO BE BLACK */
    [data-testid="stFileUploader"] label p {
        color: #000000 !important; 
        font-weight: 700 !important;
    }

    [data-testid="stFileUploader"] button div {
        color: transparent !important;
        display: none !important;
    }
    [data-testid="stFileUploader"] button::after {
        content: "Browse Files";
        color: #31333f !important;
        font-weight: 400 !important;
    }
    [data-testid="stFileUploader"] * {
        color: #31333f !important;
        font-weight: 400 !important;
        text-shadow: none !important;
    }
    </style>
    """, unsafe_allow_html=True)

if 'history_cache' not in st.session_state:
    st.session_state.history_cache = {}

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
    # REVERTED PLACEHOLDER
    client_data = st.text_area("Paste Input:", height=300, placeholder="e.g., Hakim, 39, Perfectionist, Sleeps 7h but wakes twice...")
    
    uploaded_file = st.file_uploader("Upload Client Material (Scans, PDF, Images)", type=["pdf", "png", "jpg", "jpeg"])
    if uploaded_file is not None:
        st.success(f"Attached: {uploaded_file.name}")

    generate_btn = st.button("Generate Plan")

with col_right:
    st.markdown("### Decision Engine Output")
    output_placeholder = st.empty()
    
    if generate_btn:
        if client_data:
            input_hash = get_input_hash(client_data)
            if input_hash in st.session_state.history_cache:
                cached_result = st.session_state.history_cache[input_hash]
                output_placeholder.markdown(cached_result)
                st.session_state.result = cached_result
            else:
                with st.spinner("Analyzing..."):
                    try:
                        client = OpenAI(base_url="https://integrate.api.nvidia.com/v1", api_key=api_key)
                        system_message = f"IDENTITY: {hassan_identity}\nBRAIN LOGIC: {hassan_context}"
                        response = client.chat.completions.create(
                            model="meta/llama-3.1-70b-instruct", 
                            messages=[{"role": "system", "content": system_message}, {"role": "user", "content": client_data}],
                            temperature=0.0, top_p=0.01, seed=42, stream=True
                        )
                        full_response = ""
                        for chunk in response:
                            if chunk.choices[0].delta.content:
                                full_response += chunk.choices[0].delta.content
                                output_placeholder.markdown(full_response + "▌")
                        output_placeholder.markdown(full_response)
                        st.session_state.result = full_response
                        st.session_state.history_cache[input_hash] = full_response
                    except Exception as e:
                        st.error(f"Logic Error: {e}")

    if 'result' in st.session_state:
        output_placeholder.markdown(st.session_state.result)
        if st.button("Save to Brain"):
            append_to_brain(client_data, st.session_state.result)
            st.balloons()
        st.code(st.session_state.result, language="markdown")
    else:
        st.markdown('<div class="mission-navy-box">Success Shouldn\'t Come at The Cost of Health</div>', unsafe_allow_html=True)