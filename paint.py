from kuwahara2 import Kuwahara
import cv2

def kuwahara(path, parameter):
    img = cv2.imread(path)
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    out = Kuwahara(img_rgb, parameter, True, 1.0)
    return out

def watercolor(path, parameter):
    img = cv2.imread(path)
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    res = cv2.stylization(img_rgb, sigma_s=parameter, sigma_r=0.6)
    return res
    

def pencil(path, parameter):
    img = cv2.imread(path)
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    dst_gray, dst_color = cv2.pencilSketch(img_rgb, sigma_s=parameter, sigma_r=0.06, shade_factor=0.09) 
    return dst_color


def Gaussian(path, parameter):
    img = cv2.imread(path)
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    parameter = parameter * 2 - 1
    dst = cv2.GaussianBlur(img_rgb, ksize=(parameter, parameter), sigmaX=parameter)
    return dst