import os, urllib.request, json, time
from dotenv import load_dotenv

load_dotenv()
key = os.getenv("GEMINI_API_KEY", "")

soru = "Vektor veritabanlari neden onemlidir?"
baglam = """Vektor veritabanlari, yapay zeka uygulamalarinda benzerlik aramasi yapmak icin kullanilir.
Metinler once embedding modeliyle sayisal vektorlere donusturulur.
Bu vektorler yuksek boyutlu bir uzayda anlam yakinligini temsil eder.
ChromaDB, gelistiriciler arasinda populer olan acik kaynakli bir vektor veritabanidir."""

models = [
    ("gemini-3.6-flash", 0.1),
    ("gemini-3.6-flash", 1.5),
    ("gemini-2.5-flash", 0.1),
    ("gemini-3.6-flash", 0.7),
]

for model, temp in models:
    print(f"\n{'='*60}")
    print(f"MODEL: {model} | temperature: {temp}")
    print(f"{'='*60}")

    url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={key}"
    govde = json.dumps({
        "system_instruction": {"parts": [{"text": "Baglama dayanarak kisa ve net cevap ver."}]},
        "contents": [{"parts": [{"text": f"Baglam:\n{baglam}\n\nSoru: {soru}"}]}],
        "generationConfig": {"temperature": temp, "maxOutputTokens": 300, "thinkingConfig": {"thinkingBudget": 64}},
    }).encode()
    req = urllib.request.Request(url, data=govde, headers={"Content-Type": "application/json"})

    basla = time.time()
    try:
        data = json.loads(urllib.request.urlopen(req, timeout=120).read().decode())
        sure = round(time.time() - basla, 2)
        cevap = data["candidates"][0]["content"]["parts"][0]["text"]
        token = data.get("usageMetadata", {}).get("totalTokenCount", "?")
        print(f"SURE: {sure}s | TOKEN: {token}")
        print(f"CEVAP: {cevap}")
    except Exception as e:
        print(f"HATA: {str(e)[:200]}")
