# =============================================================================
# Author: Francesco Petriglia
# Please cite: "Assessing lexical diversity and informativeness across the adult lifespan: A comprehensive investigation"
# =============================================================================
"""
This script analyzes all folders contained in the "data" directory, using
the spaCy model specified in `config.SPACY_MODEL`.
"""

import os
import csv
import re
import spacy
import config
from lexical_diversity import lex_div as ld
from lexdiv_functions import calculate_wim
from pprint import pprint


# Content and error labels depending on language
if config.LANGUAGE == "it":
    CONTENT_LABELS = ["NOME", "VERBO", "AGG", "AVV"]
    ERROR_LABELS = [
        "PARFON", "FILLER", "RIPPAR", "PARSEM", "PARVERB", "PARAGLEG", "PARAGFUNT",
        "INDEF", "NOREFOM", "NOREFES", "TANG_W", "FSE_W", "ERRFUNTCOES", "NEOL"
    ]
else:  # English
    CONTENT_LABELS = ["NOUN", "VERB", "ADJ", "ADV"]
    ERROR_LABELS = [
        "FALSTART", "PHONPAR", "NEOL", "SEMPAR", "VERBPAR", "INDEF", "NOREFEX",
        "NOREFOM", "FILLER", "REPWORD", "BOPARAG", "FUNCTPARAG",
        "CONTOM", "FUNCTOM", "INCWORDUSE", "TANGWORD"
    ]


# Prepare paths
dir_path = config.TXT_PATH
output_path = config.OUTPUT_PATH
os.makedirs(output_path, exist_ok=True)

# Load single spaCy model from config
if not hasattr(config, "SPACY_MODEL"):
    raise AttributeError("Missing variable 'SPACY_MODEL' in config.py.")
nlp = spacy.load(config.SPACY_MODEL)


# Collect all .txt or .cha files in any language subfolder
input_files = []
for root, _, files in os.walk(dir_path):
    for f in files:
        if f.endswith(".txt") or f.endswith(".cha"):
            input_files.append(os.path.join(root, f))

print(f"Files found ({len(input_files)}):")
for f in input_files:
    print("   ", f)

results = []

for file_path in input_files:
    print(f"\nProcessing file: {file_path}")
    filename = os.path.basename(file_path)

    all_words = []
    content_words = []
    informative_words = []
    uninformative_words = []

    with open(file_path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("@"):
                continue
            if line.startswith("*PAR:"):
                line = line.split("\t")[-1]

            # Clean and split
            line = re.sub(r"@\d+(\.\d+)?\.", "", line)
            words = [w for w in line.split() if "/" in w and w != "xxx" and not w.endswith("-")]

            for word in words:
                word_text, labels_raw = word.split("/", 1)
                word_labels = labels_raw.split("-")
                all_words.append(word_text.lower())

                # Content words
                if any(lbl in CONTENT_LABELS for lbl in word_labels):
                    content_words.append(word_text.lower())

                # Informative vs uninformative
                if not any(lbl in ERROR_LABELS for lbl in word_labels):
                    informative_words.append(word_text.lower())
                else:
                    uninformative_words.append(word_text.lower())

    # Lemmatize only content words
    doc = nlp(" ".join(content_words))
    lemmatized_content = [token.lemma_ for token in doc if token.is_alpha]

    # Compute metrics
    ndw = len(set(lemmatized_content))
    text = " ".join(lemmatized_content)
    win_length = 10  # MATTR window length
    hdd = ld.hdd(text) if len(lemmatized_content) >= 42 else None
    mtld = ld.mtld(text)
    mattr = ld.mattr(text, window_length=win_length)
    ttr = ld.ttr(text)
    wim_result = calculate_wim(lemmatized_content)

    # Lexical informativeness
    lexical_informativeness = (
        len(informative_words) / len(all_words) * 100 if all_words else None
    )

    results.append({
        "id": filename,
        "tokens": len(all_words),
        "Content Words": len(lemmatized_content),
        "Informative words": len(informative_words),
        "Uninformative words": len(uninformative_words),
        "Number of Different Content Words (NDW)": ndw,
        "ttr": ttr,
        f"mattr({win_length})": mattr,
        "hdd": hdd,
        "mtld": mtld,
        "wim": wim_result,
        "Lexical Informativeness (%)": lexical_informativeness
    })

    pprint(results[-1], indent=4, width=100)

# Save results
out_file = os.path.join(output_path, "lexical_diversity_results.csv")
with open(out_file, "w", newline="", encoding="utf-8") as f_out:
    writer = csv.DictWriter(
        f_out,
        fieldnames=[
            "id", "tokens", "Content Words", "Informative words", "Uninformative words",
            "Number of Different Content Words (NDW)",
            "ttr", f"mattr({win_length})", "hdd",
            "mtld", "wim", "Lexical Informativeness (%)"
        ]
    )
    writer.writeheader()
    writer.writerows(results)

print(f"\nResults saved in {out_file}")
