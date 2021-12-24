from skimage import io, segmentation, color
from kuwahara2 import Kuwahara
import cv2
import tkinter
from PIL import Image,ImageTk
import numpy as np



# root = tkinter.Tk()


#画像読み込み
img = cv2.imread("img\\ramen.jpeg")
        
# canvas = tkinter.Canvas(root, width=400, height=400, bg="gray")
# canvas.grid()

img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

out = Kuwahara(img_rgb,3,True,1.0)

io.imsave("img\\ramen_kuwahara2_3.jpg", out)
