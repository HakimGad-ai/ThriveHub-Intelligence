import os
from openai import OpenAI
from dotenv import load_dotenv

# 1. Load environment
print("Checking environment...")
load_dotenv()
api_key = os.getenv("NVIDIA_API_KEY")

if not api_key:
    print("ERROR: NVIDIA_API_KEY not found in .env file!")
else:
    print("API Key found. Initializing client...")

client = OpenAI(
    base_url="https://integrate.api.nvidia.com/v1",
    api_key=api_key
)

def thrive_router(user_input):
    print(f"Analyzing inquiry: '{user_input}'")
    
    # Load Identity
    if not os.path.exists('thrive_identity.txt'):
        return "ERROR: thrive_identity.txt file is missing!"
    
    with open('thrive_identity.txt', 'r') as f:
        identity = f.read()

    prompt = f"""
    {identity}
    
    TASK: Analyze the following client struggle and route them to the CORRECT Thrive Hub service.
    SERVICES:
    - Thrive Nutrition Reset (Metabolic health & energy management) [cite: 372]
    - Restore & Rebuild (Injury recovery & musculoskeletal health) [cite: 374]
    - The Hybrid Beast (Advanced conditioning & resilience) [cite: 376]
    - Thrive @ Work (Executive coaching & workplace health) [cite: 383, 389]

    OUTPUT: Provide the Service Name, the Lead Specialist (e.g., Hassan, Dr. Kadry), and a short 'Thrive-style' response.
    """

    print("Connecting to NVIDIA NIM...")
    try:
        response = client.chat.completions.create(
            model="meta/llama-3.1-405b-instruct",
            messages=[
                {"role": "system", "content": prompt},
                {"role": "user", "content": user_input}
            ],
            temperature=0.2
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"API ERROR: {str(e)}"

# TEST EXECUTION
inquiry = "I am a busy executive, I travel a lot, and my energy is crashing by 3 PM."
result = thrive_router(inquiry)
print("\n--- RESULTS ---")
print(result)