
import cv2
import win32api, win32con
import win32gui
import time
import os
from Stat_File import FileHelper
import glob
from PIL import ImageGrab
from PIL import Image

import numpy as np
import ctypes
user32 = ctypes.windll.user32
import webbrowser
from img.img_data import *
from AutoGui import AutoGUI


SCREEN_WIDTH =  user32.GetSystemMetrics(0)
SCREEN_HEIGHT =  user32.GetSystemMetrics(1)
print("width: ", SCREEN_WIDTH)
print("height: ", SCREEN_HEIGHT)
MIN_MATCH_COUNT = 0

class Image_Match:
    @staticmethod
    def Get_Cropped_Region_of_Interest(file1, file2):
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

        if len(good) > MIN_MATCH_COUNT:
            src_pts = np.float32([ keypoint1[m.queryIdx].pt for m in good2 ]).reshape(-1,1,2)
            dst_pts = np.float32([ keypoint2[m.trainIdx].pt for m in good2 ]).reshape(-1,1,2)

            M, mask = cv2.findHomography(src_pts, dst_pts, cv2.RANSAC,5.0)
            matchesMask = mask.ravel().tolist()

            pts = np.float32([ [0,0],[0,match_h-1],[match_w-1,match_h-1],[match_w-1,0] ]).reshape(-1,1,2)
            dst = cv2.perspectiveTransform(pts,M)
            dst = np.int32(dst)

            upper_left,lower_left,lower_right,upper_right = dst
            x1 = upper_left[0][0]
            x2 = upper_right[0][0]

            y1 = upper_left[0][1]
            y2 = lower_left[0][1]

            orig = cv2.imread(file)
            cropped_image = orig[y1:y2, x1:x2]
            return cropped_image

    @staticmethod
    def Get_Number_of_Keypoint_Matches_SIFT(image1, image2):
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
        if num_matches > MIN_MATCH_COUNT:
            #print("\tnum matches: ",num_matches)
            img3 = cv2.drawMatchesKnn(match_image, keypoint1, find_image, keypoint2, good[:100], None, flags=2)
            cv2.imshow("num matches: {}".format(len(good)), img3)
            cv2.waitKey(0)
            cv2.destroyAllWindows()
        
        return num_matches

    @staticmethod
    def screenshot():
        name_resized = os.getcwd() + r'./img/tmp/' + str(int(time.time())) +'_resized' + '.png'
        snapshot = ImageGrab.grab()
        resized = snapshot.resize((SCREEN_WIDTH, SCREEN_HEIGHT))    # resizing image so pixel locations match with get_coords
        resized.save(name_resized, 'PNG')
        return name_resized

    @staticmethod
    def status_screenshot():
        current_name = "./img/tmp/current.png"       
        snapshot = ImageGrab.grab()
        resized = snapshot.resize((SCREEN_WIDTH, SCREEN_HEIGHT))    # resizing image so pixel locations match with get_coords
        resized.save(current_name, 'PNG')
        return current_name


    # looks for an exact match of subimage in image. scale matters
    @staticmethod
    def Has_Exact_Match(image, subimage):
        img = cv2.imread(image)         #main image
        main_height, main_width, _ = img.shape
        print(subimage)

        template = cv2.imread(subimage, cv2.IMREAD_GRAYSCALE)      #subimage
        sub_height, sub_width = template.shape

        if sub_width > main_width or sub_height > main_height:  #subimage must be smaller than main image
            return False

        gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        w,h = template.shape[::-1]
        result = cv2.matchTemplate(gray_img,template, cv2.TM_CCOEFF_NORMED)
        loc = np.where(result >= 0.9)

        x_res = len(loc[0])
        y_res = len(loc[1])
        if not (x_res >0 and y_res > 0):
            return False
        else:
            print("match: ", subimage)
            return True

    @staticmethod
    def Get_Exact_Click_Location(image, clickobject, match_strength):         
        Image_Match.status_screenshot()   
        name1 = FileHelper.Get_Base_Filename(image)
        name2 = FileHelper.Get_Base_Filename(clickobject.img_match)

        img = cv2.imread(image)         #main image
        main_height, main_width, _ = img.shape
        gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        template = cv2.imread(clickobject.img_match, cv2.IMREAD_GRAYSCALE)      #subimage
        sub_height, sub_width = template.shape
        if sub_width > main_width or sub_height > main_height:
            return
        result = cv2.matchTemplate(gray_img,template, cv2.TM_CCOEFF_NORMED)

        loc = np.where(result >= match_strength)

        x_size = len(loc[0])
        y_size = len(loc[1])
        if not (x_size >0 and y_size > 0):
            return

        y_loc = loc[0][0]
        x_loc = loc[1][0]

        click = Image_Match.Draw_ClickBox(img, x_loc, y_loc, clickobject)
        return click

    @staticmethod
    def Draw_ClickBox(img, ul_x, ul_y, clickobject):            
        offset_w = int(clickobject.click_width/2)
        offset_h = int(clickobject.click_height/2)

        x_1 = clickobject.click_cen_x - offset_w
        y_1 = -clickobject.click_cen_y - offset_h
        x_2 = clickobject.click_cen_x + offset_w
        y_2 = -clickobject.click_cen_y + offset_h
        print("\tulx: {}, uly: {}".format(ul_x, ul_y) )
        print("\tx1: {}, y1: {}   x2: {}, y2: {}".format(x_1, y_1, x_2, y_2) )          
        start = (x_1+ul_x,y_1+ul_y)
        end = (x_2+ul_x,y_2+ul_y)
        print("\tdrawing box @ {},  {}".format(start, end))

        cv2.rectangle( img, start, end, (0,0,255), 2 )      

        radius = 2
        color = (0, 255, 0)     # green color in BGR
        thickness = 2       # Line thickness of 2 px
        center_coords = (ul_x+clickobject.click_cen_x , ul_y-clickobject.click_cen_y)
        cv2.circle(img, center_coords, radius, color, thickness)
        return center_coords


    @staticmethod
    def Verify_Page(match_pageimg):
        page_now = Image_Match.status_screenshot()
        if Image_Match.Has_Match(page_now, match_pageimg):
            time.sleep(1)
            return True
        else:
            return False

    @staticmethod
    def Click_On(clickobject):
        page_now = Image_Match.screenshot()
        click_loc = None
        for page in clickobject.matches:
            if Image_Match.Has_Match(page_now, page.img_match):
                print("has element matching page")
                click_loc = Image_Match.Get_Click_Location(page_now, page, 0.9)
                print("click loc: ", click_loc)
                break
        AutoGUI.mousePos(click_loc)
        time.sleep(0.1)
        AutoGUI.leftClick()

    @staticmethod
    def Wait_Until_Page_Loads(match_page_img):
        while True:
            if AutoGUI.Verify_Page(match_page_img):
                break
            time.sleep(0.25)
