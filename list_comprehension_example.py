# from spacy_patterns import metal_type, #all_patterns


# for pattern in all_patterns:
#     print(pattern)

# OR

# [expression for item in list]

# [print(pattern) for pattern in all_patterns]  # This works yo

thing = [
    {'LOWERR': 'unworn'}
    ]

# [print(thing.get("LOWER")) for  in thing]

# x = [d['LOWER'] for d in thing]
x = [d.get("LOWER") for d in thing if d.get("LOWER") is not None]

print(x)