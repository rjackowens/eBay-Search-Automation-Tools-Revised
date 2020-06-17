import spacy
from spacy.matcher import Matcher
from spacy_patterns import all_metals, all_conditions, all_prices, all_numbers


def run_matcher(title: str, match_pattern: list):
    """Run Spacy matcher against a single list of patterns"""
    nlp = spacy.load("en_core_web_sm")

    for pattern in match_pattern:
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


# run_matcher("Jaeger LeCoultre Master Ultra Thin Steel Gold Test NEW", all_conditions)
# run_matcher("Used Jaeger LeCoultre Master Ultra Thin Steel Gold Test NEW 2", all_prices)
run_matcher("Jaeger LeCoultre Master Ultra Thin Steel Gold Test NEW", all_numbers)
