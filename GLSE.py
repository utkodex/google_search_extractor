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
import pandas as pd
from pandas import DataFrame
from datetime import datetime
import pyperclip
import gspread
from oauth2client.service_account import ServiceAccountCredentials
# from cred import linkedin_username, linkedin_password  # Importing credentials
import json
import random
from fake_useragent import UserAgent
from selenium.webdriver.chrome.options import Options

class GoogleScraper:
    def __init__(self):
        self.driver = None
        self.link = "https://www.google.com/"

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


if __name__ == "__main__":
    scraper = GoogleScraper()
    scraper.get_link()