
import os
from snapeda import snapeda_parser
from Stat_File import Download_File
from Stat_File import Design_Files
from Stat_File import FileHelper
from Digikey_Scraper.digikey_scraper import digikey_scraper
from Webdriver import Driver
from selenium.webdriver.support.ui import WebDriverWait
from UltraLibrarian import UltraLibrarian
import time
from AutoGui import AutoGUI
from img.verify_data2 import *
from img.click_data import *
from zipfile38 import ZipFile
from XML_Files import XML_Parser
import re
import subprocess


DESTINATION_DIR = r'C:/Users/poppy/Documents/Cadence/Libraries/XML/Download/'
LOG_PATH = r'C:/Users/poppy/Documents/Cadence/Libraries/XML/Download/'
BROWSER_DOWNLOAD_DIR = r"C:/Users/poppy/Downloads/"


class Search_Engine:  
    def __init__(self, report_filepath ):
        self.report_filename = report_filepath
        self.report_file = open(report_filepath, 'a')
        
        self.driver = Driver.Get_ChromeDriver(LOG_PATH)
            #self.driver = Driver.Get_uChrome()
        self.wait = WebDriverWait(self.driver, 100)
        ua = self.driver.execute_script("return navigator.userAgent")
        print("useragent: ", ua)
        print("plugin length: ", self.driver.execute_script("return navigator.plugins.length"))
        print("languages: ", self.driver.execute_script("return navigator.languages"))
        #Driver.Open_Cookies(self.driver)
        #UltraLibrarian.Login(self.driver, self.wait)
        self.digikey = digikey_scraper( self.driver, self.report_filename)
        self.snapeda = snapeda_parser(self.driver, self.report_filename )
        
        self.Downloaded_Parts = []

    def Test_Detected(self):
        self.driver.get('https://recaptcha-demo.appspot.com/recaptcha-v3-request-scores.php')
        

    def Search(self, mfr_part_num, DL_symbol=False, DL_footprint=False, DL_STEP=False, DL_SPICE=False):
        part_dir = DESTINATION_DIR + mfr_part_num
        self.Downloaded_Parts.append(part_dir)
        DL_files = Design_Files(mfr_part_num, part_dir, BROWSER_DOWNLOAD_DIR, DL_symbol, DL_footprint, DL_STEP, DL_SPICE)
        print("DL Step: ", DL_STEP)
        if not os.path.isdir(part_dir):
            os.mkdir(part_dir)
        self.Search_Digikey(DL_files)
        self.Search_Snap_Eda(DL_files.mfr_part_number)
        self.Download_CAD_Data(DL_files)
        # write any related content to report file
        # pass the part dir & report file to other search engine functions that are called

    def Process_Downloads(self):
        self.Convert_Allegro_XML_Files()
        self.Cleanup_Files()

    def Cleanup_Files(self):
        sub_dirs = None
        for part_dir in self.Downloaded_Parts:
            sub_dirs = FileHelper.Get_All_Subdirectories(part_dir)
            print("sub dirs: ", sub_dirs)
            for sub_dir in sub_dirs:
                dir_name = os.path.basename(sub_dir)
                print("dir name: ", dir_name)
                FileHelper.Remove_Files_of_Type(sub_dir, ".tag")
                FileHelper.Remove_Files_of_Type(sub_dir, ".txt")
                FileHelper.Remove_Files_of_Type(sub_dir, ".script")
                if dir_name == "LOG":
                    print("removing dir")
                    FileHelper.Remove_Dir(sub_dir)

    def Convert_Allegro_XML_Files(self):
        xml_parser = XML_Parser()

        xml_files = None
        sub_dirs = None
        for part_dir in self.Downloaded_Parts:
            xml_files =  FileHelper.Get_XML_Files(part_dir) 
            sub_dirs = FileHelper.Get_Folders_In_Dir(part_dir)
            print(sub_dirs)
            for sub_dir in sub_dirs:
                dir_name = os.path.basename(sub_dir)
                print("dirname: ", dir_name)
                if "Allegro" in dir_name:
                    xml_files.append( FileHelper.Get_XML_Files(sub_dir) )

        file_list = []
        for file in xml_files:
            if type(file) is list or type(file) is set:
                for elem in file:
                    if elem is not set():
                        file_list.append(elem)
            else:
                if file is not set():
                    file_list.append(dir)
        xml_files = [x for x in file_list if x]

        print("XML Files: {}".format(xml_files) )
        for file in xml_files:
            if file.endswith("-L.xml") or file.endswith("-M.xml"):
                os.remove(file)
            else:
                file = file.replace(os.sep, '/') 
                xml_parser.Process_Allegro_XML_File(file)
                print("file: ", file)
                script_file = xml_parser.Create_Batch_File_Script(file)
                self.Execute_Footprint_Script(script_file)
                print(script_file)
                

    def Execute_Footprint_Script(self, script_filepath):
        dir_path = FileHelper.Get_Directory(script_filepath)
        os.chdir(dir_path)
        script_file = FileHelper.Get_Base_Filename(script_filepath)
        allegro_command = 'START /W C:/Cadence/SPB_17.4/tools/bin/allegro.exe -s {}'.format(script_file)
        print("allegro command: ", allegro_command)
        os.system(allegro_command)


    def Search_Digikey(self, DL_object):
        DL_object.DK_link = self.digikey.get_dk_component_url( DL_object.mfr_part_number )   # returns URL of component we want to scrape
        if DL_object.DK_link:
            self.digikey.Find_CAD_Data(DL_object.DK_link, DL_object)
            Driver.Save_Cookies(self.driver)
            #if cad_data:
                #self.Write_Digikey_to_File( mfr_part_number, cad_data)
            
    def Search_Snap_Eda(self, mfr_part_number):
        self.snapeda.Sign_In_to_SnapEda()
        print("\nSearch Part:  {}".format(mfr_part_number))
        
        self.snapeda.build_search_url(mfr_part_number)
        print("total search results: ", self.snapeda.Num_Search_Results() )
        results = self.snapeda.Get_Results_With_CAD()
        print("\tresults w/ CAD: ", len(results) )
        result = results[0]
        if result:
            self.snapeda.Print_CAD_Result(result)
            self.Write_SnapEda(mfr_part_number, result.URL)
            self.snapeda.Download_Files(result, mfr_part_number)


    def Download_CAD_Data(self, DL_object):
        part_dir = DL_object.dir
        if not os.path.isdir(part_dir):
            os.mkdir(part_dir)

        files_before = FileHelper.Get_Files_In_Download_Dir(DL_object.browser_download_dir)   # watch files in download directory

        if DL_object.Get_PDF_Files() and DL_object.Have_Datasheet_Links():
            self.Download_PDF_Files(DL_object)
    
        print("Done downloading pdf files")
        print("get EDA files? ", DL_object.Get_EDA_Files() )
        print("Have EDA links? ", DL_object.Have_EDA_Links() )


        if DL_object.Get_EDA_Files() and DL_object.Have_EDA_Links():
            self.Download_EDA_Files(DL_object)
        
        """
        if data.Has_Simulation:
        """
        files_after = FileHelper.Get_Files_In_Download_Dir(DL_object.browser_download_dir)
        new_files = FileHelper.Get_New_Files(files_before, files_after)
        FileHelper.Move_Files(new_files, part_dir)
        FileHelper.Unzip_Files(part_dir)
        self.Move_STEP_Files_to_Part_DIR(part_dir)
        self.Remove_Extraneous_Files(part_dir)

    def Move_STEP_Files_to_Part_DIR(self, part_dir):
        step_folder = None
        remove_dirs = []
        folders = FileHelper.Get_Folders_In_Dir(part_dir)

        print("folders in dir: ", folders)
        # there's usually a folder containing a date, this is the folder we want
        m = re.compile('^([0-9]{4})[-]([0]?[1-9]|[1][0-2])[-]([0][1-9]|[0|1|2]{1}[0-9]{1}|[3][0|1]|[1-9])[_]')
        for folder in folders:
            folder_name = os.path.basename(folder) # gets the directory name from the fully qualified absolute path
            match = m.match(folder_name)
            if match is not None:
                match = match.group()
                if match is not None:
                    print("remove dir: ", match)
                    cur_folder = folder
                    sub_folders = FileHelper.Get_Folders_In_Dir(cur_folder)
                    for sub_folder in sub_folders:
                        sub_folder_name = os.path.basename(sub_folder)
                        if sub_folder_name == "STEP":
                            step_folder = sub_folder
                            remove_dirs.append(folder)
                            break

        list_files = FileHelper.Get_Files_In_Dir(step_folder)
        step_files = []
        for file in list_files:
            if file.endswith(".step") or file.endswith(".STEP") or file.endswith(".stp") or file.endswith(".STP"):
                step_files.append(file)

        FileHelper.Move_Files(step_files, part_dir)
        for dir in remove_dirs:
            FileHelper.Remove_Dir(dir)

    def Remove_Extraneous_Files(self, part_dir):
        dirs = FileHelper.Get_All_Subdirectories(part_dir)
        for dir in dirs:
            FileHelper.Remove_Filenames_Containing(dir, "Import")
            FileHelper.Remove_Files_of_Type(dir, ".psm")
            FileHelper.Remove_Files_of_Type(dir, ".ILE")
            FileHelper.Remove_Files_of_Type(dir, ".bat")

    def Download_PDF_Files(self, DL_object):
        for dl_file in DL_object.PDF_Files:
            link = dl_file.link
            self.Download_PDF_File(link, DL_object.browser_download_dir)

    def Download_PDF_File(self, pdf_link, download_dir):
        files_before = FileHelper.Get_Files_In_Download_Dir(download_dir)   # watch files in download directory
        self.driver.get(pdf_link)
        FileHelper.Wait_For_File_Download(files_before, download_dir)


    def Download_EDA_Files(self, DL_object):
        if DL_object.Get_Symbol_Files():
            for dl_file in DL_object.Symbol_Files:
                link = dl_file.link
                self.Download_EDA_File(link, DL_object)
        if DL_object.Get_Footprint_Files():
            for dl_file in DL_object.Footprint_Files:
                link = dl_file.link
                self.Download_EDA_File(link, DL_object)
        if DL_object.Get_STEP_Files():
            for dl_file in DL_object.STEP_Files:
                link = dl_file.link
                self.Download_EDA_File(link, DL_object)
        if DL_object.Get_SPICE_Files():
            for dl_file in DL_object.SPICE_Files:
                link = dl_file.link
                self.Download_EDA_File(link, DL_object)

    def Download_EDA_File(self, EDA_link, DL_object):
        files_before = FileHelper.Get_Files_In_Download_Dir(DL_object.browser_download_dir)   # watch files in download directory
        #if ultralibrarian
        print("download eda file")
        print("eda link: ", EDA_link)
        if 'ultralibrarian' in EDA_link:
            #login to ultralibrairian
            print("call ultralibrarian")
            UltraLibrarian.Login(self.driver, self.wait)
            time.sleep(1)
            Driver.Save_Cookies(self.driver)
            self.driver.get(EDA_link)
            time.sleep(1)
            
            UltraLibrarian.Click_Download_Menu_Button(self.driver, self.wait)
            time.sleep(1)
            UltraLibrarian.Toggle_Cadence_Menu(self.driver, self.wait)
            time.sleep(.25)
            if DL_object.Get_Symbol_Files():
                UltraLibrarian.Select_Capture_17_2(self.driver, self.wait)
            time.sleep(.25)
            if DL_object.Get_Footprint_Files():
                UltraLibrarian.Select_Allegro_17_2(self.driver, self.wait)
            time.sleep(.25)
            if DL_object.Get_STEP_Files():
                print("toggling step files")
                UltraLibrarian.Toggle_STEP_Menu(self.driver, self.wait)
                UltraLibrarian.Select_STEP_Model(self.driver, self.wait)


            self.driver.execute_script("window.scrollTo(0,document.body.scrollHeight/4)")
            captcha_present = AutoGUI.Page_Object_Present(Captcha_Unchecked)
            if not captcha_present:
                AutoGUI.Click_On(Download_Files)

            else:
                UltraLibrarian.Check_Captcha_Button(self.driver, self.wait)
                time.sleep(1)

                if not UltraLibrarian.Captcha_Is_Solved():
                    UltraLibrarian.Click_Solver_Button(self.driver, self.wait)
                    time.sleep(1)
                time.sleep(0.1)
                UltraLibrarian.Download_Files(self.driver, self.wait)

            print("waiting until download complete page object present\n")
            AutoGUI.screenshot()
            AutoGUI.Wait_Until_Page_Object_Present(Download_Complete)
            self.driver.close()
            #FileHelper.Wait_For_File_Download(files_before, DL_object.browser_download_dir)
            


    def Done_Searching(self):
        self.driver.quit()

    def Write_SnapEda(self, part, result):
        x=5

    def Write_Digikey_to_File(self, part_number, cad):
        print("writing to: {}".format(self.report_file) )
        self.report_file.write("\n{}\n".format(part_number)) 

        if( len(cad.manufacturer_links) > 0):
            self.report_file.write("\tMANUFACTURER LINKS\n")
            for link in cad.manufacturer_links:
                self.report_file.write("\t\t{}\n".format(link))

        if( len(cad.footprint_links) > 0):
            self.report_file.write("\tFOOTPRINT LINKS\n")
            for link in cad.footprint_links:
                self.report_file.write("\t\t{}\n".format(link))

        if( len(cad.STEP_links) > 0):
            self.report_file.write("\tSTEP LINKS\n")
            for link in cad.STEP_links:
                self.report_file.write("\t\t{}\n".format(link))

        if( len(cad.SIM_model_links) > 0):
            self.report_file.write("\tSIM MODEL LINKS\n")
            for link in cad.SIM_model_links:
                self.report_file.write("\t\t{}\n".format(link))

        if( len(cad.datasheet_links) > 0):
            self.report_file.write("\tDATASHEET LINKS\n")
            for link in cad.datasheet_links:
                self.report_file.write("\t\t{}\n".format(link))

    def Close_File(self):
        self.report_file.flush()
        self.report_file.close()


