import streamlit as st
import os
from openai import OpenAI
from dotenv import load_dotenv

# 1. LOAD THE BRAIN & ENVIRONMENT
load_dotenv() 
# On Streamlit Cloud, it looks in 'Secrets'. Locally, it looks in .env
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
    @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@400;700&display=swap');
    html, body, [class*="st-"] { font-family: 'Montserrat', sans-serif; }
    
    /* Brand Palette: Navy & Teal */
    .stApp { background-color: #103b4d; color: #FFFFFF; }
    
    /* Visibility Fixes */
    .stWidgetLabel, label, p, .stMarkdown, [data-testid="stMarkdownContainer"] { 
        color: #FFFFFF !important; 
    }
    div[data-baseweb="slider"] div { color: #FFFFFF !important; }
    
    .stTextArea textarea { 
        background-color: #ffffff !important; 
        color: #103b4d !important; 
        border-radius: 8px; 
    }
    
    /* Thrive Hub Action Button */
    .stButton>button {
        width: 100%; border-radius: 4px; height: 3.5em;
        background-color: #1eb1b1; color: #ffffff; font-weight: 700;
        border: none; text-transform: uppercase; letter-spacing: 1px;
        transition: 0.3s;
    }
    .stButton>button:hover { background-color: #179393; color: #ffffff; border: none; }
    
    h1, h2, h3 { color: #ffffff !important; text-transform: uppercase; font-weight: 700; }
    hr { border-top: 1px solid #1eb1b1; }
    </style>
    """, unsafe_allow_html=True)

# 3. HEADER
st.title("⚡ THRIVE HUB INTELLIGENCE")
st.subheader("Module: Plan Builder")
st.divider()

# 4. INTERFACE
col_left, col_right = st.columns([1, 1.2], gap="large")

with col_left:
    st.markdown("### 🛠 Protocol Parameters")
    stress_level = st.select_slider("Client Stress Level", options=["Low", "Moderate", "High", "Critical"], value="Moderate")
    egypt_reality = st.toggle("Apply 'Egypt Reality' Logic", value=True)
    st.markdown("---")
    st.markdown("### 📝 Input Data")
    client_data = st.text_area(label="Paste Chat History or Assessment Data:", height=350, placeholder="e.g., Male, 39, Corporate role...")

with col_right:
    st.markdown("### 🚀 Generated Hassan-Style Plan")
    if st.button("Generate Plan"):
        if not client_data:
            st.warning("Please enter client data first.")
        elif not api_key:
            st.error("❌ API Key not found. Please add NVIDIA_API_KEY to Streamlit Secrets.")
        else:
            with st.spinner("Hassan is thinking..."):
                try:
                    # FIX: Removed the backslashes that caused the syntax error
                    client = OpenAI(base_url="https://integrate.api.nvidia.com/v1", api_key=api_key)
                    
                    prompt = f"""
                    You are Hassan, founder of Thrive Hub. Use the FOUNDATIONAL BRAIN:
                    {hassan_context}

                    INPUT:
                    - Stress Level: {stress_level}
                    - Egypt Reality: {egypt_reality}
                    - Client Info: {client_data}

                    TASK:
                    Generate an 'Executive Plan' following Rule 4 (Priority) and Rule 5 (Logic).
                    Tone: Sharp, direct, no fluff (Rule 7).
                    Include Egyptian Arabic Summary (Rule 8).
                    """
                    
                    response = client.chat.completions.create(
                        model="meta/llama-3.1-405b-instruct",
                        messages=[
                            {"role": "system", "content": "You are Hassan. Direct, premium coaching mindset."},
                            {"role": "user", "content": prompt}
                        ]
                    )
                    
                    result = response.choices[0].message.content
                    st.markdown(result)
                    st.divider()
                    st.code(result, language="markdown")
                except Exception as e:
                    st.error(f"Error: {e}")