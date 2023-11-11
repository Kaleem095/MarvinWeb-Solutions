from selenium import webdriver
import chromedriver_autoinstaller
import os, threading, time, psutil, csv
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

class MarvinGWebSolution:

    def __init__(self):
        self.chrome_options = webdriver.ChromeOptions()
        self.chrome_options.add_argument("--disable-gpu")
        self.chrome_options.add_argument("--disable-notifications")
        self.chrome_options.add_argument("--disable-popup-blocking")
        self.chrome_options.add_argument("--profile-directory=Default")
        self.chrome_options.add_argument("--ignore-certificate-errors")
        self.chrome_options.add_argument("--disable-plugins-discovery")
        self.chrome_options.add_experimental_option("debuggerAddress", "localhost:9222")

    def fileHeader(self):
        header = ['Info Email']
        # with open('MarvinWebTelephone.csv', 'w', encoding='UTF-8', newline='') as file:
        with open('MarvinWebTelephonesData.csv', 'w', encoding='UTF-8', newline='') as file:

            csv.writer(file).writerow(header)
    
    def saveToExcelDb(self, row):
        # with open('MarvinWebTelephone.csv', 'a', encoding='UTF-8', newline='') as file:
        with open('MarvinWebTelephonesData.csv', 'a', encoding='UTF-8', newline='') as file:
            csv.writer(file).writerow(row)

    def getPath(self):
        return os.system('"C:\Program Files\Google\Chrome\Application\chrome.exe" --remote-debugging-port=9222')

    def closeBrowser(self):
        try:
            PROCNAME = "chromedriver.exe"
            userName = os.getlogin()
            for proc in psutil.process_iter():
                if proc.name() == PROCNAME or proc.name() == 'chrome.exe':
                    if str(userName) in str(proc.username()):
                        proc.kill()
                
            print(proc.username())
        except Exception as ex:
            print(str(ex))

    def openBrowser(self):
        path = chromedriver_autoinstaller.install(cwd=True)
        time.sleep(2)
        self.closeBrowser()
        time.sleep(2)
        th = threading.Thread(target=self.getPath, args=())
        th.daemon = True
        th.start()
        time.sleep(3)
        driver = webdriver.Chrome(options=self.chrome_options)
        return driver
    
    def fetch_links(self, driver):
        pgNo = 1
        maxPage = 11
        linksList = []
        while True:
            siteurl = 'https://www.11880.com/suche/Webdesign/deutschland?eigenschaften=email&sorte=%7C&modul=direct'
            page_url = f'{siteurl}&page={pgNo}'
            print(f'[Getting-Page] - LINK: {page_url}')
            driver.get(page_url)
            sleepTime = int(input(f'Enter script sleep Time You want.?\n'))
            time.sleep(sleepTime)
            print(f'[SOLVING-CAPTCHA] - [PLEASE-WAIT]: Till Solved')
            try:
                link_cards = driver.find_elements(By.XPATH, '//div[contains(@class, "details__container")]//div[contains(@class, "result-list-entry-opening-hours")]')
                nextPage = driver.find_element(By.XPATH, '//div[@class="pagination"]//div[@class="next"]')
                if not nextPage:break
                if pgNo == maxPage:break
                print(f'[Get-Length]: {len(link_cards)}')
                for link in link_cards:
                    links = link.get_attribute('data-href')
                    if links:
                        link = f'https://www.11880.com{links}'
                        with open('links.txt', 'a', encoding='UTF-8') as file: file.write(link + '\n')
                        linksList.append(link)
            except:
                print(f'Unable To Solve...[SORRY]')
            
            pgNo += 1
        return linksList
    
    def main(self, driver, url):
        driver.get(url)
        time.sleep(10)
        with open('data.html', 'w', encoding='UTF-8') as file: file.write(driver.page_source)
        try:
            emailTag = driver.find_element(By.XPATH, '//div[@class="entry-detail-list__item"]//div[contains(@class, "list__icon--email")]/following-sibling::div')
            infoEmail = emailTag.text if emailTag else 'None'
            csvRow = [infoEmail]
            self.saveToExcelDb(csvRow)
            print(f'[GETTING-MAIL] - [DONE] - Emails: {infoEmail}')
        except:pass


if __name__ == '__main__':
    MarvinWeb = MarvinGWebSolution()
    MarvinWeb.fileHeader()
    driver = MarvinWeb.openBrowser()
    links = MarvinWeb.fetch_links(driver)
    for link in links:
        link = link.strip()
        print(f'GETTING-INFO: [LINKS]: {link}')
        MarvinWeb.main(driver, link)
