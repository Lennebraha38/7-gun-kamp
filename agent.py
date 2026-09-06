import os, json
from datetime import datetime, timezone, timedelta
from google import genai
from google.genai import types
from dotenv import load_dotenv

load_dotenv()
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

def saat_kac():
    """Guncel Turkiye saatini verir. Guncel saat soruldugunda kullan."""
    tr = timezone(timedelta(hours=3))
    return {"saat": datetime.now(tr).strftime("%H:%M")}

def gunaydin_iste():
    """Sabahlari kullaniciyi selamlar. Sadece selamlama istendiginde kullan."""
    return {"not": "Gunaydin!"}

MEM = {}

def hafizaya_yaz(anahtar: str, deger: str):
    """Kullanici verdigi bilgiyi hatirlar. 'Hatirla' denildiginde kullan."""
    MEM[anahtar] = deger
    return {"kaydedildi": anahtar}

def hafizadan_oku(anahtar: str):
    """Kaydedilmis bir bilgiyi getirir."""
    if anahtar in MEM:
        return {"deger": MEM[anahtar]}
    return {"hata": f"{anahtar} kayitli degil"}

print("=== AI Agent: araclar + hafiza (cikmak icin quit) ===")
print("Dene: 'saat kac?', 'Saat 13:30' diye hatirlat, 'saat 13:30 ne zaman dedim?'\n")

chat = client.chats.create(
    model="gemini-3.6-flash",
    config=types.GenerateContentConfig(
        tools=[saat_kac, gunaydin_iste, hafizaya_yaz, hafizadan_oku],
        temperature=0.2,
    ),
)

while True:
    kullanici = input("Sen: ")
    if kullanici.lower() in ["quit", "exit", "cik"]:
        break
    cevap = chat.send_message(kullanici)
    print("AI:", cevap.text)
    print()
