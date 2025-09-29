import os
import csv
import re
import spacy
import config
from lexical_diversity import lex_div as ld
from lexdiv_functions import calculate_wim 

# Content and error labels depending on language
if config.LANGUAGE == "it":
    CONTENT_LABELS = ["NOME", "VERBO", "AGG", "AVV"]
    ERROR_LABELS = [
        "PARFON", "FILLER", "PARSEM", "PARVERB", "PARAGLEG", "PARAGFUNT",
        "OMCONT", "INDEF", "NOREFOM", "NOREFES", "APOS", "TANG_W", "FSE_W",
        "ERRFUNTCOES", "IDIOS", "NEOL", "REPHR"
    ]
else:  # English
    CONTENT_LABELS = ["NOUN", "VERB", "ADJ", "ADV"]
    ERROR_LABELS = [
        "PARFON", "FILLER", "PARSEM", "PARVERB", "PARAGLEG", "PARAGFUNT",
        "OMCONT", "INDEF", "RIPPAR", "NOREFOM", "NOREFEX", "FALSESTART", "APOS",
        "TANG_W", "FSE_W", "ERRFUNTCOES", "IDIOS", "NEOL", "REPHR"
    ]

# Prepare paths
dir_path = config.TXT_PATH
output_path = config.OUTPUT_PATH
os.makedirs(output_path, exist_ok=True)

# Load spaCy model depending on config
if config.LANGUAGE not in config.SPACY_MODELS:
    raise ValueError(f"Unsupported language: {config.LANGUAGE}. Use 'it' or 'en'.")
nlp = spacy.load(config.SPACY_MODELS[config.LANGUAGE])

# Collect input files (.cha or .txt) with suffix -LANG
lang_suffix = f"-{config.LANGUAGE}.txt"
input_files = [
    t for t in os.listdir(dir_path)
    if (t.endswith(lang_suffix) or t.endswith(f"-{config.LANGUAGE}.cha"))
]
print("Files found:", input_files)

results = []

for file in input_files:
    print(f"Processing file: {file}")
    file_path = os.path.join(dir_path, file)

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
            # Clean
            line = re.sub(r"@\d+(\.\d+)?\.", "", line)
            words = [w for w in line.split() if "/" in w and w != "xxx" and not w.endswith("-")]

            for word in words:
                word_text, labels_raw = word.split("/", 1)
                word_labels = labels_raw.split("-")
                all_words.append(word_text.lower())

                # Content words
                if any(lbl in CONTENT_LABELS for lbl in word_labels):
                    content_words.append(word_text.lower())

                # Informative words
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
    perc5_length = max(1, len(lemmatized_content) * 5 // 100)
    win_length = 10  # MATTR window length
    hdd = ld.hdd(text) if len(lemmatized_content) >= 42 else None
    mtld = ld.mtld(text)
    mattr = ld.mattr(text, window_length=win_length)
    ttr = ld.ttr(text)
    wim_result = calculate_wim(lemmatized_content)

    # Lexical Informativeness
    lexical_informativeness = (
        len(informative_words) / len(all_words) * 100 if all_words else None
    )

    results.append({
        "id": file,
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
    print("\t", results[-1])

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

print(f"Results saved in {out_file}")
