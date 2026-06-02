import streamlit as st
import os
import datetime
import hashlib
import base64
from openai import OpenAI
from dotenv import load_dotenv

# 1. ENVIRONMENT & SYSTEMS INITIALIZATION
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

def process_image_to_text(uploaded_file):
    try:
        image_bytes = uploaded_file.getvalue()
        base64_image = base64.b64encode(image_bytes).decode('utf-8')
        client = OpenAI(base_url="https://integrate.api.nvidia.com/v1", api_key=api_key)
        response = client.chat.completions.create(
            model="nvidia/llama-3.2-11b-vision-instruct",
            messages=[{
                "role": "user",
                "content": [
                    {"type": "text", "text": "Extract all numbers and metrics from this health scan. Use format: Metric: Value. Output ONLY the data."},
                    {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"}}
                ]
            }],
            max_tokens=1024,
            temperature=0.0
        )
        return response.choices[0].message.content
    except Exception as e:
        return None

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

hassan_context = load_file("thrive_brain.txt")
hassan_identity = load_file("thrive_identity.txt")

# 2. GLOBAL ENTERPRISE STYLING SHEET
st.set_page_config(page_title="Thrive Hub Intelligence", page_icon="⚡", layout="wide")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@300;400;500;600;700;800&display=swap');
    
    html, body, [class*="st-"] { 
        font-family: 'Montserrat', sans-serif !important; 
    }
    .stApp { 
        background-color: #103b4d !important; 
        color: #FFFFFF !important; 
    }
    
    /* Layout Framework Restructure */
    .block-container {
        padding-top: 2rem !important;
        padding-bottom: 3rem !important;
        max-width: 1200px !important;
        margin: 0 auto !important;
    }
    
    .stMarkdown p, h1, h2, h3, h4, h5, h6 { 
        color: #FFFFFF !important; 
    }
    
    /* Segment Accents */
    .section-header {
        font-size: 1.35rem !important;
        font-weight: 700 !important;
        letter-spacing: -0.01em;
        color: #FFFFFF !important;
        margin-bottom: 20px !important;
        display: flex;
        align-items: center;
        gap: 10px;
    }
    .section-header::before {
        content: "";
        display: inline-block;
        width: 4px;
        height: 22px;
        background-color: #1eb1b1;
        border-radius: 2px;
    }

    /* Consolidated Top Row Banner Framework */
    .brand-top-banner {
        display: flex;
        align-items: center;
        gap: 16px;
        margin-top: 10px;
        margin-bottom: 20px;
        width: 100%;
    }
    .brand-logo-frame {
        height: 52px;
        width: auto;
        border-radius: 6px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.15);
    }
    .brand-tag-badge {
        background-color: #1eb1b1; 
        color: #ffffff !important;
        padding: 6px 16px; 
        border-radius: 6px;
        font-size: 0.85rem; 
        font-weight: 800;
        letter-spacing: 0.02em;
        text-transform: uppercase;
        white-space: nowrap;
    }

    /* Title Box Design */
    .main-title-box {
        background-color: #1eb1b1; 
        color: #ffffff !important;
        padding: 14px 36px; 
        border-radius: 8px;
        font-size: 2.1rem; 
        font-weight: 800; 
        display: inline-block; 
        text-align: center;
        letter-spacing: -0.02em;
    }

    /* Workspace Presentation Containers */
    .workspace-card {
        background-color: #0b2d3b !important;
        border: 1px solid rgba(255, 255, 255, 0.05);
        border-radius: 8px;
        padding: 24px;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.15);
        margin-bottom: 20px;
        min-height: 300px;
    }
    
    /* Input Elements Overrides */
    .stTextArea textarea { 
        background-color: rgba(255, 255, 255, 0.03) !important; 
        color: #FFFFFF !important; 
        border-radius: 6px !important; 
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        font-size: 1rem !important;
        padding: 14px !important;
        line-height: 1.5 !important;
    }
    .stTextArea textarea:focus {
        border-color: #1eb1b1 !important;
        box-shadow: 0 0 0 1px #1eb1b1 !important;
    }

    /* Standard Button Structuring */
    div.stButton > button { 
        width: 100% !important; 
        background-color: #1eb1b1 !important; 
        border-radius: 6px !important; 
        height: 3.8em !important; 
        border: none !important;
        transition: all 0.15s ease !important;
    }
    div.stButton > button:hover {
        background-color: #22c4c4 !important;
        box-shadow: 0 4px 12px rgba(30, 177, 177, 0.2) !important;
    }
    div.stButton > button p { 
        color: #ffffff !important; 
        font-weight: 800 !important; 
        font-size: 1.05rem !important;
    }

    /* File Uploader Formatting */
    [data-testid="stFileUploader"] { 
        background-color: #f0f2f6 !important; 
        padding: 12px !important; 
        border-radius: 6px !important; 
    }
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
    
    .status-banner { 
        background-color: #0b2d3b; 
        color: #ffffff !important; 
        padding: 12px 24px; 
        border-radius: 6px; 
        font-weight: 800; 
        display: inline-block; 
        font-size: 1.05rem;
        border: 1px solid rgba(30, 177, 177, 0.25);
        margin-top: 20px;
    }
    </style>
    """, unsafe_allow_html=True)

if 'history_cache' not in st.session_state:
    st.session_state.history_cache = {}

# 3. FIXED UNIFIED BRAND BANNER STRIP
if os.path.exists("Logo.png"):
    with open("Logo.png", "rb") as image_file:
        encoded_logo = base64.b64encode(image_file.read()).decode()
    
    st.markdown(f"""
        <div class="brand-top-banner">
            <img class="brand-logo-frame" src="data:image/png;base64,{encoded_logo}">
            <div class="brand-tag-badge">Plan Builder</div>
        </div>
    """, unsafe_allow_html=True)
else:
    st.markdown("""
        <div class="brand-top-banner">
            <div class="brand-tag-badge">Plan Builder</div>
        </div>
    """, unsafe_allow_html=True)

st.markdown('<div style="text-align: center; margin-top: 5px; margin-bottom: 25px;"><div class="main-title-box">Thrive Hub Intelligence</div></div>', unsafe_allow_html=True)
st.divider()

# 4. BALANCED WORKSPACE GRID
col_left, col_right = st.columns([1, 1], gap="large")

with col_left:
    st.markdown('<div class="section-header">Input Data</div>', unsafe_allow_html=True)
    
    client_data = st.text_area(
        "Paste Input:", 
        height=300, 
        label_visibility="collapsed",
        placeholder="e.g., Hakim, 39, Perfectionist, Sleeps 7h but wakes twice..."
    )
    
    st.markdown("<div style='margin-top: 20px;'></div>", unsafe_allow_html=True)
    uploaded_file = st.file_uploader(
        "Upload Client Material (Scans, PDF, Images)", 
        type=["png", "jpg", "jpeg"]
    )
    if uploaded_file is not None:
        st.success(f"Attached: {uploaded_file.name}")

    st.markdown("<div style='margin-top: 20px;'></div>", unsafe_allow_html=True)
    generate_btn = st.button("Generate Plan")

with col_right:
    st.markdown('<div class="section-header">Decision Engine Output</div>', unsafe_allow_html=True)
    
    st.markdown('<div class="workspace-card">', unsafe_allow_html=True)
    output_placeholder = st.empty()
    
    if generate_btn:
        if client_data:
            extracted_evidence = ""
            vision_failed = False
            
            if uploaded_file:
                with st.spinner("Vision Agent Reading Material..."):
                    extracted_evidence = process_image_to_text(uploaded_file)
                    if extracted_evidence is None:
                        vision_failed = True
            
            if vision_failed:
                st.error("SYSTEM BLOCKED: Vision endpoint timeout. Verify parameters or use text inputs directly.")
            else:
                final_input = f"USER REQUEST & CLIENT DOSSIER:\n{client_data}\n\nDATA EXTRAPOLATED FROM SCAN OVERHEAD:\n{extracted_evidence}"
                input_hash = get_input_hash(final_input)
                
                if input_hash in st.session_state.history_cache:
                    cached_result = st.session_state.history_cache[input_hash]
                    output_placeholder.markdown(cached_result)
                    st.session_state.result = cached_result
                else:
                    with st.spinner("Processing framework..."):
                        try:
                            client = OpenAI(base_url="https://integrate.api.nvidia.com/v1", api_key=api_key)
                            
                            system_message = (
                                f"IDENTITY:\n{hassan_identity}\n\n"
                                f"BRAIN LOGIC RULES:\n{hassan_context}\n\n"
                                f"CRITICAL INSTRUCTION: You are a deeply analytical Human Performance Architect. "
                                f"CRITICAL RESTRICTION: You are completely forbidden from writing traditional gym splits (e.g., Upper/Lower body, Chest/Triceps, Monday/Wednesday/Friday schedules). Do not calculate calories or write numbers for meals. Instead, focus entirely on systemic health foundations.\n\n"
                                f"You MUST structure your entire response using the exact layout below:\n\n"
                                f"### THRIVE HUB STRATEGIC AUDIT\n\n"
                                f"#### 1. CRITICAL THINKING & SYSTEM ANALYSIS\n"
                                f"- **Evidence Quality Assessment**: [Analyze data completeness based on guidelines]\n"
                                f"- **Systemic Mismatch & Uncertainties**: [Highlight contradictions, mental load vs recovery capacity]\n"
                                f"- **The Alternate Hypothesis**: [Strongest argument for and against why goals are blocked]\n"
                                f"- **Analytical Confidence Level**: [State exact %]\n\n"
                                f"#### 2. THE TRUE SYSTEMIC BOTTLENECK\n"
                                f"**Primary Bottleneck Identification**: [State the single true priority bottleneck according to the Decision Hierarchy sequence. Do not jump to nutrition or training templates if nervous system or sleep foundations are un-stabilized.]\n"
                                f"- *Why it Matters*: [System impact on physiological recovery]\n\n"
                                f"#### 3. THE RULE OF ONE INTERVENTION\n"
                                f"- **One Primary Action**: [Single high-leverage lifestyle change to stabilize the bottleneck]\n"
                                f"- **One Foundational Behavioral Rule**: [The psychological shift needed to secure consistency]\n\n"
                                f"#### 4. SUPPORTING NUTRITIONAL & MOVEMENT ARCHITECTURE\n"
                                f"- **Foundational Meal Architecture**: [Describe a sustainable, non-restrictive nutrition rhythm focused entirely on meal consistency, protein timing, and hydration. Talk about meal structure and habits qualitatively. Do not include calorie numbers, macro metrics, or precise tracking lists.]\n"
                                f"- **Foundational Movement Design**: [Provide a qualitative framework focusing purely on Functional Training, Functional Movement, Mobility, Resilience, or Primal Flows (e.g., Animal Flow mechanics, breathing coordination). Focus on supporting life and building nervous system resilience. Completely omit exercise list blocks, rep ranges, sets, or workout day schedules.]"
                            )
                            
                            response = client.chat.completions.create(
                                model="meta/llama-3.1-70b-instruct", 
                                messages=[
                                    {"role": "system", "content": system_message},
                                    {"role": "user", "content": final_input}
                                ],
                                temperature=0.0,
                                top_p=0.01,
                                seed=42,
                                stream=True
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
                            st.error(f"Processing Error: {e}")
        else:
            st.warning("Please populate background dossier details first.")

    if 'result' in st.session_state:
        output_placeholder.markdown(st.session_state.result)
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("Save to Brain"):
            if append_to_brain(client_data, st.session_state.result):
                st.balloons()
                st.success("Injected into Brain.")
        st.code(st.session_state.result, language="markdown")
    else:
        st.markdown('<div class="status-banner">Success Shouldn\'t Come at The Cost of Health</div>', unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)