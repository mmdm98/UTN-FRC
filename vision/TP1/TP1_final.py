#! /usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np
import cv2
import copy
from sys import argv

if len(argv) >= 2:
    #por si se quiere poner otra imagen, poner el path o ubicarla en el directorio
    imagen_entrada = argv[1]
else:
    #imagen por default
    imagen_entrada = 'slipknot.jpg'

#colores
blue = (255, 0, 0); green = (0, 255, 0); red = (0, 0, 255)
#globales y flags
ix, iy = -1, -1
h, w = -1, -1 
drawing = False

#funcion para cortar rectangulos de imagen
def drawNcut(event, x, y, flags, param):
    global ix, iy, drawing, mode, h, w
    #se trabaja siempre en la copia
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

#leo la imagen de entrada, resize y copia fiel
img = cv2.imread(imagen_entrada)
img = cv2.resize(img, (512, 512))
img_cpy = copy.deepcopy(img)
#guardo en array
param = [img, img_cpy]
#titulos
cv2.imshow('Recortador de Imagenes: "g" para guardar, "esc" para salir', param[1])
cv2.setMouseCallback('Recortador de Imagenes: "g" para guardar, "esc" para salir', drawNcut, param)
#loop
while (1):
    cv2.imshow('Recortador de Imagenes: "g" para guardar, "esc" para salir', param[1])
    k = cv2.waitKey(1) & 0xFF 
    if k == ord('g'):   #ord es para que lo tome bien
        crop_img = param[1][iy:h, ix:w].copy()
        cv2.imwrite('cropy.jpg', crop_img) #imagen recortada
        cv2.imshow('Recorte', crop_img)    #muestro la recortadaa
        param[1] = copy.deepcopy(param[0]) #reseteo
    elif k == 27:
        break
cv2.destroyAllWindows()
