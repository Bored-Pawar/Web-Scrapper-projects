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
            role = position.find_element(By.CSS_SELECTOR, 'a.title').text
            company_name = position.find_element(By.CSS_SELECTOR, 'a[class*="comp-name"]').text
            tenure = position.find_element(By.CSS_SELECTOR, 'span.expwdth').text
            location = position.find_element(By.CSS_SELECTOR, 'span.locWdth').text
            requirements = position.find_element(By.CSS_SELECTOR, 'span.job-desc').text
            tags = [tag.text for tag in position.find_elements(By.CSS_SELECTOR, 'li.tag-li')]
            posted_on = position.find_element(By.CSS_SELECTOR, 'span.job-post-day').text
        
        except Exception as e:
            print("Skipping block due to error:", e)
            continue

        data.append({
            'role': role,
            'company_name': company_name,
            'tenure': tenure,
            'location': location,
            'requirements': requirements,
            'tags': tags,
            'posted_on': posted_on
        })

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

    while (True and len(all_data) <= number_of_listing):

        # mqke sure the page to extract data from is loaded correctly
        fetch_page(driver)

        # extract data
        all_data.extend(extract_data(driver))

        # next page
        if not next_page(driver):
            break # the next_page function sends true when page found so till ther are pages the not will not allow the loop to break

        # sleep for random time to avoid bot detection
        delay = random.uniform(1,3)
        time.sleep(delay)

    driver.quit()

    return all_data



if __name__ == "__main__":
    start_url = "https://www.naukri.com/"
    skill = input("Enter a skill / company / designation: ")
    location = input("Enter location: ")
    experience = input("Years of expeinreince from 0 - 5: ")
    driver = get_driver()

    # Call the input function
    all_data = scrape_all_pages(driver, start_url, skill, location, experience, number_of_listing = 200)
    
    import pandas as pd
    df = pd.DataFrame(all_data)
    df.to_excel("job_listings.xlsx", index=False)
    print("Scraping completed. Data saved to job_listings.xlsx")
    df.to_csv("job_listings.csv", index=False)
    print("Scraping completed. Data saved to job_listings.csv")

    
