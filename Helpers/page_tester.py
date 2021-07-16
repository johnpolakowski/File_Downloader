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
import numpy as np
import win32api, win32con
import win32gui
import ctypes
from verify_data3 import *
user32 = ctypes.windll.user32


SCREEN_WIDTH =  user32.GetSystemMetrics(0)
SCREEN_HEIGHT =  user32.GetSystemMetrics(1)
MIN_MATCH_COUNT = 10

#SOURCE_DIR = "./img/verify_page/Select_Download_Page/"
MAIN_SOURCE_DIR = "../img/verify_page/single/"
DISPLAY_MATCH = False

outfile = 'verify_data8.py'

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


def Has_Match(image, subimage):
    img = image
    main_height, main_width, _ = img.shape
    #print(subimage)

    template = cv2.imread(subimage, cv2.IMREAD_GRAYSCALE)      #subimage
    if template is None:
        return
    sub_height, sub_width = template.shape

    if sub_width > main_width or sub_height > main_height:  #subimage must be smaller than main image
        #print("main image: w {}  h {}   sub image: w {}  h {}".format(main_width, main_height, sub_width, sub_height))
        return False

    gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    result = cv2.matchTemplate(gray_img,template, cv2.TM_CCOEFF_NORMED)
    loc = np.where(result >= 0.9)

    x_res = len(loc[0])
    y_res = len(loc[1])
    if not (x_res >0 and y_res > 0):
        return False
    else:
        print("match", x_res, y_res)
        return True


def Get_Cropped_Region_of_Interest(file1, file2):
    find_image = cv2.imread(file1)
    match_image = cv2.imread(file2)
    #print("Find image: {}  match_subimg:  {}".format(file1, file2))
    match_h, match_w, _ = match_image.shape
    find_h, find_w, _ = find_image.shape

    sift = cv2.SIFT.create()
    keypoint1, descr1 = sift.detectAndCompute(match_image, None)
    keypoint2, descr2 = sift.detectAndCompute(find_image, None)
    bf = cv2.BFMatcher()
    matches = bf.knnMatch(descr1, descr2, k=2)
    good = []
    good2 = []
    for m,n in matches:
        if m.distance < 0.75*n.distance:
            good.append([m])
            good2.append(m)

    #print("\tmatches: {}".format(len(good)))
    if len(good) > MIN_MATCH_COUNT:
        src_pts = np.float32([ keypoint1[m.queryIdx].pt for m in good2 ]).reshape(-1,1,2)
        dst_pts = np.float32([ keypoint2[m.trainIdx].pt for m in good2 ]).reshape(-1,1,2)

        M, mask = cv2.findHomography(src_pts, dst_pts, cv2.RANSAC,5.0)
        matchesMask = mask.ravel().tolist()

        try:
            pts = np.float32([ [0,0],[0,match_h-1],[match_w-1,match_h-1],[match_w-1,0] ]).reshape(-1,1,2)
            #pts = np.float32([ [0,0],[0,find_h-1],[find_w-1,find_h-1],[find_w-1,0] ]).reshape(-1,1,2)
            dst = cv2.perspectiveTransform(pts,M)

            isClosed = True
            color = (255, 0, 0)     # Blue color in BGR 
            thickness = 2           # Line thickness of 2 px 
            img2 = cv2.polylines(find_image,[np.int32(dst)],isClosed,color,thickness, cv2.LINE_AA)
            #crop_h, crop_w, _ = img2.size
            if DISPLAY_MATCH:
                cv2.imshow("polylines", img2)
                cv2.waitKey(0)
                cv2.destroyAllWindows()

            dst = np.int32(dst)
            upper_left,lower_left,lower_right,upper_right = dst
            x1 = upper_left[0][0]
            x2 = upper_right[0][0]

            y1 = upper_left[0][1]
            y2 = lower_left[0][1]

            width = x2-x1
            height = y2-y1
            print("\t\tmatch width: ", width)
            print("\t\tmatch height: ", height)


            if width > 0 and height > 0:
                orig = cv2.imread(file1)
                cropped_image = orig[y1:y2, x1:x2]
                #cropped_h, cropped_w, _ = cropped_image.size
                return cropped_image
            else:
                return None
        except cv2.error as e:
            pass


def If_Match_Get_ROI(training_file, match_obj):
    training_image = cv2.imread(training_file)
    match_image = cv2.imread(match_obj.img)
    sift = cv2.SIFT.create()
    keypoint1, descr1 = sift.detectAndCompute(training_image, None)
    keypoint2, descr2 = sift.detectAndCompute(match_image, None)
    bf = cv2.BFMatcher()
    matches = bf.knnMatch(descr1, descr2, k=2)
    good = []
    good2 = []

    min_keypoints = match_obj.min_matches

    h, w, _ = training_image.shape
    find_h, find_w, _ = match_image.shape


    for m,n in matches:
        if m.distance < 0.75*n.distance:
            good.append([m])
            good2.append(m)

    print("\t\tactual matches: {}".format(len(good) ) )
    if len(good)>min_keypoints:
        src_pts = np.float32([ keypoint1[m.queryIdx].pt for m in good2 ]).reshape(-1,1,2)
        dst_pts = np.float32([ keypoint2[m.trainIdx].pt for m in good2 ]).reshape(-1,1,2)

        M, mask = cv2.findHomography(src_pts, dst_pts, cv2.RANSAC,5.0)
        matchesMask = mask.ravel().tolist()

        pts = np.float32([ [0,0],[0,find_h-1],[find_w-1,find_h-1],[find_w-1,0] ]).reshape(-1,1,2)
        dst = None
        try: 
            dst = cv2.perspectiveTransform(pts,M)

            isClosed = True
            color = (255, 0, 0)     # Blue color in BGR 
            thickness = 2           # Line thickness of 2 px 
            img2 = cv2.polylines(match_image,[np.int32(dst)],isClosed,color,thickness, cv2.LINE_AA)

            dst = np.int32(dst)

            upper_left,lower_left,lower_right,upper_right = dst
            x1 = upper_left[0][0]
            x2 = upper_right[0][0]

            y1 = upper_left[0][1]
            y2 = lower_left[0][1]

            width = x2-x1
            height = y2-y1
            top_left = (x1,y1)

            orig = cv2.imread(training_file)
            cropped_image = orig[y1:y2, x1:x2]
            if width > 0 and height > 0:
                #print("width: ", width, "height: ", height)
                cv2.imshow('crop', cropped_image)
                cv2.imshow('match', match_image)
                cv2.waitKey(0)
                cv2.destroyAllWindows()
            else:
                return None
        except cv2.error as e:
            pass
        return cropped_image
    else:
        return None


def Is_Keypoint_Match(image, key_elem):
    img = cv2.imread(image)         #main image
    test_img = cv2.imread(key_elem.img) 
    num_keypoints = Get_Number_of_Keypoint_Matches(img, test_img)
    if num_keypoints > key_elem.min_matches:
        return True
    else:
        return False

def Is_Keypoint_Match_I(image, key_elem):
    match_img = cv2.imread(key_elem.img) 
    #print("\t\t\tkeypoint img: ", key_elem.img)
    num_keypoints = Get_Number_of_Keypoint_Matches(image, match_img)
    if num_keypoints > key_elem.min_matches:
        print("\t\t\tmin keypoint matches: {}   actual keypoint matches: {}  image: {}".format(key_elem.min_matches, num_keypoints, key_elem.img))
        return True
    else:
        return False

def Get_Number_of_Keypoint_Matches(image1, image2):
    find_image = image2
    match_image = image1
    sift = cv2.SIFT.create()
    keypoint1, descr1 = sift.detectAndCompute(match_image, None)
    keypoint2, descr2 = sift.detectAndCompute(find_image, None)
    if descr1 is None or descr2 is None:    #if descriptors of features havent been extracted, BFMatcher will fail
        return 0
    good = []

    #bf = cv2.BFMatcher(cv2.NORM_L1, crossCheck=False)
    bf = cv2.BFMatcher()
    matches = bf.knnMatch(descr1, descr2, k=2)
    for m,n in matches:
        if m.distance < 0.75*n.distance:
            good.append([m])

    num_matches = len(good)
    return num_matches

def Get_Number_of_Keypoint_Matches_File(image1, image2):
    find_image = cv2.imread(image2)
    match_image = cv2.imread(image1)

    print("Get Num Keypoint Matches FIle: find image: ", image2)
    print("Get Num Keypoint Matches FIle: match image: ", image1)
    sift = cv2.SIFT.create()
    keypoint1, descr1 = sift.detectAndCompute(match_image, None)
    keypoint2, descr2 = sift.detectAndCompute(find_image, None)
    if descr1 is None or descr2 is None:    #if descriptors of features havent been extracted, BFMatcher will fail
        return 0
    good = []

    bf = cv2.BFMatcher(cv2.NORM_L1, crossCheck=False)
    matches = bf.knnMatch(descr1, descr2, k=2)
    for m,n in matches:
        if m.distance < 0.75*n.distance:
            good.append([m])

    num_matches = len(good)
    return num_matches


def Page_Object_Present(screenshot, match_object):
    key_images = match_object.key_objects
    exact_match_elems = match_object.exact_match_elements
    ROI_match_elems = match_object.ROI_match_elements
    for keyobj in key_images:
        img_file = keyobj.img
        print("screenshot: ", screenshot)
        print("match img: ", img_file)
        num_matches_present = Get_Number_of_Keypoint_Matches_File(screenshot, img_file)
        if num_matches_present >= keyobj.min_matches:
            roi = Get_Cropped_Region_of_Interest(screenshot, img_file)
            if roi is not None:
                # see if there are exact matches against the cropped ROI img_result {try all elements until true}
                for exact_match in exact_match_elems:
                    result = Has_Match(roi, exact_match)
                    if result == True:
                        print("---TRUE------")
                        return True
                    else:
                        continue
                
                for roi_match in ROI_match_elems:
                    result = Is_Keypoint_Match_I(roi, roi_match)
                    if result == True:
                        print("---TRUE------")
                        return True
                    else:
                        continue
                # need to see if we can determine empty checkbox from keypoint matches
            else:
                continue
    
    return False

    
#######################################################################


# Folder structure is :
# [Source Dir]
#       [Sample]
#            [match]
#                pages that match
#            [no_match]
#                pages that dont match
#       match_files
def Get_Negative_Match_Files(source_dir):
    print("source_dir: ", source_dir)
    results = FileHelper.Get_Folders_In_Dir(source_dir)
    sample_dir = None
    neg_match_dir = None
    files = []
    for res in results:
        dir_name = FileHelper.path_leaf(res) # extracts just the folder name from the full filepath
        if dir_name.lower() == "Sample".lower():
            sample_dir = res
            break
    
    print("sample_dir: ", sample_dir)
    results = FileHelper.Get_Folders_In_Dir(sample_dir)
    for res in results:
        dir_name = FileHelper.path_leaf(res) # extracts just the folder name from the full filepath
        if dir_name.lower() == "no_match".lower():
            neg_match_dir = res
            break

    print("neg match dir: ", neg_match_dir)
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

def Get_Num_SIFT_Key_Matches(image1, image2, show_results=True):
    train_img = cv2.imread(image1, cv2.IMREAD_GRAYSCALE)
    find_img = cv2.imread(image2, cv2.IMREAD_GRAYSCALE)

    #sift = cv2.SIFT.create()
    #keypoint1, descr1 = sift.detectAndCompute(train_img, None)
    #keypoint2, descr2 = sift.detectAndCompute(find_img, None)

    good = []
    orb = cv2.ORB_create(nfeatures=1000)

    # find the keypoints and descriptors with ORB
    keypoint1, descr1 = orb.detectAndCompute(train_img,None)
    keypoint2, descr2 = orb.detectAndCompute(find_img,None)
    if descr1 is None or descr2 is None:    #if descriptors of features havent been extracted, BFMatcher will fail
        return
    #bf = cv2.BFMatcher(cv2.NORM_L1,crossCheck=False)
    bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
    #matches = bf.knnMatch(descr1, descr2, k=2)
    matches = bf.match(descr1, descr2)
    #for m,n in matches:
        #if m.distance < 0.7*n.distance:
            #good.append([m])

    # Sort matches in the order of their distance.
    matches = sorted(matches, key = lambda x:x.distance)
    best_matches = matches[:20]

    src_pts = np.float32([ keypoint1[m.queryIdx].pt for m in best_matches     ]).reshape(-1,1,2)
    dst_pts = np.float32([ keypoint2[m.trainIdx].pt for m in best_matches ]).reshape(-1,1,2)
    M, mask = cv2.findHomography(src_pts, dst_pts, cv2.RANSAC,5.0)
    matchesMask = mask.ravel().tolist()
    h,w = train_img.shape[:2]
    pts = np.float32([ [0,0],[0,h-1],[w-1,h-1],[w-1,0] ]).reshape(-1,1,2)
    
    dst = cv2.perspectiveTransform(pts,M)
    dst += (w, 0)  # adding offset

    num_matches = len(good)

    # cv.drawMatchesKnn expects list of lists as matches.
    #img3 = cv2.drawMatchesKnn(train_img,keypoint1,find_img,keypoint2,good,None,flags=cv2.DrawMatchesFlags_NOT_DRAW_SINGLE_POINTS)

    draw_params = dict(matchColor = (0,255,0), # draw matches in green color
                singlePointColor = None,
                matchesMask = matchesMask, # draw only inliers
                flags = 2)

    img3 = cv2.drawMatches(train_img,keypoint1,find_img,keypoint2,best_matches, None,**draw_params)

    # Draw bounding box in Red
    img3 = cv2.polylines(img3, [np.int32(dst)], True, (0,0,255),3, cv2.LINE_AA)

    scale_width = SCREEN_WIDTH / img3.shape[1]
    scale_height = SCREEN_HEIGHT / img3.shape[0]
    scale = min(scale_width, scale_height)

    #resized window width and height
    window_width = int(img3.shape[1] * scale)
    window_height = int(img3.shape[0] * scale)

    #cv2.WINDOW_NORMAL makes the output window resizealbe
    cv2.namedWindow('SIFT', cv2.WINDOW_NORMAL)

    #resize the window according to the screen resolution
    cv2.resizeWindow('SIFT', window_width, window_height)
    cv2.imshow('SIFT', img3)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    print("\tSIFT:  ", num_matches)
    return num_matches



def Get_Num_FLANN_Key_Matches(image1, image2, show_results = True):
    train_img = cv2.imread(image1, cv2.IMREAD_GRAYSCALE)
    find_img = cv2.imread(image2, cv2.IMREAD_GRAYSCALE)

    sift = cv2.SIFT.create()
    keypoint1, descr1 = sift.detectAndCompute(train_img, None)
    keypoint2, descr2 = sift.detectAndCompute(find_img, None)
    if descr1 is None or descr2 is None:    #if descriptors of features havent been extracted, BFMatcher will fail
        print("no descriptors for FLANN")
        return
        
    good = []
    num_matches = len(good)

    # FLANN parameters
    FLANN_INDEX_KDTREE = 1
    index_params = dict(algorithm = FLANN_INDEX_KDTREE, trees = 5)
    search_params = dict(checks=50)   # or pass empty dictionary
    flann = cv2.FlannBasedMatcher(index_params,search_params)
    matches = flann.knnMatch(descr1,descr2,k=2)

    # Need to draw only good matches, so create a mask
    matchesMask = [[0,0] for i in range(len(matches))]
    # ratio test as per Lowe's paper
    for i,(m,n) in enumerate(matches):
        if m.distance < 0.7*n.distance:
            matchesMask[i]=[1,0]
            good.append([m])

    draw_params = dict(matchColor = (0,255,0),
                    singlePointColor = (255,0,0),
                    matchesMask = matchesMask,
                    flags = cv2.DrawMatchesFlags_DEFAULT)

    img3 = cv2.drawMatchesKnn(train_img,keypoint1,find_img,keypoint2,matches,None,**draw_params)

    scale_width = SCREEN_WIDTH / img3.shape[1]
    scale_height = SCREEN_HEIGHT / img3.shape[0]
    scale = min(scale_width, scale_height)

    #resized window width and height
    window_width = int(img3.shape[1] * scale)
    window_height = int(img3.shape[0] * scale)

    #cv2.WINDOW_NORMAL makes the output window resizealbe
    cv2.namedWindow('FLANN', cv2.WINDOW_NORMAL)

    #resize the window according to the screen resolution
    cv2.resizeWindow('FLANN', window_width, window_height)
    cv2.imshow('FLANN', img3)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    print("\tFLANN:  ", len(good))
    return len(good)




def Capitalize_First_Letter_Ever_Word(string):
        orig_name = re.match(r'[a-zA-Z_]+[^\d.]', string)
        pattern = r'((?<=_)|(?<=\s)|^|-)[a-z]'  # pattern matching the first letter of every word
        caps_name = re.sub(pattern, lambda x: x.group().upper(), orig_name)  #capitalize first letter of every word
        return caps_name

    
############################################################################



################################################################################
"""
training_img = MAIN_SOURCE_DIR + "training.png"


source_files = FileHelper.Get_Files_In_Dir(MAIN_SOURCE_DIR)
for src_img in source_files:
    print( FileHelper.Get_Filename_No_Extension(src_img) )
    num_SIFT_keypoints = Get_Num_FLANN_Key_Matches(training_img, src_img)
    num_FLANN_keypoints = Get_Num_SIFT_Key_Matches(training_img, src_img)

"""


data_file = open(outfile, 'w')
data_file.write(header1 + "\n\n")
data_file.write(header2 + "\n\n")
source_directories = FileHelper.Get_Folders_In_Dir(MAIN_SOURCE_DIR)
for dir in source_directories:
    SOURCE_DIR = dir

    no_match_files = Get_Negative_Match_Files(SOURCE_DIR)
    match_files = Get_Positive_Match_Files(SOURCE_DIR)
    source_files = Get_Source_Files(SOURCE_DIR)
    src_res = match_object()

    pos_res = []
    neg_res = []

    neg_false_matches = []
    pos_false_matches = []

    for neg_f in no_match_files:
        print("file: ", neg_f)
        #neg_match_image = cv2.imread(neg_f)
        res = Page_Object_Present(neg_f, Download_Complete)
        if res is True:
            neg_false_matches.append(neg_f)
        neg_res.append(res)
    
    for pos_f in match_files:
        res = Page_Object_Present(pos_f, Download_Complete)
        pos_res.append(res)
        if res is False:
            pos_false_matches.append(pos_f)
        #Get_Cropped_Region_of_Interest(pos_f, "../img/verify_page/Captcha_Incomplete/unchecked16.png")

    print("neg results: ", neg_res)
    print("\n")
    print("pos results: ", pos_res)
    print("\n")
    print("false negatives: ", neg_false_matches)
    print("\n\n")
    print("pos negatives: ", pos_false_matches)
"""
    src_res.Calc_Metrics()
    src_res.Remove_Outliers()
    src_res.Calc_Cutoff()
    src_res.Print_Results()
"""




