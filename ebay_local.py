#!/usr/bin/env python
# coding: utf-8

import os
import time
import pandas as pd

from sns_test import send_text_message

from string_templates import stop_words
from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options

def run_search (search_term: str, search_filter=stop_words.get("general"),
    min_price=600, max_price=7200, export_csv=False, headless=True):
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

    """

    options = Options()
    options.headless = headless
    b = webdriver.Firefox(options=options, executable_path="/Users/jackowens/Downloads/geckodriver")

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

    # Create file for seen items if does not exist
    seen_file = f'./results/seen/{search_term}.txt'
    if not os.path.exists(seen_file):
        open(seen_file, 'a').close()

    item_titles = []
    item_prices = []
    item_dates = []

    # Loops through all listings and adds data to item_titles, item_prices, and item_dates
    # if _item does not exist in ./results/seen/{search_term}.txt
    for listing in listings:
        _item = " " # Removes "New Listing" prefix

        for name in listing.find_all('h3', attrs={'class':"s-item__title"}):
            if(str(name.find(text=True, recursive=False))!="None"):
                _item=str(name.find(text=True, recursive=False))
                
                # If item is new, adds to seen.txt and appends to item_titles
                # If item has been seen, skips over it
                with open(seen_file, mode="r+") as file:
                    if _item not in file.read():
                        # print(f"{_item} is new, adding to seen.txt")
                        file.writelines(_item + "\n")
                        item_titles.append(_item)

        if(_item != " "):
            price = listing.find('span', attrs={'class':"s-item__price"})
            item_prices.append(price.text)

        for details in listing.find_all('div', attrs={'class':"s-item__details"}):
            for date in details.find_all('span', attrs={'class':"s-item__detail s-item__detail--secondary"}):
                item_dates.append(date.text)

    print(f"\nFound {len(item_titles)} new items for {search_term} between ${min_price} and ${max_price}")

    for title, price, date in zip(item_titles, item_prices, item_dates):
        # print(title, price, date)
        send_text_message(f"{title} selling for {price}")

    # Create Pandas Dataframe
    # search_results_df = pd.DataFrame.from_dict({"Name":item_titles, "Price": item_prices, "Date": item_dates}, orient="index")
    # pd.set_option('max_colwidth', 75)
    # print(search_results_df)

    # Creates .csv with name of search term and deletes if already exists
    # if export_csv:
    #     file_name = f'./results/excel/{search_term}.csv'

    #     try:
    #         os.remove(file_name)
    #     except OSError:
    #         pass

    #     print(f"\nExporting {file_name}")
    #     search_results_df.to_csv(file_name, encoding='utf-8')

    b.quit()

# run_search("curta", 890, 1500)
run_search("Vacheron", min_price=2000, max_price=7650)
