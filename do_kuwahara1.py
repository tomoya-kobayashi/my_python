"""
こっちのフィルタはボツ

"""


from skimage import io, segmentation, color
from kuwahara1 import Kuwahara
import cv2
import tkinter
from PIL import Image,ImageTk
import numpy as np



root = tkinter.Tk()


#画像読み込み
img = cv2.imread("C:\\Users\\mieli\\my_python\\img\\cat1.jpeg")
        
canvas = tkinter.Canvas(root, width=400, height=400, bg="gray")
canvas.grid()

# 加工用にimgをコピー
img_r = img.copy()
img_g = img.copy()
img_b = img.copy()

# GとBの要素を0に変換
img_r[:, :, [1, 2]] = 0  # [G, B]
img_g[:, :, [0, 2]] = 0  # [G, B] 
img_b[:, :, [0, 1]] = 0  # [G, B] 

# RGB別々に抽出
img_r_gray = img_r[:, :, 0].copy()
img_g_gray = img_g[:, :, 1].copy()
img_b_gray = img_b[:, :, 2].copy() 

#io.imsave("C:\\Users\\mieli\\my_python\\img\\cat1_r_grey.jpeg", img_r)

#RGB別々に桑原フィルタ
out_r = Kuwahara(img_r_gray, 17)
out_g = Kuwahara(img_g_gray, 17)
out_b = Kuwahara(img_b_gray, 17)

out_rgb = np.dstack((np.dstack((out_b, out_g)), out_r))


io.imsave("C:\\Users\\mieli\\my_python\\img\\out_rgb.jpeg", out_rgb)


# io.imsave("C:\\Users\\mieli\\my_python\\img\\out_r.jpeg", out_r)
# io.imsave("C:\\Users\\mieli\\my_python\\img\\out_g.jpeg", out_r)
# io.imsave("C:\\Users\\mieli\\my_python\\img\\out_b.jpeg", out_r)



#画像表示用
image = Image.open("C:\\Users\\mieli\\my_python\\img\\out_rgb.jpeg")
w_size = int(image.width/4)
h_size = int(image.height/4)
tk_image = ImageTk.PhotoImage(image=image.resize((w_size,h_size)))
canvas.create_image(200, 200, image=tk_image)


# #test
# image = cv2.imread("C:\\Users\\mieli\\my_python\\img\\out_rgb.jpeg")
# print(image)


root.mainloop()
