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
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
        self.driver = driver


    def iniciar_proceso(self, url, search_term):
        self.driver.get(url)
        i = 0
        # Buscar por header
        try:
            header = self.driver.find_element(By.TAG_NAME, "header")
            search_box = header.find_element(By.TAG_NAME, "input")
        except Exception as e:
            print("Header or input not found, searching for nav")

            nav = self.driver.find_element(By.TAG_NAME, "nav")
            search_box = nav.find_element(By.TAG_NAME, "input")

        time.sleep(5)
        search_box.send_keys(search_term)
        search_box.submit()

        wait = WebDriverWait(self.driver, 10)

        try:        
            products_wrapper = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "div.products.wrapper.grid.products-grid")))
        except Exception as e:
            print("Products wrapper not found, searching for col large-9")
            products_wrapper = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "div.yit-wcan-container")))
            

        last_height = self.driver.execute_script("return document.body.scrollHeight")

        while True:
          self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

          time.sleep(3)
            #calcular la altura        
          new_height = self.driver.execute_script("return document.body.scrollHeight")

          if new_height == last_height:
              break

          last_height = new_height

          time.sleep(5) 




        try:
            products_list = products_wrapper.find_element(By.CSS_SELECTOR, "ol.products.list.items.product-items")
            products = products_list.find_elements(By.TAG_NAME, "li")
        except Exception as e:
            print("Products list not found, searching for product-item")
            #class="products row row-small large-columns-3 medium-columns-3 small-columns-2"
            products_list = products_wrapper.find_element(By.CSS_SELECTOR, "div.products.row.row-small.large-columns-3.medium-columns-3.small-columns-2")
           #class="product-small col has-hover product type-product post-240661 status-publish first instock product_cat-otros product_tag-cap-care product_tag-new-era has-post-thumbnail shipping-taxable purchasable product-type-simple"
            products = products_list.find_elements(By.CSS_SELECTOR, "div.product-small.col.has-hover.product.type-product.post-240661.status-publish.first.instock.product_cat-otros.product_tag-cap-care.product_tag-new-era.has-post-thumbnail.shipping-taxable.purchasable.product-type-simple")
            
        
        product_names = []
        product_prices = []

        for product in products:
            try:
                product_name = product.find_element(By.CSS_SELECTOR, "a.product-item-link").text
                product_names.append(product_name)
                product_price = product.find_element(By.CSS_SELECTOR, "span.price").text
                product_prices.append(product_price)
            except Exception as e:
                print("Product name or price not found, skipping")
                #class="name product-title woocommerce-loop-product__title"
                product_name = product.find_element(By.CSS_SELECTOR,"p.name.product-title.woocommerce-loop-product__title").text
                product_names.append(product_name)
                #class="woocommerce-Price-amount amount"
                product_price = product.find_element(By.CSS_SELECTOR, "span.woocommerce-Price-amount.amount").text
                product_prices.append(product_price)





        df = pd.DataFrame({
            'Nombre del producto': product_names,
            'Precio del producto': product_prices
        })
        i += 1
        df.to_excel(f"productos{i}.xlsx", index=False)

    def cerrar_driver(self):
        self.driver.quit()


if __name__ == "__main__":
    scraping = Scraping()
    scraping.iniciar_proceso("https://2cap.com.mx", "gorras")
    print("Proceso terminado")
   
    scraping.iniciar_proceso("https://thefantown.com", "gorras")
    print("Proceso terminado")    
    scraping.iniciar_proceso("https://www.47brand.com", "caps")
    scraping.cerrar_driver()