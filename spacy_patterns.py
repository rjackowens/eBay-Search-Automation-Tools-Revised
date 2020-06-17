# Patterns used for Spacy rule based matching

all_metals = [
    [
        {"LOWER": "gold"}
    ],
    [
        {"LOWER": "steel"}
    ],
    [
        {"LOWER": "titanium"}
    ]
]

all_conditions = [
    [
        {"LOWER": "new"}
    ],
    [
        {"LOWER": "used"}
    ],
    [
        {"LOWER": "unworn"}
    ]
]

all_colors = [
    [
        {"LOWER": "black"}
    ],
    [
        {"LOWER": "white"}
    ],
    [
        {"LOWER": "silver"}
    ],
    [
        {"LOWER": "gray"}
    ],
    [
        {"LOWER": "grey"}
    ],
    [
        {"LOWER": "yellow"}
    ]
]

all_prices = [
    [
        {"IS_CURRENCY": True}
    ]
]

all_numbers = [
    [
        {"LIKE_NUM": True}
    ]
]
