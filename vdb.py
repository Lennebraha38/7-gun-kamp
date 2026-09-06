import chromadb
from sentence_transformers import SentenceTransformer

model = SentenceTransformer("all-MiniLM-L6-v2")

cumleler = [
    "The cat is sleeping in the garden.",
    "The dog is running in the park.",
    "Artificial intelligence is evolving fast.",
]
vektorler = model.encode(cumleler).tolist()

client = chromadb.PersistentClient(path="./vdb")
col = client.get_or_create_collection("cumleler")

if col.count() == 0:
    col.add(ids=["c1", "c2", "c3"], embeddings=vektorler, documents=cumleler)
    print("kaydedildi:", col.count(), "belge")

soru = model.encode("What are pets doing?").tolist()
sonuc = col.query(query_embeddings=[soru], n_results=2)

print("--- en yakin 2 sonuc (mesafe: kucuk = yakin) ---")
for doc, dist in zip(sonuc["documents"][0], sonuc["distances"][0]):
    print(f"{dist:.3f}  {doc}")
