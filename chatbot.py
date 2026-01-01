import os
from dotenv import load_dotenv
import google.generativeai as genai

# Load environment variables
load_dotenv()

# Initialize Gemini API key
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# System prompt for the chatbot
system_prompt = "You are a friendly cybersecurity teacher bot. Guide users on processes and requirements in cybersecurity. Be helpful, patient, and encouraging. Explain concepts clearly and provide examples when possible."

# Initialize the model with system instruction
model = genai.GenerativeModel('gemini-1.5-flash', system_instruction=system_prompt)

# Start a chat session
chat = model.start_chat(history=[])

def chat_bot():
    print("Welcome to the Cybersecurity Teacher Bot! Type 'exit' to quit.")
    while True:
        user_input = input("You: ")
        if user_input.lower() == 'exit':
            print("Goodbye!")
            break

        # Send message to Gemini and get response
        response = chat.send_message(user_input)

        # Print the response
        print(f"Bot: {response.text}")

if __name__ == "__main__":
    chat_bot()
