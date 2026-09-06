import os
from google import genai
from google.genai import types
from dotenv import load_dotenv

load_dotenv()
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

print("== Tuning veri seti yukleniyor ==\n")

veri = [
    {"text_input": "Bugun hava nasil?", "output": "Bugun hava guzel ve gunesli."},
    {"text_input": "Yarin ne yapmaliyim?", "output": "Yarin planini yap, kitaplarini topla."},
]

dataset = types.TuningDataset(
    examples=[types.TuningExample(text_input=v["text_input"], output=v["output"]) for v in veri]
)

config = types.CreateTuningJobConfig(
    tuned_model_display_name="kamp-turkce-deneme-1",
    epoch_count=1,
    batch_size=1,
    learning_rate=0.001,
)

try:
    sonuc = client.tunings.tune(
        base_model="models/gemini-2.5-flash-8b",
        training_dataset=dataset,
        config=config,
    )
    print("Tuning job name:", sonuc.name)
    print("DURUM:", getattr(sonuc, "state", "?"))
except Exception as e:
    print("HATA:", str(e)[:600])
