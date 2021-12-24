from skimage import io, segmentation, color
from kuwahara2 import Kuwahara
import cv2
from PIL import Image,ImageTk
import numpy as np



#画像読み込み
img = cv2.imread("img\\ramen.jpeg")

img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

# out = Kuwahara(img_rgb,3,True,1.0)


class Data():
    def __init__(self):
        self.dict_paint_1 = {'effect':Kuwahara, 'size':3}
        self.label = 1

    def func1(self):
        pass



class Test():
    def __init__(self, data):
        self.effect = Kuwahara
        self.func = self.add
        self.data = data

    def add(self, a, b):
        return a+b

    def compute_paint_1(self, effect):
        return effect(img_rgb,3,True,1.0)




data = Data()
t = Test(data)

print(t.data.label)

# kuwa = t.compute_paint_1(data.dict_paint_1['effect'])
# print(str(data.dict_paint_1['effect']))
# print(data.func(1, 2)) 







