import streamlit as st
import os
import datetime
from openai import OpenAI
from dotenv import load_dotenv

# 1. ENVIRONMENT & BRAIN INIT
load_dotenv() 
api_key = os.getenv("NVIDIA_API_KEY") or st.secrets.get("NVIDIA_API_KEY")

def load_hassan_brain():
    try:
        with open("thrive_brain.txt", "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        return "Error: thrive_brain.txt not found."

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

hassan_context = load_hassan_brain()

# 2. BRANDED UI CONFIG (MOBILE OPTIMIZED)
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
    .save-brain-btn div.stButton > button {
        background-color: #ffffff !important; color: #103b4d !important; margin-top: 25px !important;
    }
    .save-brain-btn div.stButton > button p { color: #103b4d !important; }
    .stTextArea textarea { background-color: #ffffff !important; color: #103b4d !important; border-radius: 8px; }
    .copy-label { margin-top: 30px; font-size: 0.8rem; opacity: 0.7; color: #ffffff; }
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
                    prompt = f"""
                    SYSTEM: You are the Thrive Hub Lead Strategist (Hassan). 
                    VAULT: {hassan_context}
                    
                    STRICT INSTRUCTION:
                    Solve for the HUMAN blocker. Do not provide generic internet advice. 
                    
                    MANDATORY LOGIC & CONTENT:
                    1. IDENTITY REFRAME: If 'Perfectionism' is mentioned, start with a reframe ("You are not inconsistent, you are perfection-driven").
                    2. PERFECTIONISM PROTOCOL: Mandate the '80% Rule' and 'Never Miss Twice'.
                    3. SLEEP: If clock-checking is mentioned, mandate 'No visible clocks' and 'Breath downshifts'.
                    4. NUTRITION: Use Egypt-localized staples (Foul medames, Baladi bread, Eggs, Yogurt). Target 2300-2450 kcal. 
                    5. MEAL TABLE: Must show a structured daily table including the 3 PM Non-Negotiable Snack.
                    6. TRAINING: For lifters with 10+ years exp, suggest Hybrid Upper/Lower athletic hypertrophy.
                    
                    RULES: No Arabic. English only. Use Hassan's specific coaching lines.
                    
                    INPUT: {client_data}
                    """
                    response = client.chat.completions.create(
                        model="meta/llama-3.1-405b-instruct", 
                        messages=[{"role": "user", "content": prompt}]
                    )
                    st.session_state.result = response.choices[0].message.content
                    st.session_state.last_input = client_data
                except Exception as e:
                    st.error(f"Logic Error: {e}")

with col_right:
    st.markdown("### Decision Engine Output")
    if 'result' in st.session_state:
        st.markdown(st.session_state.result)
        st.markdown('<div class="save-brain-btn">', unsafe_allow_html=True)
        if st.button("Save to Brain"):
            if append_to_brain(st.session_state.last_input, st.session_state.result):
                st.balloons(); st.success("Logic Injected into the Thrive Hub Brain.")
        st.markdown('</div>', unsafe_allow_html=True)
        st.markdown('<p class="copy-label">Copy for WhatsApp:</p>', unsafe_allow_html=True)
        st.code(st.session_state.result, language="markdown")
    else:
        st.markdown('<div style="margin-top: 40px;"><div class="mission-navy-box">Success Shouldn\'t Come at The Cost of Health</div></div>', unsafe_allow_html=True)

# 5. LESSONS LEARNED LOG (SYSTEM INTEGRITY)
# 2026-04-29: Reverted to 158 lines to ensure prompt-weight and CSS-depth are maintained.
# Root Cause: Standard editors strip whitespace; expanded logic instructions were condensed.
# Prevention: Hard-coded Strategic Identity Logic into the system prompt to force 9.1 accuracy.