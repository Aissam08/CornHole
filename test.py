import numpy as np
import argparse
import cv2


#-- Image reading

img = cv.imread("blue_hole.jped")
hsv = cv.cvtColor(img, cv.COLOR_BGR2HSV)
h,s,v = cv.split(hsv)
ret_h, th_h = cv.threshold(h,0,255,cv.THRESH_BINARY + cv.THRESH_OTSU)