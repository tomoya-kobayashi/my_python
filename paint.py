from kuwahara2 import Kuwahara
import cv2
import numpy as np

def kuwahara(path, parameter):
    img = cv2.imread(path)
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    out = Kuwahara(img_rgb, parameter, True, 1.0)
    return out

def watercolor(path, parameter):
    img = cv2.imread(path)
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    # sigma_r = parameter / 25
    res = cv2.stylization(img_rgb, sigma_s=parameter, sigma_r=0.45)
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


def flat(path, parameter):
    img = cv2.imread("img\\segmentation.jpeg")
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    return img_rgb


def oilpaint(path, parameter):
    img = cv2.imread(path)
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    cartoon = cv2.xphoto.oilPainting(img_rgb, size=parameter, dynRatio=1)
    return cartoon


def watercolor_reformed(path, parameter):
    img = cv2.imread(path)
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    res = cv2.stylization(img_rgb, sigma_s=parameter, sigma_r=0.6)

    ### グレースケール変換
    gray = cv2.cvtColor(img_rgb, cv2.COLOR_RGB2GRAY)
    gray_x = cv2.Sobel(gray, cv2.CV_32F, 1, 0, ksize=3)
    gray_y = cv2.Sobel(gray, cv2.CV_32F, 0, 1, ksize=3)
    dst = np.sqrt(gray_x ** 2 + gray_y ** 2)

    h, w = gray.shape

    ### 色空間をBGRからHSVに変換
    img_hsv = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2HSV) 
    
    for y in range(h):
        for x in range(w):
            if(dst[y][x]<100.0):
                img_hsv[y][x] = 0
            else:
                # img_hsv[y][x][1] *= (dst[y][x]/255) * 0.8
                img_hsv[y][x][1] += 70
                img_hsv[y][x][2] -= 70
                if(img_hsv[y][x][1]>255):
                    img_hsv[y][x][1]=255
                if(img_hsv[y][x][2]<0):
                    img_hsv[y][x][2]=0

    edge_darkening = cv2.cvtColor(img_hsv, cv2.COLOR_HSV2RGB)


    for y in range(h):
        for x in range(w):
            if(img_hsv[y][x][2]>1):
                res[y][x] = edge_darkening[y][x]


    return res