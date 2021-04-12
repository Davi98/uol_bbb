import time
from log import log
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
import json


class Browser:

    def __init__(self):
        self.options = Options()
        self.options.add_argument('--headless')
        self.options.add_argument('--disable-gpu')
        self.options.add_argument('--disable-dev-shm-usage')
        self.options.add_argument('--disable-extensions')
        self.options.add_argument('--no-sandbox')
        self.driver = webdriver.Chrome(options=self.options)
        self.session_id = self.driver.session_id
        self.command_executor_url = self.driver.command_executor._url
    
    def goto(self):
        try:
            self.driver.get("https://tvefamosos.uol.com.br/bbb/")
            time.sleep(3)
            self.driver.find_element_by_xpath('//*[@id="id56400"]/div[1]/div/div[3]/div/div[5]/a').click()
            time.sleep(10)
        except Exception as err:
            log().error(f"Error in method goto: {type(err)} > {err}")
            raise err
    

    def __del__(self):
        if hasattr(self, 'driver') and self.driver is not None:
            self.driver.quit()

