import os
from datetime import datetime, timezone, timedelta
from google import genai
from google.genai import types
from dotenv import load_dotenv

load_dotenv()
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

def saat_kac():
    """Su anki Turkiye saatini verir. Guncel saat soruldugunda kullan."""
    tr = timezone(timedelta(hours=3))
    return {"saat": datetime.now(tr).strftime("%H:%M")}

def topla(a: float, b: float):
         """Iki sayiyi toplar."""
         return {"sonuc": a + b}
print("=== Aracli Asistan (cikmak icin quit) ===")

chat = client.chats.create(
    model="gemini-3.6-flash",
    config=types.GenerateContentConfig(tools=[saat_kac, topla]),
)

while True:
    user_input = input("Sen: ")
    if user_input.lower() in ["quit", "exit", "cik"]:
        break
    resp = chat.send_message(user_input)
    print("AI:", resp.text)
