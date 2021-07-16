
import pickle
from Credentials import UltraLibrarian_Credentials
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from AutoGui import AutoGUI

import time


UltraLibrarian_Login_URL = r"https://app.ultralibrarian.com/Account/Login"
UltraLibrarian__User_XPATH = r'//*[@id="Username"]'
UltraLibrarian__Password_XPATH =r'//*[@id="Password"]'
Login_Button_XPATH = r'/html/body/div/div/div/div/div[1]/form/fieldset/div[4]/button[1]'

Download_Button_XPATH='//*[@id="export-selection-btn"]'
STEP_Toggle_Button_XPATH = '//*[@id="export-submission-form"]/div[1]/div[1]/div[1]/div[1]/a'
STEP_Sel_Button_XPATH = '//*[@id="ef-1"]/div/div/label'
Cadence_Toggle_Options_XPATH = '//*[@id="export-submission-form"]/div[1]/div[1]/div[4]/div[1]/a'
Orcad_17_2_Select_XPATH = '//*[@id="ef-3"]/div/div[6]/label'
Allegro_17_2_Select_XPATH = '//*[@id="ef-3"]/div/div[3]/label'
Captcha_Button_XPATH = '//*[@id="recaptcha-anchor"]/div[1]'
Download_Now_Button_XPATH = '//*[@id="submit-export"]'
Captcha_Audio_Button_XPATH = '//*[@id="recaptcha-audio-button"]'
Play_Button_XPATH = '//*[@id=":5"]'
Reset_Button_XPATH = '//*[@id="reset-button"]'
Solve_Button_XPATH = '//*[@id="solver-button"]'
New_Challenge_Button_XPATH = '//*[@id="recaptcha-reload-button"]'



class UltraLibrarian:
    @staticmethod
    def Login(driver, wait):
        print("made it to ultra librarian login")
        credentials = UltraLibrarian_Credentials()
        print("user: ", credentials.username)
        driver.get( UltraLibrarian_Login_URL )
        time.sleep(0.25)
        print("wait for element to be clickable1")
        wait.until(EC.element_to_be_clickable((By.XPATH, Login_Button_XPATH )) )
        driver.find_element_by_xpath( UltraLibrarian__User_XPATH ).send_keys(credentials.username)
        time.sleep(0.25)
        driver.find_element_by_xpath( UltraLibrarian__Password_XPATH ).send_keys(credentials.password)
        time.sleep(1)
        driver.find_element_by_xpath( Login_Button_XPATH ).click()
        print("clicked login button")
        time.sleep(1)
        #pickle.dump( driver.get_cookies() , open("cookies.pkl","wb"))


    @staticmethod
    def Click_Download_Menu_Button(driver, wait):
        wait.until(EC.element_to_be_clickable((By.XPATH, Download_Button_XPATH)) )
        download_button = driver.find_element_by_xpath(Download_Button_XPATH)
        download_button.click()

    @staticmethod
    def Toggle_STEP_Menu(driver, wait):
        wait.until(EC.element_to_be_clickable((By.XPATH, STEP_Toggle_Button_XPATH)) )
        STEP_toggle = driver.find_element_by_xpath(STEP_Toggle_Button_XPATH)
        STEP_toggle.click()


    @staticmethod
    def Select_STEP_Model(driver, wait):
        wait.until(EC.element_to_be_clickable((By.XPATH, STEP_Sel_Button_XPATH)) )
        STEP_Sel = driver.find_element_by_xpath(STEP_Sel_Button_XPATH)
        STEP_Sel.click()


    @staticmethod
    def Toggle_Cadence_Menu(driver, wait):
        AutoGUI.screenshot()
        wait.until(EC.element_to_be_clickable((By.XPATH, Cadence_Toggle_Options_XPATH)) )
        Cadence_toggle = driver.find_element_by_xpath(Cadence_Toggle_Options_XPATH)
        Cadence_toggle.click()


    @staticmethod
    def Select_Capture_17_2(driver, wait):
        wait.until(EC.element_to_be_clickable((By.XPATH, Orcad_17_2_Select_XPATH)) )
        Orcad_Sel = driver.find_element_by_xpath(Orcad_17_2_Select_XPATH)
        Orcad_Sel.click()

    @staticmethod
    def Select_Allegro_17_2(driver, wait):
        AutoGUI.screenshot()
        wait.until(EC.element_to_be_clickable((By.XPATH, Allegro_17_2_Select_XPATH)) )
        Allegro_Sel = driver.find_element_by_xpath(Allegro_17_2_Select_XPATH)
        Allegro_Sel.click()


    #<div class="recaptcha-checkbox-border" role="presentation"></div>
    @staticmethod
    def Check_Captcha_Button(driver, wait):
        AutoGUI.screenshot()
        driver.execute_script("window.scrollTo(0,document.body.scrollHeight/8)")
        #wait.until(EC.visibility_of_element_located((By.XPATH, Captcha_Button_XPATH )))
        #wait.until(EC.element_to_be_clickable((By.XPATH, Captcha_Button_XPATH)) )
        #Captcha_Button = driver.find_element_by_xpath(Captcha_Button_XPATH)
        #UltraLibrarian.WriteXML(driver, "01.xml")

        driver.get_screenshot_as_file("01_im_not_a_robot.png")
        WebDriverWait(driver, 10).until(EC.frame_to_be_available_and_switch_to_it((By.CSS_SELECTOR,"iframe[name^='a-'][src^='https://www.google.com/recaptcha/api2/anchor?']")))
        AutoGUI.screenshot()
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, Captcha_Button_XPATH))).click()
        driver.find_element_by_xpath( Captcha_Button_XPATH )


        #Captcha_Button = driver.find_element_by_css_selector('#recaptcha-anchor > div.recaptcha-checkbox-border')
        #Captcha_Button.click()


    @staticmethod
    def WriteXML(driverw, filename):
        html = driverw.page_source
        writefile = open(filename, "w")
        writefile.write(html)
        writefile.close()

    @staticmethod
    def Click_Captcha_Audio_Button(driver, wait):
        AutoGUI.screenshot()
        wait.until(EC.element_to_be_clickable((By.XPATH, Captcha_Audio_Button_XPATH)) )

    @staticmethod
    def Captcha_Is_Solved():
        current_page = AutoGUI.screenshot()
        status_roi = AutoGUI.Look_For(current_page, Captcha_Checkbox)


    @staticmethod
    def Click_Solver_Button(driver, wait):
        AutoGUI.screenshot()
        UltraLibrarian.WriteXML(driver, "./src/02.xml")
        print("02 waiting for solver frame to be visible")
        driver.switch_to.default_content()
        #driver.get_screenshot_as_file("./src/02_captcha_popup.png")
        WebDriverWait(driver, 10).until(EC.frame_to_be_available_and_switch_to_it((By.CSS_SELECTOR,"iframe[title='recaptcha challenge']")))
        time.sleep(.5)
        #UltraLibrarian.WriteXML(driver, "./src/03.xml")
        print("03 popup here")
        #driver.get_screenshot_as_file("./src/03_before_clicking_audio_button.png")
        #WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, Solve_Button_XPATH))).click()
        AutoGUI.screenshot()
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, Captcha_Audio_Button_XPATH))).click()
        time.sleep(1)
        print(" looking for solver button")
        driver.switch_to.default_content()
        WebDriverWait(driver, 10).until(EC.frame_to_be_available_and_switch_to_it((By.CSS_SELECTOR,"iframe[title='recaptcha challenge']")))
        #WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, Solve_Button_XPATH))).click()
        #WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#rc-imageselect > div.rc-footer > div.rc-controls > div.primary-controls > div.rc-buttons > div.button-holder.help-button-holder"))).click()
        #solver_button = driver.find_element_by_css_selector("#rc-imageselect > div.rc-footer > div.rc-controls > div.primary-controls > div.rc-buttons > div.button-holder.help-button-holder")
        solver_button = driver.find_element_by_xpath(Solve_Button_XPATH)
        #shadow_parent = shadow_parent[0]
        print("04 clicking solve button (1)")
        #UltraLibrarian.WriteXML(driver, "./src/04.xml")
        #driver.get_screenshot_as_file("./src/04_before_clicking_solve_button.png")
        AutoGUI.screenshot()
        solver_button.click()
        time.sleep(1)
        print("05 reset button")
        UltraLibrarian.WriteXML(driver, "./src/05.xml")
        driver.get_screenshot_as_file("./src/05_before_clicking_reset_button.png")
        AutoGUI.screenshot()
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, Reset_Button_XPATH))).click()
        time.sleep(1)
        print("06 check captcha (2)")
        UltraLibrarian.WriteXML(driver, "./src/06.xml")
        driver.get_screenshot_as_file("./src/06_before_clicking_check_captcha_button.png")
        UltraLibrarian.Check_Captcha_Button(driver, wait)
        print("waiting for solver frame to be visible")
        driver.switch_to.default_content()
        WebDriverWait(driver, 10).until(EC.frame_to_be_available_and_switch_to_it((By.CSS_SELECTOR,"iframe[title='recaptcha challenge']")))
        time.sleep(0.5)
        print("07 new challenge button")
        UltraLibrarian.WriteXML(driver, "./src/07.xml")
        driver.get_screenshot_as_file("07_before_clicking_new_challenge_button.png")
        AutoGUI.screenshot()
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, New_Challenge_Button_XPATH))).click()
        time.sleep(0.25)
        print("08 audio button")
        UltraLibrarian.WriteXML(driver, "./src/08.xml")
        driver.get_screenshot_as_file("./src/08_before_clicking_audio_button.png")
        AutoGUI.screenshot()
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, Captcha_Audio_Button_XPATH))).click()
        shadow_parent = driver.find_elements_by_css_selector("#rc-imageselect > div.rc-footer > div.rc-controls > div.primary-controls > div.rc-buttons > div.button-holder.help-button-holder")
        shadow_parent = shadow_parent[0]
        print("09 clicking solve (2)")
        UltraLibrarian.WriteXML(driver, "./src/09.xml")
        driver.get_screenshot_as_file("./src/09_before_clicking_solve_button.png")
        shadow_parent.click()
        time.sleep(0.5)
        driver.switch_to.default_content()
        driver.execute_script("window.scrollTo(0,document.body.scrollHeight/4)")
        driver.get_screenshot_as_file("./src/10_before_clicking_download_button.png")
        UltraLibrarian.WriteXML(driver, "./src/10.xml")
        AutoGUI.screenshot()
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, Download_Now_Button_XPATH))).click()

    



    @staticmethod
    def Download_Files(driver, wait):
        wait.until(EC.element_to_be_clickable((By.XPATH, Download_Now_Button_XPATH)) )
        Download_Button = driver.find_element_by_xpath(Download_Now_Button_XPATH)
        Download_Button.click()

    @staticmethod
    def expand_shadow_element(driver, element):
        shadow_root = driver.execute_script('return arguments[0].shadowRoot', element)
        return shadow_root

"""
launch chrome
go to ultra librarian
click login
    navigate to login page 
    click in username box
    enter text
    click in password box
    enter text 
    hit enter
may auto login
click address bar
enter link
hit enter
part page
    -click download now
    -move over tree links
    - do ocr on links
    -move over link until cursor changes to hand
    -click link to expand tree
    -select appropriate links
    -click im not a robot captcha
    -click download now
    """