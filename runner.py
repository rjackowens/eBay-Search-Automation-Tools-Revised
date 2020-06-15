from ebay import run_search
from string_templates import search_terms

for item in search_terms:
    run_search(item)
