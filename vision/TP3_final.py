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

#funcion que hace el overlay entre las dos imagenes

#Bueno, escala en grises de la original, hace dos mascaras a partir de una binarizacion, guarda la mascara de 0s por un lado y la de 1s por otro
#despues hace una and entre la warp y ella misma, en la mascara que predominan 0s(o sea negros), todo lo negro va a quedar igual, solo cambia en
#donde tenga un 1(blanco), cabe destacar que la operacion es bitwise en 8 bits por pixel. Lo mismo pasa con la imagen original, pero se usa la 
#mascara de 1s, entonces en donde tenga blanco en la mascara, voy a ver mi imagen original, y en donde tenga negro se queda negro. Al final se
#suman las dos, es como si en una trabajara los blancos, y en otra los negros, al sumar: en donde tenia negro voy a tener el blanco y en donde
#tenia blanco voy a tener el negro. En otras palabras, estoy por hacer galletas, corto un cuadrado de masa con dos moldes complementarios, 
#decoro cada galleta, y despues las uno en el cuadrado original. 

def overlay(warp, original):
    rows, cols, channels = original.shape #toma filas, columnas y canales(png) de la original(que es la copia xd)
    img2gray = cv2.cvtColor(warp,cv2.COLOR_BGR2GRAY)                #escala en grises     
    ret, mask = cv2.threshold(img2gray, 1, 255, cv2.THRESH_BINARY)  #treshold para binarizar en blanco o negro (1 o 0 resp)
    mask_not = cv2.bitwise_not(mask)                                #mascara de 1s
    img1_bg = cv2.bitwise_and(warp, warp, mask = mask)              #lo que entiendo, agarra el area de la warp hace and con la mask de 0s
    img2_fg = cv2.bitwise_and(original, original, mask = mask_not)  #hace and con la original y la mascara de unos
    dst = cv2.add(img1_bg, img2_fg)                                 #suma
    cv2.imencode('.jpg', dst)[1].tofile('bastaaa.jpg')              #guardo la nueva porque si
    cv2.imshow('Imagen rectificada', dst)                           #la muestroo

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
        cv2.imshow('warpeada', warp_dst)
        param[1] = copy.deepcopy(param[0]) #reestablezco copia a original
    elif k == 27: #sale con escape
        break
cv2.destroyAllWindows()
#a futuro agregar un point sorter para que no haya que hacerlo en una manera en específica