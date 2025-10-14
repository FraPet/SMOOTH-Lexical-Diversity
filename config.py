# Configuration file for SMOOTH-Lexical-Diversity

# Path to the folder containing CHAT (.cha) or text (.txt) transcripts.
# Each utterance should be on a separate line.
TXT_PATH = "data"

# Path where results will be stored
OUTPUT_PATH = "output"

# Language setting: "it" for Italian, "en" for English
LANGUAGE = "it"

# Map language codes to spaCy models
SPACY_MODELS = {
    "it": "it_core_news_lg",
    "en": "en_core_web_lg"
}

# specify model for "main.py" script
SPACY_MODEL = "it_core_news_lg"