import numpy as np
import argparse
import cv2 as cv


#-- Image reading

img = cv.imread("/home/aissam/Stage/CornHole/blue_hole.jpeg")
hsv = cv.cvtColor(img, cv.COLOR_BGR2HSV)
h,s,v = cv.split(hsv)
ret_h, th_h = cv.threshold(s,0,255,cv.THRESH_BINARY + cv.THRESH_OTSU)
ret_s, th_s = cv.threshold(s,0,255,cv.THRESH_BINARY + cv.THRESH_OTSU)

#-- Fusionner les bords
th = cv.bitwise_or(th_h,th_s)

#-- Ajout à l'image
bordersize=10
th = cv.copyMakeBorder(th, top=bordersize, bottom=bordersize, left=bordersize, right=bordersize, borderType=cv.BORDER_CONSTANT, value=[0,0,0])

#-- Remplissage des contours
im_floodfill=th.copy() 
h, w = th.shape[:2]
mask=np.zeros((h+2, w+2), np.uint8)
cv.floodFill(im_floodfill, mask, (0,0), 255)
im_floodfill_inv = cv.bitwise_not(im_floodfill)

th = th | im_floodfill_inv

#-- Enlèvement du bord de l'image
th = th[bordersize: len(th) - bordersize, bordersize: len(th[0])-bordersize]
resultat=cv.bitwise_and(img, img, mask=th)
cv.imwrite("im_floodfill.png", im_floodfill)
cv.imwrite("th.png", th)
cv.imwrite("resultat.png", resultat)
contours, hierarchy = cv.findContours(th, cv.RETR_TREE, cv.CHAIN_APPROX_NONE)

#-- Création de la nouvelle image
print(len(contours))
for i in range(len(contours)):
    mask_BB_i = np.zeros((len(th), len(th[0])), np.uint8)
    x,y,w,h   = cv.boundingRect(contours[i])
    cv.drawContours(mask_BB_i, contours, i, (255,255,255), -1)
    BB_i=cv.bitwise_and(img,img,mask=mask_BB_i)
    if h>25 and w>25:
        BB_i=BB_i[y:y+h,x:x+w]
        cv.imwrite("BB_"+str(i)+".png", BB_i)