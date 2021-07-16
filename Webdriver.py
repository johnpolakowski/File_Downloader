
import undetected_chromedriver as uc
#uc.install()
from selenium.webdriver import Chrome
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.proxy import Proxy, ProxyType
from pathlib import Path
import time
from fake_useragent import UserAgent
import pickle


LOG_PATH = r'C:/Users/poppy/Documents/Cadence/Libraries/XML/Download/'


class Driver:
    @staticmethod
    def Get_ChromeDriver(Download_Directory):
        options = Driver.Get_Chrome_Options()
        log_path = Path(Download_Directory)
        headless_log_path = Path.joinpath(log_path.parent, 'headless_log') 
        driver = webdriver.Chrome(r"C:\Chromedriver\chromedriver_nodetect.exe", chrome_options=options, service_log_path=headless_log_path)
        driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
            "source": """
              Object.defineProperty(navigator, 'webdriver', {
                get: () => undefined
              })
            """
        })
        #driver.execute_cdp_cmd('Network.setUserAgentOverride', {"userAgent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.53 Safari/537.36'})
        #driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
        return driver


    @staticmethod
    def Get_uChrome():  
        options = Driver.Get_Chrome_Options()
        driver = Chrome(options=options)
        driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
        return driver

    @staticmethod
    def Get_Chrome_Options():
        options = webdriver.ChromeOptions()
        prefs = {}
        prefs["profile.default_content_settings.popups"]=0
        prefs["download.prompt_for_download"]=False
        prefs["download.directory_upgrade"]=True
        prefs["plugins.always_open_pdf_externally"]=True
        options.add_experimental_option("prefs", prefs)
        options.add_argument("start-maximized");
        options.add_experimental_option('excludeSwitches', ['enable-logging'])
        options.add_argument('--ignore-certificate-errors')
        options.add_argument(f'user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36')
        #options.add_argument("--disable-extensions")
        options.add_argument("--disable-gpu")                #applicable to windows os only
        options.add_argument("--user-data-dir=chrome-data")
        options.add_argument("--no-sandbox")
        options.add_extension('./buster_extension.crx')
        options.add_argument(r"user-data-dir=C:\Users\poppy\AppData\Local\Google\Chrome\User Data\Default") #Path to your chrome profile
        #options.add_argument("window-size=1280,800")
        #options.add_argument('--user-agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36"')
        #options.add_user_profile_preference("credentials_enable_service", false)
        #options.AddUserProfilePreference("profile.password_manager_enabled", false)

        #options.add_argument("--incognito")
        #options.add_argument("--remote-debugging-port=9225")
        options.add_argument("--disable-blink-features")
        options.add_argument("--disable-blink-features=AutomationControlled")
        #options.add_experimental_option('useAutomationExtension', False)
        #options.add_experimental_option("excludeSwitches", ["enable-automation"])
        return options


#Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36


    @staticmethod
    def Save_Cookies(driver):
        pickle.dump( driver.get_cookies() , open("cookies.pkl","wb"))
        
    @staticmethod
    def Open_Cookies(driver):
        cookies = pickle.load(open("cookies.pkl", "rb"))
        for cookie in cookies:
            driver.add_cookie(cookie)

"""
Things done:
replacing cdc in exe
no debug port (enables webdriver flag)
disabled webdriver flag with            options.add_argument("--disable-blink-features=AutomationControlled")
set webdriver flag to undefined: driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
set window size: option.add_argument("window-size=1280,800")
"""