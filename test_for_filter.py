import cv2
from PIL import Image
from my_convert import jpg_to_png, png_to_rgba
from skimage import io, segmentation, color
import numpy as np
from my_mask import do_mask, make_do_mask, make_mask


img = cv2.imread("img\\input.jpeg")
img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

### sobel filter

### グレースケール変換
gray = cv2.cvtColor(img_rgb, cv2.COLOR_RGB2GRAY)
gray_x = cv2.Sobel(gray, cv2.CV_32F, 1, 0, ksize=3)
gray_y = cv2.Sobel(gray, cv2.CV_32F, 0, 1, ksize=3)
dst = np.sqrt(gray_x ** 2 + gray_y ** 2)

h, w = gray.shape

img_hsv = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2HSV) # 色空間をBGRからHSVに変換

for y in range(h):
    for x in range(w):
        if(dst[y][x]<100.0):
            img_hsv[y][x] = 0
        else:
            # img_hsv[y][x][1] *= (dst[y][x]/255) * 0.8
            img_hsv[y][x][1] += 70
            img_hsv[y][x][2] -= 70
            if(img_hsv[y][x][1]>255):
                img_hsv[y][x][1]=255
            if(img_hsv[y][x][2]<0):
                img_hsv[y][x][2]=0

img_rgb = cv2.cvtColor(img_hsv, cv2.COLOR_HSV2RGB)

print(dst)
print(img_hsv)

cv2.imwrite("img\\edge_darkening.jpeg", img_rgb)
cv2.imwrite("img\\sobel.jpeg", dst)