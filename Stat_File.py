
import os
import glob
import ntpath
import time
import shutil
from zipfile38 import ZipFile

class Download_File:
    def __init__(self):
        self.filepath = None
        self.link = None

class Design_Files:
    def __init__(self, mfr_part_num, download_dir, browser_dir, get_symbol, get_footprint, get_STEP, get_SPICE):
        self.mfr_part_number = mfr_part_num
        self.dir = download_dir
        self.browser_download_dir = browser_dir
        self.DK_link = None
        self.Symbol_Files = []
        self.Footprint_Files = []
        self.STEP_Files = []
        self.SPICE_Files = []
        self.PDF_Files = []
        self.Design_Resources = []
        self.get_symbol = get_symbol
        self.get_footprint = get_footprint
        self.get_STEP = get_STEP
        self.get_SPICE = get_SPICE

    def Get_EDA_Files(self):
        return (self.get_symbol or self.get_footprint)

    def Get_Symbol_Files(self):
        return (self.get_symbol)

    def Get_Footprint_Files(self):
        return (self.get_footprint)

    def Get_SPICE_Files(self):
        return (self.get_SPICE)

    def Get_STEP_Files(self):
        return (self.get_SPICE)

    def Get_PDF_Files(self):
        return (self.Get_PDF_Files)

    def Have_EDA_Links(self):
        return (len(self.Symbol_Files) > 0 or len(self.Footprint_Files) > 0)

    def Have_SPICE_Links(self):
        return (len(self.SPICE_Files) > 0 )

    def Have_STEP_Links(self):
        return (len(self.STEP_Files) > 0 )

    def Have_Datasheet_Links(self):
        return (len(self.PDF_Files) > 0 )


class FileHelper:  
    @staticmethod
    def path_leaf(path):
        head, tail = ntpath.split(path)
        return tail or ntpath.basename(head)

    @staticmethod
    def Get_XML_Files(directory_path):
        file_list = []
        print(directory_path)
        for filename in glob.glob(os.path.join(directory_path, '*.xml')): #iterate through each .xml file in current directory
            file_list.append(filename)
            print("\t" + FileHelper.Get_Base_Filename(filename))
        return file_list

    @staticmethod
    def Get_STEP_Files(directory_path):
        FileHelper.Rename_Files(directory_path, ".stp", ".step")
        FileHelper.Rename_Files(directory_path, ".STEP", ".step")
        FileHelper.Rename_Files(directory_path, ".STP", ".step")
        file_list = []
        print(directory_path)
        for filename in glob.glob(os.path.join(directory_path, '*.step')): #iterate through each .xml file in current directory
            file_list.append(filename)
            print("\t" + FileHelper.Get_Base_Filename(filename))
        return file_list

    @staticmethod
    def Rename_Files(directory_path, orig_extension, new_extension):
        file_list = []
        search_extension = "*" + orig_extension
        for filename in glob.glob(os.path.join(directory_path, search_extension)): #iterate through each .xml file in current directory
            file_list.append(filename)

        for old_file in file_list:
            old_name_no_extension = FileHelper.Get_Filepath_No_Extension(old_file)
            new_name = old_name_no_extension + new_extension
            os.rename(old_file, new_name)

    #returns the "file+extension", without the full absolute path
    @staticmethod
    def Get_Base_Filename(filepath):
        read_filename = FileHelper.path_leaf(filepath)          
        return read_filename

    @staticmethod
    def Get_Filename_No_Extension(filepath):
        read_file_no_ext = os.path.splitext( filepath )[0]              # get path of xml file without the ".xml" extension
        file_no_ext_fixed = read_file_no_ext.replace(os.sep, '/')        # replace backslashes with forward slashes
        read_filename = FileHelper.path_leaf(file_no_ext_fixed)
        return read_filename
    
    @staticmethod
    def Get_Filepath_No_Extension(filepath):
        read_file_no_ext = os.path.splitext( filepath )[0]              # get path of xml file without the ".xml" extension
        file_no_ext_fixed = read_file_no_ext.replace(os.sep, '/')        # replace backslashes with forward slashes
        return file_no_ext_fixed

    #returns the directory path from the filepath
    @staticmethod
    def Get_Directory(filepath):
        return os.path.dirname(filepath)

    @staticmethod
    def Match_STEP_Files(XML_dir, STEP_files, Allegro_STEP_dir):
        read_file_no_ext = os.path.splitext( Allegro_STEP_dir )[0]              # get path of xml file without the ".xml" extension
        file_no_ext_fixed = read_file_no_ext.replace(os.sep, '/')                # replace backslashes with forward slashes
        return file_no_ext_fixed
    #def Get_XML_Filename(filepath):
    #def Change_PadStack_Names(root_tag):
    #def Change_Footprint_Name(root_tag):

    @staticmethod
    def Get_Files_In_Download_Dir(download_dir):
        path_to_watch = download_dir
        files=set()
        for file in os.listdir(path_to_watch):
            fullpath=os.path.join(path_to_watch, file)
            if os.path.isfile(fullpath) or os.path.isdir(fullpath):
                files.add(fullpath)
        return files

    @staticmethod
    def Get_Folders_In_Dir(dir):
        path_to_watch = dir
        dirs=set()
        for file in os.listdir(path_to_watch):
            fullpath=os.path.join(path_to_watch, file)
            if os.path.isdir(fullpath):
                dirs.add(fullpath)
        list_ret = list()
        if len(dirs) > 0:
            for item in dirs:
                list_ret.append(item)
            return list_ret
        else:
            return None

    @staticmethod
    def Get_Files_In_Dir(dir):
        path_to_watch = dir
        files=set()
        for file in os.listdir(path_to_watch):
            fullpath=os.path.join(path_to_watch, file)
            if os.path.isfile(fullpath):
                files.add(fullpath)
        return files

    @staticmethod
    def Wait_For_File_Download(files_before, download_dir):
        print("files before: ")
        FileHelper.Print_Files(files_before)
        print("Download dir: ", download_dir)
        while 1:
            time.sleep(1)
            files_after = FileHelper.Get_Files_In_Download_Dir(download_dir)
            new_files = [file for file in files_after if not file in files_before]
            if len(new_files) > 0:
                print("\nNEW FILE DETECTED!! OOGA BOOGA!\n")
                FileHelper.Print_Files(new_files)
                break

    @staticmethod
    def Get_New_Files(before_files, after_files):
        new_files = [file for file in after_files if not file in before_files]
        return new_files

    @staticmethod
    def Get_All_Subdirectories(dir):
        dir_list = list()
        dir_list.append(dir)
        dirs = FileHelper.Get_Folders_Recursive(dir)
        for dir in dirs:
            if type(dir) is list or type(dir) is set:
                for elem in dir:
                    if elem is not set() and elem is not None:
                        dir_list.append(elem)
            else:
                if dir is not set() and dir is not None:
                    dir_list.append(dir)
        ret_list = FileHelper.Flatten_List(dir_list)
        return ret_list


    @staticmethod
    def Get_Folders_Recursive(target_dir):
        dir_list = []
        folders = FileHelper.Get_Folders_In_Dir(target_dir)
        if folders is not None:
            dir_list.append(folders)
        else: 
            return None
        for folder in folders:
            lst = FileHelper.Get_Folders_Recursive(folder)
            if folder is not None:
                dir_list.append(lst)

        if len(dir_list) > 0:
            if len(dir_list) == 1:
                return dir_list[0]
            else:
                ret_list = [x for x in dir_list if x]
                return ret_list
        else:
            return None

    @staticmethod
    def Move_Files(move_files, dest_dir):
        print("Files placed in {}:".format(dest_dir) )
        for file in move_files:
            print("\t{}".format(FileHelper.Get_Base_Filename(file)) )
            FileHelper.Move_File_to_Destination_Dir(file, dest_dir)

    @staticmethod
    def Remove_Dir(delete_dir):
        print("deleting dir {}:".format(delete_dir) )
        shutil.rmtree(delete_dir)

    @staticmethod
    def Remove_Filenames_Containing(target_dir, match_string):
        files = FileHelper.Get_Files_In_Dir(target_dir)
        for file in files:
            filename = FileHelper.Get_Filename_No_Extension(file)
            if match_string.lower() in filename.lower():
                os.remove(file)
    
    @staticmethod
    def Remove_Files_of_Type(target_dir, extension_string):
        files = FileHelper.Get_Files_In_Dir(target_dir)
        for file in files:
            filename = FileHelper.Get_Base_Filename(file)
            extension = os.path.splitext(filename)[1]
            if extension_string.lower() == extension.lower():
                os.remove(file)

    @staticmethod
    def Unzip_Files(dest_dir):
        file_list = list()
        sub_dirs = FileHelper.Get_All_Subdirectories(dest_dir)
        for dir in sub_dirs:
            files = FileHelper.Get_Files_In_Dir(dir)
            flat_f_list = FileHelper.Flatten_List(files)
            for f in flat_f_list:
                file_list.append(f)
        
        files = FileHelper.Flatten_List(file_list)
        print("files: ", files)
        for file in files:
            if file.endswith(".zip"):
                # unzip to folder and delete the zip file
                target_dir = FileHelper.Get_Directory(file)
                os.chdir(target_dir)
                zip_file = ZipFile(file)
                zip_file.extractall()
                zip_file.close()
                os.remove(file)
                print("unzipped {}:".format(file) )

    @staticmethod
    def Flatten_List(lst):
        if not FileHelper.List_Is_Flattened(lst):
            print("main function, list is not flat")
            new_list = FileHelper.Flatten_List_Recursive(lst)
            return new_list
        else:
            return lst

    @staticmethod
    def Flatten_List_Recursive(lst):
        new_list = list()
        for elem in lst:
            if type(elem) is list or type(elem) is set:
                new_elem = FileHelper.Flatten_List_Recursive(elem)
                new_list.append(new_elem)
            else:
                if elem is not None:
                    new_list.append(elem)
        if len(new_list) == 1:      # if only one element in the list, return the element
            return new_list[0]
        else:
            return new_list

    @staticmethod
    def List_Is_Flattened(lst):
        for elem in lst:
            elem_type = type(elem)
            if elem_type is not list and elem_type is not set and elem_type is not dict:
                continue
            else:
                return False
        return True


    @staticmethod
    def Move_File_to_Destination_Dir(src_file, dest_dir):
        filename = FileHelper.Get_Base_Filename(src_file)
        destination_path = dest_dir + "/" + filename
        if not os.path.exists(destination_path):
            shutil.move(src_file, destination_path)
        else:
            os.remove(src_file)

    @staticmethod
    def Print_Files(file_list):
        stringlist = "[ "
        for file in file_list:
            filename = FileHelper.Get_Base_Filename(file)
            stringlist = stringlist + " {},".format(filename)
        stringlist = stringlist + " ]"
        print(stringlist)