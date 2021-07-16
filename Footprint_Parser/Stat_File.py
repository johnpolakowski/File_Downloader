
import os
import glob
import ntpath

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

    @staticmethod
    def Match_STEP_Files(XML_dir, STEP_files, Allegro_STEP_dir):
        read_file_no_ext = os.path.splitext( Allegro_STEP_dir )[0]              # get path of xml file without the ".xml" extension
        file_no_ext_fixed = read_file_no_ext.replace(os.sep, '/')        # replace backslashes with forward slashes
        return file_no_ext_fixed
    #def Get_XML_Filename(filepath):
    #def Change_PadStack_Names(root_tag):
    #def Change_Footprint_Name(root_tag):




