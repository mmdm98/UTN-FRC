from __future__ import print_function
import cv2 as cv
import numpy as np
import argparse
parser = argparse.ArgumentParser(description='Code for Affine Transformations tutorial.')
parser.add_argument('--input', help='Path to input image.', default='slipknot.jpg')
args = parser.parse_args()
src = cv.imread(cv.samples.findFile(args.input))
src = cv.resize(src, (512, 512))
img1 = cv.imread('logo.jpg')
img1 = cv.resize(img1, (260, 260))
if src is None:
    print('Could not open or find the image:', args.input)
    exit(0)
srcTri = np.array( [[0, 0], [src.shape[1] - 1, 0], [0, src.shape[0] - 1]] ).astype(np.float32)
dstTri = np.array( [[0, src.shape[1]*0.33], [src.shape[1]*0.85, src.shape[0]*0.25], [src.shape[1]*0.15, src.shape[0]*0.9]] ).astype(np.float32)
warp_mat = cv.getAffineTransform(srcTri, dstTri)
warp_dst = cv.warpAffine(img1, warp_mat, (src.shape[1], src.shape[0]))
# Rotating the image after Warp
blue = (255, 0, 0); green = (0, 255, 0); red = (0, 0, 255)
center = (warp_dst.shape[1]//2, warp_dst.shape[0]//2)
angle = -50
scale = 0.6
rot_mat = cv.getRotationMatrix2D( center, angle, scale )
warp_rotate_dst = cv.warpAffine(warp_dst, rot_mat, (warp_dst.shape[1], warp_dst.shape[0]))
print(srcTri,dstTri)
cv.circle(src, tuple(dstTri[0]), 4, red, -1)
cv.circle(src, tuple(dstTri[1]), 4, red, -1)
cv.circle(src, tuple(dstTri[2]), 4, red, -1)
cv.imshow('Source image', src)
cv.imshow('Warp', warp_dst)
cv.imshow('Warp + Rotate', warp_rotate_dst)
cv.waitKey()