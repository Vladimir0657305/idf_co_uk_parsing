from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.proxy import Proxy, ProxyType
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import os
import dotenv
import requests
import time
from selenium.common.exceptions import TimeoutException


from dotenv import load_dotenv
load_dotenv()

# proxy_username = os.getenv('PROXY_USERNAME')
# proxy_password = os.getenv('PROXY_PASSWORD')
proxy_username = 'brd-customer-hl_db7162d7-zone-unblocker'
proxy_password = '2ksf5kpyn6pk'

PROXY_HOST = "zproxy.lum-superproxy.io"
PROXY_PORT = "22225"

proxy = Proxy({
    'proxyType': 'MANUAL',
    'httpProxy': f"{proxy_username}:{proxy_password}@{PROXY_HOST}:{PROXY_PORT}"
})

chrome_options = Options()
chrome_options.add_argument('--ignore-certificate-errors')
chrome_options.add_argument("--proxy-server=http://%s" % proxy.no_proxy)

driver = webdriver.Chrome(service=Service(executable_path="C:/Program Files/Pyton/chromedriver"), options=chrome_options)

# def get_doctors_links(page):
#     url = f'https://www.idf.co.uk/patients/find-a-doctor.aspx?Specialty=20&SubSpecialty=0&AreaCode=W1G&SearchCriteria=London&PageNumber={page}'
#     driver.get(url)
#     time.sleep(55) 
#     wait = WebDriverWait(driver, 10)
#     wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, '.results-summary')))
#     html = driver.page_source
#     soup = BeautifulSoup(html, 'html.parser')
#     links = soup.select('.docresults a[href]')
#     doctor_links = [link['href'] for link in links]
#     return doctor_links

def get_doctors_links(page):
    url = f'https://www.idf.co.uk/patients/find-a-doctor.aspx?Specialty=20&SubSpecialty=0&AreaCode=W1G&SearchCriteria=London&PageNumber={page}'
    wait = WebDriverWait(driver, 20)
    while True:
        try:
            driver.get(url)
            wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, '.results-summary')))
            break
        except TimeoutException:
            driver.get(url)
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')
    links = soup.select('.docresults a[href]')
    doctor_links = [link['href'] for link in links]
    return doctor_links



def main():
    print(proxy_username, proxy_password)
    
    doctor_links = get_doctors_links(1)
    print(driver.current_url)
    print(doctor_links)


if __name__ == '__main__':
    main()
