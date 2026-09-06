import os, json, urllib.parse
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

def webde_ara(konu: str):
    """Tum interneti arar, en guncel ve ilgili ilk 5 sonucu doner. Guncel haber, urun, surum bilgisi soruldugunda kullan."""
    try:
        from ddgs import DDGS
        sonuclar = []
        with DDGS() as ddgs:
            for r in ddgs.text(konu, region="tr-tr", max_results=5):
                sonuclar.append({
                    "baslik": r.get("title", ""),
                    "url": r.get("href", ""),
                    "ozet": r.get("body", "")[:300],
                })
        return {"sonuclar": sonuclar}
    except ImportError:
        return {"hata": "ddgs paketi yok. Kur: python -m pip install ddgs"}
    except Exception as e:
        return {"hata": str(e)[:200]}

print("=== Web Arastirmaci Agent (cikmak icin quit) ===")
print("Dene: 'saat kac?', 'Claude en son surumu ara'")

chat = client.chats.create(
    model="gemini-3.6-flash",
    config=types.GenerateContentConfig(
        tools=[saat_kac, webde_ara],
        temperature=0.2,
    ),
)

while True:
    kullanici = input("\nSen: ")
    if kullanici.lower() in ["quit", "exit", "cik"]:
        break
    cevap = chat.send_message(kullanici)
    print("AI:", cevap.text)
