#! /usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np
import cv2
import copy
from sys import argv
#pop up---------------------------------------------------
import ctypes  # para el mensaje de info
tutorial = 'Seleccionar puntos en el siguiente orden:\n\n\n Primer Punto: Esquina superior izquierda. \n\n Segundo Punto: Esquina superior derecha \n\n Tercer Punto: Esquina inferior izquierda \n\n Cuarto Punto: Esquina inferior derecha. '

def Mbox(title, text, style):
    return ctypes.windll.user32.MessageBoxW(0, text, title, style)
Mbox('INFO', tutorial, 0)
#fin pop up ----------------------------------------------

if len(argv) >= 2:
    #por si se quiere poner otra imagen, poner el path o ubicarla en el directorio
    imagen_entrada1 = argv[1]
else:
    #imagen por default
    imagen_entrada1 = 'slipknot.jpg'


#colores
blue = (255, 0, 0); green = (0, 255, 0); red = (0, 0, 255)
H, W = 512, 512   #alto y ancho por defecto
count  = 0        #contador de circulos en 0
points = []       #caja para guardar puntos
coords = [[-1,-1], [-1,-1], [-1,-1], [-1,-1]] #coordenadas iniciales

#funcion para dibujar 3 puntos que se guardan
def draw4dots(event, x, y, flags, param):
    global count, points, coords #toma el valor de las variables globales
    if event == cv2.EVENT_LBUTTONDOWN:
        if (count == 4):  #si cuente cuatro circulos reseteo el mundo
            param[1] = copy.deepcopy(param[0])
            count = 0
        #toma coordenadas de los clicks
        coords[3] = coords[2]
        coords[2] = coords[1]
        coords[1] = coords[0]
        coords[0] = x, y
        #abajo las guardo (float)
        points = np.array([coords[3], coords[2], coords[1], coords[0]]).astype(np.float32)
        cv2.circle(param[1], (x, y), 4, red, -1) #dibuja circulos
        count = count + 1                        #contador de circulos

#captura y redimension de imagenes 
img_orig = cv2.resize((cv2.imread(imagen_entrada1)), (H, W))

#copio la original y la guardo
img_copy = copy.deepcopy(img_orig)
param = [img_orig, img_copy] #creo un paquete en donde guardar una original y una copia

#muestro en pantalla
cv2.imshow('Marcar 4 Puntos, con "g" guardar', param[1])
#activo callback y le paso la funcion + la original y la copia || preguntar porque anda acá y no necesariamente en el while*
cv2.setMouseCallback('Marcar 4 Puntos, con "g" guardar', draw4dots, param) #ya entendí porque se puede escribir aca y no en el while

#loop
while (1):
    cv2.imshow('Marcar 4 Puntos, con "g" guardar', param[1])            #siempre muestro la copia, en donde trabajo
    k = cv2.waitKey(1) & 0xFF                                           #cosas de teclado
    if k == ord('g'):                                                   #ord es para que agarre bien
        points2 = np.array([[0, 0], [img_orig.shape[1], 0], [0, img_orig.shape[1]], [img_orig.shape[0], img_orig.shape[1]]]).astype(np.float32)  #guardo cuatro puntos (float) de la img_aux
        warp_mat = cv2.getPerspectiveTransform(points, points2)  #se obtiene matriz que deforma de los cuatro puntos de img_aux, a los cuatro puntos click
        warp_dst = cv2.warpPerspective(param[1], warp_mat, (H,W)) #aplico la transformada afin a la img_aux y la muestro
        cv2.imshow('Imagen Rectificada', warp_dst)
        cv2.imwrite('dst.jpg', warp_dst)   
        param[1] = copy.deepcopy(param[0]) #reestablezco copia a original
    elif k == 27: #sale con escape
        break
cv2.destroyAllWindows()
#a futuro agregar un point sorter para que no haya que hacerlo en una manera en específica