import cv2
import win32api, win32con
import win32gui
import time
import os
from Stat_File import FileHelper
import glob
from PIL import ImageGrab
from PIL import Image
from Credentials import UltraLibrarian_Credentials
from Webdriver import Driver
from selenium.webdriver.support.ui import WebDriverWait
import numpy as np
import ctypes
user32 = ctypes.windll.user32
import webbrowser
#from img.img_data import *
from img.verify_data2 import *
from img.click_data import *

#import img.verify_data2

import win32com.client
shell = win32com.client.Dispatch("WScript.Shell")

Images_Examined = []
Images_Matched = []

UltraLibrarian__User_XPATH = r'//*[@id="Username"]'
UltraLibrarian__Password_XPATH =r'//*[@id="Password"]'
Login_Button_XPATH = r'/html/body/div/div/div/div/div[1]/form/fieldset/div[4]/button[1]'

DISPLAY_MATCH = False

#url = r"https://app.ultralibrarian.com/Account/Login"
url = r"https://ultralibrarian.com"

# Windows
chrome_path = r'C:/Program Files (x86)/Google/Chrome/Application/chrome.exe %s'

MIN_MATCH_COUNT = 10

SCREEN_WIDTH =  user32.GetSystemMetrics(0)
SCREEN_HEIGHT =  user32.GetSystemMetrics(1)
print("native screenshot width: ", SCREEN_WIDTH)
print("native screenshot height: ", SCREEN_HEIGHT)
x_pad = 0
y_pad = 0

"""
TODO

create alternate profiles at website to download files

Helpers:
    -click location helper
    -screenshot capture helper (take screenshot whenever enter key is pressed)

detect what current page we are on



auto erase unused screenshots
    - two screenshot methods: one for getting screenshots, one as justs a status check of current page location

speed up image processing

detect if captcha forces audio
    - download the file and analyze

put in log file if there were errors with captcha or site navigation

run two drivers simultaneously: chromedriver to parse text, chrome to get past difficult login stuff

figure out how to change ip: use protonvpn to get a different ip. do this on linux
"""



class AutoGUI:
    @staticmethod
    def leftClick():
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,0,0)
        time.sleep(.1)
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,0,0)
        print("Click.")          #completely optional. But nice for debugging purposes.

    #left mouse button down
    @staticmethod
    def leftDown():
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,0,0)
        time.sleep(.1)
        print('left Down')
    
    #left mouse button up
    @staticmethod
    def leftUp():
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,0,0)
        time.sleep(.1)
        print('left release')

    #move the mouse to position
    @staticmethod
    def mousePos(coord):
        win32api.SetCursorPos((x_pad + coord[0], y_pad + coord[1]))

    # get mouse coordinates
    @staticmethod
    def get_coords():
        x,y = win32api.GetCursorPos()
        x = x - x_pad
        y = y - y_pad
        print(x,y)

    @staticmethod
    def screenshot():
        name = os.getcwd() + '\\full_snap__' + str(int(time.time()))
        #screenshot_name = name +'.png'
        current_name = "./img/tmp/current.png"
        name_resized = os.getcwd() + r'./img/tmp/full_snap__' + str(int(time.time())) +'_resized'
        screenshot_resized = name_resized +'.png'
        
        snapshot = ImageGrab.grab()
        #snapshot.save(screenshot_name, 'PNG')
        resized = snapshot.resize((SCREEN_WIDTH, SCREEN_HEIGHT))    # resizing image so pixel locations match with get_coords
        resized.save(screenshot_resized, 'PNG')
        resized.save(current_name, 'PNG')
        return screenshot_resized

    @staticmethod
    def status_screenshot():
        current_name = "./img/tmp/current.png"       
        snapshot = ImageGrab.grab()
        resized = snapshot.resize((SCREEN_WIDTH, SCREEN_HEIGHT))    # resizing image so pixel locations match with get_coords
        resized.save(current_name, 'PNG')
        return current_name

    @staticmethod
    def Has_Match(image, subimage):
        img = cv2.imread(image)         #main image
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
            #print("match", x_res, y_res)
            return True

    @staticmethod
    def Has_Match_I(image, subimage):
        img = image         #main image
        main_height, main_width, _ = img.shape

        template = cv2.imread(subimage, cv2.IMREAD_GRAYSCALE)      #subimage
        #cv2.imshow("template", template)
        #cv2.waitKey(0)
        #cv2.destroyAllWindows()
        if template is None:
            print("template is None")
            return False
        sub_height, sub_width = template.shape

        if sub_width > main_width or sub_height > main_height:  #subimage must be smaller than main image
            #print("main image: w {}  h {}   sub image: w {}  h {}".format(main_width, main_height, sub_width, sub_height))
            print(" subimage larger than find main image")
            return False

        gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        result = cv2.matchTemplate(gray_img,template, cv2.TM_CCOEFF_NORMED)
        loc = np.where(result >= 0.9)

        x_res = len(loc[0])
        y_res = len(loc[1])
        if not (x_res >0 and y_res > 0):
            print("no matching locations")
            return False
        else:
            #print("match", x_res, y_res)
            return True

    @staticmethod
    def Login():
        credentials = UltraLibrarian_Credentials()
        AutoGUI.Click_On(Login_Button)


    @staticmethod
    def Match_Exactly(image, match_obj):
        img = cv2.imread(image)         #main image
        main_height, main_width, _ = img.shape

        print("find image: ", image)
        for elem in match_obj.matches:
            subimage  = elem.img_match
            print("\t", subimage)
            template = cv2.imread(subimage, cv2.IMREAD_GRAYSCALE)      #subimage
            if template is None:
                print("none type")
                continue
            sub_height, sub_width = template.shape

            if sub_width > main_width or sub_height > main_height:  #subimage must be smaller than main image
                #print("main image: w {}  h {}   sub image: w {}  h {}".format(main_width, main_height, sub_width, sub_height))
                continue

            gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            result = cv2.matchTemplate(gray_img,template, cv2.TM_CCOEFF_NORMED)
            loc = np.where(result >= 0.9)

            x_res = len(loc[0])
            y_res = len(loc[1])
            if not (x_res >0 and y_res > 0):
                continue
            else:
                print("\t--exact match")
                return True
        return False

    @staticmethod
    def Is_Keypoint_Match(image, key_elem):
        img = cv2.imread(image)         #main image
        test_img = cv2.imread(key_elem.img) 
        num_keypoints = AutoGUI.Get_Number_of_Keypoint_Matches(img, test_img)
        if num_keypoints > key_elem.min_matches:
            return True
        else:
            return False

    @staticmethod
    def Is_Keypoint_Match_I(image, key_elem):
        img = image
        test_img = cv2.imread(key_elem.img) 
        num_keypoints = AutoGUI.Get_Number_of_Keypoint_Matches(img, test_img)
        if num_keypoints > key_elem.min_matches:
            return True
        else:
            return False

    @staticmethod
    def Get_Number_of_Keypoint_Matches_File(image1, image2):
        find_image = cv2.imread(image2)
        match_image = cv2.imread(image1)

        #print("Get Num Keypoint Matches file: find image: ", image2)
        #print("Get Num Keypoint Matches file: match image: ", image1)
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

    @staticmethod
    def Has_Keypoint_Match(image, verify_list):
        global Images_Examined
        global Images_Matched

        img = cv2.imread(image)         #main image

        for elem in verify_list.matches:
            if elem is None:
                continue
            Images_Examined.append(elem.img_match)
            test_img = cv2.imread(elem.img_match) 
            num_keypoints = AutoGUI.Get_Number_of_Keypoint_Matches(img, test_img)
            if num_keypoints > elem.min_merit_value:
                Images_Matched.append(elem.img_match)
                return True
            else:
                continue
        return False

    @staticmethod
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

    @staticmethod
    def Match_Image(image, subimage, match_strength):            
        global Images_Examined
        global Images_Matched
        Images_Examined.append(subimage)
        name1 = FileHelper.Get_Base_Filename(image)
        name2 = FileHelper.Get_Base_Filename(subimage)
        description = "comparing {} to {}".format(name1, name2)
        print(description)

        img = cv2.imread(image)         #main image
        main_height, main_width, _ = img.shape
        gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        template = cv2.imread(subimage, cv2.IMREAD_GRAYSCALE)      #subimage
        sub_height, sub_width = template.shape
        if sub_width > main_width or sub_height > main_height:
            print("return width")
            return
        w,h = template.shape[::-1]
        print("main image: w {}  h {}   sub image: w {}  h {}".format(main_width, main_height, sub_width, sub_height))
        result = cv2.matchTemplate(gray_img,template, cv2.TM_CCOEFF_NORMED)

        loc = np.where(result >= match_strength)
        
        cv2.imshow(name1,img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

        cv2.imshow(name2,template)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

        x_size = len(loc[0])
        y_size = len(loc[1])
        if not (x_size >0 and y_size > 0):
            print("no match")
            return
        y_loc = loc[0][0]
        x_loc = loc[1][0]
        
        print(description)
        print("\thas match @ x: {}, y: {}".format(x_loc, y_loc))

        for pt in zip(*loc[::-1]):
            cv2.rectangle(img, pt,(pt[0] + w,pt[1] +h), (0,255,0),2)

        cv2.imshow(description,img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    @staticmethod
    def Draw_Box(SubObject):            
        img = cv2.imread(SubObject.img_match)         #main image
        offset_w = int(SubObject.click_width/2)
        offset_h = int(SubObject.click_height/2)

        x_1 = SubObject.click_cen_x - offset_w
        y_1 = -SubObject.click_cen_y - offset_h
        x_2 = SubObject.click_cen_x + offset_w
        y_2 = -SubObject.click_cen_y + offset_h
        print(SubObject.img_match)
        print("\t", x_1, y_1, "    ", x_2, y_2)
        #cv2.rectangle(img,(0,10),(8,2),(0,0,255),2)           
        start = (x_1,y_1)
        end = (x_2,y_2)
        #print(start)
        #print(end)

        cv2.rectangle( img, start, end, (0,0,255), 2 )      
        cv2.imshow("X",img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    @staticmethod
    def Draw_ClickBox(img, ul_x, ul_y, clickobject):            
        offset_w = int(clickobject.click_width/2)
        offset_h = int(clickobject.click_height/2)

        x_1 = clickobject.click_cen_x - offset_w
        y_1 = -clickobject.click_cen_y - offset_h
        x_2 = clickobject.click_cen_x + offset_w
        y_2 = -clickobject.click_cen_y + offset_h
        #print(clickobject.img_match)
        print("\tulx: {}, uly: {}".format(ul_x, ul_y) )
        print("\tx1: {}, y1: {}   x2: {}, y2: {}".format(x_1, y_1, x_2, y_2) )
        #cv2.rectangle(img,(0,10),(8,2),(0,0,255),2)           
        start = (x_1+ul_x,y_1+ul_y)
        end = (x_2+ul_x,y_2+ul_y)
        #print(start)
        #print(end)
        print("\tdrawing box @ {},  {}".format(start, end))

        cv2.rectangle( img, start, end, (0,0,255), 2 )      

        radius = 2
        color = (0, 255, 0)     # green color in BGR
        thickness = 2       # Line thickness of 2 px
        center_coords = (ul_x+clickobject.click_cen_x , ul_y-clickobject.click_cen_y)
        cv2.circle(img, center_coords, radius, color, thickness)
        return center_coords

    @staticmethod
    def Get_Match_Location(image, subimage):            
        img = cv2.imread(image)         #main image
        main_height, main_width, _ = img.shape
        gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        template = cv2.imread(subimage, cv2.IMREAD_GRAYSCALE)      #subimage
        sub_height, sub_width = template.shape
        if sub_width > main_width or sub_height > main_height:
            return
        w,h = template.shape[::-1]
        #print("main image: w {}  h {}   sub image: w {}  h {}".format(main_width, main_height, sub_width, sub_height))
        result = cv2.matchTemplate(gray_img,template, cv2.TM_CCOEFF_NORMED)

        loc = np.where(result >= 0.9)
        x_loc = loc[0][0]
        y_loc = loc[1][0]

        print( x_loc, y_loc)


    @staticmethod
    def Match_Image_to_Click(image, clickobject, match_strength):            
        name1 = FileHelper.Get_Base_Filename(image)
        name2 = FileHelper.Get_Base_Filename(clickobject.img_match)
        description = "comparing {} to {}".format(name1, name2)

        img = cv2.imread(image)         #main image
        main_height, main_width, _ = img.shape
        gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        template = cv2.imread(clickobject.img_match, cv2.IMREAD_GRAYSCALE)      #subimage
        sub_height, sub_width = template.shape
        if sub_width > main_width or sub_height > main_height:
            return
        w,h = template.shape[::-1]
        #print("main image: w {}  h {}   sub image: w {}  h {}".format(main_width, main_height, sub_width, sub_height))
        result = cv2.matchTemplate(gray_img,template, cv2.TM_CCOEFF_NORMED)

        loc = np.where(result >= match_strength)

        x_size = len(loc[0])
        y_size = len(loc[1])
        if not (x_size >0 and y_size > 0):
            return

        x_loc = loc[1][0]
        y_loc = loc[0][0]

        x2 = x_loc+w
        y2 = y_loc+h

        print(description)
        print("\thas match @ x: {}, y: {}".format(x_loc, y_loc))
        print("\tclick @ x: {}, y: {}".format(x_loc+w/2, y_loc+h/2))

        for pt in zip(*loc[::-1]):
            print("pt: ", pt)
            cv2.rectangle(img, pt,(pt[0] + w,pt[1] +h), (0,255,0),2)

        #cv2.rectangle( img, (x_loc, y_loc), (x2,y2), (0,255,0), 2 )     
        click = AutoGUI.Draw_ClickBox(img, x_loc, y_loc, clickobject)

        cv2.imshow(description,img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
        return click

    @staticmethod
    def Get_Click_Location(image, clickobject, match_strength):    
        global Images_Examined
        global Images_Matched
        Images_Examined.append(clickobject.img_match)
        print("Getting click location")      
        name1 = FileHelper.Get_Base_Filename(image)
        name2 = FileHelper.Get_Base_Filename(clickobject.img_match)
        description = "\tcomparing {} to {}".format(name1, name2)
        print(description)

        img = cv2.imread(image)         #main image
        main_height, main_width, _ = img.shape
        gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        template = cv2.imread(clickobject.img_match, cv2.IMREAD_GRAYSCALE)      #subimage
        sub_height, sub_width = template.shape
        if sub_width > main_width or sub_height > main_height:
            return None
        #print("main image: w {}  h {}   sub image: w {}  h {}".format(main_width, main_height, sub_width, sub_height))
        result = cv2.matchTemplate(gray_img,template, cv2.TM_CCOEFF_NORMED)

        loc = np.where(result >= match_strength)

        x_size = len(loc[0])
        y_size = len(loc[1])
        if not (x_size >0 and y_size > 0):
            return None

        Images_Matched.append(clickobject.img_match)
        y_loc = loc[0][0]
        x_loc = loc[1][0]

        click_X = x_loc + clickobject.click_cen_x
        click_Y = y_loc + clickobject.click_cen_y
        return (click_X, click_Y)

    @staticmethod
    def Verify_Page(match_page_obj):
        page_now = AutoGUI.status_screenshot()
        if AutoGUI.Has_Keypoint_Match(page_now, match_page_obj):
            time.sleep(0.05)
            return True
        else:
            return False

    @staticmethod
    def If_Match_Get_ROI(training_file, match_file):
        training_image = cv2.imread(training_file)
        test_image = cv2.imread(match_file)
        sift = cv2.SIFT.create()
        keypoint1, descr1 = sift.detectAndCompute(training_image, None)
        keypoint2, descr2 = sift.detectAndCompute(test_image, None)
        good = []
        good2 = []

        h, w, _ = training_image.shape
        find_h, find_w, _ = test_image.shape

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

            pts = np.float32([ [0,0],[0,h-1],[w-1,h-1],[w-1,0] ]).reshape(-1,1,2)
            dst = None
            try: 
                dst = cv2.perspectiveTransform(pts,M)

                isClosed = True
                color = (255, 0, 0)     # Blue color in BGR 
                thickness = 2           # Line thickness of 2 px 
                img2 = cv2.polylines(test_image,[np.int32(dst)],isClosed,color,thickness, cv2.LINE_AA)

                dst = np.int32(dst)

                upper_left,lower_left,lower_right,upper_right = dst
                x1 = upper_left[0][0]
                x2 = upper_right[0][0]

                y1 = upper_left[0][1]
                y2 = lower_left[0][1]

                width = x2-x1
                height = y2-y1
                top_left = (x1,y1)

                orig = cv2.imread(file)
                cropped_image = orig[y1:y2, x1:x2]
                if width > 0 and height > 0:
                    print("width: ", width, "height: ", height)
                    cv2.imshow('crop', cropped_image)
                    cv2.waitKey(0)
                else:
                    return None
            except cv2.error as e:
                pass
            return cropped_image
        else:
            return None

    @staticmethod
    def Page_Object_Present(match_object):
        print("checking if page object is present: ", match_object.description)
        screenshot = AutoGUI.status_screenshot()
        key_images = match_object.key_objects
        exact_match_elems = match_object.exact_match_elements
        ROI_match_elems = match_object.ROI_match_elements
        for keyobj in key_images:
            img_file = keyobj.img
            num_matches_present = AutoGUI.Get_Number_of_Keypoint_Matches_File(screenshot, img_file)
            if num_matches_present >= keyobj.min_matches:
                roi = AutoGUI.Get_Cropped_Region_of_Interest(screenshot, img_file)
                if roi is not None:
                    # see if there are exact matches against the cropped ROI img_result {try all elements until true}
                    for exact_match in exact_match_elems:
                        result = AutoGUI.Has_Match_I(roi, exact_match)
                        print("\texact match: {} , result: {}".format(exact_match, result))
                        if result == True:
                            print("\t---TRUE EXACT .... {}------".format(exact_match))
                            return True
                        else:
                            continue
                    
                    for roi_match in ROI_match_elems:
                        result = AutoGUI.Is_Keypoint_Match_I(roi, roi_match)
                        if result == True:
                            cv2.imwrite("./img/temp/roi_shot.png", roi)
                            print("---TRUE ROI.... {}------".format(roi_match.img))
                            return True
                        else:
                            continue
                    # need to see if we can determine empty checkbox from keypoint matches
                else:
                    continue
        
        return False

    @staticmethod
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

    @staticmethod
    def Click_On(clickobject):
        time.sleep(0.1)

        click_loc = None
        while click_loc is None:
            for page in clickobject.matches:
                page_now = AutoGUI.screenshot()
                print("\tclickobj: ", page.img_match)
                if AutoGUI.Has_Match(page_now, page.img_match):
                    print("\thas element matching page")
                    click_loc = AutoGUI.Get_Click_Location(page_now, page, 0.9)
                    if click_loc is not None:
                        break
        #print("click loc: ", click_loc)
        AutoGUI.mousePos(click_loc)
        time.sleep(0.1)
        AutoGUI.leftClick()

    @staticmethod
    def Wait_Until_Page_Loads(match_page_obj):
        while True:
            if AutoGUI.Verify_Page(match_page_obj):
                break
            time.sleep(0.5)

    @staticmethod
    def Wait_Until_Page_Object_Present(match_page_obj):
        print("waiting until {} page object present\n".format(match_page_obj.description))
        while True:
            if AutoGUI.Page_Object_Present(match_page_obj):
                break
            time.sleep(0.5)

    @staticmethod
    def Wait_Until_Page_Match(match_image):
        while True:
            page_now = AutoGUI.status_screenshot()
            if AutoGUI.Has_Match(page_now, match_image):
                break
            time.sleep(0.5)

    @staticmethod
    def Scroll_Down_Until_Element_Visible(match_obj):
        while True:
            shell.SendKeys('{DOWN}')
            time.sleep(0.25)
            shell.SendKeys('{DOWN}')
            time.sleep(0.25)
            shell.SendKeys('{DOWN}')
            time.sleep(0.25)
            page_now = AutoGUI.status_screenshot()

            if AutoGUI.Match_Exactly(page_now, match_obj):
                break

    @staticmethod
    def Write_Click_Results_to_File():
        global Images_Examined
        global Images_Matched
        No_Matches = [x for x in Images_Examined if x not in Images_Matched]

        writefile = open("results.txt", 'w')
        writefile.write("Images with Matches: \n")
        for img in Images_Matched:
            writefile.write(img+"\n")

        writefile.write("\nImages No Matches: \n")
        for img in No_Matches:
            writefile.write(img+"\n")

    @staticmethod
    def Is_Captcha_Solved(current_image):
        # open current image
        # see if checkbox is present
        # if it is, 
        # send to kepoint match
        current_mat = cv2.imread(current_image)
        #Captcha_Completed
        #Captcha_Not_Completed


    @staticmethod
    def Scroll_Down():
        shell.SendKeys('{DOWN}')
        time.sleep(0.05)
        shell.SendKeys('{DOWN}')
        time.sleep(0.05)
        shell.SendKeys('{DOWN}')
        time.sleep(0.15)

def main(self):
    """
    TODO
    eliminate delays
    add code to capture screenshots (not status shot) and timeout when unexpected behavior happens

    detect page
    delete cookies
    """
    webbrowser.get(chrome_path).open(url)
    time.sleep(1)
    AutoGUI.Wait_Until_Page_Loads(Main_Page)
    time.sleep(.1)
    AutoGUI.Click_On(Login_Button_Main)
    time.sleep(0.5)
    login_page = AutoGUI.Page_Object_Present(Log_In_Page)
    print("login page result: ", login_page)
    if login_page:
        print("logging in")
        AutoGUI.Login()

    AutoGUI.Wait_Until_Page_Loads(Logged_In_Page)
    print("logged in page is loaded")
    time.sleep(.15)
    AutoGUI.Click_On(Url_Bar)
    time.sleep(.1)
    shell.SendKeys('https://app.ultralibrarian.com/details/57553220-109C-11E9-AB3A-0A3560A4CCCC/Vishay/2N7002K-T1-E3?ref=digikey')
    time.sleep(.1)
    shell.SendKeys('{ENTER}')
    time.sleep(.25)
    AutoGUI.Wait_Until_Page_Loads(Component_Page)
    print("component page is loaded")
    print("scrolling down until element is visible")
    AutoGUI.Scroll_Down_Until_Element_Visible(Download_Now)
    AutoGUI.Click_On(Download_Now)
    time.sleep(.2)
    AutoGUI.Wait_Until_Page_Loads(Select_Download_Page)
    AutoGUI.Click_On(Cadence_Menu)
    AutoGUI.Wait_Until_Page_Loads(Cadence_Expanded_Menu)
    AutoGUI.Click_On(Pcb_Unchecked)
    AutoGUI.Click_On(Capture_Unchecked)
    AutoGUI.Click_On(ThreeD_Menu)
    AutoGUI.Click_On(Step_Unchecked)
    AutoGUI.Scroll_Down()
    AutoGUI.Click_On(Download_Files)
    AutoGUI.Click_On(Recaptcha_Checkbox)
    print("clicked on captcha checkbox")
    time.sleep(0.5)

    captcha_complete = AutoGUI.Page_Object_Present(Captcha_Solved)

    print("waiting until page loads")
    if captcha_complete:
    #AutoGUI.Wait_Until_Page_Loads(Captcha_Completed)
        print("captcha is completed")
        AutoGUI.Click_On(Download_Files)
        AutoGUI.Wait_Until_Page_Loads(Download_Complete)

    AutoGUI.Click_On(Url_Bar)
    time.sleep(.1)
    shell.SendKeys('https://app.ultralibrarian.com/details/7a168ee0-109b-11e9-ab3a-0a3560a4cccc/Analog-Devices-Linear-Technology/LTZ1000ACH')
    time.sleep(.1)
    shell.SendKeys('{ENTER}')
    AutoGUI.Write_Click_Results_to_File()

if __name__ == '__main__':
    self =1
    main(self)


#scale screenshots to 1536x864
#start matching images to locations

"""
Captcha_Unchecked
Captcha_Solved
Captcha_Audio
Captcha_Picture
"""