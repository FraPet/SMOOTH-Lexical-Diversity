import os
import csv
import re
import spacy
import config
from lexdiv_functions import calculate_wim
from lexical_diversity import lex_div as ld

# Prepare paths
dir_path = config.TXT_PATH
output_path = config.OUTPUT_PATH
os.makedirs(output_path, exist_ok=True)

# Load spaCy model depending on config
if config.LANGUAGE not in config.SPACY_MODELS:
    raise ValueError(f"Unsupported language: {config.LANGUAGE}. Use 'it' or 'en'.")
nlp = spacy.load(config.SPACY_MODELS[config.LANGUAGE])

# Collect input files (.cha or .txt)
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
            # Clean and tokenize
            line = re.sub(r"@\d+(\.\d+)?\.", "", line)
            tokens = [w.replace(".", "") for w in line.split() if "-" not in w and w != "xxx"]
            all_words.extend(tokens)

    # Lemmatize
    doc = nlp(" ".join(all_words))
    all_words = [token.lemma_ for token in doc if token.is_alpha]

    # Compute metrics
    ndw = len(set(all_words))
    text = " ".join(all_words)
    perc5_length = max(1, len(all_words) * 5 // 100)

    hdd = ld.hdd(text)
    mtld = ld.mtld(text)
    mattr = ld.mattr(text, window_length=15)
    mattr5perc = ld.mattr(text, window_length=perc5_length)
    ttr = ld.ttr(text)
    wim_result = calculate_wim(all_words)

    results.append({
        "id": file.split("_")[0],
        "tokens": len(all_words),
        "NDW": ndw,
        "ttr": ttr,
        "mattr": mattr,
        "mattr5perc": mattr5perc,
        "hdd": hdd,
        "mtld": mtld,
        "wim": wim_result
    })

# Save results
out_file = os.path.join(output_path, "lexical_diversity_results.csv")
with open(out_file, "w", newline="", encoding="utf-8") as f_out:
    writer = csv.DictWriter(f_out, fieldnames=["id", "tokens", "NDW", "ttr", "mattr", "mattr5perc", "hdd", "mtld", "wim"])
    writer.writeheader()
    writer.writerows(results)

print(f"Results saved in {out_file}")
