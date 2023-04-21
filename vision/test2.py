import cv2

img2 = cv2.imread('slipknot.jpg')
img1 = cv2.imread('logo.jpg')
img1 = cv2.resize(img1, (512, 512))
img2 = cv2.resize(img2, (512, 512))
#img1=cv2.imread(r'D:\360MoveData\Users\Administrator\Desktop\wo\zly.jpg')
#img2=cv2.imread(r'D:\360MoveData\Users\Administrator\Desktop\wo\yx.jpg')

# 此处可以控制合成的位置（哪些位置进行改变）
# 这里两幅图一样大，不起作用
rows,cols,channels = img2.shape
roi = img1[0:rows, 0:cols ]

img2gray = cv2.cvtColor(img2,cv2.COLOR_BGR2GRAY)      # 将图片灰度化
cv2.imshow('img2gray',img2gray)
# 灰度图 把 大于175（不感兴趣）的值改为 255 ，也就是变为白色
ret, mask = cv2.threshold(img2gray, 175, 255, cv2.THRESH_BINARY)
cv2.imshow('mask',mask)
# 把mask取反，兴趣区域-->白色   无兴趣区域-->黑色
mask_not = cv2.bitwise_not(mask)
cv2.imshow('mask_not',mask_not)
# 对张靓颖图片和mask进行取与操作，作用相当于把mask中为黑色的部分，
# 在张靓颖图片中也附黑，白色部分不变。
img1_bg = cv2.bitwise_and(roi,roi,mask = mask)
cv2.imshow('img1_bg',img1_bg)
# 对风景图片和mask_not进行取与操作，作用相当于把mask中为黑色的部分，
# 在风景图片中也附黑，白色部分不变。
img2_fg = cv2.bitwise_and(img2,img2,mask = mask_not)
cv2.imshow('img2_fg',img2_fg)
# 相加即可
dst = cv2.add(img1_bg,img2_fg)
img1[0:rows, 0:cols ] = dst
# 保存
cv2.imencode('.jpg', dst)[1].tofile('bastaaa.jpg')
cv2.imshow('dst', dst)
cv2.waitKey(0)