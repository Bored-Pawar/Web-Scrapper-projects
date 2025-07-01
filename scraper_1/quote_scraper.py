# import necessary libraries for get driver block
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

# function to initialize and return a selenium web browser
def get_driver(headless: bool = False): # the parameter "headless" which is a boolean tells the function if to return the function in headless mode or not

    # options_setting is a object of options that will be used to define the settings of the headless browser
    options_settings = Options()

    # below block of code defines the settings of the headless browser
    if headless:
        options_settings.add_argument('--headless')
        options_settings.add_argument('--disable-gpu')
        options_settings.add_argument('--window-size=1920,1080')

    # setting chrome as driver
    driver = webdriver.Chrome(options = options_settings)

    return driver

# import necessary libraries for the fetch block
from selenium.webdriver.common.by import By # it let's u define how u are indentifying elements like  tag , class, id
from selenium.webdriver.support.ui import WebDriverWait # creates a wait timer instead of sleeping blindly
from selenium.webdriver.support import expected_conditions # tells the wait command to wait until the sondition defined by expencted_conditions is satisfied

# function to fetch URL
def fetch_page(driver, url, wait_time = 10): # driver get the browser we created earlier by get_driver()
    # tells the browser to get url; it is the same as searching a url in the browser
    driver.get(url)

    # this function tells the driver to wait until the said condition is satisfied
    try:
        WebDriverWait(driver, wait_time).until(
            expected_conditions.presence_of_element_located((By.TAG_NAME, "body")) # waits for the Html body to appear
            # in the above line there are not double paranthesis the pre expected_conditions.presence_of _element_located takes one agrgument
            # which is of type tuple (By.TAG_NAME, "body") is a tuple
        )
    except:
        print("Timeout or Error loading pafe.")
    
    return driver.page_source

# import necessary libraries for the parse block
from bs4 import BeautifulSoup

# function to parse the page
def parse_page(driver):
    html = driver.page_source # grabs the entire html of the url loaded
    soup = BeautifulSoup(html, 'html.parser') # parses the given html into structured format that u can  query with functions
    return soup

# function to extract data; for this u need to know thw basic html and the structure of a site
def extract_data(soup):
    data = [] # empty list to store data_dictionaries before appending
    quote_blocks = soup.find_all('div', class_ = 'quote') # class_ coz class is a reserved keyword
    
    # loop throught the quote blocks to extract data
    for block in quote_blocks:
        quote_text = block.find('span', class_ = 'text').get_text(strip = True)
        author = block.find('small', class_ = 'author').get_text(strip = True)
        tags = [tag.get_text(strip = True) for tag in block.find('a', class_ = 'tag')]

        data.append({
            'quote' : quote_text,
            'author' : author,
            'tags' : tags
        })

    return data

# this code block only runs when the file is run directly and doesn't run when the file is called
if __name__ == "__main__": 
    driver = get_driver(True) # starting browser
    url = "https://quotes.toscrape.com/"  # page we want to visit and scrape
    fetch_page(driver, url) # going to that page
    soup = parse_page(driver) # getting html from the page
    data = extract_data(soup) # extracting data

    # print data
    for i, item in enumerate(data, 1):
        print(f"Quote no: {i}:")
        print(f"  Quote: {item['quote']}")
        print(f"  Author: {item['author']}")
        print(f"  Tags  : {', '.join(item['tags'])}")
        print("-" * 50 + "\n")

    driver.quit()