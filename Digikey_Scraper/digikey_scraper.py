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
import requests
import urllib.request
import time
from .component import *
from .IC_type import Find_IC_Type
from bs4 import BeautifulSoup
from CAD_Object import CAD_Data_Object
from Stat_File import FileHelper
from Stat_File import Download_File

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from Webdriver import Driver
from Credentials import UltraLibrarian_Credentials
from UltraLibrarian import UltraLibrarian
from pathlib import Path

LOG_PATH = r'C:/Users/poppy/Documents/Cadence/Libraries/XML/Download/'
DOWNLOAD_DIR = r"C:/Users/poppy/Downloads/"


class digikey_scraper:
    def __init__(self, driver, report_file ):
        self.search_string = None
        #self.url_string = 'http://www.digikey.com/products/en?sv=0&pv7=243&keywords='
        self.url_string = 'http://www.digikey.com/products/en?keywords='
        self.dk_search_url = None                           #self.url_string + self.search_string  # create search URL from dikey site URL and MFGpart #
        self.component_url = None
        self.component_type = None
        self.report_file = open( report_file, 'w', newline='')
        self.component = None
        self.parts_list_no_results = []
        self.driver = driver
        self.wait = WebDriverWait(self.driver, 100)


    def set_search_keyword(self, search_string):
        self.search_string = search_string
        self.dk_search_url = self.url_string + self.search_string

    def set_search_url(self, url_string):
        self.url_string = url_string
        self.dk_search_url = self.url_string + self.search_string

    # get the exact url link to component
    def get_dk_component_url(self, search_string):
        self.search_string = self.Clean_Up_Search_Characters( search_string)    # remove hashtag characters from search string
        self.dk_search_url = self.url_string + self.search_string
        self.search_string = search_string
        print( "dk search url: ", self.dk_search_url )
        if self.dk_search_url:
            #html = requests.get(self.dk_search_url).text
            self.driver.get(self.dk_search_url)
            html = self.driver.page_source
            if html:
                soup = BeautifulSoup(html, "lxml")
                if soup:
                    num_results = self.Num_Search_Results( soup )
                    if num_results == 1:
                        self.component_url = self.Extract_Part_URL( soup )
                        print("\nFOUND:\t", self.search_string, "\t", self.component_url)
                        return self.component_url
                    elif num_results > 1:
                        self.component_url = self.Get_URL_From_Search_Results(soup, self.dk_search_url)
                        if self.component_url:
                            return self.component_url
                        else:
                            print("\tCOULD NOT MATCH THIS PART NUMBER FROM SEARCH RESULTS\n ")
                            return None
        else:
            print(" !!! NO SEARCH URL ")
            return None  

    def close_report_file(self):
        write_string = "\n\n\t"+ '\nTHESE PART NUMBERS HAD NO SEARCH RESULTS:\n'
        self.report_file.write(write_string)
        for part in self.parts_list_no_results:
            write_string = "\n" + part
            self.report_file.write(write_string)
        self.report_file.close()

    def Single_Result(self, soup):
        main_tag = soup.find("main")
        if(main_tag):
            single_result = soup.find("div", {"data-evg": "product-details-overview"})
            if single_result:
                return True
        return False


    def Num_Search_Results(self,  soup ):
        single_result = self.Single_Result(soup)

        multiple_results = soup.find("table", {"id": "productTable"})   # found multiple search results, in table form

        different_results = soup.find("span", {"id": "matching-records-text"}) # found multiple search results, in table form
        no_results = soup.find("div", {"id": "noResults"})
        alternate_results_page = soup.find_all("table", {"class": "exactPartList"})
        count = 0
        if single_result:        
            return 1
        elif multiple_results:
            search_results = soup.find_all("td", {"class": "tr-mfgPartNumber"})
            for result in search_results:
                count = count + 1
            print("\n'", self.search_string, "' SEARCH RESULTS: ", count )
            return count
        elif alternate_results_page:
            for result in alternate_results_page:
                count = count + 1
                print("\n'", self.search_string, "' ALTERNATE SEARCH RESULTS: ", count )
            return count
        elif no_results:           # found no results matching search string
            part_type = str(self.component_type).upper()
            write_string = "\n\n" + self.search_string + "\t" + "NOT FOUND" + "\n"
            self.parts_list_no_results.append(self.search_string)
            print("\n" + self.search_string + "\t0 search results\n")
            return 0

        else:
            print("Selectors didnt work for this part. Search string: "+"'"+self.search_string+"'"+"\t" + self.dk_search_url + "\n")
            write_string = "\n" + self.search_string + "\t" + "SELECTOR ERROR" + "\n"
            self.report_file.write( write_string )
            return 0

    def Get_URL_From_Search_Results(self, soup, search_string):
        all_results = soup.find("tbody", {"id": "lnkPart"}).find_all("tr")    # table body
        matches = {}
        similar_parts = {}
        part_number = None
        part_link = None
        for result in all_results:
            part_number_cell = result.find("td", {"class": "tr-mfgPartNumber"})
            if part_number_cell:
                part_number = part_number_cell.find('span').text  # in each row grab the manufacturer part number
                temp_part_link = 'http://digikey.com' + part_number_cell.find('a').get('href')  # in each row grab digikey link
                print("\t", part_number, "\t", temp_part_link)
            if part_number:
                similar_parts[part_number] = temp_part_link
                if part_number == self.search_string or self.Part_Match(self.search_string, part_number):          # if the content of the span tag matches the search string (mfg part#), add it to match results
                    matches[part_number] = temp_part_link
                    min_quantity_cell = result.find("td", {'class': 'tr-minQty'} )   # look for minimum quantity cell 
                    if min_quantity_cell:
                        if min_quantity_cell.find('span'):
                            min_quantity_str = min_quantity_cell.find('span').text  # grab the actual minimum quantity text
                            min_quantity_str = re.sub(r"[\n\t\s]*", "", min_quantity_str)
                            min_quantity_str = min_quantity_str.replace(',', '')
                            if not min_quantity_str.isdigit():
                                min_quantity_str = re.search(r'\d+', min_quantity_str)
                                min_quantity_str = min_quantity_str.group(0)
                            min_quantity = int( min_quantity_str )
                            if( int(min_quantity) == 1):                             # grabbing only results with "1" as min QTY, so we can get the price
                                part_link = temp_part_link
                                self.component_url = temp_part_link
                                print( "\nFOUND \t", self.search_string, self.component_url )
                                return self.component_url

        num_matches = len(matches)  # if theres only one match, return it
        if num_matches == 1:
            for url_match in matches:
                self.component_url = matches[url_match]
            print( "\nMATCH: \t", self.search_string, "\t", self.component_url )
            return self.component_url
        elif num_matches > 1:
            for url_match in matches:
                self.component_url = matches[url_match]
            print( "\nMATCH: \t", self.search_string, "\t", self.component_url )
            return self.component_url
        elif num_matches == 0 and len(similar_parts) > 0:                  # if no search results match, write the similar parts in search results to the report file
            write_string = "\n\nNO EXACT MATCHES FOR:\t" + "'" + self.search_string + "'" + "\tSIMILAR PARTS FOUND:"
            print(write_string)
            self.report_file.write( write_string )
            for part in similar_parts:
                write_string = "\n\t"+ part + "  \t" + similar_parts[part] 
                print(write_string)
                self.report_file.write(write_string)
            return None

    def Extract_Part_URL(self, soup ):
        tag = soup.find("link", {"rel": "canonical"})    # gets the tag: <link href="https://www.digikey.com/product-detail/en/yageo/RT0402BRD07102KL/" rel="canonical"/>
        if tag:
            parse_line = str(tag)  # get string representation of the tag
            regex = re.compile(r'(?<=")(?:\\.|[^"\\])*(?=")')   # regular expression to grab the url within the quotes
            url_quoted = re.search(regex, parse_line)           # execute the regular expression on the tag
            url = url_quoted.group()                            # gets the string representation of the link
            if url:
                return url
        else:
            tag = soup.find("span", {"dir": "ltr"})
            if tag:
                url = tag.find('a').get('href') 
                if url:
                    return url
            else:
                return None




    def Part_Match(self, BOM_part_num, DK_part_num):
        DK_part_num.strip()
        BOM_part_num.strip()
        if BOM_part_num == DK_part_num:
            return True
        
        elif BOM_part_num in DK_part_num:
            print('SIMILAR PART MATCH')
            return True
        else:
            print("'",BOM_part_num,"'"," not in ","'",DK_part_num,"'")

        return self.Compare_Parts_Recursive(BOM_part_num, DK_part_num)

        for i in range( len(BOM_part_num) ):
            if i < len(DK_part_num):            # verify we arent exceeding index of second string
                if BOM_part_num[i] == DK_part_num[i]:
                    continue
                else:
                    char_difference1 = BOM_part_num[i]
                    char_difference2 = DK_part_num[i]
                    if char_difference2 in '#*-_ .,/\(':     # try removing punctuation character from digikey string
                        DK_part_num_mod = self.remove_char_at(DK_part_num, i)
                        if (BOM_part_num in DK_part_num_mod) or (BOM_part_num == DK_part_num_mod):
                            print('SIMILAR PART MATCH')
                            return True
                        else:
                            print("'",BOM_part_num,"'"," not in ","'",DK_part_num_mod,"'")
                            return False
                    elif char_difference1 in '#*-_ .,/\(': 
                        BOM_part_num_mod = self.remove_char_at(BOM_part_num, i)
                        if BOM_part_num_mod in DK_part_num or BOM_part_num_mod == DK_part_num:
                            print('SIMILAR PART MATCH')
                            return True
                        else:
                            return False
                        return False
            else:
                print(BOM_part_num," != ", DK_part_num, " at index: ", i, "char: ", BOM_part_num[i] )
                return False

    def remove_char_at(self, string, index):
        length = len(string)
        if (index + 1) <= length:
            return string[:index] + string[index+1:]
        else:
            return string[:index]


    # recursively removes punctuation characters ( '-', '#', ',' etc) or leading zeroes to attempt a part match
    def Compare_Parts_Recursive(self, BOM_pn, DK_pn):
        BOM_pn.strip()
        DK_pn.strip()
        if (BOM_pn in DK_pn) or (BOM_pn == DK_pn):
            print('\tSIMILAR MATCH:  ',BOM_pn, " ~= " , DK_pn )
            return True
        
        elif (DK_pn in BOM_pn):
            print('\tSIMILAR MATCH:  ',BOM_pn, " ~= " , DK_pn )
            return True

        if '%23' in BOM_pn:
            BOM_pn.replace('%23', '#')      # if %23, put it back to hashtag
        for i in range( len(BOM_pn) ):
            if i < len(DK_pn):            # verify we arent exceeding index of second string
                if BOM_pn[i] == DK_pn[i]:
                    continue
                else:
                    char_difference1 = BOM_pn[i]
                    char_difference2 = DK_pn[i]
                    if char_difference2 in '#*-_ .,/\(':     # try removing punctuation character from digikey string
                        DK_pn_mod = self.remove_char_at(DK_pn, i)
                        return self.Compare_Parts_Recursive( BOM_pn, DK_pn_mod)
                    elif char_difference2 in '0' and i == 0:
                        DK_pn_mod = self.remove_char_at(DK_pn, i)
                        return self.Compare_Parts_Recursive( BOM_pn, DK_pn_mod)

                    if char_difference1 in '#*-_ .,/\(': 
                        BOM_pn_mod = self.remove_char_at(BOM_pn, i)
                        return self.Compare_Parts_Recursive(BOM_pn_mod, DK_pn)
                    elif char_difference1 in '0' and i == 0:
                        BOM_pn_mod = self.remove_char_at(BOM_pn, i)
                        return self.Compare_Parts_Recursive( BOM_pn_mod, DK_pn)
                        
            else:
                print(BOM_pn," != ", DK_pn, " at index: ", i, "char: ", BOM_pn[i] )
                return False
        
        return True

    def Clean_Up_Search_Characters( self, search_string ):
        if "#" in search_string:
            return search_string.replace('#', '%23')    # digikey doesnt like hashtag character in search url
        else:
            return  search_string

    def Find_CAD_Data(self, dk_part_url, DL_object):
        self.driver.get(dk_part_url)
        html = self.driver.page_source
        #print(dk_part_url)
        if html:
            soup = BeautifulSoup(html, "lxml")
            if soup:
                body = soup.find("body") # found multiple search results, in table form
                if body:
                    main = body.find("main")
                    if main:
                        media_tag = main.find("div", {"data-evg": "product-details-docs-n-media"})
                        if media_tag:
                            table_tag = media_tag.find("tbody", {"class": "MuiTableBody-root"})
                            if table_tag:
                                table_rows = table_tag.find_all("tr", {"class": "MuiTableRow-root"})
                                if table_rows:
                                    for row in table_rows:
                                        text = row.find("td").text
                                        #print("title: ", text)
                                        if "Datasheet" in text and not "HTML" in text:
                                            datasheet_link = row.find("a").get("href")
                                            print("datasheet")
                                            print("\tdatasheet: ", datasheet_link)
                                            dl_file = Download_File()
                                            dl_file.link = datasheet_link
                                            DL_object.PDF_Files.append(dl_file)

                                        elif "EDA / CAD Models" in text:
                                            print("cad models")
                                            cad_models = row.find_all("a")
                                            for model in cad_models:
                                                model_link = model.get("href")
                                                print("\t\tcad model: ", model_link)
                                                dl_file = Download_File()
                                                dl_file.link = model_link
                                                DL_object.Footprint_Files.append(dl_file)
                                        elif "Simulation Models" in text:
                                            print("sim models")
                                            cad_models = row.find_all("a")
                                            for model in cad_models:
                                                model_link = model.get("href")
                                                print("\t\tsim model: ", model_link)
                                                dl_file = Download_File()
                                                dl_file.link = model_link
                                                DL_object.SPICE_Files.append(dl_file)

                                        elif "Mfg CAD Models" in text:
                                            print("STEP models")
                                            cad_models = row.find_all("a")
                                            for model in cad_models:
                                                model_link = model.get("href")
                                                print("\t\tcad model: ", model_link)
                                                dl_file = Download_File()
                                                dl_file.link = model_link
                                                DL_object.STEP_Files.append(dl_file)

                                        elif "Design Resources" in text:
                                            print("design resources")
                                            cad_models = row.find_all("a")
                                            for model in cad_models:
                                                model_link = model.get("href")
                                                print("\t\tresource: ", model_link)
                                                DL_object.Design_Resources.append(model_link)
                                            # may have a footprints and symbols link here
                                            # see: https://www.digikey.com/en/products/detail/analog-devices-inc/LT6105HMS8-TRPBF/1785493

                                        elif "Product Training Modules" in text:
                                            print("training modules")
                                            cad_models = row.find_all("a")
                                            for model in cad_models:
                                                model_link = model.get("href")
                                                print("\t\tmodules: ", model_link)

    def Download_CAD_Data(self, DL_object):
        part_dir = DL_object.dir
        if not os.path.isdir(part_dir):
            os.mkdir(part_dir)

        files_before = FileHelper.Get_Files_In_Download_Dir(DL_object.browser_download_dir)   # watch files in download directory

        if DL_object.Get_PDF_Files() and DL_object.Have_Datasheet_Links():
            self.Download_PDF_Files(DL_object)
    
        print("Done downloadinf pdf files")

        if DL_object.Get_EDA_Files() and DL_object.Have_EDA_Links():
            self.Download_EDA_Files(DL_object)
        
        """
        if data.Has_Simulation:
        """
        files_after = FileHelper.Get_Files_In_Download_Dir(DL_object.browser_download_dir)
        new_files = FileHelper.Get_New_Files(files_before, files_after)
        FileHelper.Move_Files(new_files, part_dir)

    def Download_PDF_Files(self, DL_object):
        for dl_file in DL_object.PDF_Files:
            link = dl_file.link
            self.Download_PDF_File(link, DL_object.browser_download_dir)

    def Download_PDF_File(self, pdf_link, download_dir):
        files_before = FileHelper.Get_Files_In_Download_Dir(download_dir)   # watch files in download directory
        self.driver.get(pdf_link)
        FileHelper.Wait_For_File_Download(files_before, download_dir)


    def Download_EDA_Files(self, DL_object):
        for dl_file in DL_object.PDF_Files:
            link = dl_file.link
            self.Download_EDA_File(link, DL_object)



    def Download_EDA_File(self, EDA_link, DL_object):
        files_before = FileHelper.Get_Files_In_Download_Dir(DL_object.browser_download_dir)   # watch files in download directory
        #if ultralibrarian
        if 'ultralibrarian' in EDA_link:
            #login to ultralibrairian
            UltraLibrarian.Login(self.driver, self.wait)
            self.driver.get(EDA_link)
            UltraLibrarian.Click_Download_Menu_Button(self.driver, self.wait)
            UltraLibrarian.Toggle_Cadence_Options(self.driver, self.wait)
            if DL_object.Get_Symbol_Files():
                UltraLibrarian.Select_Capture_17_2(self.driver, self.wait)
            if DL_object.Get_Footprint_Files():
                UltraLibrarian.Select_Allegro_17_2(self.driver, self.wait)
            if DL_object.Get_STEP_Files():
                UltraLibrarian.Toggle_STEP_Options(self.driver, self.wait)
                UltraLibrarian.Select_STEP_Model(self.driver, self.wait)

            UltraLibrarian.Check_Captcha_Button(self.driver, self.wait)
            UltraLibrarian.Download_Files(self.driver, self.wait)
        FileHelper.Wait_For_File_Download(files_before, DL_object.browser_download_dir)