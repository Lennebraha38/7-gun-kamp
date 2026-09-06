import os
import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")
if not API_KEY:
    print("Hata: GEMINI_API_KEY bulunamadı!")
    exit()

URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-3.6-flash:generateContent?key={API_KEY}"

# Konuşma geçmişini tutacak liste
history = []

SYSTEM_INSTRUCTION = "Sen kısa, realist ve teknik konularda pratik yanıtlar veren bir asistansın."

headers = {
    "Content-Type": "application/json"
}

print("--- Gemini CLI Asistanı (Çıkmak için 'q' yazın) ---\n")

while True:
    user_input = input("Siz: ")
    if user_input.strip().lower() == 'q':
        print("Sohbet kapatıldı.")
        break
    
    if not user_input.strip():
        continue

    history.append({
        "role": "user",
        "parts": [{"text": user_input}]
    })

    payload = {
        "contents": history,
        "systemInstruction": {
            "parts": [{"text": SYSTEM_INSTRUCTION}]
        },
        "generationConfig": {
            "temperature": 0.7
        }
    }

    # Hatalı satır düzeltildi: headers ve json parametreleri ayrıldı
    response = requests.post(URL, headers=headers, json=payload)

    if response.status_code == 200:
        data = response.json()
        bot_reply = data["candidates"][0]["content"]["parts"][0]["text"]
        
        print(f"\nGemini: {bot_reply}\n")
        
        history.append({
            "role": "model",
            "parts": [{"text": bot_reply}]
        })
    else:
        print(f"\nHata! Code: {response.status_code}")
        print("Detay:", response.text)
