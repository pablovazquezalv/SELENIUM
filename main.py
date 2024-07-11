from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import time

chrome_options = Options()


chrome_options.add_argument('--ignore-certificate-errors')
chrome_options.add_argument('--ignore-ssl-errors')
chrome_options.add_argument('--disable-web-security')   
chrome_options.add_argument('--allow-running-insecure-content')

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

driver.get("https://2cap.com.mx")

search_box = driver.find_element(By.ID, "search") 

search_box.send_keys("gorras")
search_box.submit()

wait = WebDriverWait(driver, 10)
products_wrapper = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "div.products.wrapper.grid.products-grid")))

last_height = driver.execute_script("return document.body.scrollHeight")

while True:
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        
    time.sleep(3)
        #calcular la altura        
    new_height = driver.execute_script("return document.body.scrollHeight")
        
    if new_height == last_height:
        break
        
    last_height = new_height

time.sleep(5) 

products_list = products_wrapper.find_element(By.CSS_SELECTOR, "ol.products.list.items.product-items")
products = products_list.find_elements(By.TAG_NAME, "li")

product_names = []
product_prices = []

for product in products:
    product_name = product.find_element(By.CSS_SELECTOR, "a.product-item-link").text
    product_names.append(product_name)
        
    product_price = product.find_element(By.CSS_SELECTOR, "span.price").text
    product_prices.append(product_price)
    
df = pd.DataFrame({
        'Nombre del producto': product_names,
        'Precio del producto': product_prices
})

df.to_excel('gorras.xlsx', index=False)
df.to_csv('gorras.csv', index=False)    
print("guardados")

driver.quit()