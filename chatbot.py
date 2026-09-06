import os
from google import genai
from dotenv import load_dotenv

load_dotenv()
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

print("=== AI Chatbot ===")

chat = client.chats.create(model="gemini-3.6-flash")

while True:
    user_input = input("Sen: ")
    if user_input.lower() in ["quit", "exit", "cik"]:
        break
    response = chat.send_message(user_input)
    print("AI:", response.text)
