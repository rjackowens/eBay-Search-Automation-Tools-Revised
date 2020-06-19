import spacy
import os
import json

from spacy.matcher import Matcher
from colorama import Fore, Style
# from aws_resources.dynamodb import add_single_item


def get_all_spacy_patterns(json_file_name="spacy_patterns.json"):
    """Imports all Spacy patterns from json file

    Args:
        json_file_name: Location of json file containing patterns

    """

    try:
        with open(os.path.join(os.path.dirname(__file__), json_file_name), "r") as json_file:
            data = json.load(json_file)
    except OSError as e:
        raise e

    patterns = []
    for item in data["patterns"]:
        pattern = data["patterns"].get(item)
        patterns.append(pattern)

    # Maps lists into list of lists
    all_patterns = []
    for pattern in patterns:
        nested_list = list(map(lambda el:[el], pattern))
        all_patterns.append(nested_list)

    return all_patterns


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

    all_keyword_matches = {}
    num_keyword_matches = []
    count = 0

    for pattern in get_all_spacy_patterns():
        for element in pattern:

            matcher = Matcher(nlp.vocab)
            matcher.add("is_number", None, element)  # MATCH_ID can eventually be name of pattern itself

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
                    span = doc[start:end]  # The matched token
                    print(f"{Fore.YELLOW}Found keyword match: {span.text}{Style.RESET_ALL}")

                    match_id_name = nlp.vocab.strings[match_id]  # Get string representation of match, i.e. MATCH_ID
                    all_keyword_matches[match_id_name] = span.text  # In the future match_id_name will be name of match filter
                    count += 1  # Note: Unable to use enumerate() with empty iterators

    print(f"\nTitle was: {title}")
    print(f"Found {count} total matches.")
    print(f"Matched rule(s): {list(all_keyword_matches.keys())[0]}")  # BROKEN: Need to Update match_id_name to == match filter


run_matcher_multiple("Good Condition Jaeger LeCoultre Master 2015 Spring Drive Ultra Thin Steel Gold Test NEW")
