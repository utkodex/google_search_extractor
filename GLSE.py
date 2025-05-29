from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import TimeoutException
import time
from datetime import datetime
import gspread
from oauth2client.service_account import ServiceAccountCredentials
# from cred import linkedin_username, linkedin_password  # Importing credentials
import json
import random
from fake_useragent import UserAgent
from selenium.webdriver.chrome.options import Options

from utils.my_tools import keyword_creator

# position = "Legal Head, VP, AVP, AGM, GM"
# industry = "MSME, SME"
# from_page = 1
# to_page = 10

class GoogleScraper:
    def __init__(self, position=None, industry=None, from_page=None, to_page=None):
        # self.driver = None
        self.link = "https://www.google.com/"
        self.position = position
        self.industry = industry
        self.subsheet_title = 'Linkedin Profile MSME'
        self.from_page = from_page
        self.to_page = to_page

    def sheet_init(self, subsheet_title):
        # Google Sheets configuration
        gc = gspread.service_account(filename='credentials.json')  # Replace with the path to your credentials.json file
        spreadsheet_url = 'https://docs.google.com/spreadsheets/d/1MV3GXRFBeEUnZ9YxlgJIOlW6y7HOWWC80ugLc_zZPKM/edit?gid=0#gid=0'  # Replace with the URL of your Google Sheet

        # Open the Google Sheet by URL
        sh = gc.open_by_url(spreadsheet_url)

        # Identify the subsheet by title
        # subsheet_title = 'Linkedin Profile MSME'  # Replace with the title of your subsheet
        worksheet = sh.worksheet(subsheet_title)

        return worksheet

    def initialize_driver(self):
        # Create a fake user-agent
        ua = UserAgent()
        fake_user_agent = ua.random  # Get a random user-agent

        # Set up undetected-chromedriver
        options = uc.ChromeOptions()
        options.add_argument(f"user-agent={fake_user_agent}") 
        options.add_argument("--disable-popup-blocking")
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_argument("--disable-cache")
        options.add_argument("--aggressive-cache-discard")
        options.add_argument("--disable-application-cache")
        options.add_argument("--disable-offline-load-stale-cache")
        options.add_argument("--disk-cache-size=0")
        # Uncomment if you want headless mode
        # options.add_argument("--headless=new")

        # Initialize undetected-chromedriver
        self.driver = uc.Chrome(version_main=136, options=options)

    def get_link(self):
        self.initialize_driver()
        self.driver.get(self.link)

    def search_init(self):
        self.get_link()

        # Enter the company name in the search bar and search
        random_number = random.uniform(2, 5)
        time.sleep(random_number)

        search_box = self.driver.find_element(By.NAME, "q")

        search_box.clear()

        search_query = keyword_creator(self.position, self.industry)
        print("Search Query:", search_query)

        search_box.send_keys(search_query)

        search_box.send_keys(Keys.RETURN)

        random_number = random.uniform(1, 2)
        time.sleep(random_number)

    def scrolls(self):

        random_integer = random.randint(5, 8)
        for _ in range(random_integer):
            
            # Execute JavaScript to scroll down
            random_number = random.uniform(600, 800)
            self.driver.execute_script(f"window.scrollBy(0, {random_number});")
            
            # Wait for the content to load if applicable
            random_number = random.uniform(0, 1)
            time.sleep(random_number)

    def page_skipper(self):
        try:
            # Wait for the element to be present
            page_box_xpath = "//table[@role='presentation']"
            page_box = WebDriverWait(self.driver, 20).until(EC.presence_of_element_located((By.XPATH, page_box_xpath)))
            pagination_text = page_box.text
            
            # Split the text by newline character and filter out non-numeric values
            numbers = [int(num) for num in pagination_text.split("\n") if num.isdigit()]
            
            # Get the greatest number
            greatest_page_number = max(numbers)
            
            # Print the greatest page number
            print("The greatest page number is:", greatest_page_number)
            
            while self.from_page > greatest_page_number:
            
                try:
                    next_page_button = WebDriverWait(self.driver, 20).until(EC.element_to_be_clickable((By.XPATH, f"//a[@aria-label='Page {greatest_page_number}']")))
                    next_page_button.click()
                    greatest_page_number += 1
                except TimeoutException:
                    print("No more pages available.")
                    break
                    
        except TimeoutException:
                print("Pagination element not found")

    def data_scraper(self):

        self.search_init()
        self.page_skipper()

        for i in range(self.from_page, self.to_page+1):
            self.scrolls()

            if i > 1:  # Skip clicking next page button if page number is 1
                next_page_xpath = f"//a[@aria-label='Page {i}']"
                try:
                    next_page_button = WebDriverWait(self.driver, 20).until(EC.element_to_be_clickable((By.XPATH, next_page_xpath)))
                    next_page_button.click()
                except TimeoutException:
                    print("No more pages available.")
                    break  

            # Wait for the search results to load
            google_searchs = WebDriverWait(self.driver, 20).until(
                EC.presence_of_all_elements_located((By.XPATH, "//div[@class='N54PNb BToiNc']"))
            )
            
            # Iterate through each search result
            for google_search in google_searchs:
                try:
                    # Extract the title of the search result
                    search_result = google_search.find_element(By.XPATH, ".//h3[@class='LC20lb MBeuO DKV0Md']").text
                except:
                    search_result = None
            
                try:
                    # Extract the URL from the search result
                    ID_link = google_search.find_element(By.XPATH, ".//a[@jsname='UWckNb']").get_attribute("href")
                except:
                    ID_link = None

                # Output the collected data
                print(f"Page No.: {i}")
                print(f"Search Result Title: {search_result}")
                print(f"URL: {ID_link}")
                print("=====================================================================")

                self.data_uploader(i, search_result, ID_link)

            # print(f"//a[@aria-label='Page {i}']")
            # pages = WebDriverWait(self.driver, 2).until(EC.presence_of_element_located((By.XPATH, f"//a[@aria-label='Page {i}']")))
            # pages.click()
            
            random_number = random.uniform(0.5, 1)
            time.sleep(random_number)

            self.bot_informer(i)

            # return search_result, ID_link

    def data_uploader(self, i, search_result, ID_link):
        worksheet = self.sheet_init(self.subsheet_title)

        data_list = []

        # Append data to the DataFrame
        data_dict = {
            'Page No.': i,
            'Search Result Title': search_result,
            'URL': ID_link,
        }             
    
        # Append the dictionary to the list
        data_list.append(data_dict)
    
        # Append data to the Google Sheet
        worksheet.append_rows([list(data_dict.values())], value_input_option="RAW")

    def bot_informer(self, i):
        from_page = i-1
        print(from_page)

        body_text = self.driver.find_element(By.TAG_NAME, "body").text
        if "Our systems have detected unusual traffic from your computer network" in body_text:
            
            print(f"The scraping stoped because of Bot checkbox. Please start again with page no. {from_page}")
            time.sleep(5)
            self.driver.quit()

            # Update the from_page attribute
            self.from_page = from_page
            self.data_scraper()

        else:
            print("not here")

if __name__ == "__main__":
    scraper = GoogleScraper()
    scraper.data_scraper()