from scipy.stats import entropy
from collections import Counter
import numpy as np

def calculate_wim(word_list):
    word_counts = Counter(word_list)
    total_words = len(word_list)
    word_probabilities = np.array([count / total_words for count in word_counts.values()])
    wim = entropy(word_probabilities, base=2)
    return wim
