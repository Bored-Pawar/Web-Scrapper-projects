# necessary lib for get_driver block
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

def get_driver(headless: bool = False):
    options_settings = Options()

    if headless:
        options_settings.add_argument('--headless')
        options_settings.add_argument('--disable-gpu')
        options_settings.add_argument('--window-size=1980,1080')

    driver = webdriver.Chrome(options = options_settings)

    return driver

# necessary lib for dynamic input block
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.common.keys import Keys

# dynamic input block
def dynamic_input(driver, start_url, skill_or_job_user_input, location_user_input, experiance_input, wait_time = 10):
    driver.get(start_url)

    try:
        WebDriverWait(driver, wait_time).until(
            expected_conditions.presence_of_element_located((By.CLASS_NAME, 'qsb'))
        )
    except Exception as e:
        print(f"Error occoured in dynamic_input_search block: {e}")

    try:
        search_box = driver.find_element(By.CLASS_NAME, 'qsb')
        skill_or_job_div = search_box.find_element(By.CLASS_NAME, 'keywordSugg')
        skills_or_job_input = skill_or_job_div.find_element(By.CLASS_NAME, 'suggestor-input')
        skills_or_job_input.send_keys(skill_or_job_user_input)

    except Exception as e:
        print(f"Error occoured in skills_or_job_input block: {e}") 

    try:
        search_box = driver.find_element(By.CLASS_NAME, 'qsb')
        location_input_div = search_box.find_element(By.CLASS_NAME, 'locationSugg')
        location_input = location_input_div.find_element(By.CLASS_NAME, 'suggestor-input')
        location_input.send_keys(location_user_input)

    except Exception as e:
        print (f"Error occured in location_input block: {e}")
    
    experiance_text = "Fresher" if experiance_input == "0" else f"{experiance_input} year" if experiance_input == "1" else f"{experiance_input} years"

    try:
        exp_dropdown = driver.find_element(By.XPATH, '//*[@id="expereinceDD"]')
        exp_dropdown.click()

        # wait for dropdown
        WebDriverWait(driver, wait_time).until(
            expected_conditions.visibility_of_element_located((By.XPATH, f"//li[contains(text(), '{experiance_text}')]"))
        ).click()

    except Exception as e:
        print (f"Error occured in experience dropdown: {e}")

    try:
        search_box = driver.find_element(By.CLASS_NAME, 'qsb')
        search = search_box.find_element(By.CLASS_NAME, 'qsbSubmit')
        search.click()
        driver.switch_to.window(driver.window_handles[-1])
        

    except Exception as e:
        location_input.send_keys(Keys.ENTER)
        # After clicking search, switch to the newest tab
        driver.switch_to.window(driver.window_handles[-1])
                
    return driver.current_url

    


# necessary libraries for fetch_page
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By

#fetch page block
def fetch_page(driver, wait_time = 10):

    try:
        WebDriverWait(driver, wait_time).until(
            expected_conditions.presence_of_all_elements_located((By.CSS_SELECTOR, 'span.job-post-day'))
            # here instead of using CLASS_NAME and job-post-day we used CSS_SELECTOR and span.job-post-day
            # becoz CSS_SELECTOR is more flexible and it will make sure that we are looking for the right element
        )
    except Exception as e:
        print(f"Error in fetching page: {e}")

    return driver.page_source

# necessary libs for extract block
from selenium.webdriver.common.by import By
# extract block
def extract_data(driver):
    data = []

    position_blocks = driver.find_elements(By.CSS_SELECTOR, 'div.cust-job-tuple')

    for position in position_blocks:
        try:
            # role = position.find_element(By.CSS_SELECTOR, 'a.title').text
            company_name = position.find_element(By.CSS_SELECTOR, 'a[class*="comp-name"]').text
            # tenure = position.find_element(By.CSS_SELECTOR, 'span.expwdth').text
            # location = position.find_element(By.CSS_SELECTOR, 'span.locWdth').text
            # requirements = position.find_element(By.CSS_SELECTOR, 'span.job-desc').text
            # tags = [tag.text for tag in position.find_elements(By.CSS_SELECTOR, 'li.tag-li')]
            # posted_on = position.find_element(By.CSS_SELECTOR, 'span.job-post-day').text
        
        except Exception as e:
            print("Skipping block due to error:", e)
            continue

        data.append(company_name)

    return data

# necessary libs for next page
from selenium.common.exceptions import NoSuchElementException
# next page block
def next_page(driver):
    next_button = driver.find_element(By.XPATH, '//a[contains(@class, "styles_btn-secondary__2AsIP") and span[text()="Next"]]')
    
    try:
        next_button.click()
        return True
    except NoSuchElementException:
        return False
    
# necessary libs for scrape_all_pages
import random
import time
# scrape_all_pages
def scrape_all_pages(driver, start_url, skill, location, experience, number_of_listing = 200):

    # function to get the searched page by user & create a empty main file
    current_url = dynamic_input(driver, start_url, skill, location, experience)
    print(f"Initial search page is: {current_url}")
    all_data = []

    while (True and len(set(all_data)) <= number_of_listing):

        # mqke sure the page to extract data from is loaded correctly
        fetch_page(driver)

        # extract data
        all_data.extend(extract_data(driver))

        # next page
        if not next_page(driver):
            break # the next_page function sends true when page found so till ther are pages the not will not allow the loop to break

        # sleep for random time to avoid bot detection
        delay = random.uniform(1,2)
        time.sleep(delay)


    return all_data

# main google map search
# necessary lib for dynamic input block
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions

def dynamic_input_google_search(search_user_input, driver, start_url, wait_time = 10):
    driver.get(start_url)

    # set a wt condition to makw sure that the code wait's till the search bar is detected
    try:
        WebDriverWait(driver, wait_time).until(
            expected_conditions.presence_of_element_located((By.XPATH, '//*[@id="searchboxinput"]'))
        )
    
    except Exception as e:
        print (f"Error in waiting for search bar: {e}")
    
    # set a wt condition to makw sure that the code wait's till the search bar is detected
    try:
        search_box = driver.find_element(By.XPATH, '//*[@id="searchboxinput"]')
        search_box.send_keys(search_user_input)    
        search_box.send_keys(Keys.ENTER)
        # After clicking search, switch to the newest tab
        driver.switch_to.window(driver.window_handles[-1])

    except Exception as e:
        print ("Error while searching: {e}")

    return driver.current_url

# necessary lib for the google extract block and initlaize seen_company set
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.common.exceptions import NoSuchElementException
import re
import time
import random
seen_companies = set()
# extract block
def extract_data_google(driver, seen_companies, wait_time = 10):
    data = []

    # WebDriverWait(driver, wait_time).until(
    #     expected_conditions.presence_of_all_elements_located((By.CSS_SELECTOR, 'a.hfpxzc'))
    # )

    # find all the listings on page & creat a temp list named data
    try:
        company_cards = driver.find_elements(By.CSS_SELECTOR, 'a.hfpxzc')
        print(f"Found {len(company_cards)} cards")
    
    except NoSuchElementException as e:
        print(f"error in getting company cards: {e}")

    for card in company_cards:

        # get company name
        try:  
            driver.execute_script("arguments[0].scrollIntoView(true);", card)
            WebDriverWait(driver, wait_time).until(
                expected_conditions.element_to_be_clickable(card)
            ).click()
            WebDriverWait(driver, wait_time).until(
                expected_conditions.presence_of_element_located((By.CSS_SELECTOR, 'h1.DUwDvf.lfPIob'))
            )
            company_name = driver.find_element(By.CSS_SELECTOR, 'h1.DUwDvf.lfPIob').text
        
        except Exception as e:
            print(f"error in getting company name before extracting data: {e}")
            break

        # check if it has been seen before
        if company_name in seen_companies:
            continue
        else:
            seen_companies.add(company_name)

            # scroll to elemnt and click
            try:
                driver.execute_script("arguments[0].scrollIntoView(true);", card)
                WebDriverWait(driver, wait_time).until(
                    expected_conditions.element_to_be_clickable(card)
                ).click()
            except Exception as e:
                print(f"error in clicking the card: {e}")

            WebDriverWait(driver, wait_time).until(
                expected_conditions.presence_of_element_located((By.CSS_SELECTOR, 'h1.DUwDvf.lfPIob'))
            )

            # extract all details
            # name block
            try:
                name = driver.find_element(By.CSS_SELECTOR, 'h1.DUwDvf.lfPIob').text

            except Exception as e:
                print(f"error in extracting company name: {e}")
                continue

            # address block
            try:
                address = driver.find_element(By.XPATH, '//*[@id="QA0Szd"]/div/div/div[1]/div[3]/div/div[1]/div/div/div[2]/div[7]/div[3]/button/div/div[2]/div[1]').text

            except Exception as e:
                print(f"error in extracting company address: {e}")
                address = "not found"

            # phone number block
            try:
                all_extract = [element.text for element in driver.find_elements(By.CSS_SELECTOR, 'div.Io6YTe.fontBodyMedium.kR99db.fdkmkc')]
                element_joined = " || ".join(all_extract)
                # define pattern for mobile + landline numbers
                pattern = re.compile(r'(?:\+91[\s-]?|0)?\d{5}\s\d{5}|\d{3}\s\d{4}\s\d{4}')

                match = pattern.search(element_joined)
                if match:
                    phone = match.group()
                else:
                    phone = "not found"
            except Exception as e:
                print(f"error in extracting company phone number: {e}")
                phone = "not found coz of error"

            # url which will also be used to extract the latitude longitude using regex
            try:
                url = driver.current_url

            except Exception as e:
                print(f"error in fetching the page url: {e}")
                continue

            # extracting latitude & longitude
            try:
                latitude_longitude = re.compile(r'!3d(-?\d{1,3}\.\d+)!4d(-?\d{1,3}\.\d+)')
                matching_objects = latitude_longitude.search(url)
                latitude = matching_objects.group(1)
                longitude = matching_objects.group(2)

            except Exception as e:
                print(f"Error in extracting latitude longitude: {e}")
            
            data.append({
            'company_name': name,
            'address': address,
            'phone number': phone,
            'latitude': latitude,
            'longitude': longitude,
            'url': url
            })
            delay = random.uniform(1,3)
            time.sleep(delay)
        
    return data


if __name__ == "__main__":
    start_url = "https://www.naukri.com/"
    skill = input("Enter a skill / company / designation: ")
    location = input("Enter location: ")
    experience = input("Years of expeinreince from 0 - 5: ")
    driver = get_driver()

    # Call the input function
    company_list= scrape_all_pages(driver, start_url, skill, location, experience, number_of_listing = 150)
    company_set = set(company_list)
    final_list = list(company_set)

    all_data = []



    for company in final_list:
        search_prompt = company + " " + location
        google_map_url = "https://www.google.com/maps/@19.0825555,72.8789412,11z?entry=ttu&g_ep=EgoyMDI1MDYzMC4wIKXMDSoASAFQAw%3D%3D"
        dynamic_input_google_search(search_prompt, driver, google_map_url, wait_time = 10)
        # delay = random.uniform(3)
        time.sleep(3)
        all_data.extend(extract_data_google(driver, seen_companies))


    
    import pandas as pd
    df = pd.DataFrame(all_data)
    df.to_excel("companies_at_desired_location.xlsx", index=False)
    print("Scraping completed. Data saved to companies_at_desired_location.xlsx")
    df.to_csv("companies_at_desired_location.csv", index=False)
    print("Scraping completed. Data saved to companies_at_desired_location.csv")