import cv2
from skimage import io, segmentation, color

img = cv2.imread('img\\ramen.jpeg')
img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
res = cv2.stylization(img_rgb, sigma_s=40, sigma_r=0.6)

# out = color.label2rgb(res, img, kind = 'avg', bg_label=0)
# sigma_s controls the size of the neighborhood. Range 1 - 200
# sigma_r controls the how dissimilar colors within the neighborhood will be averaged. A larger sigma_r results in large regions of constant color. Range 0 - 1

io.imsave('img\\ramen_watercolor_40-0.6.jpeg', res)