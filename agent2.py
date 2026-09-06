import os, json, urllib.parse, urllib.request
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
    """Webi arastirir, konu hakkinda ozet bilgi getirir. Guncel veya genel bilgi soruldugunda kullan."""
    try:
        url = ("https://tr.wikipedia.org/w/api.php?action=query&list=search"
               "&srlimit=3&format=json&utf8=1&srsearch=" + urllib.parse.quote(konu))
        req = urllib.request.Request(url, headers={"User-Agent": "kamp-agent/1.0"})
        data = json.loads(urllib.request.urlopen(req, timeout=20).read().decode())
        sonuclar = []
        for s in data["query"]["search"]:
            sonuclar.append(s["title"] + ": " + s["snippet"].replace("<span class=\"searchmatch\">", "").replace("</span>", ""))
        return {"basliklar": sonuclar[:3]}
    except Exception as e:
        return {"hata": str(e)[:150]}

print("=== Web Arastirmaci Agent (cikmak icin quit) ===")
print("Dene: 'saat kac?', 'Gemini nedir arastir', 'Tomatoes kac kalori arastir'")

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
