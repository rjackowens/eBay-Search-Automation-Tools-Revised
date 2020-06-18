import json
from itertools import chain


def get_pattern_single(pattern_name: str, json_file_name="spacy_patterns.json"):
    """Imports single Spacy pattern from json file

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


# def login_required(func):
#    def new_func():
#        if is_logged_in():
#            return func()
#        else:
#            raise NotAllowedException
#    return new_func


# @login_required
# def my_account_view():
#    pass


# def get_all_values(nested_dictionary):
#     for key, value in nested_dictionary.items():
#         if type(value) is dict:
#             get_all_values(value)
#         else:
#             print(key, ":", value)


def get_pattern_all(json_file_name="spacy_patterns.json"):
    """Imports all Spacy patterns from json file

    Args:
        pattern_name: Name of pattern to import from file.
        json_file_name: Location of json file containing patterns

    """

    try:
        with open(json_file_name, "r") as json_file:
            data = json.load(json_file)
    except OSError as e:
        raise e

    patterns = []
    for item in data["patterns"]:
        y = data["patterns"].get(item)
        patterns.append(y)

    # return patterns # this works

    # Maps lists into list of lists
    all_results = []
    for pattern in patterns:
        z = list(map(lambda el:[el], pattern))
        all_results.append(z)
    
    return all_results

    # return list(map(lambda el:[el], patterns))  # Maps list into list of lists


# NEED TO GET: [[{'LOWE5R': 'gold'}], [{'LOWER': 'steel'}], [{'LOWER': 'titanium'}]]

# x = get_pattern_all()
# # print(x)

# result = chain(get_pattern_all())
# # print(result)

# for x in result:
#     print(x)
