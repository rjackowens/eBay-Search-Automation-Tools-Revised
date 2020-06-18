import spacy
from spacy.matcher import Matcher
from colorama import Fore, Style
from import_spacy_patterns import get_pattern_single, get_pattern_all


def run_matcher_single(title: str, match_pattern: str):
    """Run Spacy matcher against a single array of patterns

    args:
        title: Title string to run matcher against.
        match_pattern: Name of pattern to run. Corresponds to arrays in json_file_name.

    """

    nlp = spacy.load("en_core_web_sm")

    for pattern in get_pattern_single(match_pattern):

        matcher = Matcher(nlp.vocab)
        matcher.add("MATCH_ID", None, pattern)  # MATCH_ID can eventually be name of pattern itself

        doc = nlp(title)
        matches = matcher(doc)

        # print([token.text for token in doc])  # Visualize all tokens

        # If token does not match pattern
        if matches == []:

            # Extracting key/value from pattern
            key_name = [list(k.keys()) for k in pattern][0]
            value_name = [v.get(*key_name) for v in pattern]

            if key_name[0] == "LOWER":
                print(f"No keyword matches found for: {value_name[0]}")
            else:
                print(f"No matches found for: {key_name[0]}")

        else:
            for match_id, start, end in matches:
                # string_id = nlp.vocab.strings[match_id]  # Get string representation of match, i.e. MATCH_ID
                span = doc[start:end]  # The matched span
                print(f"Found keyword match: {span.text}")


# run_matcher_single("Jaeger LeCoultre Master Ultra Thin Steel Gold Test NEW", "metals")
# run_matcher_single("Used Jaeger LeCoultre Master Ultra Thin Steel Gold Test NEW 2", "colors")
# run_matcher_single("Jaeger LeCoultre Master Ultra Thin Steel Gold Test NEW", "conditions")

def run_matcher_multiple(title: str):
    """Run Spacy matcher against multiple arrays of patterns

    args:

        title: Title string to run matcher against.

    """

    nlp = spacy.load("en_core_web_sm")

    for pattern in get_pattern_all():
        for element in pattern:

            matcher = Matcher(nlp.vocab)
            matcher.add("MATCH_ID", None, element)  # MATCH_ID can eventually be name of pattern itself

            doc = nlp(title)
            matches = matcher(doc)

            # print([token.text for token in doc])  # Visualize all tokens

            # If token does not match pattern
            if matches == []:

                # Extracting key/value from pattern
                key_name = [list(k.keys()) for k in element][0]
                value_name = [v.get(*key_name) for v in element]

                if key_name[0] == "LOWER":
                    print(f"{Fore.RED}No keyword matches found for: {value_name[0]}{Style.RESET_ALL}")
                else:
                    print(f"{Fore.RED}No matches found for: {key_name[0]}{Style.RESET_ALL}")

            else:
                for match_id, start, end in matches:
                    # string_id = nlp.vocab.strings[match_id]  # Get string representation of match, i.e. MATCH_ID
                    span = doc[start:end]  # The matched span
                    print(f"{Fore.YELLOW}Found keyword match: {span.text}")


run_matcher_multiple("Good Condition Jaeger LeCoultre Master Spring Drive Ultra Thin 2015 Steel Gold Test NEW")
