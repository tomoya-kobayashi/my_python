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
    pass