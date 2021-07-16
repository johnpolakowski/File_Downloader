
import cv2
import numpy as np
import matplotlib.pyplot as plt
import time
from time import time
import os
from Stat_File import FileHelper

GREEN = (0,255,0)
RED = (0,0,255)

test_files = FileHelper.Get_Files_In_Download_Dir("./img/tmp")


def Scale_Image(img, ratio):
    src = cv2.imread(img, cv2.IMREAD_UNCHANGED)

    new_width = int(src.shape[1] * ratio)
    new_height = int(src.shape[0] * ratio)

    dsize = (new_width, new_height)
    output = cv2.resize(src, dsize)

    font = cv2.FONT_HERSHEY_SIMPLEX
    cv2.putText(output,str(ratio),(600,45), font, 2,RED,3,cv2.LINE_AA)

    dir = os.path.dirname(img)
    dir = dir + "/" + str(ratio) +"/"
    if not os.path.isdir(dir):
        os.mkdir( dir )

    base_name = FileHelper.Get_Filename_No_Extension(img)
    new_name = dir + base_name + "_" + str(ratio) + ".png"
    print(new_name)

    cv2.imwrite(new_name,output) 
    #cv2.imshow(new_name, output)
    ##cv2.waitKey(0)
    #cv2.destroyAllWindows()


test_files = FileHelper.Get_Files_In_Download_Dir("./img/verify_page/target/")
#Scale_Image("./img/verify_page/Ultralibrarian.png", 0.96)


for file in test_files:
    if(os.path.isfile(file)):
        Scale_Image(file, 0.96)
        Scale_Image(file, 0.94)
        Scale_Image(file, 0.92)
        Scale_Image(file, 0.90)
        Scale_Image(file, 0.88)
        Scale_Image(file, 0.86)

"""
file = "./img/verify_page/Main_Page.png"
if(os.path.isfile(file)):
    Scale_Image(file, 0.96)
    Scale_Image(file, 0.94)
    Scale_Image(file, 0.92)
    Scale_Image(file, 0.90)
    Scale_Image(file, 0.88)
    Scale_Image(file, 0.86)
"""