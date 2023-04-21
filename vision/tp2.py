#! /usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np
import cv2
import copy
#inicio, largo en x, largo en y
blue = (255, 0, 0); green = (0, 255, 0); red = (0, 0, 255)
drawing = False  #true if mouse is pressed
mode = True  #if True, draw rectangle. Press ’m’ to toggle to curve
ix, iy = -1, -1
h, w = -1, -1 
count = 0
points = []
coords=[[-1,-1],[-1,-1],[-1,-1]]

def drawNcut(event, x, y, flags, param):
    global ix, iy, drawing, mode, h, w, count, points, coords
    if event == cv2.EVENT_LBUTTONDOWN:
        print(coords)
        drawing = False
        #param = copy.deepcopy(img)
        if (count == 3):
            param[1] = copy.deepcopy(param[0])
            drawing = True
            count = 0
        
        coords[2]=coords[1]
        coords[1]=coords[0]
        coords[0]=x,y
        # print(coords[0])
        # coords[0]=x,y
        # print(coords[0])
        # print(coords[1])
        # coords[1]=coords[0]
        # print(coords[1])
        # print(coords[2])
        # coords[2]=coords[1]
        # print(coords[2])
        #iix, iiy = ix, iy
        ix, iy = x, y
        points = np.array([coords[2], coords[1], coords[0]]).astype(np.float32)
        #points = np.array([[iix, iiy], [ix,iy], [x,y]]).astype(np.float32)
        cv2.circle(param[1], (ix, iy), 4, red, -1)
        count = count+1
        print(points)
    #elif event == cv2.EVENT_MOUSEMOVE:
    #        if drawing is True:
            #if mode is True:
    #            param[1] = copy.deepcopy(param[0])
                #cv2.circle(param[1], (ix, iy), 2, red, -1)
                #cv2.rectangle(param[1], (ix, iy), (x, y), green, 0)
    #         else:
    #             cv2.circle(img, (ix, iy), 10, red, 1)
    #elif event == cv2.EVENT_LBUTTONUP:
    #    drawing = False
    #    w, h = x, y 
        #cv2.imshow('image', param)
        #cv2.rectangle(param[1], (ix, iy), (x, y), green, 0)
 

img = cv2.imread('slipknot.jpg')
img1 = cv2.imread('logo.jpg')
img1 = cv2.resize(img1, (512, 512))
img = cv2.resize(img, (512, 512))

img_cpy = copy.deepcopy(img)
param = [img, img_cpy]
#cv2.imshow('image', param[0])
#img = np.zeros((512, 512, 3), np.uint8)
#cv2.namedWindow('image')
#param = img_cpy
cv2.imshow('imagen dos', img1)
cv2.imshow('Recortador de Imagenes', param[1])
cv2.setMouseCallback('Recortador de Imagenes', drawNcut, param)
while (1):
    cv2.imshow('Recortador de Imagenes', param[1])
    k = cv2.waitKey(1) & 0xFF
    if k == ord('g'):
        print(drawing)
        points2=np.array([[0,0], [260,0], [0,260]]).astype(np.float32)
        #points3=np.array([[0,0], [100,0], [0,100]]).astype(np.float32)
        print(points2,points)
        warp_mat = cv2.getAffineTransform(points2, points)
        print(warp_mat)
        warp_dst = cv2.warpAffine(img1, warp_mat, (512,512))
        mask = cv2.threshold(warp_dst, 10, 255, cv2.THRESH_BINARY)
        img2_fg = cv2.bitwise_and(img1, img1, mask=mask)
        dst = cv2.add(param[1], img2_fg)
        cv2.imshow('iwarwp', param[1])
        cv2.imshow('iwarp', warp_dst)
        #crop_img = param[1][iy:h, ix:w].copy()
        #cv2.imwrite('cropy.jpg', crop_img)
        param[1] = copy.deepcopy(param[0])
    elif k == 27:
        break
cv2.destroyAllWindows()
