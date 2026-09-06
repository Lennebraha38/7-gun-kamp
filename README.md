# 7-Gun-Kamp — Yapay Zeka Uygulama Geliştirme

Tablet üzerinden (Codespaces + Termux SSH) yürütülen, bir haftalık yoğun AI/LLM kampının çıktıları.

## İçerik

| Dosya | Konu | Ne Öğretiyor |
|-------|------|--------------|
| `chatbot.py` | Terminal AI chatbot | Gemini API, sohbet oturumu |
| `deney.py` | Temperature deneyi | LLM cevap çeşitliliği, çıktı kontrolü |
| `arac.py` | Function calling | Model'in dış fonksiyon çağırması (saat, toplama) |
| `vektor.py` | Embedding | Metni vektöre çevirme, kosinüs benzerliği |
| `vdb.py` | Vektör veritabanı | ChromaDB ile benzerlik araması |
| `parcala.py` | Chunking | Uzun metni parçalama stratejileri |
| `rag.py` | RAG pipeline | Retrieval + generation adımlarının birleşimi |
| `karsilastir.py` | Model karşılaştırma | Aynı soruda model/ayar farklarını ölçme |
| `ft_olustur.py` | Fine-tuning denemesi | Gemini tuning API, veri formatı |
| `agent.py` | AI Agent | Araç kararı + hafıza ile kendi kendine çalışan sistem |

## Kurulum

```bash
python -m pip install google-genai python-dotenv sentence-transformers chromadb pypdf
```

`.env` dosyasına API anahtarını ekle (AI Studio'dan alınır):

```
GEMINI_API_KEY=...
```

## Kullanım

```bash
# Temel chatbot
python chatbot.py

# Temperature farkını görmek için
python deney.py

# Fonksiyon çağıran asistan
python arac.py

# RAG: belgeden soru-cevap
python rag.py

# Araçlı + hafızalı agent
python agent.py
```

## Notlar

- Gemini ücretsiz katmanda **günde ~20 istek** kotası vardır (model başına). 429 hatası alırsan ertesi gün devam et.
- Model adı `gemini-3.6-flash` kullanılıyor; eski modeller zamanla kapatılıyor.
- `vdb/` klasörü vektörlerin diske kayıtlı hali olduğu için `.gitignore`'dadır.
- Kısa ömürlü `AQ...` anahtarlar sık sık 401 verir; kalıcı `AIza...` anahtarı tercih et.
