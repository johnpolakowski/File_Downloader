from __future__ import print_function
from __future__ import division
from matplotlib import pyplot as plt
import cv2 as cv
import numpy as np
import argparse
import os
import ntpath
import regex
import re
#from Image_Match import Image_Match

VERIFY_ELEMENTS_DIR = '../img/verify_elements/'
VERIFY_PAGE_DIR = '../img/verify_page/'
SAMPLE_PAGES_DIR = '../img/tmp/Sample/'

title_window = 'trackbar'
image_window = 'image'

global click_X
global click_Y
global status


"""
TODO
helper to determine strength required of verify page and verify elements
    -loop over all sample pages and print distribution
    - allow to accept an image with right click
    - match recaptcha images

"""

outfile = 'verify_data.py'

header1 = """class Verify_Element:
    def __init__(self, match=None, figure_of_merit=None):
        self.img_match = match
        self.min_merit_value = figure_of_merit"""

header2 = """class VerifyList:
    def __init__(self, match=None):
        self.matches = []         # relative to coordinates returned by match (upper left hand corner)
        self.matches.append(match)

    def Add(self, match):
        self.matches.append(match)"""

"""
class file_obj:
    def __init__(self, filepath ):
        self.filepath = filepath
        self.name = Get_Filename_No_Extension(filepath)

def Get_Files_In_Dir(dir):
    path_to_watch = dir
    files=set()
    for file in os.listdir(path_to_watch):
        fullpath=os.path.join(path_to_watch, file)
        if os.path.isfile(fullpath) or os.path.isdir(fullpath):
            files.add(fullpath)
    return files

def path_leaf(path):
    head, tail = ntpath.split(path)
    return tail or ntpath.basename(head)

def Get_Filename_No_Extension(filepath):
    read_file_no_ext = os.path.splitext( filepath )[0]              # get path of xml file without the ".xml" extension
    file_no_ext_fixed = read_file_no_ext.replace(os.sep, '/')        # replace backslashes with forward slashes
    read_filename = path_leaf(file_no_ext_fixed)
    return read_filename
"""



def Match_Exactly(image, subimage):
    img = cv.imread(image)         #main image
    main_height, main_width, _ = img.shape
    print(subimage)

    template = cv.imread(subimage, cv.IMREAD_GRAYSCALE)      #subimage
    sub_height, sub_width = template.shape

    print("main image: w {}  h {}   sub image: w {}  h {}".format(main_width, main_height, sub_width, sub_height))
    if sub_width > main_width or sub_height > main_height:  #subimage must be smaller than main image
        #print("main image: w {}  h {}   sub image: w {}  h {}".format(main_width, main_height, sub_width, sub_height))
        print("bad size")
        return False

    gray_img = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    w,h = template.shape[::-1]
    result = cv.matchTemplate(gray_img,template, cv.TM_CCOEFF_NORMED)
    loc = np.where(result >= 0.9)

    x_res = len(loc[0])
    y_res = len(loc[1])
    if not (x_res >0 and y_res > 0):
        return False
    else:
        print("match: ", subimage)
        return True



def Write_Match_Object_to_File(writefile, obj_name, x, y, img_path):
    line = """{} = Click_Match()
{}.click_cen_x = {}             #click x loc relative to top left of image
{}.click_cen_y = {}             #click y loc relative to top left of image
{}.img_match = "{}" """.format(obj_name, obj_name, x, obj_name, y, obj_name, img_path)
    writefile.write(line + "\n\n")


#####################################

subimg = "../img/verify_page/Log_In_Page/elements/login01.png"
page = "../img/tmp/Select_Download/current.png"
result = Match_Exactly(page, subimg)
print("result: ", result)

"""
img = cv.imread(cv.samples.findFile(page))
cv.imshow(image_window, img)
cv.waitKey(0)


img = cv.imread(cv.samples.findFile(subimg))
cv.imshow(image_window, img)
cv.waitKey(0)
"""

"""

data_file = open(outfile, 'w')
data_file.write(header1 + "\n\n")
data_file.write(header2 + "\n\n")


files = Get_Files_In_Dir("../img/click_elements/")

f_list = []
for file in files:
    f = file_obj(file)
    f_list.append(f)

sorted_files = sorted(f_list, key=lambda f: f.name) # sort file alphabetically, by the filename part, not the full path
file = None

for item in sorted_files:
    #file = "../img/verify_page/Main_Page.png"
    file = item.filepath
    print("\t", file)
    image_window = file
    img = cv.imread(cv.samples.findFile(file))
    height,width, _ = img.shape
    window_width = width
    window_height = height
    pixel_x_max = width
    pixel_y_max = height

    if img is None:
        print('Could not open or find the image: ')
        exit(0)

    cv.namedWindow(title_window, cv.WINDOW_AUTOSIZE)
    cv.moveWindow(title_window, 100, 100)   # Move it to (x,y)
    trackbar_X_name = 'Click X' 
    trackbar_Y_name = 'Click Y' 
    cv.createTrackbar(trackbar_X_name, title_window , 0, pixel_x_max, on_trackbar_X)
    cv.createTrackbar(trackbar_Y_name, title_window , 0, pixel_y_max, on_trackbar_Y)
    #cv.resizeWindow(title_window, 450, 30)

    cv.namedWindow(image_window)
    cv.moveWindow(image_window, 565, 100)   # Move it to (x,y)
    cv.imshow(image_window, img)
    cv.setMouseCallback(image_window, click_event)

    status = 0
    while(1 and status==0):
        k = cv.waitKey(1) #wait 50 ms for a key press. if no key press, it returns -1
        if k==27 or status == 1:    # Esc key to stop
            break
        elif k == ord('w'):
            keyboard_event('w')
        elif k == ord('z'):
            keyboard_event('z')
        elif k == ord('a'):
            keyboard_event('a')
        elif k == ord('s'):
            keyboard_event('s')
        elif k==-1:  # normally -1 returned,so don't print it
            continue
        else:
            print(k) # else print its value
    #cv.waitKey()
    object_name = Get_Filename_No_Extension(file)
    Write_Click_Object_to_File(data_file, object_name, click_X, click_Y, file)

    cv.destroyAllWindows()

matchlist = None
obj_list = []
for i in range(len(sorted_files)):
    if matchlist is None:
        matchlist = []
        matchlist.append(sorted_files[i])
        # create new Match Object, add first str to it
    try:
        str1 = sorted_files[i].name
        str2 = sorted_files[i+1].name
        #name1 = re.match('[ \w-]+?(?=\.)')
        name1 = re.match(r'[a-zA-Z_]+[^\d.]', str1).group(0)
        name2 = re.match(r'[a-zA-Z_]+[^\d.]', str2).group(0)
        print("compare: {}  to  {} ".format(name1, name2) )
        if name1 == name2:  
            print("\t--- match! ---")
            matchlist.append(sorted_files[i+1])
        else:
            #print("matchlist:")
            #for m in matchlist:
                #print("\t", m.name)
            obj_list.append(matchlist)
            matchlist = None
            # write matchlist to file
            # empty matchlist
    except:
        # add 
        pass

print("------------")
line = None
for obj in obj_list:
    for i in range(len(obj)):
        elem = obj[i]
        orig_name = re.match(r'[a-zA-Z_]+[^\d.]', elem.name).group(0)
        pattern = r'((?<=_)|(?<=\s)|^|-)[a-z]'  # pattern matching the first letter of every word
        obj_name = re.sub(pattern, lambda x: x.group().upper(), orig_name)  #capitalize first letter of every word
        line = "{} = MatchList({})".format(obj_name, elem.name)
        if i == 0:
            line = "{} = MatchList({})".format(obj_name, elem.name)
        else:
            line = "{}.Add({})".format(obj_name, elem.name)
        data_file.write(line+"\n")
        data_file.flush()
        print(line)
    data_file.write("\n")  



data_file.close()

"""