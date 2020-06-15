import time
from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.common.keys import Keys

b = webdriver.Firefox(executable_path="/Users/jackowens/Downloads/geckodriver")

def run_search(URL, search_term):

    b.get(URL)
    b.implicitly_wait(2)

    # Search for Item
    search = b.find_element_by_xpath("//input[@id='query']")
    search.click()
    search.send_keys(search_term + Keys.RETURN)

    time.sleep(2)  # Wait for results to load

    # Sort Results by Date
    select_dropdown = b.find_element_by_xpath("//div[@class='search-sort']")
    select_dropdown.click()
    select_date = b.find_element_by_xpath("//a[@data-selection='date']")
    select_date.click()

    page_source_results = b.page_source
    soup = BeautifulSoup(page_source_results, features="lxml")
    raw_results = soup.findAll("a", class_="result-title hdrlnk")
    raw_price = soup.findAll("span", class_="result-price")

    for result, price in zip(raw_results, raw_price):
        print(f"{result.text} <> {price.text}")

    b.quit()

run_search("https://stlouis.craigslist.org/", "bicycle")
