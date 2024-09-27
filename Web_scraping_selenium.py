from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options


chrome_options = Options()
chrome_options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36')

service = Service()
driver = webdriver.Chrome(service=service, options=chrome_options)
driver.delete_all_cookies()
driver.get("https://www.casasbahia.com.br/")


WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.ID, "search-form-input"))
)


search_box = driver.find_element(By.ID, "search-form-input")
search_box.send_keys("iPhone")
time.sleep(10)

search_box.send_keys(Keys.RETURN)
time.sleep(10)
driver.save_screenshot('erro.png')
