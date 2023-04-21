#reziseador de imagenes
import cv2

img2 = cv2.imread('slipknot.jpg')
img1 = cv2.imread('logo.jpg')
img1 = cv2.resize(img1, (260, 260))
img2 = cv2.resize(img2, (512, 512))

cv2.imwrite('slip.jpg', img2)
cv2.imwrite('loguito.jpg', img1)