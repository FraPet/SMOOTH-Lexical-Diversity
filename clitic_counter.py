import os
import re
import csv
import spacy
import config

# Prepare paths
dir_path = config.TXT_PATH
output_path = config.OUTPUT_PATH
os.makedirs(output_path, exist_ok=True)

# Load spaCy model depending on config
if config.LANGUAGE not in config.SPACY_MODELS:
    raise ValueError(f"Unsupported language: {config.LANGUAGE}. Use 'it' or 'en'.")
nlp = spacy.load(config.SPACY_MODELS[config.LANGUAGE])

# Collect input files
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

            # NLP analysis
            doc = nlp(line)
            clitics = []
            for tok in doc:
                # print(f"Token: {tok.text} | POS: {tok.pos_} | Morph: {tok.morph}")
                if tok.pos_ == "PRON" and tok.morph.get("Clitic") == ["Yes"]:
                    print(f"\t[INFO] Found clitic:\t{tok.text} | [{tok.morph}] in file {file}")
                    clitics.append(tok.text)

    results.append({
        "id": file.split("_")[0],
        "total_tokens": len(all_words),
        "clitic_count": len(clitics),
        "clitics_found": ", ".join(clitics)
    })

# Save results
out_file = os.path.join(output_path, "clitic_results.csv")
with open(out_file, "w", newline="", encoding="utf-8") as f_out:
    writer = csv.DictWriter(f_out, fieldnames=["id", "total_tokens", "clitic_count", "clitics_found"])
    writer.writeheader()
    writer.writerows(results)

print(f"Results saved in {out_file}")
