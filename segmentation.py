from skimage import io, segmentation, color
from slic_class import *

# img = io.imread("C:\\Users\\mieli\\my_python\\img\\cat1.jpeg")
# label = segmentation.slic(img, compactness=20, start_label=1)
# out = color.label2rgb(label, img, kind = 'avg', bg_label=0)
# io.imsave("C:\\Users\\mieli\\my_python\\img\\cat1_slic.jpeg", out)

"""opencvにおけるSLIC法の関数　（型：numpy　⇒　cv2として扱える？）"""
def slic_opencv(image_sk, k):
    label = segmentation.slic(image_sk, compactness=20, start_label=1)
    out = color.label2rgb(label, image_sk, kind = 'avg', bg_label=0)
    # io.imsave("img\\cat1_slic.jpeg", out)
    return out


def slic(image_cv2, var_k=100):
    slic = SLIC(k = var_k)
    slic.fit(image_cv2)
    a = slic
    res = slic.transform()
    # io.imsave("img\\new_img_saliency.jpeg", res)
    return res, a


def slic_saliency(saliency_map, slic):
    # slic = SLIC(k = 100)
    # slic.fit(image_cv2)
    # res = slic.transform()
    saliency = slic.segment_saliency(saliency_map)
    return saliency



