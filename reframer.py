import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
client = OpenAI(
    base_url="https://integrate.api.nvidia.com/v1",
    api_key=os.getenv("NVIDIA_API_KEY")
)

def thrive_reframer(objection):
    with open('thrive_identity.txt', 'r') as f:
        identity = f.read()

    prompt = f"""
    {identity}
    
    TASK: Use the 'Thrive Hub Objection Response Formula' to handle a client concern.
    FORMULA:
    1. Validate the concern (show empathy).
    2. Reframe the issue (change their perspective).
    3. Simplify the solution (make it feel easy).
    4. Give ONE immediate action step.

    STRICT RULES:
    - No clinical language.
    - Keep it supportive but realistic.
    - Max 3-4 sentences.
    """

    response = client.chat.completions.create(
        model="meta/llama-3.1-405b-instruct",
        messages=[
            {"role": "system", "content": prompt},
            {"role": "user", "content": f"Client Objection: {objection}"}
        ],
        temperature=0.4 # Slightly higher for a bit more 'human' warmth
    )
    return response.choices[0].message.content

# TEST IT
client_doubt = "Healthy food is just too expensive and I don't have time to cook."
print("\n--- OBJECTION REFRAMED ---")
print(thrive_reframer(client_doubt))