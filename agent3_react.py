import os, json
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
client = OpenAI(
    api_key=os.getenv("GEMINI_API_KEY"),
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
)
MODEL = "gemini-3.6-flash"

def web_ara(konu):
    try:
        from ddgs import DDGS
        sonuclar = []
        with DDGS() as ddgs:
            for r in ddgs.text(konu, region="tr-tr", max_results=5):
                sonuclar.append({"baslik": r.get("title",""), "url": r.get("href",""), "ozet": r.get("body","")[:200]})
        return {"sonuclar": sonuclar}
    except Exception as e:
        return {"hata": str(e)[:150]}

ARACLAR = {"webde_ara": web_ara}

TOOLS = [
    {"type": "function", "function": {
        "name": "webde_ara",
        "description": "Tum interneti arar, ilgili 5 sonucu doner. Mutlaka arama yapip sonucu kullan.",
        "parameters": {"type": "object", "properties": {"konu": {"type": "string"}}, "required": ["konu"]}}},
]

print("=== ReAct Agent (tool izi gorunur, cikmak icin quit) ===")

mesajlar = [{"role": "system", "content": "Sen webde arastirma yapan asistansin. Soruya cevap vermeden ONCE webde_ara aracini cagir, buldugun sonuclari kullan. Arac sonucu yoksa cevap verme."}]

while True:
    kullanici = input("\nSen: ")
    if kullanici.lower() in ["quit", "exit", "cik"]:
        break
    mesajlar.append({"role": "user", "content": kullanici})

    for tur in range(5):
        yanit = client.chat.completions.create(model=MODEL, messages=mesajlar, tools=TOOLS, temperature=0.1)
        secim = yanit.choices[0].message
        if getattr(secim, "tool_calls", None):
            for tc in secim.tool_calls:
                ad = tc.function.name
                arg = json.loads(tc.function.arguments or "{}")
                print(f"  >>> [arac: {ad} {arg}]")
                sonuc = ARACLAR[ad](**arg)
                print(f"  <<< {json.dumps(sonuc, ensure_ascii=False)[:120]}...")
                mesajlar.append({"role": "assistant", "content": None, "tool_calls": [tc.model_dump()]})
                mesajlar.append({"role": "tool", "tool_call_id": tc.id, "content": json.dumps(sonuc, ensure_ascii=False)})
        else:
            print("AI:", secim.content)
            break
