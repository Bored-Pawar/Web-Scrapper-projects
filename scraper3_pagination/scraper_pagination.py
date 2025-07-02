from selenium import webdriver
from selenium.webdriver.chrome.options import Options

# block to initialize driver
def get_driver(headless: bool = False):
    options_settings = Options()

    if headless:
        options_settings.add_argument('--headless')
        options_settings.add_argument('--disable-gpu')
        options_settings.add_argument('--window-size=1920,1080')
    
    driver = webdriver.Chrome(options = options_settings)

    return driver

# necessary libraries for fetch data
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions

# block to fetch page
def fetch_page(driver, wait_time = 10):
    try:
        WebDriverWait(driver,wait_time).until(
            expected_conditions.presence_of_all_elements_located((By.CLASS_NAME, 'quote'))
        )
    except Exception as e:
        print(f"Error while loading page: {e}")
    
    return driver.page_source

# necessary libraries for extract_data
from selenium.webdriver.common.by import By

#  extract block below
def extract_data(driver):
    data = []

    quote_elements = driver.find_elements(By.CLASS_NAME, 'quote')

    for quote in quote_elements:
        text = quote.find_element(By.CLASS_NAME, 'text').text
        author = quote.find_element(By.CLASS_NAME, 'author').text
        tags = [tag.text for tag in quote.find_elements(By.CLASS_NAME, 'tag')]

        data.append({
            'quote' : text,
            'author' : author,
            'tags' : tags
        })

    return data

# necessary libraries for the next page block
from selenium.common.exceptions import NoSuchElementException

# next_page function below
def next_page(driver):
    try:
        next_button = driver.find_element(By.CLASS_NAME, 'next')
        next_link = next_button.find_element(By.TAG_NAME, 'a')
        next_link.click()
        return True
    except NoSuchElementException:
        return False

# necessary libraries for the scrape all pages block
import time
# fuction to scrape all the pages
def scrape_all_pages(start_url):
    
    # start the brower & create a mainholding list
    driver = get_driver(headless = False)
    all_data = []
    
    try:
        driver.get(start_url)
        while True:
            # fetch page
            fetch_page(driver)

            # extract data
            all_data.extend(extract_data(driver))

            # next page
            if not next_page(driver):
                break # the next_page function sends true when page found so till ther are pages the not will not allow the loop to break
            
            time.sleep(1)

    finally:
        driver.quit()

    return all_data

#necessary libraries for main block
import pandas as pd

# main block
if __name__ == "__main__":
    start_url = "https://quotes.toscrape.com/js/page/1/"
    all_data = scrape_all_pages(start_url)

    #print data in terminal
    for item in all_data:
        print(f"quote: {item['quote']}")
        print(f"author: {item['author']}")
        print(f"tags: {','.join(item['tags'])}")
        print("-" * 50)

    # save data to csv
    df = pd.DataFrame(all_data)
    df.to_csv("quotes.csv", index = False)
    print("Saved all quotes to quotes.csv")
    
