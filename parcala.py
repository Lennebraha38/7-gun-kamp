ORNEK = """Vektor veritabanlari, yapay zeka uygulamalarinda benzerlik aramasi yapmak icin kullanilir.
Metinler once embedding modeliyle sayisal vektorlere donusturulur.
Bu vektorler yuksek boyutlu bir uzayda anlam yakinligini temsil eder.

ChromaDB, gelistiriciler arasinda populer olan acik kaynakli bir vektor veritabanidir.
Belgeleri ve vektorlerini diskte saklar, soru geldiginde en yakin kayitlari dondurur.
Kullanim kolayligi nedeniyle prototiplerde sikca tercih edilir.

Chunking, uzun belgeleri kucuk parcalara bolme islemidir.
Cok buyuk parcalar aramada gurultu yaratir, cok kucuk parcalar baglami kaybeder.
Parcalar arasinda kisa bir ortusme birakmak cumle bolunmelerini azaltir.

RAG, retrieval ve generation adimlarini birlestirir.
Once ilgili parcalar bulunur, sonra dil modeline baglam olarak verilir.
Boylece model yalnizca egitim verisine degil guncel belgelere de dayanir.

Temperature degeri dusuk tutuldugunda model belgeden sapmadan cevap uretir.
Yuksek temperature yaratici yazimda ise yarar ama bilgi sorularinda risklidir.
Bu yuzden RAG sistemlerinde 0.0 ile 0.3 arasi degerler kullanilir."""

import os
if not os.path.exists("ornek.txt"):
    with open("ornek.txt", "w") as f:
        f.write(ORNEK)
    print("ornek.txt olusturuldu")

with open("ornek.txt") as f:
    metin = f.read()

def chunkla(metin, boyut=300, ortusme=50):
    chunks = []
    basla = 0
    while basla < len(metin):
        chunks.append(metin[basla:basla + boyut])
        basla += boyut - ortusme
    return chunks

chunks = chunkla(metin, boyut=800)
for i, c in enumerate(chunks):
    onizleme = c[:100].replace("\n", " ")
    print(f"--- chunk {i} ({len(c)} karakter) ---")
    print(onizleme + "...")
print(f"\ntoplam metin: {len(metin)} karakter -> {len(chunks)} chunk")
