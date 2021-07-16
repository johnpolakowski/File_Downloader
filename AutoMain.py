import cv2
import win32api, win32con
import time
import os
from Stat_File import FileHelper
import glob
from PIL import ImageGrab
from PIL import Image

import numpy as np
import ctypes
user32 = ctypes.windll.user32

SCREEN_WIDTH =  user32.GetSystemMetrics(0)
SCREEN_HEIGHT =  user32.GetSystemMetrics(1)
print("width: ", SCREEN_WIDTH)
print("height: ", SCREEN_HEIGHT)
x_pad = 0
y_pad = 0

class AutoGUI:
    @staticmethod
    def leftClick():
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,0,0)
        time.sleep(.1)
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,0,0)
        print("Click.")          #completely optional. But nice for debugging purposes.

    @staticmethod
    def leftDown():
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,0,0)
        time.sleep(.1)
        print('left Down')
            
    @staticmethod
    def leftUp():
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,0,0)
        time.sleep(.1)
        print('left release')

    @staticmethod
    def mousePos(coord):
        win32api.SetCursorPos((x_pad + coord[0], y_pad + coord[1]))

    @staticmethod
    def get_coords():
        x,y = win32api.GetCursorPos()
        x = x - x_pad
        y = y - y_pad
        print(x,y)

    @staticmethod
    def screenshot():
        print("yob yob")
        print(os.getcwd())
        name = os.getcwd() + '\\full_snap__' + str(int(time.time()))
        screenshot_name = name +'.png'
        name_resized = os.getcwd() + '\\full_snap__' + str(int(time.time())) +'_resized'
        screenshot_resized = name_resized +'.png'
        
        snapshot = ImageGrab.grab()
        #snapshot.save(screenshot_name, 'PNG')
        resized = snapshot.resize((SCREEN_WIDTH, SCREEN_HEIGHT))    # resizing image so pixel locations match with get_coords
        resized.save(screenshot_resized, 'PNG')
        return screenshot_resized

    @staticmethod
    def Has_Match(image, subimage):
        img = cv2.imread(image)         #main image
        main_height, main_width, _ = img.shape

        template = cv2.imread(subimage, cv2.IMREAD_GRAYSCALE)      #subimage
        sub_height, sub_width = template.shape

        if sub_width > main_width or sub_height > main_height:  #subimage must be smaller than main image
            #print("main image: w {}  h {}   sub image: w {}  h {}".format(main_width, main_height, sub_width, sub_height))
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
            return True

    @staticmethod
    def Match_Image(image, subimage, match_strength):            
        name1 = FileHelper.Get_Base_Filename(image)
        name2 = FileHelper.Get_Base_Filename(subimage)
        description = "comparing {} to {}".format(name1, name2)

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

        loc = np.where(result >= match_strength)

        x_size = len(loc[0])
        y_size = len(loc[1])
        if not (x_size >0 and y_size > 0):
            return
        x_loc = loc[0][0]
        y_loc = loc[1][0]
        
        print(description)
        print("\thas match @ x: {}, y: {}".format(x_loc, y_loc))

        for pt in zip(*loc[::-1]):
            cv2.rectangle(img, pt,(pt[0] + w,pt[1] +h), (0,255,0),2)

        cv2.imshow(description,img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

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

    @staticmethod
    def Get_Match_Files():
        file_list = []
        print("Main Image Files:")
        for filename in glob.glob(os.path.join("./Match", '*.png')): #iterate through each .xml file in current directory
            file_list.append(filename)
            print("\t" + FileHelper.Get_Base_Filename(filename))
        return file_list

    @staticmethod
    def Get_Img_Files():
        file_list = []
        print("Sub Image Files:")
        for filename in glob.glob(os.path.join("./img", '*.png')): #iterate through each .xml file in current directory
            file_list.append(filename)
            print("\t" + FileHelper.Get_Base_Filename(filename))
        return file_list

def main(self):
    #time.sleep(3)
    #screenshot = AutoGUI.screenshot()
    #AutoGUI.Match_Image("./Match/Cadence_Menu.png", "img/username.png")

    match_files = AutoGUI.Get_Match_Files()
    img_files = AutoGUI.Get_Img_Files()
    for file in match_files:
        for subimg in img_files:
            if AutoGUI.Has_Match(file, subimg):
                AutoGUI.Match_Image(file, subimg, 0.95)
    #AutoGUI.Match_Image("./Full.png", "img/UL_login.png")

if __name__ == '__main__':
    self =1
    main(self)


#scale screenshots to 1536x864
#start matching images to locations

"""
	source = cvLoadImage('simpson.jpg')
	template = cvLoadImage('milhouse.jpg')

	width = source.width - template.width + 1
	height = source.height - template.height + 1
	result = cvCreateImage(cvSize(width, height), 32, 1)

	mathod = CV_TM_SQDIFF
	#mathod = CV_TM_SQDIFF_NORMED
	#mathod = CV_TM_CCORR
	#mathod = CV_TM_CCORR_NORMED
	#mathod = CV_TM_CCOEFF
	#mathod = CV_TM_CCOEFF_NORMED
	cvMatchTemplate(source, template, result, mathod)

	minval, maxval, minloc, maxloc = cvMinMaxLoc(result, 0)
	
	matchloc = cvPoint(0, 0)
	if mathod == CV_TM_SQDIFF or mathod == CV_TM_SQDIFF_NORMED:
		matchloc = minloc
	else:
		matchloc = maxloc

	cvRectangle(source, cvPoint(matchloc.x, matchloc.y), cvPoint(matchloc.x + template.width, matchloc.y + template.height), CV_RGB(255, 0, 0))

	cvNamedWindow('Source', CV_WINDOW_AUTOSIZE)
	cvNamedWindow('Result', CV_WINDOW_AUTOSIZE)	

	cvShowImage('Source', source)
	cvShowImage('Result', result)

	cvWaitKey(0)

	cvReleaseImage(source)
	cvReleaseImage(template)
	cvReleaseImage(result)

	cvDestroyWindow('Source')
	cvDestroyWindow('Result')
"""