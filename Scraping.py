from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
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
        chrome_options.add_argument('--disable-blink-features=AutomationControlled')
        chrome_options.add_argument("start-maximized")

        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

    def iniciar_proceso(self, url, search_term):
        self.driver.get(url)

        # Buscar por header
        try:
            header = self.driver.find_element(By.TAG_NAME, "header")
            search_box = header.find_element(By.TAG_NAME, "input")
        except Exception as e:
            print("Header or input not found, searching for nav")
            # Si no encuentra el header o el input, buscar por nav
            nav = self.driver.find_element(By.TAG_NAME, "nav")
            search_box = nav.find_element(By.TAG_NAME, "input")

        # Ingresar el término de búsqueda y enviar
        time.sleep(5)
        search_box.send_keys(search_term)
        search_box.submit()

        wait = WebDriverWait(self.driver, 10)
        
        try:
            products_wrapper = wait.until(EC.presence_of_element_located((By.TAG_NAME, "ol")))
            products_list = products_wrapper.find_elements(By.TAG_NAME, "li")
        except Exception as e:
            print("Products not found with tag ol, searching by class")

            # Intentar hacer clic en el botón del CAPTCHA si está presente
            try:
                captcha_button = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "yCmsContentSlot.navigation-menu-desktop.hidden-sm.hidden-xs")))
                actions = ActionChains(self.driver)
                actions.click_and_hold(captcha_button).pause(5).release().perform()
                print("Captcha resolved and button clicked")
            except Exception as e:
                print("Captcha button not found or not clickable")

            # Buscar por la clase específica en los divs
            products_wrapper = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".products.columns-4")))
            products_list = products_wrapper.find_elements(By.CSS_SELECTOR, "div.product-small.col.has-hover")

        last_height = self.driver.execute_script("return document.body.scrollHeight")

        while True:
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(3)
            new_height = self.driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height

        time.sleep(5)

        product_names = []
        product_prices = []

        for product in products_list:
            try:
                product_name = product.find_element(By.CSS_SELECTOR, "p.name.product-title.woocommerce-loop-product__title a").text
                product_names.append(product_name)
            except Exception as e:
                print("No se encontró el nombre del producto")
                product_names.append("N/A")

            try:
                product_price = product.find_element(By.CSS_SELECTOR, "span.price span.woocommerce-Price-amount.amount").text
                product_prices.append(product_price)
            except Exception as e:
                print("No se encontró el precio del producto")
                product_prices.append("N/A")

        df = pd.DataFrame({
            'Nombre del producto': product_names,
            'Precio del producto': product_prices
        })

        df.to_excel(f'{search_term}.xlsx', index=False)

    def cerrar_driver(self):
        self.driver.quit()


if __name__ == "__main__":
    scraping = Scraping()
    scraping.iniciar_proceso("https://2cap.com.mx", "gorras")
    print("Proceso terminado")
   
    scraping.iniciar_proceso("https://thefantown.com/?s=gorras&post_type=product", "gorras")
    print("Proceso terminado")    
    scraping.iniciar_proceso("https://www.47brand.com", "caps")
    scraping.cerrar_driver()