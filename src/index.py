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

from dotenv import load_dotenv
load_dotenv()
# os.environ['PROXY_USERNAME'] = 'brd-customer-hl_db7162d7-zone-unblocker'
# os.environ['PROXY_PASSWORD'] = '2ksf5kpyn6pk'
proxy_username = os.environ.get('PROXY_USERNAME')
proxy_password = os.environ.get('PROXY_PASSWORD')


PROXY_HOST = "zproxy.lum-superproxy.io"
PROXY_PORT = "22225"
PROXY_USER = os.getenv('PROXY_USERNAME')
PROXY_PASS = os.getenv('PROXY_PASSWORD')

proxy = Proxy({
    'proxyType': 'MANUAL',
    'httpProxy': f"{PROXY_USER}:{PROXY_PASS}@{PROXY_HOST}:{PROXY_PORT}"
})

chrome_options = Options()
chrome_options.add_argument('--ignore-certificate-errors')
chrome_options.add_argument("--proxy-server=http://%s" % proxy.noProxy)

driver = webdriver.Chrome(options=chrome_options)

def get_doctors_links(page):
    url = f'https://www.idf.co.uk/patients/find-a-doctor.aspx?Specialty=20&SubSpecialty=0&AreaCode=W1G&SearchCriteria=London&PageNumber={page}'
    driver.get(url)
    wait = WebDriverWait(driver, 10)
    wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, '.results-summary')))
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')
    links = soup.select('.docresults a[href]')
    doctor_links = [link['href'] for link in links]
    return doctor_links


def main():
    print(os.getenv('PROXY_USERNAME'))
    print(os.getenv('PROXY_PASSWORD'))
    doctor_links = get_doctors_links(1)
    print(doctor_links)


if __name__ == '__main__':
    main()
