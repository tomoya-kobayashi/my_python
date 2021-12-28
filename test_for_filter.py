import cv2
from PIL import Image
from my_convert import jpg_to_png, png_to_rgba
from skimage import io, segmentation, color
import numpy as np
from my_mask import do_mask, make_do_mask, make_mask


src = cv2.imread("img\\input.jpeg")

### gaussian filter
dst = cv2.GaussianBlur(src, ksize=(7, 7), sigmaX=2)

### sobel filter
# dst = cv2.Sobel(src, cv2.CV_32F, 1, 1, ksize=3)

cv2.imwrite("img\\gaussian.jpeg", dst)