"""
顕著度マップ関数リスト
mainでimportして使用される
"""


import cv2


"""ittiのsaliency map の計算"""
def itti_saliency(image_cv2):
    saliency = cv2.saliency.StaticSaliencySpectralResidual_create()
    bool, map = saliency.computeSaliency(image_cv2)
    out = (map * 255).astype("uint8")
    # io.imsave("C:\\Users\\mieli\\my_python\\img\\saliency_out.jpeg", out)
    return out