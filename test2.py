from skimage import io, segmentation, color
import cv2

img = io.imread("img\\ramen.jpeg")
label = segmentation.slic(img, compactness=20, start_label=1)
out = color.label2rgb(label, img, kind = 'avg', bg_label=0)
# io.imsave("img\\cat1_slic.jpeg", out)

img_cv2 = cv2.imread("img\\ramen.jpeg")

print(type(img))
print(type(out))
print(type(img_cv2))