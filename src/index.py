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
from bs4.element import Tag
import re
import os
import dotenv
import requests
import time
from selenium.common.exceptions import TimeoutException
from urllib.parse import urljoin
import csv

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
last_page = 2

# Получение учетных данных прокси-сервера из переменных окружения
PROXY_USERNAME = os.getenv('PROXY_USERNAME')
PROXY_PASSWORD = os.getenv('PROXY_PASSWORD')

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

# Создаем список для хранения всех ссылок на врачей
all_doctor_links = []

# Создаем цикл для перебора всех страниц
for page in range(1, last_page+1):
    # Формируем ссылку на текущую страницу
    url = f'https://www.idf.co.uk/patients/find-a-doctor.aspx?Specialty=20&SubSpecialty=0&AreaCode=W1G&SearchCriteria=London&PageNumber={page}'

    # Загружаем страницу
    driver.get(url)

    # Ожидание загрузки страницы
    wait = WebDriverWait(driver, 10)
    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'div.section')))

    # Получение HTML-кода страницы с результатами поиска
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')
    links = soup.select('.docresults a[href]')
    doctor_links = [urljoin(base_url, link['href']) for link in links]

    # Добавляем найденные ссылки на врачей на текущей странице в общий список
    all_doctor_links.extend(doctor_links)

# Открываем CSV-файл для записи
with open('doctors.csv', 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)

    # Записываем заголовки столбцов
    writer.writerow(['Counter', 'Name', 'Qualifications', 'Specialty', 'Address', 'Telephone', 'Email', 'Website', 'Biography', 'Research Interests'])

    # Создаем глобальный счетчик
    counter = 1

    # Создаем цикл для перебора всех врачей
    for doctor_link in all_doctor_links:
        # Загружаем страницу врача
        driver.get(doctor_link)
        # Ожидание загрузки страницы
    wait = WebDriverWait(driver, 10)
    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'div.content3')))

    # Получение HTML-кода страницы врача
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')

    # Извлечение данных врача
    try:
        name = soup.select_one('h2.memberprofile').get_text(strip=True)
    except AttributeError:
        name = 'No name data'
    try:
        qualifications = soup.select_one('.qualifications').get_text(strip=True)
    except AttributeError:
        qualifications = 'No qualifications data'
    try:
        specialty_label = soup.select_one('.profile-specialty')
        specialty = specialty_label.contents[1].strip()
    except AttributeError:
        specialty = 'No specialty data'
    try:
        address_label = soup.find('li', {'id': 'ctl00_MainContentPlaceHolder_AddressLi'})
        address_items = address_label.contents
        address = ''.join([str(item).strip() for item in address_items if not (item.name == 'span' and item.get('class') == 'strong')])
        soup_address = BeautifulSoup(address, 'html.parser')
        for strong_tag in soup_address.find_all('span', {'class': 'strong'}):
            strong_tag.decompose()
        address = soup_address.get_text().strip()
    except AttributeError:
        address = 'No address data'
    try:
        telephone_label = soup.find('li', {'id': 'ctl00_MainContentPlaceHolder_TelephoneLi'})
        telephone_span = telephone_label.find('span', {'class': 'strong'}, text='Appointments Telephone:')
        telephone = telephone_span.find_next_sibling('br').next_sibling.strip().replace('Tel: ', '')
    except AttributeError:
        telephone = 'No telephone data'
    try:
        email_label = soup.find('li', {'id': 'ctl00_MainContentPlaceHolder_EmailAddressLi'})
        email = email_label.find('a', href=True).text.strip()
    except AttributeError:
        email = 'No email data'
    try:
        website_label = soup.find('li', {'id': 'ctl00_MainContentPlaceHolder_WebsiteLi'})
        website = website_label.find('a', href=True).text.strip()
    except AttributeError:
        website = 'No website data'
    

    print(f"Name: {name}")
    print(f"Qualifications: {qualifications}")
    print(f"Specialty: {specialty}")
    print(f"Address: {address}")
    print(f"Telephone: {telephone}")
    print(f"Email: {email}")
    print(f"Website: {website}")


    # Записываем данные врача в CSV-файл
    writer.writerow([counter, name, qualifications, specialty, address, telephone, email, website])

    # Увеличиваем глобальный счетчик на 1
    counter += 1
# Закрываем браузер
driver.quit()