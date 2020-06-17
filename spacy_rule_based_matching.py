import spacy
from spacy.matcher import Matcher
from spacy_patterns import metal_type, all_metals, all_conditions


def run_matcher(title: str, match_pattern: list):
    """Run Spacy matcher against list of patterns"""
    nlp = spacy.load("en_core_web_sm")
    for pattern in match_pattern:
        matcher = Matcher(nlp.vocab)
        matcher.add("MATCH_ID", None, pattern)  # MATCH_ID can eventually be name of pattern itself

        doc = nlp(title)
        matches = matcher(doc)

        if matches == []:
            x = [d.get("LOWER") for d in pattern]
            print(f"No keyword matches found for: {x[0]}")
            # x = [d.get("LOWER") for d in thing if d.get("LOWER") is not None]
        else:
            for match_id, start, end in matches:
                # string_id = nlp.vocab.strings[match_id]  # Get string representation of match, i.e. MATCH_ID
                span = doc[start:end]  # The matched span
                print(f"Found keyword match: {span.text}")


run_matcher("Used Jaeger LeCoultre Master Ultra Thin Steel Gold Test", all_conditions)
