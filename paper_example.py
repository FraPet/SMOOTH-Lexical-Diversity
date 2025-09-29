import re
import spacy
from lexical_diversity import lex_div as ld
from lexdiv_functions import calculate_wim

SPACY_MODELS = {
    "en": "en_core_web_lg",
}

LANGUAGE = "en"
CONTENT_LABELS = ["NOUN", "VERB", "ADJ", "ADV"]

# Test snippet (annotated transcript)
SNIPPET = """
*PAR: she/NOREFEX shows/VERB to/ADP him/NOREFEX the/DET little/ADJ bird/NOUN that/PRON is/VERB on/ADP the/DET branch/NOREFEX with/ADP the/DET nest/NOUN with/ADP the/DET chicks/NOUN *
*PAR: he/PRON climbs/VERB up/SCONJ to/SCONJ take/VERB the/DET nest/NOUN *
*PAR: the/DET bird/NOUN-APOS
*PAR: the/RIPPAR bird/RIPPAR gets/VERB scared/VERB *
*PAR: he/PRON falls/VERB because/SCONJ the/DET branch/NOUN breaks/VERB *
*PAR: so/FILLER he/FILLER learned/FILLER not/FILLER to/FILLER disturb/FILLER the/FILLER nest/FILLER-ENUNCFIL *
"""

# Carica modello spacy
nlp = spacy.load(SPACY_MODELS[LANGUAGE])

# Estrazione parole di contenuto
all_words = []
content_words = []
for line in SNIPPET.split("\n"):
    line = line.strip()
    if not line or line.startswith("@"):
        continue
    if line.startswith("*PAR:"):
        line = line.replace("*PAR:", "").strip()
        line = re.sub(r"@\d+(\.\d+)?\.", "", line)
        words_no_excl = [w for w in line.split() if "/" in w and w != "xxx"]
        words = [w for w in line.split() if "/" in w and w != "xxx" and not w.endswith("-")]

        for word in words:
            word_text, labels_raw = word.split("/", 1)
            all_words.append(word_text.lower())

        for word in words:
            word_text, labels_raw = word.split("/", 1)
            word_labels = labels_raw.split("-")
            if any(lbl in CONTENT_LABELS for lbl in word_labels):
                content_words.append(word_text.lower())



print(f"All words:\t{all_words}")

# Lemmatizzazione
doc = nlp(" ".join(content_words))
print(f"Content Words:\t{content_words}")
lemmas = [token.lemma_ for token in doc if token.is_alpha]
print(f"Lemmatized Content Words:\t{lemmas}")

# Calcolo metriche
ndw = len(set(lemmas))
tokens = len(lemmas)
text = " ".join(lemmas)
perc5_length = max(1, tokens * 5 // 100)
win_length = 10

metrics = {
    "Content Words": tokens,
    "Number of Different Content Words (NDW)": ndw,
    "TTR": ld.ttr(text),
    f"MATTR({win_length})": ld.mattr(text, window_length=win_length),
    "MATTR(5%)": ld.mattr(text, window_length=perc5_length),
    "HD-D": ld.hdd(text),
    "MTLD": ld.mtld(text),
    "WIM": calculate_wim(lemmas),
}

print("Results for example snippet:")
for k, v in metrics.items():
    print(f"{k}: {v}")
