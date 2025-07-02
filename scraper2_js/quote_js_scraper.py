# necessary libraries for the getdriver block
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

# function to initialize and return a selenium function
def get_driver(headless: bool = False):

    # creating a Options object called options_settings
    options_settings = Options()

    # setting the options_settings for headless browser 
    if headless:
        options_settings.add_argument('--headless')
        options_settings.add_argument('--disable-gpu')
        options_settings.add_argument('--window-size=1920,1080')
    
    # getting chrome as driver for 
    driver = webdriver.Chrome(options = options_settings)
    
    return driver

# necessary libraries for ur fetch block
from selenium.webdriver.common.by import By # let's u define how to identify elements also used for extract block
from selenium.webdriver.support.ui import WebDriverWait # tell the webdriver to wait until ec executed or the wait time
from selenium.webdriver.support import expected_conditions # the condition after which the webdriverwait ends

# function to fetch page ie load page
def fetch_page(driver, url, wait_time = 10):
    driver.get(url)

    try:
        WebDriverWait(driver, wait_time).until(
            expected_conditions.presence_of_all_elements_located((By.CLASS_NAME, "quote")) # Waits for a specific element with class "quote"
            # it is better becuase >>> Even though <body> appears quickly, JavaScript content (like quotes) may load much later.
        )
    except:
        print("Timeout or error loading page")
    
    return driver.page_source # Html after Js is loaded

# necessary libraries for the extract bloack
from selenium.webdriver.common.by import By

def extract_data(driver):
    data = [] # empty list to hold dictionaries of data

    # find all quotes by class name
    quote_elements = driver.find_elements(By.CLASS_NAME, 'quote')

    # from block of quotes i.e quote elements
    for quote in quote_elements:
        # extract quote text, author, tags
        text = quote.find_element(By.CLASS_NAME, 'text').text
        author = quote.find_element(By.CLASS_NAME, 'author').text
        tags =  [tag.text for tag in quote.find_elements(By.CLASS_NAME, 'tag')]

        # append to list as dictionary
        data.append({
            "quote text" : text,
            "author" : author,
            "tags" : tags
        })

    return data

#necessary lib for this block
import pandas as pd
if __name__ == "__main__":
    driver = get_driver(True)
    url = "https://quotes.toscrape.com/js/"
    fetch_page(driver, url)
    data = extract_data(driver)

    # to print data
    for item in data:
        print(f"quote: {item['quote text']}")
        print(f"author: {item['author']}")
        print(f"tags: {', '.join(item['tags'])}") # use single quotes n not double quote
        print('-' * 50)
    
    # save as csv
    df = pd.DataFrame(data)
    df.to_csv('one_page_quotes.csv', index = False)