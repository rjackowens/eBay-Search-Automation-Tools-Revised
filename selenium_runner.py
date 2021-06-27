import os
import platform
from pathlib import Path
from selenium import webdriver


def verify_file_exists(file_path):
    if Path(file_path).is_file():
        print(f"Using {file_path}")
    else:
        print(f"Unable to locate {file_path}")


def run_selenium(headless_mode=False) -> webdriver:
    """Runs OS specific Selenium with options"""

    operating_system = platform.system()

    if operating_system == "Windows":
        from selenium.webdriver.chrome.options import Options
        selenium_path = os.path.expandvars("%USERPROFILE%\Downloads\chromedriver.exe")
        verify_file_exists(selenium_path)

        options = Options()
        options.headless = headless_mode
        b = webdriver.Chrome(options=options, executable_path=selenium_path)

    elif operating_system == "Darwin": # Mac
        from selenium.webdriver.firefox.options import Options
        selenium_path = "/Users/jackowens/Downloads/geckodriver"
        verify_file_exists(selenium_path)

        options = Options()
        options.headless = headless_mode
        b = webdriver.Chrome(options=options, executable_path=selenium_path)

    elif operating_system == "Linux":
        from selenium.webdriver.firefox.options import Options
        selenium_path = "/Users/jackowens/Downloads/geckodriver"
        verify_file_exists(selenium_path)

        options = Options()
        options.headless = headless_mode
        b = webdriver.Chrome(options=options, executable_path=selenium_path)

    else:
        raise OSError ("Unable to determine operating system")

    return b


# run_selenium().get("https://ebay.com")