import os, json
from datetime import datetime, timezone, timedelta
from groq import Groq
from dotenv import load_dotenv

load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))
MODEL = "llama-3.3-70b-versatile"

def web_ara(konu):
    try:
        from ddgs import DDGS
        sonuclar = []
        with DDGS() as ddgs:
            for r in ddgs.text(konu, region="tr-tr", max_results=5):
                sonuclar.append({"baslik": r.get("title", ""), "url": r.get("href", ""), "ozet": r.get("body", "")[:250]})
        return {"sonuclar": sonuclar}
    except Exception as e:
        return {"hata": str(e)[:150]}

def saat_kac():
    tr = timezone(timedelta(hours=3))
    return {"saat": datetime.now(tr).strftime("%H:%M")}

ARACLAR = {"saat_kac": saat_kac, "webde_ara": web_ara}

TOOLS = [
    {"type": "function", "function": {
        "name": "saat_kac",
        "description": "Guncel Turkiye saatini verir. Guncel saat soruldugunda kullan.",
        "parameters": {"type": "object", "properties": {}}}},
    {"type": "function", "function": {
        "name": "webde_ara",
        "description": "Tum interneti arar, en ilgili 5 sonucu doner. Guncel bilgi, haber, urun, surum soruldugunda kullan.",
        "parameters": {"type": "object", "properties": {"konu": {"type": "string"}}, "required": ["konu"]}}},
]

print("=== Groq Agent (cikmak icin quit) ===")
print("Dene: 'saat kac?', 'Claude en son surumu ara'")

mesajlar = [{"role": "system", "content": "Sen bilgiye ulasan bir asistansin. Arac sonuclarini kullanarak kisa ve dogru cevap ver."}]

while True:
    kullanici = input("\nSen: ")
    if kullanici.lower() in ["quit", "exit", "cik"]:
        break
    mesajlar.append({"role": "user", "content": kullanici})

    for _ in range(5):
        yanit = client.chat.completions.create(
            model=MODEL, messages=mesajlar, tools=TOOLS, tool_choice="auto", temperature=0.2)
        secim = yanit.choices[0].message

        if secim.tool_calls:
            for tc in secim.tool_calls:
                ad = tc.function.name
                arg = json.loads(tc.function.arguments or "{}")
                print(f"  [arac calisti: {ad} {arg}]")
                sonuc = ARACLAR[ad](**arg)
                mesajlar.append({"role": "assistant", "content": None, "tool_calls": [tc.model_dump()]})
                mesajlar.append({"role": "tool", "tool_call_id": tc.id, "content": json.dumps(sonuc, ensure_ascii=False)})
        else:
            mesajlar.append({"role": "assistant", "content": secim.content})
            print("AI:", secim.content)
            break
