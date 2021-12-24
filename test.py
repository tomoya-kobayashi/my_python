import cv2
from PIL import Image
from my_convert import jpg_to_png, png_to_rgba
from skimage import io, segmentation, color
import numpy as np
from my_mask import do_mask, make_do_mask, make_mask

# # JPGをPNGに変換して保存
# jpg_to_png('img\\cat1.jpeg', 'img\\cat1.png')

# # PNGをRGBA化して保存
# png_to_rgba('img\\cat1.png', 'img\\cat1_rgba.png', 255)

# PNGをRGBA方式で読み込み（第２引数は'-1'）
# image = cv2.imread('img\\cat1_rgba.png', -1)
# saliency_rgb = cv2.imread('img\\saliency_out.jpeg')
# saliency_gray = cv2.cvtColor(saliency_rgb, cv2.COLOR_BGR2GRAY)


# # saliency map の２値化
# ret, binary = cv2.threshold(saliency_gray, 20, 255, cv2.THRESH_BINARY)
# io.imsave('img\\binary.png', binary)

# img_alpha = image[:, :, 3].copy()
# out = np.multiply(img_alpha, binary)
# out = np.multiply(out, 255)
# image[:, :, 3] = out
# io.imsave('img\\mask_out.png', image)



# make_mask('img\\saliency_out.jpeg', 10, 'img\\mask10.jpg')
# make_mask('img\\saliency_out.jpeg', 20, 'img\\mask20.jpg')
# make_mask('img\\saliency_out.jpeg', 80, 'img\\mask80.jpg')

# jpg_to_png('img\\kuwahara2_out.jpg', 'img\\kuwahara2_out.png')
# png_to_rgba('img\\kuwahara2_out.png', 'img\\kuwahara2_out_rgba.png')
# do_mask('img\\kuwahara2_out_rgba.png', 'img\\mask10.jpg', 'img\\kuwahara2_mask_out.png')



# make_do_mask('img\\kuwahara2_out_rgba.png', 'img\\saliency_out.jpeg', 20, 'img\\kuwahara2_mask_out.png')



# jpg_to_png('img\\cat1_slic.jpeg', 'img\\cat1_slic.png')
# png_to_rgba('img\\cat1_slic.png', 'img\\cat1_slic_rgba.png')

# img = cv2.imread('img\\cat1.jpeg')
# img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
# bi_1 = cv2.bilateralFilter(img_rgb, 15, 50, 20)
# bi_2 = cv2.bilateralFilter(bi_1, 15, 50, 20)
# bi_3 = cv2.bilateralFilter(bi_2, 15, 50, 20)
# bi_4 = cv2.bilateralFilter(bi_3, 15, 50, 20)
# bi_5 = cv2.bilateralFilter(bi_4, 15, 50, 20)
# bi_6 = cv2.bilateralFilter(bi_5, 15, 50, 20)
# bi_7 = cv2.bilateralFilter(bi_6, 15, 50, 20)
# bi_8 = cv2.bilateralFilter(bi_7, 15, 50, 20)
# io.imsave('img\\bilateral_out.jpg', bi_7)


### MeanShiftFilter
# image = cv2.imread('img\\cat1.jpeg')
# img_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
# shifted = cv2.pyrMeanShiftFiltering(img_rgb, 21, 51)
# io.imsave('img\\MeanShift_out.jpg', shifted)
 

### 画像読み込み
# layer1 = Image.open('img\\kuwahara2_mask_out.png') 
# im_back = Image.open('img\\cat1_slic_rgba.png') 
# im_back = Image.open('img\\bilateral_out.jpg')
im_back = Image.open('img\\ramen_slic.jpeg')
# kuwahara = Image.open('img\\kuwahara2_out_rgba.png')
kuwahara = Image.open('img\\ramen_kuwahara2_3.jpg')
watercolor = Image.open('img\\ramen_watercolor_40-0.6.jpeg')
pencil = Image.open('img\\ramen_pencil.jpeg')

# マスク画像 alpha=0で
# mask = Image.new("L", layer1.size, 0)
mask1 = Image.open('img\\ramen_mask50.png')
mask2 = Image.open('img\\ramen_mask120.png')

# 透けない背景画像に半スケを貼る

# out1 = Image.composite(watercolor, im_back, mask2)
# out2 = Image.composite(kuwahara, out1, mask1)

out1 = Image.composite(watercolor, kuwahara, mask1)
out1.save('img\\test.png')
