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
doctors_data = []

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

page = 1
# Создаем глобальный счетчик
counter = 1
# Создаем цикл для перебора всех страниц
while True:
    # Формируем ссылку на текущую страницу
    url = f'https://www.idf.co.uk/patients/find-a-doctor.aspx?Specialty=20&SubSpecialty=0&AreaCode=W1G&SearchCriteria=London&PageNumber={page}'

    # Загружаем страницу
    driver.get(url)

    # Ожидание загрузки страницы
    wait = WebDriverWait(driver, 10)
    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'div.diversity')))

    # Получение HTML-кода страницы с результатами поиска
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')
    links = soup.select('.docresults a[href]')
    all_doctor_links = [urljoin(base_url, link['href']) for link in links]

    # Создаем цикл для перебора всех врачей
    for doctor_link in all_doctor_links:
        print(doctor_link)
        # Загружаем страницу врача
        driver.get(doctor_link)
        # Ожидание загрузки страницы
        wait = WebDriverWait(driver, 10)
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'footer')))
        print('GET')

    # Получение HTML-кода страницы врача
        html = driver.page_source
        soup = BeautifulSoup(html, 'html.parser')
        print('WORKING')
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
    
    # Добавляем данные врача в список
        # doctors_data.append([counter, name, qualifications, specialty, address, telephone, email, website])
        doctors_data.append({
            'Counter': counter,
            'Name': name,
            'Qualifications': qualifications,
            'Specialty': specialty,
            'Address': address,
            'Telephone': telephone,
            'Email': email,
            'Website': website
        })

# Печатаем данные для проверки
        # for doctor in doctors_data:
        #     print(doctor)

    # Увеличиваем глобальный счетчик на 1
        counter += 1

    # Проверяем, является ли текущая страница последней
    if page == last_page:
        break
    # Увеличиваем значение счетчика цикла
    page += 1
# Закрываем браузер
driver.quit()

# Записываем данные в файл CSV
import csv

with open('doctors.csv', mode='w', encoding='utf-8', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['Counter','Name', 'Qualifications', 'Specialty', 'Address', 'Telephone', 'Email', 'Website'])
    for doctor in doctors_data:
        print(doctor)
        writer.writerow(doctor.values())

print('Data has been scraped and saved to doctors_data.csv')


