from sentence_transformers import SentenceTransformer, util

model = SentenceTransformer("all-MiniLM-L6-v2")

cumleler = [
         "The cat is sleeping in the garden.",
         "The dog is running in the park.",
         "Artificial intelligence is evolving fast.",
]

vektorler = model.encode(cumleler)
print("vektor boyutu:", vektorler.shape)
print()

soru = model.encode("What are pets doing?")
skorlar = util.cos_sim(soru, vektorler)[0]

for cumle, skor in sorted(zip(cumleler, skorlar), key=lambda x: x[1], reverse=True):
    print(f"{float(skor):.3f}  {cumle}")
