


import cv2
import numpy as np
import matplotlib.pyplot as plt
import time
from time import time
from timeit import Timer
from Stat_File import FileHelper
import os

"""
TODO

features to match on ultralibrarian
    -login button

"""

SOURCE_DIR = "./img/verify_page/single/Captcha_Incomplete/Sample/match/"




MIN_MATCH_COUNT = 10

class match_result:
    def __init__(self):
        self.filepath = None
        self.match_strength = None
        self.result = None


def Get_Cropped_Region_of_Interest(file1, file2):
    print("Cropped ROI Func")
    find_image = cv2.imread(file2)
    match_image = cv2.imread(file1)
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

    print("\tmatches: {}".format(len(good)))
    if len(good) > MIN_MATCH_COUNT:
        src_pts = np.float32([ keypoint1[m.queryIdx].pt for m in good2 ]).reshape(-1,1,2)
        dst_pts = np.float32([ keypoint2[m.trainIdx].pt for m in good2 ]).reshape(-1,1,2)

        M, mask = cv2.findHomography(src_pts, dst_pts, cv2.RANSAC,5.0)
        matchesMask = mask.ravel().tolist()

        try:
            pts = np.float32([ [0,0],[0,match_h-1],[match_w-1,match_h-1],[match_w-1,0] ]).reshape(-1,1,2)
            dst = cv2.perspectiveTransform(pts,M)
            dst = np.int32(dst)

            upper_left,lower_left,lower_right,upper_right = dst
            x1 = upper_left[0][0]
            x2 = upper_right[0][0]

            y1 = upper_left[0][1]
            y2 = lower_left[0][1]

            width = x2-x1
            height = y2-y1
            top_left = (x1,y1)
            #print("\ttop_left: ", top_left)
            print("\t\tmatch width: ", width)
            print("\t\tmatch height: ", height)


            if width > 0 and height > 0:
                orig = cv2.imread(file)
                cropped_image = orig[y1:y2, x1:x2]
                cv2.imshow("cropped roi_1", cropped_image)
                cv2.waitKey(0) #wait 50 ms for a key press. if no key press, it returns -1
                cv2.destroyAllWindows()
                return cropped_image
            else:
                return None
        except cv2.error as e:
            pass


def Get_Number_of_Matches(image1, image2):
    #find_image = cv2.imread(file2)
    #match_image = cv2.imread(file1)
    find_image = image2
    match_image = image1

    sift = cv2.SIFT.create()
    keypoint1, descr1 = sift.detectAndCompute(match_image, None)
    keypoint2, descr2 = sift.detectAndCompute(find_image, None)
    if descr1 is None or descr2 is None:    #if descriptors of features havent been extracted, BFMatcher will fail
        return
    good = []
    good2 = []

    bf = cv2.BFMatcher(cv2.NORM_L1,crossCheck=False)

    matches = bf.knnMatch(descr1, descr2, k=2)
    for m,n in matches:
        if m.distance < 0.75*n.distance:
            good.append([m])
            good2.append(m)

    num_matches = len(good)
    """
    if num_matches > MIN_MATCH_COUNT:
        print("\tnum matches: ",num_matches)
        img3 = cv2.drawMatchesKnn(match_image, keypoint1, find_image, keypoint2, good[:100], None, flags=2)
        cv2.imshow("num matches: {}".format(len(good)), img3)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
    """
    
    return num_matches


def Find_Match(find_image, file):
    find_img = cv2.imread(find_image)
    match_image = cv2.imread(file)
    sift = cv2.SIFT.create()
    keypoint1, descr1 = sift.detectAndCompute(find_img, None)
    keypoint2, descr2 = sift.detectAndCompute(match_image, None)
    good = []
    good2 = []

    find_h, find_w, _ = find_img.shape
    match_h, match_w, _ = match_image.shape

    bf = cv2.BFMatcher()
    matches = bf.knnMatch(descr1, descr2, k=2)
    for m,n in matches:
        if m.distance < 0.75*n.distance:
            good.append([m])
            good2.append(m)

    if len(good)>MIN_MATCH_COUNT:
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

            cv2.imshow("polylines", img2)
            cv2.waitKey(0)

            dst = np.int32(dst)

            upper_left,lower_left,lower_right,upper_right = dst
            x1 = upper_left[0][0]
            x2 = upper_right[0][0]

            y1 = upper_left[0][1]
            y2 = lower_left[0][1]
            #print("x1: ", x1)
            #print("x2: ", x2)
            #print("y1: ", y1)
            #print("y2: ", y2)

            width = x2-x1
            height = y2-y1
            top_left = (x1,y1)
            #print("\ttop_left: ", top_left)
            print("\t\tmatch width: ", width)
            print("\t\tmatch height: ", height)



            orig = cv2.imread(file)
            cv2.imshow('FindMatch, original', orig)
            cv2.waitKey(0)

            cropped_image = orig[y1:y2, x1:x2]
            if width > 0 and height > 0:
                print("width: ", width, "height: ", height)
                cv2.imshow('FindMatch, crop', cropped_image)
                cv2.waitKey(0)


            """
            dir = os.path.dirname(file)
            dir = dir + "/" + "crop" +"/"
            if not os.path.isdir(dir):
                os.mkdir( dir )

            base_name = FileHelper.Get_Filename_No_Extension(file)
            new_name = dir + base_name + "_" + "crop" + ".png"
            print(new_name)

            cv2.imwrite(new_name,cropped_image) 
            """
            match_area = "    match region: {} x {}   ".format(width, height)

            filename = FileHelper.Get_Base_Filename(file)
            num_matches = "FindMatch,   img: {}   num matches: {}     ".format(filename, len(good))
            num_matches = num_matches 
            print(num_matches)
            cv2.imshow(num_matches, img2)
            cv2.waitKey(0)

            draw_params = dict(matchColor = (0,255,0), # draw matches in green color
                            singlePointColor = None,
                            matchesMask = matchesMask, # draw only inliers
                            flags = 2)

            img3 = cv2.drawMatches(find_img,keypoint1,match_image,keypoint2,good2,None,**draw_params)
            cv2.imshow(num_matches, img3)
            cv2.waitKey(0)
            cv2.destroyAllWindows()
            return img3
        except cv2.error as e:
            pass
        #plt.imshow(img3, 'gray'),plt.show()
    else:
        print("\tnot enough matches: ", len(good))
#############################


SOURCE_DIR = "./img/verify_page/single/Captcha_Audio/Sample/no_match/"

cwd = FileHelper.Get_Files_In_Download_Dir( SOURCE_DIR )
allfiles = []
for file in cwd:
    if( os.path.isfile(file) ):
        allfiles.append(file)
    if( os.path.isdir(file) ):
        print("DIR: ", file)
        dir = file
        files = FileHelper.Get_Files_In_Download_Dir( dir )
        for f in files:
            if( os.path.isfile(f) ):
                allfiles.append(f)

#match_img = "./img/verify_page/single/Captcha_Incomplete/unchecked15.png"
#test_img = "./img/verify_page/single/Captcha_Incomplete/unchecked15.png"


match_img = "./img/verify_page/single/Captcha_Audio/F.png"

## Matching Single File against sample files
target = match_img
match_image = cv2.imread(target)
target_name = FileHelper.Get_Filename_No_Extension(target)
print("TARGET: ", target_name)
results = []


for file in allfiles:
    print(target, file)
    img_res = match_result()
    img_res.filepath = file
    img3 = Find_Match(match_img, file)
    #cv2.imshow("result", img3)
    #print(file)
    #cropped_roi = Get_Cropped_Region_of_Interest(match_img, file)
    cropped_roi = None
    #find_image = cv2.imread(file)
    #img_res.match_strength = Get_Number_of_Matches(match_image, find_image)
    if cropped_roi is not None:
        cv2.imshow("cropped roi_2", cropped_roi)
        cv2.waitKey(0) #wait 50 ms for a key press. if no key press, it returns -1
        cv2.destroyAllWindows()
