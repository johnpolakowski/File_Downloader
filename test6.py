


import cv2
import numpy as np
import matplotlib.pyplot as plt
import time
from time import time
from timeit import Timer
from Stat_File import FileHelper
import os
import win32api, win32con
import win32gui
import ctypes


user32 = ctypes.windll.user32
SCREEN_WIDTH =  user32.GetSystemMetrics(0)
SCREEN_HEIGHT =  user32.GetSystemMetrics(1)

MIN_MATCH_COUNT = 10

#original = "./img/verify_page/single/Captcha_Picture/Sample/no_match/02.png"
#match_image = cv2.imread("./img/verify_page/single/Captcha_Picture/button.png")

original = "./img/verify_page/single/opencv/01C.png"
match_image = cv2.imread("./img/verify_page/single/opencv/01A.png")

find_image = cv2.imread(original)

scale_width = (SCREEN_WIDTH / find_image.shape[1])*.9
scale_height = (SCREEN_HEIGHT / find_image.shape[0])*.9
scale = min(scale_width, scale_height)

#resized window width and height
window_width = int(find_image.shape[1] * scale)
window_height = int(find_image.shape[0] * scale)
cv2.namedWindow('ORIGINAL', cv2.WINDOW_NORMAL)
cv2.resizeWindow('ORIGINAL', window_width, window_height)
cv2.imshow("ORIGINAL", find_image)
cv2.waitKey(0)


sift = cv2.SIFT.create()
keypoint1, descr1 = sift.detectAndCompute(match_image, None)
keypoint2, descr2 = sift.detectAndCompute(find_image, None)
good = []
good2 = []

find_h, find_w, _ = match_image.shape
match_h, match_w, _ = find_image.shape

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
        img2 = cv2.polylines(find_image,[np.int32(dst)],isClosed,color,thickness, cv2.LINE_AA)

        scale_width = (SCREEN_WIDTH / img2.shape[1])*.9
        scale_height = (SCREEN_HEIGHT / img2.shape[0])*.9
        scale = min(scale_width, scale_height)

        #resized window width and height
        window_width = int(img2.shape[1] * scale)
        window_height = int(img2.shape[0] * scale)
        cv2.namedWindow('POLYLINES', cv2.WINDOW_NORMAL)
        cv2.resizeWindow('POLYLINES', window_width, window_height)
        cv2.imshow("POLYLINES", img2)
        cv2.waitKey(0)


        dst = np.int32(dst)
        upper_left,lower_left,lower_right,upper_right = dst
        x1 = upper_left[0][0]
        x2 = upper_right[0][0]
        y1 = upper_left[0][1]
        y2 = lower_left[0][1]
        print("x1: ", x1)
        print("x2: ", x2)
        print("y1: ", y1)
        print("y2: ", y2)

        width = x2-x1
        height = y2-y1
        top_left = (x1,y1)
        #print("\ttop_left: ", top_left)
        print("\tcalculated width: ", width)
        print("\tcalculated height: ", height)



        orig = cv2.imread(original)
        cropped_image = orig[y1:y2, x1:x2]
        actual_height, actual_width, _ = cropped_image.shape
        print("\tactual width: ", actual_width)
        print("\tactual height: ", actual_height)
        cv2.imshow('ORIGINAL CROPPED', cropped_image)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    except cv2.error as e:
        pass





