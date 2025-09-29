"""
paper_example.py

Example script for computing lexical diversity and lexical informativeness
indices from an annotated transcript snippet. This script reproduces the
pipeline described in the manuscript, using a minimal excerpt.
"""

import re
import spacy
from lexical_diversity import lex_div as ld
from lexdiv_functions import calculate_wim

# spaCy models
SPACY_MODELS = {
    "en": "en_core_web_lg",
    "it": "it_core_news_lg",
}

# Language switch
LANGUAGE = "en"
if LANGUAGE == "it":
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

# Test snippet (annotated transcript, English example)
SNIPPET = """
*PAR: she/NOREFEX shows/VERB to/ADP him/NOREFEX the/DET little/ADJ bird/NOUN that/PRON is/VERB on/ADP the/DET branch/NOREFEX with/ADP the/DET nest/NOUN with/ADP the/DET chicks/NOUN *
*PAR: he/PRON climbs/VERB up/SCONJ to/SCONJ take/VERB the/DET nest/NOUN *
*PAR: the/DET bird/NOUN-APOS
*PAR: the/RIPPAR bird/RIPPAR gets/VERB scared/VERB *
*PAR: he/PRON falls/VERB because/SCONJ the/DET branch/NOUN breaks/VERB *
*PAR: so/FILLER he/FILLER learned/FILLER not/FILLER to/FILLER disturb/FILLER the/FILLER nest/FILLER-ENUNCFIL *
"""

# Load spaCy model
nlp = spacy.load(SPACY_MODELS[LANGUAGE])

# Extract words
all_words = []
content_words = []
informative_words = []
uninformative_words = []

for line in SNIPPET.split("\n"):
    line = line.strip()
    if not line or line.startswith("@"):
        continue
    if line.startswith("*PAR:"):
        line = line.replace("*PAR:", "").strip()
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

print(f"All words:\t{all_words}")
print(f"Content Words:\t{content_words}")
print(f"Informative Words:\t{informative_words}")
print(f"Uninformative Words:\t{uninformative_words}")

# Lemmatization of content words
doc = nlp(" ".join(content_words))
lemmas = [token.lemma_ for token in doc if token.is_alpha]
print(f"Lemmatized Content Words:\t{lemmas}")

# Compute metrics
ndw = len(set(lemmas))
tokens = len(lemmas)
text = " ".join(lemmas)
perc5_length = max(1, tokens * 5 // 100)
win_length = 10
hdd = ld.hdd(text) if len(lemmas) >= 42 else None

# Lexical Informativeness
lexical_informativeness = (len(informative_words) / len(all_words) * 100) if all_words else None

metrics = {
    "tokens": len(all_words),
    "Content Words": len(lemmas),
    "Informative words": len(informative_words),
    "Uninformative words": len(uninformative_words),

    "Content Words": tokens,
    "Number of Different Content Words (NDW)": ndw,
    "TTR": ld.ttr(text),
    f"MATTR({win_length})": ld.mattr(text, window_length=win_length),
    "MATTR(5%)": ld.mattr(text, window_length=perc5_length),
    "HD-D": hdd,
    "MTLD": ld.mtld(text),
    "WIM": calculate_wim(lemmas),
    "Lexical Informativeness (%)": lexical_informativeness,
}

print("Results for example snippet:")
for k, v in metrics.items():
    print(f"{k}: {v}")
