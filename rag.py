import os, urllib.request, json
import chromadb
from sentence_transformers import SentenceTransformer
from dotenv import load_dotenv

load_dotenv()
key = os.getenv("GEMINI_API_KEY", "")

with open("ornek.txt") as f:
    metin = f.read()

def chunkla(metin, boyut=300, ortusme=50):
    chunks = []
    basla = 0
    while basla < len(metin):
        chunks.append(metin[basla:basla + boyut])
        basla += boyut - ortusme
    return chunks

chunks = chunkla(metin)
print(f"{len(chunks)} chunk olustu")

model = SentenceTransformer("all-MiniLM-L6-v2")
vektorler = model.encode(chunks).tolist()

client = chromadb.PersistentClient(path="./vdb")
col = client.get_or_create_collection("belgeler")
if col.count() == 0:
    col.add(ids=[f"d{i}" for i in range(len(chunks))],
            embeddings=vektorler, documents=chunks)

soru = "What is chunking and what should be considered?"
soru_vektor = model.encode(soru).tolist()
sonuc = col.query(query_embeddings=[soru_vektor], n_results=2)
baglam = "\n\n".join(sonuc["documents"][0])
print("--- bulunan parcalar (ilk 200 karakter) ---")
print(baglam[:200] + "...")

url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-3.6-flash:generateContent?key={key}"
govde = json.dumps({
    "system_instruction": {"parts": [{"text": "Yalnizca verilen baglama dayanarak cevap ver. Baglamda yoksa bilmiyorum de."}]},
    "contents": [{"parts": [{"text": f"Baglam:\n{baglam}\n\nSoru: {soru}"}]}],
    "generationConfig": {"temperature": 0.1, "maxOutputTokens": 300},
}).encode()
req = urllib.request.Request(url, data=govde, headers={"Content-Type": "application/json"})
cevap = json.loads(urllib.request.urlopen(req, timeout=30).read().decode())
print("\n--- model cevabi ---")
print(cevap["candidates"][0]["content"]["parts"][0]["text"])
