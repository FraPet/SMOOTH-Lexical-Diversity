import os
import csv
import re
import spacy
import config
from lexdiv_functions import calculate_wim
from lexical_diversity import lex_div as ld

dir_path = config.TXT_PATH
output_path = config.OUTPUT_PATH
os.makedirs(output_path, exist_ok=True)

if config.LANGUAGE not in config.SPACY_MODELS:
    raise ValueError(f"Unsupported language: {config.LANGUAGE}. Use 'it' or 'en'.")
nlp = spacy.load(config.SPACY_MODELS[config.LANGUAGE])

input_files = [t for t in os.listdir(dir_path) if t.endswith(".cha") or t.endswith(".txt")]
print("Files found:", input_files)

results = []

for file in input_files:
    print(f"Processing file: {file}")
    file_path = os.path.join(dir_path, file)

    all_words = []
    with open(file_path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("@"):
                continue
            if line.startswith("*CHI:"):
                line = line.split("\t")[-1]
            line = re.sub(r"@\d+(\.\d+)?\.", "", line)
            tokens = [w.replace(".", "") for w in line.split() if "-" not in w and w != "xxx"]
            all_words.extend(tokens)

    doc = nlp(" ".join(all_words))
    all_words = [token.lemma_ for token in doc if token.is_alpha]

    ndw = len(set(all_words))
    perc5_length = max(1, len(all_words) * 5 // 100)

    results.append({
        "id": file.split("_")[0],
        "tokens": len(all_words),
        "NDW": ndw,
        "ttr": ld.ttr(all_words),
        "mattr": ld.mattr(all_words, window_length=15),
        "mattr5perc": ld.mattr(all_words, window_length=perc5_length),
        "hdd": ld.hdd(all_words),
        "mtld": ld.mtld(all_words),
        "wim": calculate_wim(all_words)
    })

out_file = os.path.join(output_path, "lexical_diversity_results.csv")
with open(out_file, "w", newline="", encoding="utf-8") as f_out:
    writer = csv.DictWriter(f_out, fieldnames=["id", "tokens", "NDW", "ttr", "mattr", "mattr5perc", "hdd", "mtld", "wim"])
    writer.writeheader()
    writer.writerows(results)

print(f"Results saved in {out_file}")
