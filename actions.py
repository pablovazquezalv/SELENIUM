import time
import pandas as pd
import os
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup

def handle_click(driver, wait, action, site_name):
    try:
        
        print(f"Clicking on {site_name}")
        print(action['selector']['by'])
        print(action['selector']['value'])

        element = wait.until(EC.element_to_be_clickable((getattr(By, action['selector']['by'].upper()), action['selector']['value'])))
        element.click()
        
    except Exception as e:
        print(f"Error clicking on {site_name}: {e}")

def handle_extract(driver, wait, action, site_name):
    try:

        time.sleep(5)
       
        container = driver.find_element(by=getattr(By, action['container_selector']['by'].upper()), value=action['container_selector']['value'])

        # Encuentra todos los elementos <li> dentro del contenedor
        print(container)
        rows = container.find_elements(by=getattr(By, action['item_selector']['by'].upper()), value=action['item_selector']['value'])


        print(f"Total rows found in {site_name}: {len(rows)}")

        extracted_data = []
        for row in rows:
            data = {}
            for field in action['fields']:
                try:
                    element = row.find_element(by=getattr(By, field['selector']['by'].upper()), value=field['selector']['value'])
                    data[field['name']] = element.text.strip() if field['name'] != 'link' else element.get_attribute('href').strip()
                except NoSuchElementException:
                    data[field['name']] = ''
            if any(data.values()):
                extracted_data.append(data)
                print(f"Extracted data: {data}")

        save_to_files(extracted_data, site_name)
    except Exception as e:
        print(f"Error extracting data in {site_name}: {e}")

def handle_extract_table(driver, wait, action, site_name):
    try:
        time.sleep(5)
        html_content = driver.page_source
        soup = BeautifulSoup(html_content, 'html.parser')
        table = soup.select_one(action['selector']['value'])
        rows = table.find_all('tr')

        extracted_data = []
        for row in rows[1:]:
            cells = row.find_all('td')
            if cells:
                data = {}
                for field in action['fields']:
                    try:
                        cell = cells[action['fields'].index(field)]
                        data[field['name']] = cell.get_text(strip=True)
                    except IndexError:
                        data[field['name']] = ''
                if any(data.values()):
                    extracted_data.append(data)
                    print(f"Extracted data: {data}")

        save_to_files(extracted_data, site_name)
    except Exception as e:
        print(f"Error extracting table data in {site_name}: {e}")

def handle_scroll(driver, wait, action, site_name):
    try:
        settings = action['settings']
        last_height = driver.execute_script("return document.body.scrollHeight")
        for i in range(settings['repetitions']):
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(settings['wait_time'])
            new_height = driver.execute_script("return document.body.scrollHeight")
            print(f"Scrolling {i+1}/{settings['repetitions']}: last_height = {last_height}, new_height = {new_height}")
            if new_height == last_height:
                break
            last_height = new_height
            time.sleep(2)
            for j in range(10):
                driver.execute_script("window.scrollBy(0, window.innerHeight / 10);")
                time.sleep(2)
        time.sleep(5)
    except Exception as e:
        print(f"Error scrolling in {site_name}: {e}")

def handle_send_keys(driver, wait, action, site_name):
    try:
        print(f"Sending keys to {site_name}")
        

        element = wait.until(EC.element_to_be_clickable((getattr(By, action['selector']['by'].upper()), action['selector']['value'])))
        element.send_keys(action['value'])
        element.send_keys(Keys.ENTER)
    except Exception as e:
        print(f"Error sending keys in {site_name}: {e}")

def handle_wait(driver, wait, action, site_name):
    try:
        if action['selector']['by'] == 'seconds':
            time.sleep(action['selector']['value'])
        else:
            wait.until(EC.presence_of_element_located((getattr(By, action['selector']['by'].upper()), action['selector']['value'])))
    except Exception as e:
        print(f"Error waiting for element in {site_name}: {e}")

def save_to_files(data, description):
    try:
        df = pd.DataFrame(data)
        df.to_csv(f'{description}.csv', index=False)
        print(f"Data saved to {description}.csv")
    except Exception as e:
        print(f"Error saving data to {description}.csv: {e}")


