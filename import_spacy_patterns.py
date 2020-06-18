import json


def get_pattern(pattern_name: str, json_file_name="spacy_patterns.json"):
    """Imports Spacy pattern from json file

    Args:
        pattern_name: Name of pattern to import from file.
        json_file_name: Location of json file containing patterns

    """

    try:
        with open(json_file_name, "r") as json_file:
            data = json.load(json_file)
    except OSError as e:
        raise e

    pattern = []
    for items in data["patterns"].get(pattern_name):
        pattern.append(items)
    
    # return pattern
    return list(map(lambda el:[el], pattern))  # Maps list into list of lists


# get_pattern("metals")
# x = get_pattern("metals")
# print(x)
