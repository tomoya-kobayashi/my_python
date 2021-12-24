from skimage import io, segmentation, color
from slic_class import *

# img = io.imread("C:\\Users\\mieli\\my_python\\img\\cat1.jpeg")
# label = segmentation.slic(img, compactness=20, start_label=1)
# out = color.label2rgb(label, img, kind = 'avg', bg_label=0)
# io.imsave("C:\\Users\\mieli\\my_python\\img\\cat1_slic.jpeg", out)

"""opencvにおけるSLIC法の関数　（型：numpy　⇒　cv2として扱える？）"""
def slic_opencv(image_sk, path):
    label = segmentation.slic(image_sk, compactness=20, start_label=1)
    out = color.label2rgb(label, image_sk, kind = 'avg', bg_label=0)
    # io.imsave("img\\cat1_slic.jpeg", out)
    return out


def slic(path):
    slic = SLIC(k = 100)
    slic.fit(path)
    res = slic.transform()
    # saliency = slic.segment_saliency("img\\ramen.jpeg")
    # io.imsave("img\\new_img_saliency.jpeg", res)
    return res



