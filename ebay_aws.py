#!/usr/bin/env python
# coding: utf-8

import time
# import pandas as pd

from selenium_runner import run_selenium
from string_templates import stop_words
from dynamodb import add_single_item, get_item_by_attr
from timestamp import generate_timestamp
from sns import send_text_message
from spacy_rule_based_matching import run_matcher_multiple

from bs4 import BeautifulSoup
from selenium.webdriver.common.keys import Keys


def run_search (search_term: str, search_filter=stop_words.get("general"),
    min_price=600, max_price=7200, export_csv=False, headless=False):
    """Run eBay search query with search filters and price constraints.

    Args:
        search_term: Item(s) to search for.
        search_filter: Keyword(s) to avoid using eBay query syntax
        min_price: Lowest price constraint for search.
        max_price: Max price constraint for search.
        export_csv: Exports csv to ./results/excel.
        headless: Runs Firefox in headless mode.

    Returns:
        Pandas dataframe consisting of item title, item price, and item date.

    Description:
        Runs eBay search queries and adds results to DynamoDB table that matches name of search.
        If result(s) do not already exist in relevant DynamoDB table, sends text message via SNS.

    """

    time_stamp = generate_timestamp()

    b = run_selenium(headless_mode=headless)

    b.get("https://www.ebay.com/")
    b.implicitly_wait(2)

    # Search for Item
    input_field = b.find_element_by_xpath("//input[@id='gh-ac']")
    input_field.click()
    input_field.send_keys(search_term + search_filter + Keys.RETURN)

    time.sleep(2)  # Wait for results to load

    # Select Buy It Now
    buy_it_now = b.find_element_by_xpath("//h2[contains(., 'Buy It Now')]")
    buy_it_now.click()

    # Sort by Newly Listed
    page_url = b.current_url
    page_url = page_url + "&_sop=10"
    b.get(page_url)

    # Set Price Constraints
    page_url = b.current_url
    page_url = page_url + f"&_udhi={max_price}&rt=nc&_udlo={min_price}"
    b.get(page_url)

    # Save Page Source
    page_source_results = b.page_source
    soup = BeautifulSoup(page_source_results, features="lxml")

    # Parse Item Titles
    listings = soup.find_all("li", class_="s-item") # <class 'bs4.element.ResultSet'>

    item_titles = []
    item_prices = []
    item_dates = []

    # Loops through all listings and adds data to item_titles, item_prices, and item_dates
    # if _item does not already exist in relevant DynamoDB table
    for listing in listings:
        _item = " " # Removes "New Listing" prefix

        price = listing.find('span', attrs={'class':"s-item__price"}) or None
        if price is not None:
            item_prices.append(price.text)

        for name in listing.find_all('h3', attrs={'class':"s-item__title"}):
            if(str(name.find(text=True, recursive=False))!="None"):
                _item = str(name.find(text=True, recursive=False))

                # If item is new, adds to DynamoDB and appends to item_titles
                # If item has been seen, skips over it
                if (get_item_by_attr(_attr=_item)) == []: # if not found in DynamoDB
                    print(f"{_item} for {price.text} is new, adding to DynamoDB")
                    run_matcher_multiple(_item)

                    add_single_item(title=str(_item), price=str(price.text), time_stamp=time_stamp, brand=search_term) # adds item to DynamoDB
                    item_titles.append(_item) # Necessary to report num of new items
                    # send_text_message(f"{_item} selling for {price.text}")

        # if(_item != " "):
        #     for details in listing.find_all('div', attrs={'class':"s-item__details"}):
        #         for date in details.find_all('span', attrs={'class':"s-item__detail s-item__detail--secondary"}):
        #             if date.text is not None:
        #                 add_single_item(date=date.text)

    print(f"\nFound {len(item_titles)} new items for {search_term} between ${min_price} and ${max_price}")

    # Send text message with new result(s)
    # for title, price in zip(item_titles, item_prices):
    #     send_text_message(f"{title} selling for {price}")

    b.quit()

# run_search("zenith")
run_search("Breguet", min_price=4000, max_price=7650)
