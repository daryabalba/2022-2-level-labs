"""
Frequency-driven keyword extraction starter
"""
import json
from pathlib import Path
from main import clean_and_tokenize, \
    remove_stop_words, calculate_frequencies, \
    get_top_n, calculate_tf, calculate_tfidf, \
    calculate_expected_frequency, calculate_chi_values, extract_significant_words


if __name__ == "__main__":

    # finding paths to the necessary utils
    PROJECT_ROOT = Path(__file__).parent
    ASSETS_PATH = PROJECT_ROOT / 'assets'

    # reading the text from which keywords are going to be extracted
    TARGET_TEXT_PATH = ASSETS_PATH / 'Дюймовочка.txt'
    with open(TARGET_TEXT_PATH, 'r', encoding='utf-8') as file:
        target_text = file.read()

    # reading list of stop words
    STOP_WORDS_PATH = ASSETS_PATH / 'stop_words.txt'
    with open(STOP_WORDS_PATH, 'r', encoding='utf-8') as file:
        stop_words = file.read().split('\n')

    # reading IDF scores for all tokens in the corpus of H.C. Andersen tales
    IDF_PATH = ASSETS_PATH / 'IDF.json'
    with open(IDF_PATH, 'r', encoding='utf-8') as file:
        idf = json.load(file)

    # reading frequencies for all tokens in the corpus of H.C. Andersen tales
    CORPUS_FREQ_PATH = ASSETS_PATH / 'corpus_frequencies.json'
    with open(CORPUS_FREQ_PATH, 'r', encoding='utf-8') as file:
        corpus_freqs = json.load(file)

    ALPHA = 0.001
    if clean_and_tokenize(target_text) and remove_stop_words(clean_and_tokenize(target_text), stop_words):
        cleaned = remove_stop_words(clean_and_tokenize(target_text), stop_words)  # a list of words w/o stop words
        frequency = calculate_frequencies(cleaned)
        if calculate_tf(frequency):
            calculated_tfidf = calculate_tfidf(calculate_tf(frequency), idf)
            print(get_top_n(calculated_tfidf, 10))
            expected_frequency = calculate_expected_frequency(frequency, corpus_freqs)
            if expected_frequency:
                chi_value = calculate_chi_values(expected_frequency, frequency)
                if chi_value:
                    signific_words = extract_significant_words(chi_value, ALPHA)
                    print(get_top_n(signific_words, 10))
    RESULT = signific_words
    # DO NOT REMOVE NEXT LINE - KEEP IT INTENTIONALLY LAST
    assert RESULT, 'Keywords are not extracted'
