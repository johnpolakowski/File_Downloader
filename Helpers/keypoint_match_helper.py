import cv2
import numpy as np
import matplotlib.pyplot as plt
import time
from time import time
from timeit import Timer
from Stat_File import FileHelper
import os
from statistics import stdev
import regex
import re

#SOURCE_DIR = "./img/verify_page/Select_Download_Page/"
MAIN_SOURCE_DIR = "../img/verify_page/single/"

outfile = 'verify_data3.py'

header1 = """class Verify_Element:
    def __init__(self, match=None, figure_of_merit=None):
        self.img_match = match
        self.min_merit_value = figure_of_merit"""

header2 = """class VerifyList:
    def __init__(self, match=None):
        self.matches = []         # relative to coordinates returned by match (upper left hand corner)
        if match is not None:
            self.matches.append(match)

    def Add(self, match):
        self.matches.append(match)"""


class match_object:
    def __init__(self):
        self.filepath = None
        self.neg_results = []
        self.pos_results = []
        self.max_neg_res = None
        self.min_pos_res = None
        self.avg_pos = None
        self.avg_neg = None
        self.pos_stdev = None
        self.cutoff_match = None

    def Get_Max_Negative_Result_Keypoints(self):
        self.max_neg_res = max(self.neg_results)
        return self.max_neg_res

    def Get_Min_Positive_Result_Keypoints(self):
        self.min_pos_res = min(self.pos_results)
        return self.min_pos_res

    def Get_Avg_Positive_Keypoints(self):
        tot_sum = sum(self.pos_results)
        num_points = len(self.pos_results)
        self.avg_pos = int(tot_sum/num_points)
        return self.avg_pos

    def Get_Avg_Negative_Keypoints(self):
        tot_sum = sum(self.neg_results)
        num_points = len(self.neg_results)
        self.avg_neg = int(tot_sum/num_points)
        return self.avg_neg

    def Get_Std_Deviation(self):
        self.pos_stdev = stdev(self.pos_results)
        return self.pos_stdev

    # removes low hanging outlier values (more than 1 std dev from average) from positive results
    def Remove_Outliers(self):
        for res in self.pos_results:
            if res < (self.avg_pos - self.pos_stdev):
                self.pos_results.remove(res)

    def Calc_Cutoff(self):
        self.Calc_Metrics()
        self.Remove_Outliers()
        self.Calc_Metrics()
        delta = 0.5*(self.avg_pos - self.min_pos_res)
        cutoff1 = self.avg_pos - delta

        avg_diff = self.avg_pos - self.avg_neg
        cutoff2 = self.min_pos_res - .05*avg_diff

        self.cutoff_match = int( (cutoff1 + cutoff2)/2 )
        if self.cutoff_match > self.min_pos_res:
            self.cutoff_match = self.min_pos_res
        print("\ncutoff1: ", cutoff1)
        print("cutoff2: ", cutoff2)

    def Calc_Metrics(self):
        self.Get_Avg_Positive_Keypoints()
        self.Get_Avg_Negative_Keypoints()
        self.Get_Min_Positive_Result_Keypoints()
        self.Get_Max_Negative_Result_Keypoints()
        self.Get_Std_Deviation()

    def Print_Results(self):
        print("Results for image: {}".format(self.filepath))
        print("\tpos match keypoints: {}".format(self.pos_results))
        print("\t\tmin: {}\t avg: {}".format(self.Get_Min_Positive_Result_Keypoints(), self.Get_Avg_Positive_Keypoints() ))
        print("\tneg match keypoints: {}".format(self.neg_results))
        print("\t\tmax: {}\t avg: {}".format(self.Get_Max_Negative_Result_Keypoints(), self.Get_Avg_Negative_Keypoints() ))
        print("\tmin cutoff for positive match: ", self.cutoff_match)





# Folder structure is :
# [Source Dir]
#       [Sample]
#            [match]
#                pages that match
#            [no_match]
#                pages that dont match
#       match_files
def Get_Negative_Match_Files(source_dir):
    results = FileHelper.Get_Folders_In_Dir(source_dir)
    sample_dir = None
    neg_match_dir = None
    files = []
    for res in results:
        dir_name = FileHelper.path_leaf(res) # extracts just the folder name from the full filepath
        if dir_name.lower() == "Sample".lower():
            sample_dir = res
            break
    
    results = FileHelper.Get_Folders_In_Dir(sample_dir)
    for res in results:
        dir_name = FileHelper.path_leaf(res) # extracts just the folder name from the full filepath
        if dir_name.lower() == "no_match".lower():
            neg_match_dir = res
            break

    files = FileHelper.Get_Files_In_Dir(neg_match_dir)
    return files


def Get_Positive_Match_Files(source_dir):
    results = FileHelper.Get_Folders_In_Dir(source_dir)
    sample_dir = None
    neg_match_dir = None
    files = []
    for res in results:
        dir_name = FileHelper.path_leaf(res) # extracts just the folder name from the full filepath
        if dir_name.lower() == "Sample".lower():
            sample_dir = res
            break
    
    results = FileHelper.Get_Folders_In_Dir(sample_dir)
    for res in results:
        dir_name = FileHelper.path_leaf(res) # extracts just the folder name from the full filepath
        if dir_name.lower() == "match".lower():
            neg_match_dir = res
            break

    files = FileHelper.Get_Files_In_Dir(neg_match_dir)
    return files

def Get_Source_Files(source_dir):
    print(source_dir)
    return FileHelper.Get_Files_In_Dir(source_dir)

def Get_Number_of_Keypoint_Matches(image1, image2):
    find_image = image2
    match_image = image1

    sift = cv2.SIFT.create()
    keypoint1, descr1 = sift.detectAndCompute(match_image, None)
    keypoint2, descr2 = sift.detectAndCompute(find_image, None)
    if descr1 is None or descr2 is None:    #if descriptors of features havent been extracted, BFMatcher will fail
        return
    good = []

    bf = cv2.BFMatcher(cv2.NORM_L1,crossCheck=False)
    matches = bf.knnMatch(descr1, descr2, k=2)
    for m,n in matches:
        if m.distance < 0.75*n.distance:
            good.append([m])

    num_matches = len(good)
    return num_matches

def Capitalize_First_Letter_Ever_Word(string):
        orig_name = re.match(r'[a-zA-Z_]+[^\d.]', string)
        pattern = r'((?<=_)|(?<=\s)|^|-)[a-z]'  # pattern matching the first letter of every word
        caps_name = re.sub(pattern, lambda x: x.group().upper(), orig_name)  #capitalize first letter of every word
        return caps_name

    
############################################################################

################################################################################
data_file = open(outfile, 'w')
data_file.write(header1 + "\n\n")
data_file.write(header2 + "\n\n")
source_directories = FileHelper.Get_Folders_In_Dir(MAIN_SOURCE_DIR)
for dir in source_directories:
    SOURCE_DIR = dir

    no_match_files = Get_Negative_Match_Files(SOURCE_DIR)
    match_files = Get_Positive_Match_Files(SOURCE_DIR)
    source_files = Get_Source_Files(SOURCE_DIR)

    elem_list = []
    for src_f in source_files:
        src_res = match_object()    # get object that records the template matching results
        src_res.filepath = src_f
        src_image = cv2.imread(src_f)

        #get num keypoint matches for negative results
        for neg_f in no_match_files:
            neg_match_image = cv2.imread(neg_f)
            num_keypoints = Get_Number_of_Keypoint_Matches(src_image, neg_match_image)
            #print("\tneg match file: {}  keypoints: {} ".format(FileHelper.path_leaf(neg_f), num_keypoints) )
            src_res.neg_results.append(num_keypoints)
        
        for pos_f in match_files:
            match_image = cv2.imread(pos_f)
            num_keypoints = Get_Number_of_Keypoint_Matches(src_image, match_image)
            #print("\tpos match file: {}  keypoints: {} ".format(FileHelper.path_leaf(pos_f), num_keypoints) )
            src_res.pos_results.append(num_keypoints)

        src_res.Calc_Metrics()
        src_res.Remove_Outliers()
        src_res.Calc_Cutoff()
        src_res.Print_Results()
        
        var_name = FileHelper.Get_Filename_No_Extension(src_f)
        write_str = "{} = Verify_Element(\"{}\", {})".format(var_name, src_f, src_res.cutoff_match)
        data_file.write(write_str + "\n")
        elem_list.append(var_name)

    verify_obj = FileHelper.path_leaf(SOURCE_DIR)
    write_str = "{} = VerifyList()".format(verify_obj)
    data_file.write(write_str + "\n")
    for elem in elem_list:
        write_str = "{}.Add({})".format(verify_obj, elem)
        data_file.write(write_str + "\n")
    data_file.write("\n")
data_file.flush()
data_file.close()


