import spacy
# from spacy.lang.en.stop_words import STOP_WORDS # Imports Default List of Stop Words
# STOP_WORDS.add("ORION") # This adds stop words to default list

example_title = "Good Condition Jaeger LeCoultre Master Ultra Thin 145.2.79.S Diamond 18K Rose Gold"

# Import spaCy Language Model
nlp = spacy.load('en_core_web_sm')


# Need to ignore capitalization
# Need to store stop words in DynamoDB instead of file
def import_custom_stop_words():
    """Imports stop words from file"""

    try:
        with open("watchfilter.txt", "r") as filter:
            custom_stop_words = filter.read().splitlines()

        # Add Custom Stop Words to spaCy
        for stopword in custom_stop_words:
            lexeme = nlp.vocab[stopword]
            lexeme.is_stop = True
    except IOError as e:
        raise e


def stop_word_remover(title: str):
    """Removes stop words from string"""
    import_custom_stop_words()  # This should be ran outside this function
    spacy_text = nlp(title)  # Type is <class 'spacy.tokens.doc.Doc'>

    # Removes Keywords Included on Stop Word List
    detected_stop_words = []
    clean_words = []
    for token in spacy_text:
        if token.is_stop is True:
            detected_stop_words.append(token)
        else:
            clean_words.append(token)

    print(*clean_words, sep=" ")
    print(*detected_stop_words)


stop_word_remover(example_title)
