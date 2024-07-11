from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import time

class Scraping:



    def __init__(self):
       chrome_options = Options()
       chrome_options.add_argument('--ignore-certificate-errors')
       chrome_options.add_argument('--ignore-ssl-errors')
       chrome_options.add_argument('--disable-web-security')   
       chrome_options.add_argument('--allow-running-insecure-content')
       driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
       


    def iniciarProceso(self, driver):
        driver.get("https://2cap.com.mx")



if __name__ == "__main__":
    scraping = Scraping()
    driver = scraping.__init__()
    scraping.iniciarProceso(driver)

       