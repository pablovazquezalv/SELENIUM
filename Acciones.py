import time
import pandas as pd
import os
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup

class Accion:

    def hacerClick(self, driver, wait, accion, pagina):
        try:
        
            print(f"Clicking on {pagina}")
            print(accion['selector']['by'])
            print(accion['selector']['value'])

            element = wait.until(EC.element_to_be_clickable((getattr(By, accion['selector']['by'].upper()), accion['selector']['value'])))
            element.click()
            
        except Exception as e:
            print(f"Error clicking on {pagina}: {e}")

    def esperarPagina(self, driver, wait, accion, pagina):
        try:

                time.sleep(5)
            
                container = driver.find_element(by=getattr(By, accion['container_selector']['by'].upper()), value=accion['container_selector']['value'])

                # Encuentra todos los elementos <li> dentro del contenedor
                print(container)
                rows = container.find_elements(by=getattr(By, accion['item_selector']['by'].upper()), value=accion['item_selector']['value'])

                #ver las rows
                pd.DataFrame(rows).to_csv('rows.csv')
                print(f"Total rows found in {pagina}: {len(rows)}")
                print(rows) 
                extracted_data = []
                for row in rows:
                    data = {}
                    for field in accion['fields']:
                        try:
                            element = row.find_element(by=getattr(By, field['selector']['by'].upper()), value=field['selector']['value'])
                            data[field['name']] = element.text.strip() if field['name'] != 'link' else element.get_attribute('href').strip()
                        except NoSuchElementException:
                            data[field['name']] = ''
                    if any(data.values()):
                        extracted_data.append(data)
                        print(f"Extracted data: {data}")

                self.save_to_files(extracted_data, pagina)

        except Exception as e:
            print(f"Error extracting data in {pagina}: {e}")
        
    def escribirPalabra(self, driver, wait, accion, pagina):
        try:
            print(f"Sending keys to {pagina}")
            
            time.sleep(10)
            element = wait.until(EC.element_to_be_clickable((getattr(By, accion['selector']['by'].upper()), accion['selector']['value'])))
            element.send_keys(accion['value'])
            element.send_keys(Keys.ENTER)
        except Exception as e:
            print(f"Error sending keys in {pagina}: {e}")

    def hacerScroll(self, driver, wait, accion, pagina):
        try:
            if accion['selector']['by'] == 'seconds':
                time.sleep(accion['selector']['value'])
            else:
                wait.until(EC.presence_of_element_located((getattr(By, accion['selector']['by'].upper()), accion['selector']['value'])))
        except Exception as e:
            print(f"Error waiting for element in {pagina}: {e}")

    def extraerInfo(self, driver, wait, accion, pagina):
        try:
            time.sleep(10)
            container = driver.find_element(by=getattr(By, accion['container_selector']['by'].upper()), value=accion['container_selector']['value'])
            # Encuentra todos los elementos <li> dentro del contenedor
            print(container)
            rows = container.find_elements(by=getattr(By, accion['item_selector']['by'].upper()), value=accion['item_selector']['value'])

            print(f"Total rows found in {pagina}: {len(rows)}")

            extracted_data = []
            for row in rows:
                data = {}

                for field in accion['fields']:
                    try:
                        element = row.find_element(by=getattr(By, field['selector']['by'].upper()), value=field['selector']['value'])
                        print(f"Element found for field '{field['name']}': {element.text}")
                        data[field['name']] = element.text.strip() if field['name'] != 'link' else element.get_attribute('href').strip()
                    except Exception as e:
                        print(f"Error extracting field '{field['name']}' in {pagina}: {e}")
                        data[field['name']] = None  # Puedes optar por guardar 'None' o algún valor predeterminado

                if any(data.values()):
                    extracted_data.append(data)
                    print(f"Extracted data: {data}")

            print(f"Extracted data from {pagina}: {extracted_data}")   
            self.save_to_files(extracted_data, pagina)
        except Exception as e:
            print(f"Error extracting data in {pagina}: {e}")      
    # def extraerInfo(self, driver, wait, accion, pagina):
    #     try:

    #         time.sleep(5)
        
    #         container = driver.find_element(by=getattr(By, accion['container_selector']['by'].upper()), value=accion['container_selector']['value'])

    #         # Encuentra todos los elementos <li> dentro del contenedor
    #         print(container)
    #         rows = container.find_elements(by=getattr(By, accion['item_selector']['by'].upper()), value=accion['item_selector']['value'])


    #         print(f"Total rows found in {pagina}: {len(rows)}")

    #         extracted_data = []
    #         for row in rows:
    #             data = {}
    #             for field in accion['fields']:
    #                 try:
    #                     element = row.find_element(by=getattr(By, field['selector']['by'].upper()), value=field['selector']['value'])
    #                     data[field['name']] = element.text.strip() if field['name'] != 'link' else element.get_attribute('href').strip()
    #                 except NoSuchElementException:
    #                     data[field['name']] = ''
    #             if any(data.values()):
    #                 extracted_data.append(data)
    #                 print(f"Extracted data: {data}")

    #         self.save_to_files(extracted_data, pagina)
    #     except Exception as e:
    #         print(f"Error extracting data in {pagina}: {e}")
        

    def extraerTabla(self, driver, wait, accion, pagina):
        
        try:
            time.sleep(5)
            html_content = driver.page_source
            soup = BeautifulSoup(html_content, 'html.parser')
            table = soup.select_one(accion['container_selector']['value'])
            rows = table.find_all('tr')
            extracted_data = []
            for row in rows[1:]:
                cells = row.find_all('td')
                if cells:
                    data = {}
                    for field in accion['fields']:
                        try:
                            if 'property' in field:
                                element = driver.find_element_by_css_selector(field['container_selector']['value'])
                                if field['property'] == 'is_visible':
                                    data[field['name']] = element.is_displayed()
                                elif field['property'] == 'is_active':
                                    data[field['name']] = 'active' in element.get_attribute('class')
                            else:
                                cell = cells[accion['fields'].index(field)]
                                data[field['name']] = cell.get_text(strip=True)
                        except IndexError:
                            data[field['name']] = ''
                    if any(data.values()):
                        extracted_data.append(data)
                        print(f"Extracted data from {pagina}: {data}")
            # Guarda los datos o haz algo con ellos
            print(f"Extracted data from {pagina}: {extracted_data}")
            self.save_to_files(extracted_data, pagina)
        except Exception as e:
            print(f"Error extracting table data on {pagina}: {e}")

    def save_to_files(self,data, description):
            try:
                df = pd.DataFrame(data)

                df.to_csv(f'{description}.csv', index=False)
                print(f"Data saved to {description}.csv")
            except Exception as e:
                print(f"Error saving data to {description}.csv: {e}")