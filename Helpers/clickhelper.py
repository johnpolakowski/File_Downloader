from __future__ import print_function
from __future__ import division
from matplotlib import pyplot as plt
import cv2 as cv
import argparse
import os
import ntpath
import regex
import re

CLICK_ELEMENTS_DIR = '../img/click_elements/'
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

outfile = 'click_data2.py'

header1 = """class Click_Match:
    def __init__(self):
        self.click_cen_x = None         
        self.click_cen_y = None         
        self.click_width = None
        self.click_height = None
        self.img_match = None"""

header2 = """class MatchList:
    def __init__(self, match=None):
        self.matches = []         # relative to coordinates returned by match (upper left hand corner)
        if match is not None:
            self.matches.append(match)

    def Add(self, match):
        self.matches.append(match)"""




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

def on_trackbar_X( val ):
    global click_X
    global click_Y
    click_X = val
    #print("X: ", val)
    img = cv.imread( cv.samples.findFile(file) )
    draw_click_location( img, click_X, click_Y )
    cv.imshow(image_window, img)

def on_trackbar_Y( val ):
    global click_X
    global click_Y
    click_Y = val
    #print("Y: ", val)   
    img = cv.imread( cv.samples.findFile(file) )
    draw_click_location( img, click_X, click_Y )
    cv.imshow( image_window, img )

#click event function
def click_event(event, x, y, flags, param):
    global click_X
    global click_Y
    global status
    if event == cv.EVENT_LBUTTONDOWN:
        click_X = x
        click_Y = y
        img = cv.imread(cv.samples.findFile(file))
        #print(x,",",y)
        cv.setTrackbarPos(trackbar_X_name, title_window, x)
        cv.setTrackbarPos(trackbar_Y_name, title_window, y)
        draw_click_location(img, x, y)
        cv.imshow(image_window, img)
    
    if event == cv.EVENT_RBUTTONDOWN:
        status = 1

def keyboard_event(key_press):
    global click_X
    global click_Y
    if key_press == 'w':
        print("pressed w")
        click_Y = click_Y-1
        img = cv.imread(cv.samples.findFile(file))
        cv.setTrackbarPos(trackbar_X_name, title_window, click_X)
        cv.setTrackbarPos(trackbar_Y_name, title_window, click_Y)
        draw_click_location(img, click_X, click_Y)
        cv.imshow(image_window, img)
    elif key_press == 'a':
        print("pressed a")
        click_X = click_X-1
        img = cv.imread(cv.samples.findFile(file))
        cv.setTrackbarPos(trackbar_X_name, title_window, click_X)
        cv.setTrackbarPos(trackbar_Y_name, title_window, click_Y)
        draw_click_location(img, click_X, click_Y)
        cv.imshow(image_window, img)
    elif key_press == 's':
        print("pressed s")
        click_X = click_X+1
        img = cv.imread(cv.samples.findFile(file))
        cv.setTrackbarPos(trackbar_X_name, title_window, click_X)
        cv.setTrackbarPos(trackbar_Y_name, title_window, click_Y)
        draw_click_location(img, click_X, click_Y)
        cv.imshow(image_window, img)
    elif key_press == 'z':
        print("pressed z")
        click_Y = click_Y+1
        img = cv.imread(cv.samples.findFile(file))
        cv.setTrackbarPos(trackbar_X_name, title_window, click_X)
        cv.setTrackbarPos(trackbar_Y_name, title_window, click_Y)
        draw_click_location(img, click_X, click_Y)
        cv.imshow(image_window, img)

def show_In_Moved_Window(winname, img, x, y):
    cv.namedWindow(winname)        # Create a named window
    cv.moveWindow(winname, x, y)   # Move it to (x,y)
    cv.imshow(winname,img)

def Move_Window(win_name, x, y):
    cv.moveWindow(win_name, x, y)   # Move it to (x,y)

def draw_click_location(draw_img, click_x, click_y):
    radius = 2
    color = (0, 255, 0)     # green color in BGR
    thickness = 2       # Line thickness of 2 px
    center_coords = (click_x , click_y)
    cv.circle(draw_img, center_coords, radius, color, thickness)

def create_window(title, trackbar_min, trackbar_max):
    cv.namedWindow(title_window, cv.WINDOW_NORMAL)
    trackbar_X_name = 'Click X' 
    trackbar_Y_name = 'Click Y' 
    cv.createTrackbar(trackbar_X_name, title_window , 0, pixel_x_max, on_trackbar_X)
    cv.createTrackbar(trackbar_Y_name, title_window , 0, pixel_y_max, on_trackbar_Y)

def path_leaf(path):
    head, tail = ntpath.split(path)
    return tail or ntpath.basename(head)

def Get_Filename_No_Extension(filepath):
    read_file_no_ext = os.path.splitext( filepath )[0]              # get path of xml file without the ".xml" extension
    file_no_ext_fixed = read_file_no_ext.replace(os.sep, '/')        # replace backslashes with forward slashes
    read_filename = path_leaf(file_no_ext_fixed)
    return read_filename

def Write_Click_Object_to_File(writefile, obj_name, x, y, img_path):
    line = """{} = Click_Match()
{}.click_cen_x = {}             #click x loc relative to top left of image
{}.click_cen_y = {}             #click y loc relative to top left of image
{}.img_match = "{}" """.format(obj_name, obj_name, x, obj_name, y, obj_name, img_path)
    writefile.write(line + "\n\n")


#####################################
data_file = open(outfile, 'w')
data_file.write(header1 + "\n\n")
data_file.write(header2 + "\n\n")

files = Get_Files_In_Dir("../img/click/")

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
        if name1 == name2:  
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