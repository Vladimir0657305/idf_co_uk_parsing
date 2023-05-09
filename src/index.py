from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.proxy import Proxy, ProxyType
from seleniumwire import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver import Chrome
from bs4 import BeautifulSoup
import os
import dotenv
import requests
import time
from selenium.common.exceptions import TimeoutException
from urllib.parse import urljoin

# Загрузка настроек из файла .env
from dotenv import load_dotenv
load_dotenv()

base_url = "https://www.idf.co.uk/"

# Получаем общее количество страниц
url_page = "https://www.idf.co.uk/patients/find-a-doctor.aspx?Specialty=20&SubSpecialty=0&AreaCode=W1G&SearchCriteria=London&PageNumber=1"
response = requests.get(url_page)
soup_page = BeautifulSoup(response.content, 'html.parser')
pages = soup_page.find('p', class_='center').find_all('a')
last_page = int(pages[-1].get_text(strip=True))

# Получение учетных данных прокси-сервера из переменных окружения
PROXY_USERNAME = os.getenv('PROXY_USERNAME')
PROXY_PASSWORD = os.getenv('PROXY_PASSWORD')
# proxy_username = 'lum-customer-CUST_ID-zone-ZONE_NAME'
# proxy_password = 'PASSWORD'

# Указание настроек прокси-сервера
PROXY_HOST = "zproxy.lum-superproxy.io"
PROXY_PORT = "22225"

proxy = Proxy({
    'proxyType': 'MANUAL',
    'httpProxy': f"{PROXY_USERNAME}:{PROXY_PASSWORD}@{PROXY_HOST}:{PROXY_PORT}"
})

# Опции браузера Chrome
chrome_options = Options()
chrome_options.add_argument('--ignore-certificate-errors')
chrome_options.add_argument("--proxy-server=http://%s" % proxy.no_proxy)

# Указание пути к исполняемому файлу драйвера Chrome
driver_path = "C:/Program Files/Pyton/chromedriver"

# Инициализация драйвера Chrome
driver = webdriver.Chrome(service=Service(executable_path=driver_path), options=chrome_options)

# Выполнение запроса с использованием прокси-сервера
url = f'https://www.idf.co.uk/patients/find-a-doctor.aspx?Specialty=20&SubSpecialty=0&AreaCode=W1G&SearchCriteria=London&PageNumber=1'
driver.get(url)

# Ожидание загрузки страницы
wait = WebDriverWait(driver, 10)
wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'div.section')))

# Ввод текста в поисковую строку и отправка запроса
# search_box = driver.find_element(By.CSS_SELECTOR, 'input#id-search-field')
# search_box.send_keys('beautiful soup')
# search_box.submit()

# Ожидание загрузки страницы с результатами поиска
# wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'li.list-recent-events')))

# Получение HTML-кода страницы с результатами поиска
html = driver.page_source
soup = BeautifulSoup(html, 'html.parser')
links = soup.select('.docresults a[href]')
doctor_links = [urljoin(base_url, link['href']) for link in links]
print(doctor_links)

# for href in hrefs:
#     full_url = urljoin(base_url, href)
#     print(full_url)

# for link in links:
#     print(link['href'])


# Закрытие браузера
driver.quit()