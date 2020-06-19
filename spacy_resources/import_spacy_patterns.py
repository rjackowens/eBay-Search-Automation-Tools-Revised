import json
import os


def get_pattern_single(pattern_name: str, json_file_name="spacy_patterns.json"):
    """Imports single Spacy pattern from json file

    Args:
        pattern_name: Name of pattern to import from file.
        json_file_name: Location of json file containing patterns

    """

    try:
        with open(os.path.join(os.path.dirname(__file__), json_file_name), "r") as json_file:
            data = json.load(json_file)
    except OSError as e:
        raise e

    pattern = []
    for items in data["patterns"].get(pattern_name):
        pattern.append(items)

    return list(map(lambda el:[el], pattern))  # Maps list into list of lists


def get_pattern_all(json_file_name="spacy_patterns.json"):
    """Imports all Spacy patterns from json file

    Args:
        pattern_name: Name of pattern to import from file.
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


# NEED TO GET: [[{'LOWE5R': 'gold'}], [{'LOWER': 'steel'}], [{'LOWER': 'titanium'}]]

# x = get_pattern_all()
# # print(x)
