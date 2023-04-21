#! /usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np
import cv2
import copy

blue = (255, 0, 0); green = (0, 255, 0); red = (0, 0, 255)
drawing = False  #true if mouse is pressed
mode = True  #if True, draw rectangle. Press ’m’ to toggle to curve
ix, iy = -1, -1
h, w = -1, -1 

def drawNcut(event, x, y, flags, param):
    global ix, iy, drawing, mode, h, w
    if event == cv2.EVENT_LBUTTONDOWN:
        drawing = True
        #param = copy.deepcopy(img)
        param[1] = copy.deepcopy(param[0])
        ix, iy = x, y
    elif event == cv2.EVENT_MOUSEMOVE:
            if drawing is True:
            #if mode is True:
                param[1] = copy.deepcopy(param[0])
                cv2.rectangle(param[1], (ix, iy), (x, y), green, 0)
                
    #         else:
    #             cv2.circle(img, (ix, iy), 10, red, 1)
    elif event == cv2.EVENT_LBUTTONUP:
        drawing = False
        w, h = x, y 
        #cv2.imshow('image', param)
        cv2.rectangle(param[1], (ix, iy), (x, y), green, 0)
 

img = cv2.imread('slipknot.jpg')
img = cv2.resize(img, (512, 512))
img_cpy = copy.deepcopy(img)
param = [img, img_cpy]
#cv2.imshow('image', param[0])
#img = np.zeros((512, 512, 3), np.uint8)
#cv2.namedWindow('image')
#param = img_cpy
cv2.imshow('Recortador de Imagenes', param[1])
cv2.setMouseCallback('Recortador de Imagenes', drawNcut, param)
while (1):
    cv2.imshow('Recortador de Imagenes', param[1])
    k = cv2.waitKey(1) & 0xFF
    if k == ord('g'):
        crop_img = param[1][iy:h, ix:w].copy()
        cv2.imwrite('cropy.jpg', crop_img)
        param[1] = copy.deepcopy(param[0])
    elif k == 27:
        break
cv2.destroyAllWindows()
