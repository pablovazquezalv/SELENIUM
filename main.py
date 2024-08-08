import json
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
from Acciones import Accion

class WebScraper:

    def __init__(self, config_file):
        self.config_file = config_file
        self.driver = None
        self.wait = None
        options = Options()
        options.add_argument("--ignore-certificate-errors")
        options.add_argument("--ignore-ssl-errors")
        options.add_argument("--disable-web-security")
        options.add_argument("--allow-running-insecure-content")
        self.config = self.cargarJson()

    def cargarJson(self):
        with open(self.config_file, 'r') as file:
            return json.load(file)

    def configurarDriver(self):
        service = Service(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=service, options=Options())
        self.wait = WebDriverWait(self.driver, 20)

    def hacerAcciones(self):
        accion = Accion()
        for pagina in self.config['paginas']:
            self.driver.get(pagina['url'])
            for accion_config in pagina['acciones']:
                action_type = accion_config['tipo']
                print(f"Executing action {action_type} on {pagina['pagina']}")
                if action_type == 'click':
                    accion.hacerClick(self.driver, self.wait, accion_config, pagina['pagina'])
                elif action_type == 'esperar_elemento':
                    accion.esperarPagina(self.driver, self.wait, accion_config, pagina['pagina'])
                elif action_type == 'send_keys':
                    accion.escribirPalabra(self.driver, self.wait, accion_config, pagina['pagina'])
                elif action_type == 'scroll':
                    accion.hacerScroll(self.driver, self.wait, accion_config, pagina['pagina'])
                elif action_type == 'extract':
                    accion.extraerInfo(self.driver, self.wait, accion_config, pagina['pagina'])
                elif action_type == 'extract_table':
                    accion.extraerTabla(self.driver, self.wait, accion_config, pagina['pagina'])

    def quit(self):
        if self.driver:
            self.driver.quit()

if __name__ == "__main__":
    scraper = WebScraper(config_file='examen.json')
    scraper.configurarDriver()
    scraper.hacerAcciones()
    scraper.quit()