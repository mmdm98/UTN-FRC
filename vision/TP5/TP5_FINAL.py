import cv2
import numpy as np
from Calibracion import *


#inicializacion de parametros
parametros = cv2.aruco.DetectorParameters_create()

#diccionarie
diccionario = cv2.aruco.Dictionary_get(cv2.aruco.DICT_5X5_100)

#camarita
cap = cv2.VideoCapture(1)
cap.set(3, 1280)
cap.set(4, 720)
cont = 0

#calibracion
calibracion = calibracion()
matrix, dist = calibracion.calibracion_cam()
print("Matriz de la camara: ", matrix)
print("Coeficientes de Distorcion: ", dist)

overlay = cv2.imread('C:/Users/Usuario/Documents/SEXTO/vision/TP5/otrasimagenes/eye.png', cv2.IMREAD_UNCHANGED)

while (1):
    ret, frame = cap.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    #detectamos marcadores de la imagen
    #camera matrix: calibracion de la imagen
    esquinas, ids, candidatos_malos = cv2.aruco.detectMarkers(gray, diccionario, parameters = parametros, cameraMatrix = matrix, distCoeff= dist)


    try:
        #si hay markers encontrados por el detector
        if np.all(ids != None):
            #iterar en marcadores
            for i in range(0, len(ids)):
                #estima la pose de cada marcador y devuelve los valores rvec y tvec -- diferentes de los coef de la camara
                rvec, tvec, markerPoint = cv2.aruco.estimatePoseSingleMarkers(esquinas[i], 0.02, matrix, dist)

                #eliminamos el error de la matriz de valores numpy
                (rvec - tvec).any()

                #dibuja un cuadrado alrededor de los marcadores
                cv2.aruco.drawDetectedMarkers(frame, esquinas)

                #dibujamos los ejes
                cv2.aruco.drawAxis(frame, matrix, dist, rvec, tvec, 0.01)

                #coordenada x del centro del marcador
                c_x = (esquinas[i][0][0][0] + esquinas[i][0][1][0] + esquinas[i][0][2][0] + esquinas[i][0][3][0]) / 4

                #coordenada y del centro del marcador
                c_y = (esquinas[i][0][0][1] + esquinas[i][0][1][1] + esquinas[i][0][2][1] + esquinas[i][0][3][1]) / 4

                #mostramos el id
                cv2.putText(frame, "id" + str(ids[i]), (int(c_x), int(c_y)), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (50, 225, 250), 2)

                #extraemos los puntos de las esquinas en coordenadas separadas
                c1 = (esquinas[0][0][0][0], esquinas[0][0][0][1])
                c2 = (esquinas[0][0][1][0], esquinas[0][0][1][1])
                c3 = (esquinas[0][0][2][0], esquinas[0][0][2][1])
                c4 = (esquinas[0][0][3][0], esquinas[0][0][3][1])
                v1, v2 = c1[0], c1[1]
                v3, v4 = c2[0], c2[1]
                v5, v6 = c3[0], c3[1]
                v7, v8 = c4[0], c4[1]

                # #cubo piola
                # #cara inferior
                # cv2.line(frame, (int(v1), int(v2)), (int(v3), int(v4)), (255, 255, 0), 3)
                # cv2.line(frame, (int(v5), int(v6)), (int(v7), int(v8)), (255, 255, 0), 3)
                # cv2.line(frame, (int(v1), int(v2)), (int(v7), int(v8)), (255, 255, 0), 3)
                # cv2.line(frame, (int(v3), int(v4)), (int(v5), int(v6)), (255, 255, 0), 3)

                # #cara superior
                # cv2.line(frame, (int(v1), int(v2 - 200)), (int(v3), int(v4 - 200)), (255, 255, 0), 3)
                # cv2.line(frame, (int(v5), int(v6 - 200)), (int(v7), int(v8 - 200)), (255, 255, 0), 3)
                # cv2.line(frame, (int(v1), int(v2 - 200)), (int(v7), int(v8 - 200)), (255, 255, 0), 3)
                # cv2.line(frame, (int(v3), int(v4 - 200)), (int(v5), int(v6 - 200)), (255, 255, 0), 3)

                # #caras laterales
                # cv2.line(frame, (int(v1), int(v2 - 200)), (int(v1), int(v2)), (255, 255, 0), 3)
                # cv2.line(frame, (int(v3), int(v4 - 200)), (int(v3), int(v4)), (255, 255, 0), 3)
                # cv2.line(frame, (int(v5), int(v6 - 200)), (int(v5), int(v6)), (255, 255, 0), 3)
                # cv2.line(frame, (int(v7), int(v8 - 200)), (int(v7), int(v8)), (255, 255, 0), 3)

                # #carita sonriente piola
                # cv2.circle(frame, (int(c_x)-60, (int(c_y))-200), 20, (222, 222, 0), 6)
                # cv2.circle(frame, (int(c_x)+60, (int(c_y))-200), 20, (222, 222, 0), 6)
                # cv2.line(frame, (int(c_x)+40, (int(c_y))-100), (int(c_x)-40, (int(c_y))-100), (255, 255, 0), 5)
                # cv2.line(frame, (int(c_x)+40, (int(c_y))-100), (int(c_x)+50, (int(c_y))-130), (255, 255, 0), 5)
                # cv2.line(frame, (int(c_x)-40, (int(c_y))-100), (int(c_x)-50, (int(c_y))-130), (255, 255, 0), 5)

                #lentes piola
                cv2.circle(frame, (int(c_x)-70, (int(c_y))-300), 45, (222, 222, 0), -1)
                cv2.circle(frame, (int(c_x)+70, (int(c_y))-300), 45, (222, 222, 0), -1)
                #rail
                cv2.line(frame, (int(c_x)-35, (int(c_y))-300), (int(c_x)+35, (int(c_y))-300), (0, 0, 0), 5)
                cv2.circle(frame, (int(c_x)-70, (int(c_y))-300), 45, (0, 0, 0), 5)
                cv2.circle(frame, (int(c_x)+70, (int(c_y))-300), 45, (0, 0, 0), 5)
                #luz
                cv2.line(frame, (int(c_x)-85, (int(c_y))-320), (int(c_x)-70, (int(c_y))-330), (255, 255, 255), 3)
                cv2.line(frame, (int(c_x)-85, (int(c_y))-310), (int(c_x)-70, (int(c_y))-320), (255, 255, 255), 3)
                cv2.line(frame, (int(c_x)+70, (int(c_y))-320), (int(c_x)+85, (int(c_y))-330), (255, 255, 255), 3)
                cv2.line(frame, (int(c_x)+70, (int(c_y))-310), (int(c_x)+85, (int(c_y))-320), (255, 255, 255), 3)



    except:
        if ids is None or len(ids) == 0:
            print("FALLO TODO")

    cv2.imshow('realidad virtual', frame)

    k = cv2.waitKey(1)

    #fotos para medir
    if k == 97:
        print("imagen guardada")
        cv2.imwrite("cali{}.png".format(cont), frame)
        cont = cont + 1

    if k == 27:
        break

cap.release()
cv2.destroyAllWindows()