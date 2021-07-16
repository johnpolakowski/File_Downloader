#scraper_digikey.py
# This is the digikey scraper that I made for BOMGarten. Because python is a scripting language
# I decided against implementing an "interface" like with what you'd see in C# or "virtual" like
# you might see in C++.
#
# In order for a scraper to be a scraper it just needs to implement the get functions below and have
# the same signitures.


# import wx
# import urllib2
import os
import csv
import re
import sys
import requests
import urllib3
import urllib.request
import time
from Stat_File import FileHelper
from bs4 import BeautifulSoup, NavigableString, Tag
from CAD_Object import CAD_Data_Object
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
import io
from lxml import etree
from stat import ST_CTIME
import shutil
from Webdriver import Driver
from pathlib import Path


CHROMEDRIVER_PATH = r'C:\Chromedriver\chromedriver.exe'
Snap_Eda_Login_Link = 'https://www.snapeda.com/account/login/'
DESTINATION_DIR = r'C:/Users/poppy/Documents/Cadence/Libraries/XML/Download/'
DOWNLOAD_DIR = r"C:/Users/poppy/Downloads/"

Symbol_Button_XPATH = '//*[@id="main-col"]/div[2]/div[1]/div/div[3]/div/a/i'
Footprint_Button_XPATH = '//*[@id="main-col"]/div[2]/div[2]/div/div[3]/div/a'
Orcad_Button_XPATH = '//*[@id="orange-gradient-list"]/li[6]/a'
Login_Button_XPATH = '//*[@id="s-form-login"]/fieldset/div/input'
STEP_Model_Tab_XPATH = '//*[@id="main-col"]/div[1]/ul/li[2]'
STEP_Model_Button_XPATH = '//*[@id="download_step_model"]'




class SnapEda_Result:
    def __init__(self):
        self.Has_Symbol = False
        self.Has_Footprint = False
        self.Has_STEP = False
        self.Has_Simulation = False
        self.URL = None
        self.manufacturer_part_num = None

class snapeda_parser:
    def __init__(self, driver, report_file):
        self.search_string = None
        self.url_string = None
        self.snapeda_search_url = None          #self.url_string + self.search_string  # create search URL from dikey site URL and MFGpart #
        self.manufacturer_part_num = None
        self.search_results = []
        self.driver = driver
        self.wait = WebDriverWait(self.driver, 100)


    def build_search_url(self, part_num):
        self.search_string = part_num
        self.manufacturer_part_num = part_num
        self.snapeda_search_url = 'https://www.snapeda.com/search/?q={}&search-type=parts'.format(self.search_string)

    def Sign_In_to_SnapEda(self):
        self.driver.get(Snap_Eda_Login_Link)
        self.wait.until(EC.element_to_be_clickable((By.XPATH, Login_Button_XPATH)) )
        self.driver.find_element_by_xpath('//*[@id="id_username"]').send_keys("frankie_forceps")
        self.driver.find_element_by_xpath('//*[@id="id_password"]').send_keys("guVqZ9vV8jYmRhL")
        self.driver.find_element_by_xpath('//*[@id="s-form-login"]/fieldset/div/input').click()
        time.sleep(2)

    def Write_XML_To_File(self, xml):
        with io.open("snap.xml", "w", encoding="utf-8") as file:
            if isinstance(xml, list):
                for item in xml:
                    self.Write_XML_Element_To_File(item, file)
            else:
                self.Write_XML_Element_To_File(xml, file)
            file.flush()
            file.close()

    def enable_download(self):
        self.driver.command_executor._commands["send_command"] = ("POST", '/session/$sessionId/chromium/send_command')
        params = {'cmd':'Page.setDownloadBehavior', 'params': {'behavior': 'allow', 'downloadPath': DOWNLOAD_DIR}}
        self.driver.execute("send_command", params)

    def Write_XML_Element_To_File(self, xml_content, file):
        xml_str = self.Prettify_XML(xml_content) + "\n"
        file.write(xml_str)


    def Prettify_XML(self, xml):
        xml_str = str(xml)
        root_str = etree.fromstring(xml_str)
        xml_str = etree.tostring(root_str, pretty_print=True).decode()
        return str(xml_str)

    def Num_Search_Results(self):
        if self.snapeda_search_url:
            print("Search URL:  {}\n".format(self.snapeda_search_url) )
            self.driver.get(self.snapeda_search_url)
            self.wait.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="results"]/table')) )
            html = self.driver.page_source
            if html:
                soup = BeautifulSoup(html, "lxml")
                if soup:
                    div = soup.find("div", {"id": "results"})
                    if div:
                        table = div.find("table", {"class": ["table", "search-results-table"]})
                        if table:
                            tbody = table.find("tbody")
                            if tbody:
                                table_rows = tbody.find_all("tr")
                            if table_rows:
                                self.Write_XML_To_File(table_rows)
                                for result in table_rows:
                                    self.search_results.append(result)
                                return len(self.search_results)

    def Get_Results_With_CAD(self):
        if len(self.search_results) > 0:
            result_list = []
            for result in self.search_results:
                #soup = etree.XML(str(result))
                result = str('<?xml version="1.0" encoding="utf-8" ?>') + str(result) 
                soup2 = BeautifulSoup(result, "html.parser")

                data = self.Get_Result_CAD_Data(soup2)
                if data is not None:
                    data.URL = self.Get_Result_URL(soup2)
                    result_list.append(data)
            return result_list

    def Get_Result_URL(self, xml):
        td = xml.find("td", {"class": "part-result2"})
        if td:
            url = td.find("a").get("href")
            print("\t", url)
            return url

    def Get_Result_CAD_Data(self, xml ):
        result = None
        for index in range(0,len(self.search_results)):
            selector_string = "data{}".format(index)
            td = xml.find("td", {"id": selector_string})
            if td:
                img_tags = td.find_all("img")
                if img_tags:
                    for img in img_tags:
                        text = img.get("data-original-title")
                        if "Symbol" in text or "Footprint" in text or "3D" in text or "Sim" in text:
                            if not "not" in text:
                                if result == None:
                                    result = SnapEda_Result()
                                if "Symbol" in text:
                                    result.Has_Symbol = True
                                if "Footprint" in text:
                                    result.Has_Footprint = True
                                if "3D" in text:
                                    result.Has_STEP = True
                                if "Sim" in text:
                                    result.Has_Simulation = True
                    return result

    def Print_CAD_Result(self, result):
        str = "Result has: [ "
        if result.Has_Symbol == True:
            str = str + "Symbol"
        if result.Has_Footprint == True:
            str = str + ", Footprint"
        if result.Has_STEP == True:
            str = str + ", STEP"
        if result.Has_Simulation == True:
            str = str + ", Simulation"
        str = str + " ]"
        print(str)

    def remove_char_at(self, string, index):
        length = len(string)
        if (index + 1) <= length:
            return string[:index] + string[index+1:]
        else:
            return string[:index]

    def Clean_Up_Search_Characters( self, search_string ):
        if "#" in search_string:
            return search_string.replace('#', '%23')    # digikey doesnt like hashtag character in search url
        else:
            return  search_string

    def Download_Files(self, data, mfr_part_num):
        # make folder of mfr part name
        part_dir = DESTINATION_DIR + mfr_part_num + "/SnapEda"
        if not os.path.isdir(part_dir):
            os.mkdir(part_dir)

        files_before = self.Get_Files_In_Download_Dir()
        if data.Has_Symbol:
            print("downloading symbol and footprint")
            self.Download_Symbol_And_Footprint(data.URL)
    
        elif data.Has_Footprint:
            print("downloading only footprint")
            self.Download_Footprint(data.URL)

        if data.Has_STEP:
            print("downloading step file")
            self.Download_STEP_File(data.URL)
        
        """
        if data.Has_Simulation:
        """
        time.sleep(0.1)
        files_after = self.Get_Files_In_Download_Dir()
        new_files = self.Get_New_Files(files_before, files_after)
        self.Move_Files(new_files, part_dir)
        #FileHelper.Unzip_Files(part_dir)




    def Download_Footprint(self, url):
        files_before = self.Get_Files_In_Download_Dir()

        self.driver.get(url)
        self.wait.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="main-col"]/div[2]')) )
        symbol_button = self.driver.find_element_by_xpath(Footprint_Button_XPATH)
        symbol_button.click()
        time.sleep(.25)

        self.Click_Orcad()
        self.Wait_For_File_Download(files_before)

    def Download_Symbol_And_Footprint(self, url):
        files_before = self.Get_Files_In_Download_Dir()

        self.driver.get(url)
        self.wait.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="main-col"]/div[2]')) )
        symbol_button = self.driver.find_element_by_xpath(Symbol_Button_XPATH)
        symbol_button.click()
        time.sleep(.25)

        self.Click_Orcad()
        self.Wait_For_File_Download(files_before)

    def Download_STEP_File(self, url):
        files_before = self.Get_Files_In_Download_Dir()
        self.driver.get(url)
        self.wait.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="main-col"]/div[2]')) )
        symbol_button = self.driver.find_element_by_xpath(STEP_Model_Tab_XPATH)
        symbol_button.click()
        time.sleep(1)
        self.wait.until(EC.visibility_of_element_located((By.XPATH, STEP_Model_Button_XPATH)) )
        symbol_button = self.driver.find_element_by_xpath(STEP_Model_Button_XPATH)
        symbol_button.click()
        time.sleep(1)

        self.Wait_For_File_Download(files_before)

    def Click_Orcad(self):
        self.wait.until(EC.element_to_be_clickable((By.XPATH, Orcad_Button_XPATH)) )
        orcad_button = self.driver.find_element_by_xpath(Orcad_Button_XPATH)
        orcad_button.click()
        time.sleep(0.5)

    def Get_Files_In_Download_Dir(self):
        path_to_watch = DOWNLOAD_DIR
        files=set()
        for file in os.listdir(path_to_watch):
            fullpath=os.path.join(path_to_watch, file)
            if os.path.isfile(fullpath) or os.path.isdir(fullpath):
                if not fullpath.endswith("crdownload"):
                    files.add(fullpath)
        return files

    def Wait_For_File_Download(self, files_before):
        while 1:
            time.sleep(0.25)
            files_after = self.Get_Files_In_Download_Dir()
            new_files = [file for file in files_after if not file in files_before]
            if len(new_files) > 0:
                break
    
    def Get_New_Files(self, before_files, after_files):
        new_files = [file for file in after_files if not file in before_files]
        return new_files

    def Move_Files(self, move_files, dest_dir):
        time.sleep(1)
        print("Files placed in {}:".format(DESTINATION_DIR) )
        for file in move_files:
            print("\t{}".format(FileHelper.Get_Base_Filename(file)) )
            self.Move_File_to_Destination_Dir(file, dest_dir)

    def Move_File_to_Destination_Dir(self, src_file, dest_dir):
        filename = FileHelper.Get_Base_Filename(src_file)
        destination_path = dest_dir + "/" + filename
        shutil.move(src_file, destination_path)


    def Close_Driver(self):
        self.driver.quit()





    def Get_Main_Window_Handle(self):
        main_window_handle = None
        while not main_window_handle:
            main_window_handle = self.driver.current_window_handle
        return main_window_handle

    def Get_Popup_Window_Handle(self, main_window_handle):
        popup_window_handle = None
        while not popup_window_handle:
            for handle in self.driver.window_handles:
                if handle != main_window_handle:
                    popup_window_handle = handle
                    break
        return popup_window_handle