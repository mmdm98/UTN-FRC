#! /usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np
import cv2
import copy

blue = (255, 0, 0); green = (0, 255, 0); red = (0, 0, 255)
ix, iy = -1, -1
h, w = -1, -1 
drawing = False

def drawNcut(event, x, y, flags, param):
    global ix, iy, drawing, mode, h, w
    if event == cv2.EVENT_LBUTTONDOWN:
        drawing = True
        param[1] = copy.deepcopy(param[0])
        ix, iy = x, y
    
    elif event == cv2.EVENT_MOUSEMOVE:
        if drawing is True:
            param[1] = copy.deepcopy(param[0])
            cv2.rectangle(param[1], (ix, iy), (x, y), green, 0)

    elif event == cv2.EVENT_LBUTTONUP:
        drawing = False
        w, h = x, y 
        cv2.rectangle(param[1], (ix, iy), (x, y), green, 0)
 
img = cv2.imread('slipknot.jpg')
img = cv2.resize(img, (512, 512))
img_cpy = copy.deepcopy(img)
param = [img, img_cpy]
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
