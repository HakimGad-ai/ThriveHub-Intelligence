import os
from openai import OpenAI
from dotenv import load_dotenv

# Initialize Environment
load_dotenv()
client = OpenAI(
    base_url="https://integrate.api.nvidia.com/v1",
    api_key=os.getenv("NVIDIA_API_KEY")
)

def get_thrive_response(task_type, user_input):
    # Load the Brand Soul
    if not os.path.exists('thrive_identity.txt'):
        return "ERROR: thrive_identity.txt not found!"
    
    with open('thrive_identity.txt', 'r') as f:
        identity = f.read()
    
    # Task Logic Configuration
    if task_type == "1":
        task_desc = "Analyze this inquiry and route to: Nutrition Reset, Restore & Rebuild, Hybrid Beast, or Thrive @ Work."
    elif task_type == "2":
        task_desc = """
        Apply the Thrive Objection Formula: 
        1. Validate (Short empathy). 
        2. Reframe (Link to Performance/Metabolic Rhythm). 
        3. Simplify (Basic Proteins/Meal Repetition). 
        4. Action (One 5-minute task). 
        STRICT: No clichés like 'break the bank'. Keep it sharp and executive.
        """
    elif task_type == "3":
        task_desc = "Generate a Thrive-style WhatsApp broadcast or LinkedIn post. Focus on practical wins and sustainability."
    else:
        return "Invalid selection."

    # API Call
    response = client.chat.completions.create(
        model="meta/llama-3.1-70b-instruct",
        messages=[
            {"role": "system", "content": f"{identity}\n\nTASK: {task_desc}"},
            {"role": "user", "content": user_input}
        ],
        temperature=0.3
    )
    return response.choices[0].message.content

def main():
    print("\n" + "="*40)
    print("   THRIVE HUB INTELLIGENCE ENGINE v1.0")
    print("="*40)
    print("1. [Router] Route a New Lead")
    print("2. [Reframer] Handle a Client Objection")
    print("3. [Content] Generate Branded Content")
    print("q. Quit")
    
    choice = input("\nSelect an option (1-3): ")
    if choice.lower() == 'q': 
        print("Closing Engine...")
        return

    user_text = input("\nEnter the client message or topic: ")
    print("\n" + "-"*20 + " PROCESSING " + "-"*20)
    
    try:
        result = get_thrive_response(choice, user_text)
        print(f"\n{result}")
    except Exception as e:
        print(f"\nAn error occurred: {e}")
    
    # This keeps the app running so you don't have to restart it
    main()

if __name__ == "__main__":
    main()