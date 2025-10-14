import os
import subprocess

LANGUAGES = ["it", "en"]
BASE_PATH = "data"

for lang in LANGUAGES:
    lang_path = os.path.join(BASE_PATH, lang)
    if not os.path.exists(lang_path):
        continue
    print(f"=== Elaborazione lingua: {lang} ===")
    # Esegue test.py con la lingua corrispondente
    subprocess.run(["python", "test.py", lang])
