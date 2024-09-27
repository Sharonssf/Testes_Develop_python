import time
import selenium
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options

# Configurações do Chrome
chrome_options = Options()
chrome_options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36')

service = Service()
driver = webdriver.Chrome(service=service, options=chrome_options)

# Criação do DataFrame para armazenar os dados
data = {
    "Nome": [],
    "Link": []
}
df = pd.DataFrame(data)

try:
    driver.get("https://www.casasbahia.com.br/")
    driver.delete_all_cookies()

    # Durante o código foi utilizado alguns WebDriverWait e o sleep para garantir que o site carregaria por completo e para ajudar ao site não achar o bot
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "search-form-input"))
    )

    
    search_box = driver.find_element(By.ID, "search-form-input")
    search_box.send_keys("iPhone")

   
    search_box.send_keys(Keys.RETURN)

    # Percorrendo as 21 páginas do site das casas Bahia
    for page in range(1, 22):
        print(f"Raspando a página {page}...")

        WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'span[aria-hidden="true"]'))
        )

        # Extraindo informações dos produtos
        products = driver.find_elements(By.CSS_SELECTOR, 'span[aria-hidden="true"]')
        links = driver.find_elements(By.CSS_SELECTOR, 'a[data-testid="product-card-link-overlay"]')

        for product, link in zip(products, links):
            product_name = product.text
            product_link = link.get_attribute('href')

            # Adiciona os dados ao DataFrame
            df = df.append({"Nome": product_name, "Link": product_link}, ignore_index=True)

    
        try:
            
            next_button = WebDriverWait(driver, 20).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, 'button[aria-label="Próxima página"]'))
            )
            next_button.click()

            
            time.sleep(10)  
        except Exception as e:
            print(f"Erro ao navegar para a próxima página: {e}")
            break

        # Tentativa de verificar se o navegador ainda está aberto
        try:
            driver.title  
        except selenium.common.exceptions.NoSuchWindowException:
            print("A janela do navegador foi fechada.")
            break

    # Salva os dados em uma planilha Excel
    df.to_excel("produtos_casas_bahia.xlsx", index=False)
    print("Dados salvos na planilha 'produtos_casas_bahia.xlsx'.")

finally:
    # Fecha o navegador de forma segura
    driver.quit()
