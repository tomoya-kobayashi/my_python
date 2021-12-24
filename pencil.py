import cv2
from skimage import io, segmentation, color

img = cv2.imread('img\\ramen.jpeg')

img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

dst_gray, dst_color = cv2.pencilSketch(img_rgb, sigma_s=120, sigma_r=0.06, shade_factor=0.09) 
# sigma_s and sigma_r are the same as in stylization.
# shade_factor is a simple scaling of the output image intensity. The higher the value, the brighter is the result. Range 0 - 0.1

io.imsave("img\\ramen_pencil.jpeg", dst_color)
