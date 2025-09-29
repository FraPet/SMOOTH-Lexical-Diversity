import os
import csv
import re
import spacy
import config
from lexical_diversity import lex_div as ld
from lexdiv_functions import calculate_wim 

# Labels to be considered as content words
if config.LANGUAGE == "it":
    CONTENT_LABELS = ["NOME", "VERBO", "AGG", "AVV"]
else:
    CONTENT_LABELS = ["NOUN", "VERB", "ADJ", "ADV"]


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

# For demonstration purposes only -en or -it ending files are processed. comment out this section for elaborate entire data folder
lang_suffix = f"-{config.LANGUAGE}.txt"
input_files = [
    t for t in os.listdir(dir_path)
    if (t.endswith(lang_suffix) or t.endswith(f"-{config.LANGUAGE}.cha"))
]
print("Files found:", input_files)
# print("Files found:", input_files)


results = []

for file in input_files:
    print(f"Processing file: {file}")
    file_path = os.path.join(dir_path, file)

    content_words = []
    with open(file_path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("@"):
                continue
            if line.startswith("*CHI:"):
                line = line.split("\t")[-1]
            # Clean
            line = re.sub(r"@\d+(\.\d+)?\.", "", line)
            words = [w for w in line.split() if "/" in w and "-" not in w and w != "xxx"]

            for word in words:
                word_text, word_labels = word.split("/")[0], word.split("/")[1].split("-")
                if any(label in CONTENT_LABELS for label in word_labels):
                    print(f"\tAdded content: {word_text.lower()}/{word_labels}")
                    content_words.append(word_text.lower())

    # Lemmatize only content words
    doc = nlp(" ".join(content_words))
    lemmatized_content = [token.lemma_ for token in doc if token.is_alpha]

    # Compute metrics
    ndw = len(set(lemmatized_content))
    text = " ".join(lemmatized_content)
    perc5_length = max(1, len(lemmatized_content) * 5 // 100)

    hdd = ld.hdd(text)
    mtld = ld.mtld(text)
    mattr = ld.mattr(text, window_length=15)
    mattr5perc = ld.mattr(text, window_length=perc5_length)
    ttr = ld.ttr(text)
    wim_result = calculate_wim(lemmatized_content)

    results.append({
        "id": file.split("_")[0],
        "tokens": len(lemmatized_content),
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
