import os, urllib.request, json
from dotenv import load_dotenv

load_dotenv()
key = os.getenv("GEMINI_API_KEY", "")
model = "gemini-3.6-flash"
url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={key}"

soru = "Bana kisa bir motivasyon cumlesi yaz."

for temp in [0.0, 1.5]:
    print(f"--- temperature={temp} ---")
    body = json.dumps({
        "system_instruction": {"parts": [{"text": "Sen bir Turkce yasam kocusun."}]},
        "contents": [{"parts": [{"text": soru}]}],
        "generationConfig": {"temperature": temp, "maxOutputTokens": 200},
    }).encode()
    req = urllib.request.Request(url, data=body, headers={"Content-Type": "application/json"})
    try:
        data = json.loads(urllib.request.urlopen(req, timeout=30).read().decode())
        print(data["candidates"][0]["content"]["parts"][0]["text"])
    except Exception as e:
        print("HATA:", str(e)[:300])
    print()
